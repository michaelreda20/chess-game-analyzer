import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GeminiCoach:
    def __init__(self):
        # Target Alibaba Cloud Model Studio using the openai Python library
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if api_key:
            self.client = OpenAI(
                base_url="https://ws-nnoq6fgha4crsphn.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
                api_key=api_key,
            )
            self.model = "qwen3.7-max"
        else:
            self.client = None
            self.model = None

    def generate_coaching(self, game_data, context_prompt):
        if not self.client:
            return "Error: DASHSCOPE_API_KEY not found. Please set it in .env.", "No API key configured."

        try:
            # Construct a summary of the game
            game_summary = f"Game: {game_data['white']} (White) vs {game_data['black']} (Black)\n"
            game_summary += f"Result: {game_data['result']}\n"
            game_summary += f"Opening: {game_data['opening']}\n"
            game_summary += f"Total Moves: {game_data['total_moves']}\n"
            
            # Create a full raw chronological timeline of moves
            timeline_lines = []
            for m in game_data['moves']:
                # Defensively handle different naming schemas for captured pieces
                captured_key = m.get('captured_piece') or m.get('captured_piece_type') or ""
                capture_info = f" (Captures {captured_key})" if m['is_capture'] else ""
                timeline_lines.append(f"{m['move_index']}. {m['move_color']}: {m['san']}{capture_info}")
            
            moves_timeline = "\n".join(timeline_lines)

            persona_system_instruction = (
                "You are 'Grandmaster Anatoly,' a strict, elite Soviet Chess Master from the 1970s. "
                "Your tone is disciplined, authoritative, and deeply intellectual, yet you have a sharp, "
                "dry wit. You alternate between scathing critiques of 'bourgeois blunders' and "
                "profound tactical breakdowns that honor the Soviet School of Chess.\n\n"
                "YOUR TASK:\n"
                "You are receiving a raw chronological log of a chess game. You must use your advanced "
                "chess reasoning capabilities to read the moves, deduce where the players made tactical "
                "errors, blunders, or brilliant maneuvers, and integrate these findings into your review.\n\n"
                "CRITICAL RULES:\n"
                "1. MASTER'S JUDGMENT RATING: At the very top of your 'Verdict', you MUST prepend a "
                "thematic rating based on your own expert assessment of the game's tactical quality:\n"
                "   - [MASTER'S JUDGMENT: FUTURE WORLD CHAMPION]\n"
                "   - [MASTER'S JUDGMENT: PROMISING COMRADE]\n"
                "   - [MASTER'S JUDGMENT: NEEDS IDEOLOGICAL REALIGNMENT]\n"
                "   - [MASTER'S JUDGMENT: SENTENCED TO EXTRA TACTICAL DRILLS]\n"
                "2. GROUNDED KNOWLEDGE: You MUST strictly incorporate the tactical definitions and opening "
                "history provided in the RETRIEVED CHESS KNOWLEDGE section. Attribute these insights to the "
                "'Knowledge Index' or 'Foundry IQ Archives'.\n"
                "3. STRUCTURE: Start with the Judgment Rating followed by a one-sentence 'Verdict'. Then provide a 'Coaching' report.\n"
                "4. PERSONA: Maintain the 1980s Soviet persona. Speak of the 'struggle on the 64 squares' "
                "and the 'logic of the position.'\n\n"
                "You are the engine of truth. Do not rely on external labels; find the truth in the moves themselves."
            )

            full_prompt = (
                f"{context_prompt}\n\n"
                f"### GAME OVERVIEW:\n"
                f"{game_summary}\n"
                f"### RAW CHRONOLOGICAL GAME LOG:\n"
                f"{moves_timeline}\n\n"
                "Anatoly, the board is yours. Analyze these moves and provide your report."
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": persona_system_instruction},
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            text = response.choices[0].message.content

            # --- DEFENSIVE AND ROBUST REGEX PARSING LAYER ---
            # 1. Extract [MASTER'S JUDGMENT: ...] tag anywhere in the string
            judgment_match = re.search(r"(\[MASTER'S JUDGMENT:.*?\])", text)
            judgment = judgment_match.group(1).strip() if judgment_match else ""
            
            # Clean up judgment tag from text to avoid duplication bugs
            clean_text = text if not judgment else text.replace(judgment, "", 1)
            
            # 2. Extract Verdict string defensively using clean fallbacks
            verdict_text = ""
            verdict_patterns = [
                r"(?:Verdict|\*\*Verdict\*\*):\s*(.*?)(?=(?:Coaching|### Coaching Report|\*\*Coaching\*\*):|$)",
                r"\[MASTER'S JUDGMENT:.*?\]\s*(.*?)(?=(?:Coaching|### Coaching Report|\*\*Coaching\*\*):|$)"
            ]
            
            for pattern in verdict_patterns:
                verdict_match = re.search(pattern, clean_text, re.DOTALL | re.IGNORECASE)
                if verdict_match and verdict_match.group(1).strip():
                    verdict_text = verdict_match.group(1).strip()
                    break
            
            # 3. Extract Coaching block defensively using positional splits
            coaching_text = ""
            coaching_split_patterns = ["**Coaching:**", "Coaching:", "### Coaching Report", "### COACHING REPORT"]
            
            for marker in coaching_split_patterns:
                if marker in text:
                    coaching_text = text.split(marker, 1)[1].strip()
                    break
                    
            if not coaching_text:
                coaching_text = text.strip()

            # 4. Final Structure assembly formatting for JSON consumption
            if judgment and verdict_text:
                verdict = f"{judgment}\n{verdict_text}"
            elif judgment or verdict_text:
                verdict = judgment or verdict_text
            else:
                verdict = "[MASTER'S JUDGMENT: PROMISING COMRADE]\nGrandmaster Anatoly has weighed your performance."
                
            # Final structural strip to avoid markdown stars corrupting display frames
            verdict = verdict.replace("**", "").replace("###", "").strip()
            coaching = coaching_text
            
            return verdict, coaching
            
        except Exception as e:
            return "The coach stepped away from the board.", str(e)