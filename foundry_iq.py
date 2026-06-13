import os

class FoundryIQ:
    """
    Mock implementation of Microsoft Foundry IQ pattern.
    In a real-world scenario, this would connect to Azure AI Search
    or a Microsoft Foundry IQ managed index.
    """
    
    def __init__(self):
        # Mock Chess Knowledge Index - Enriched with History, Quotes, and Psychology
        self.knowledge_base = [
            # --- OPENINGS & HISTORY ---
            {
                "topic": "Sicilian Defense",
                "category": "Opening History",
                "content": "The Sicilian (1. e4 c5) was first analyzed by Giulio Polerio in 1594. It was once considered 'rebel chess' by the elite, but became the weapon of choice for Garry Kasparov. It is the most winning response to 1. e4.",
                "source": "Chess Knowledge Index v1.0 - Openings"
            },
            {
                "topic": "Ruy Lopez",
                "category": "Opening History",
                "content": "Named after the 16th-century Spanish priest Ruy López de Segura, this is 'The Spanish Torture.' It's one of the oldest openings, focusing on long-term pressure rather than immediate knockout blows.",
                "source": "Chess Knowledge Index v1.0 - Openings"
            },
            {
                "topic": "Queen's Gambit",
                "category": "Opening History",
                "content": "Popularized by the Netflix series, the Queen's Gambit (1. d4 d5 2. c4) is actually a 'pseudo-sacrifice.' If Black takes the pawn, White quickly regains it while controlling the center. It's the ultimate test of structural integrity.",
                "source": "Chess Knowledge Index v1.0 - Openings"
            },
            # --- TACTICS & PSYCHOLOGY ---
            {
                "topic": "Fork",
                "category": "Tactical Psychology",
                "content": "A fork attacks two pieces at once. Psychologically, it creates 'option paralysis'—the opponent must choose which piece to lose. Mikhail Tal once said, 'You must take your opponent into a deep dark forest where 2+2=5.'",
                "source": "Chess Knowledge Index v1.0 - Tactics"
            },
            {
                "topic": "Pin",
                "category": "Tactical Psychology",
                "content": "A pin is a knife to the throat. The pinned piece is physically on the board but spiritually paralyzed. As Siegbert Tarrasch noted: 'The power of a pin is that the threat is often stronger than its execution.'",
                "source": "Chess Knowledge Index v1.0 - Tactics"
            },
            {
                "topic": "Skewer",
                "category": "Tactical Psychology",
                "content": "The skewer is the 'inverse pin.' It forces the most valuable piece to run for its life, leaving its loyal subjects behind to be captured. It's a brutal demonstration of hierarchy on the board.",
                "source": "Chess Knowledge Index v1.0 - Tactics"
            },
            # --- PLAYER QUOTES & PHILOSOPHY ---
            {
                "topic": "Bobby Fischer",
                "category": "Quote",
                "content": "Bobby Fischer famously said: 'Chess is war over the board. The object is to crush the opponent's mind.' This aggressive philosophy defined the 1970s era of chess.",
                "source": "Chess Knowledge Index v1.0 - Famous Players"
            },
            {
                "topic": "Mikhail Tal",
                "category": "Quote",
                "content": "The 'Magician from Riga' Mikhail Tal believed: 'There are two types of sacrifices: correct ones, and mine.' He prioritized tactical chaos over material safety.",
                "source": "Chess Knowledge Index v1.0 - Famous Players"
            },
            {
                "topic": "Blunder",
                "category": "Psychology",
                "content": "Blunders often happen due to 'chess blindness' or the 'Kotov Syndrome'—where a player thinks for 20 minutes, gets confused, and makes a move they didn't even calculate.",
                "source": "Chess Knowledge Index v1.0 - Glossary"
            },
            # --- STRUCTURE ---
            {
                "topic": "Development",
                "category": "Structure",
                "content": "Development is the deployment of your army. Bringing pieces out without a plan is just 'moving'; bringing them out to control the center is 'developing.' Time is the only resource you can never get back.",
                "source": "Chess Knowledge Index v1.0 - Fundamentals"
            },
            {
                "topic": "Castling",
                "category": "Structure",
                "content": "Castling is the only time the King runs to the corner. It's a transition from 'opening' to 'middlegame.' A king in the center after move 15 is a king in a coffin.",
                "source": "Chess Knowledge Index v1.0 - Strategy"
            }
        ]

    def retrieve_context(self, query):
        """
        Simulates agentic knowledge retrieval.
        Finds relevant chess concepts based on the query.
        """
        relevant_chunks = []
        query_lower = query.lower()
        
        # Enhanced matching: check topic, category, and content keywords
        for chunk in self.knowledge_base:
            match_score = 0
            
            # Direct topic/category match
            if chunk["topic"].lower() in query_lower or chunk["category"].lower() in query_lower:
                match_score += 10
            
            # Keyword matching
            query_words = set(query_lower.replace("?", "").replace(".", "").split())
            content_words = set(chunk["content"].lower().split())
            matches = query_words.intersection(content_words)
            match_score += len(matches)

            if match_score > 0:
                relevant_chunks.append((match_score, chunk))
        
        # Sort by score descending and return top 3
        relevant_chunks.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in relevant_chunks[:3]]

    def get_grounded_prompt(self, base_prompt, context_chunks):
        """
        Anchors the prompt to retrieved knowledge.
        """
        if not context_chunks:
            return base_prompt
            
        context_str = "\n\n".join([f"Source: {c['source']} ({c['category']})\nTopic: {c['topic']}\nContent: {c['content']}" for c in context_chunks])
        
        grounded_instructions = (
            "You are an expert AI Chess Coach. Use the following GROUNDED KNOWLEDGE "
            "from Microsoft Foundry IQ to provide accurate coaching. If the information "
            "is not in the context, use your general knowledge but prioritize the sources below.\n\n"
            f"### RETRIEVED CHESS KNOWLEDGE:\n{context_str}\n\n"
            f"### USER REQUEST:\n{base_prompt}"
        )
        
        return grounded_instructions
