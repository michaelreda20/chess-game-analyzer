from flask import Flask, render_template, request, jsonify
from chess_engine import ChessEngine
from foundry_iq import FoundryIQ
from gemini_coach import GeminiCoach
import os

app = Flask(__name__)

# Initialize components
engine = ChessEngine()
foundry = FoundryIQ()
coach = GeminiCoach()

@app.route('/')
def index():
    sample_pgn = '[Event "Casual Game"]\n[Site "Online"]\n[Date "2026.06.13"]\n[White "Player1"]\n[Black "Player2"]\n[Result "1-0"]\n\n1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 e5 6. Ndb5 d6 7. Bg5 a6 8. Na3 b5 9. Bxf6 gxf6 10. Nd5 f5 11. Bd3 Be6 12. O-O Bxd5 13. exd5 Ne7 14. c3 Bg7 15. Qh5 e4 16. Bc2 O-O 17. Rae1 b4 18. cxb4 Bxb2 19. Nc4 Bc3 20. Re3 Bxd4 21. Rh3 Re8 22. Qxh7+ Kf8 23. Rg3 Ng6 24. Bb3 Qf6 25. Na5 f4 26. Rh3 e3 27. fxe3 Rxe3 28. Kh1 Rxh3 29. Qxh3 Kg7 30. Nc6 Rh8 31. Qg4 Rh4 32. Qf3 Rxh2+ 33. Kxh2 Qh4+ 34. Qh3 Bg1+ 35. Kxg1 Qxh3 36. gxh3 1-0'
    return render_template('index.html', sample_pgn=sample_pgn)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    pgn = data.get('pgn')
    
    if not pgn:
        return jsonify({"error": "No PGN provided"}), 400
        
    # 1. Engine Analysis
    analysis = engine.analyze_pgn(pgn)
    if "error" in analysis:
        return jsonify(analysis), 400
        
    # 2. Foundry IQ Retrieval
    # We'll search for context based on the opening and result
    query = f"{analysis['opening']} chess game {analysis['result']}"
    context_chunks = foundry.retrieve_context(query)
    
    # 3. Gemini Coaching
    base_prompt = (
        f"Review this chess game where {analysis['white']} played as White and {analysis['black']} as Black. "
        f"The opening was {analysis['opening']}. "
        "Analyze the full move timeline and provide constructive feedback."
    )
    
    grounded_prompt = foundry.get_grounded_prompt(base_prompt, context_chunks)
    
    verdict, coaching = coach.generate_coaching(analysis, grounded_prompt)
    
    # 4. Combine results
    analysis['verdict'] = verdict
    analysis['coaching'] = coaching
    
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
