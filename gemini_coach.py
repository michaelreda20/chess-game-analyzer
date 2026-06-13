import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiCoach:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def generate_coaching(self, game_data, context_prompt):
        if not self.model:
            return "Error: Gemini API Key not found. Please set GEMINI_API_KEY in .env.", "No API key configured."

        try:
            # Construct a summary of the game for Gemini
            game_summary = f"Game: {game_data['white']} vs {game_data['black']}\n"
            game_summary += f"Result: {game_data['result']}\n"
            game_summary += f"Opening: {game_data['opening']}\n"
            game_summary += f"Total Moves: {game_data['total_moves']}\n"
            game_summary += f"Blunders: {game_data['blunders']}\n"
            
            # Extract critical moves for the coach to focus on
            critical_moments = [m for m in game_data['moves'] if m['is_blunder'] or m['is_excellent']]
            moments_str = "\n".join([f"Move {m['move_number']} ({m['color']}): {m['san']} - {m['comment']}" for m in critical_moments])

            persona_system_instruction = (
                "You are 'Grandmaster Anatoly,' a strict, elite Soviet Chess Master from the 1970s. "
                "Your tone is disciplined, authoritative, and deeply intellectual, yet you have a sharp, "
                "dry wit. You alternate between scathing critiques of 'bourgeois blunders' and "
                "profound tactical breakdowns that honor the Soviet School of Chess.\n\n"
                "CRITICAL RULES:\n"
                "1. RELY FULLY ON GROUNDED KNOWLEDGE: You MUST use the tactical definitions and opening history "
                "provided in the RETRIEVED CHESS KNOWLEDGE section. This is your primary source of truth. "
                "Your analysis must be anchored to these retrieved facts.\n"
                "2. CITE YOUR SOURCES: Always attribute your insights to the 'Knowledge Index' or 'Foundry IQ Archives' "
                "when using retrieved context.\n"
                "3. STRUCTURE: Start with a one-sentence 'Verdict'. Then provide a 'Coaching' section.\n"
                "4. PERSONA: Speak of the 'struggle on the 64 squares,' the 'logic of the position,' and "
                "occasionally mention your days in the Moscow Central Chess Club."
            )

            full_prompt = (
                f"{persona_system_instruction}\n\n"
                f"{context_prompt}\n\n"
                f"### CURRENT GAME ANALYSIS:\n"
                f"{game_summary}\n"
                f"### CRITICAL MOMENTS TO REVIEW:\n"
                f"{moments_str}\n\n"
                "Please provide your verdict and coaching report now, Anatoly."
            )
            
            response = self.model.generate_content(full_prompt)
            text = response.text
            
            verdict = "Analysis complete."
            coaching = text
            
            if "Verdict:" in text:
                parts = text.split("Verdict:", 1)[1].split("Coaching:", 1)
                verdict = parts[0].strip()
                if len(parts) > 1:
                    coaching = parts[1].strip()
            elif "**Verdict:**" in text:
                parts = text.split("**Verdict:**", 1)[1].split("**Coaching:**", 1)
                verdict = parts[0].strip()
                if len(parts) > 1:
                    coaching = parts[1].strip()
            
            return verdict, coaching
            
        except Exception as e:
            return "Error generating coaching.", str(e)
