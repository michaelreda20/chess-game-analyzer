import chess
import chess.pgn
import io

class ChessEngine:
    def __init__(self):
        # Local openings database for quick identification
        self.openings_db = {
            "e4 c5": "Sicilian Defense",
            "e4 e6": "French Defense",
            "e4 e5 Nf3 Nc6 Bb5": "Ruy Lopez",
            "e4 e5 Nf3 Nc6 Bc4": "Italian Game",
            "d4 d5 c4": "Queen's Gambit",
            "e4 e5 Nf3 Nf6": "Petrov's Defense",
            "e4 c6": "Caro-Kann Defense",
            "d4 Nf6 c4 e6 Nc3 Bb4": "Nimzo-Indian Defense",
            "e4 d5": "Scandinavian Defense",
            "e4 d6 d4 Nf6": "Pirc Defense",
            "e4 Nf6": "Alekhine's Defense",
            "d4 Nf6 c4 g6": "King's Indian Defense",
            "d4 d5 Bf4": "London System",
            "d4 d5 c4 c6": "Slav Defense",
            "d4 Nf6 c4 c5": "Benoni Defense",
            "c4": "English Opening",
            "Nf3": "Reti Opening"
        }

    def identify_opening(self, moves_san):
        """Identifies the opening based on the first few moves."""
        moves_str = " ".join(moves_san[:6]) 
        sorted_keys = sorted(self.openings_db.keys(), key=len, reverse=True)
        
        for pattern in sorted_keys:
            if moves_str.startswith(pattern):
                return self.openings_db[pattern]
        return None

    def analyze_pgn(self, pgn_string):
        """
        Parses PGN and returns a clean timeline of moves.
        Blunder detection is deferred to the LLM.
        """
        pgn = io.StringIO(pgn_string)
        game = chess.pgn.read_game(pgn)
        
        if game is None:
            return {"error": "Invalid PGN"}

        board = game.board()
        moves_data = []
        
        white_player = game.headers.get("White", "White")
        black_player = game.headers.get("Black", "Black")
        result = game.headers.get("Result", "*")
        
        mainline_moves = list(game.mainline_moves())
        all_moves_san = []
        
        # Pre-calculate SANs for opening detection
        temp_board = game.board()
        for m in mainline_moves:
            all_moves_san.append(temp_board.san(m))
            temp_board.push(m)
            
        opening = game.headers.get("Opening")
        if not opening or opening == "Unknown Opening":
            identified = self.identify_opening(all_moves_san)
            opening = identified if identified else "Unknown Opening"

        for i, move in enumerate(mainline_moves):
            move_number = (i // 2) + 1
            is_white_turn = board.turn == chess.WHITE
            color = "White" if is_white_turn else "Black"
            san = board.san(move)
            
            # Check for capture before pushing the move
            captured_piece = board.piece_at(move.to_square)
            is_capture = "x" in san
            captured_type = chess.piece_name(captured_piece.piece_type) if captured_piece else None
            
            board.push(move)
            
            moves_data.append({
                "move_index": i + 1,
                "move_number": move_number,
                "move_color": color,
                "san": san,
                "is_capture": is_capture,
                "captured_piece_type": captured_type
            })

        return {
            "white": white_player,
            "black": black_player,
            "result": result,
            "opening": opening,
            "total_moves": len(moves_data),
            "moves": moves_data
        }
