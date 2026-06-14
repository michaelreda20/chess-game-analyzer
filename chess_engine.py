import chess
import chess.pgn
import io

class ChessEngine:
    def __init__(self):
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
        # joins moves into a string to match against the DB
        # We'll check from longest to shortest to avoid partial matches
        moves_str = " ".join(moves_san[:6]) 
        
        # Sort by length of key descending
        sorted_keys = sorted(self.openings_db.keys(), key=len, reverse=True)
        
        for pattern in sorted_keys:
            if moves_str.startswith(pattern):
                return self.openings_db[pattern]
        return None

    def get_piece_value(self, piece):
        if piece is None:
            return 0
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values.get(piece.piece_type, 0)

    def get_material_balance(self, board):
        balance = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                val = self.get_piece_value(piece)
                if piece.color == chess.WHITE:
                    balance += val
                else:
                    balance -= val
        return balance

    def analyze_pgn(self, pgn_string):
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

        blunders = 0
        mistakes = 0
        excellent = 0
        
        for i, move in enumerate(mainline_moves):
            move_number = (i // 2) + 1
            is_white_turn = board.turn == chess.WHITE
            color = "White" if is_white_turn else "Black"
            san = board.san(move)
            
            # Information before the move
            from_square = move.from_square
            to_square = move.to_square
            piece_moved = board.piece_at(from_square)
            piece_captured = board.piece_at(to_square)
            
            # Execute the move
            board.push(move)
            
            is_blunder = False
            is_excellent = False
            alerts = []
            comment = ""
            
            # 1. Check if the piece moved was hung for free (without capturing something of equal/greater value)
            if board.is_attacked_by(board.turn, to_square):
                defenders = board.attackers(not board.turn, to_square)
                if not defenders:
                    val_moved = self.get_piece_value(piece_moved)
                    val_captured = self.get_piece_value(piece_captured)
                    
                    # If it's a capture, it's only a blunder if we lose more than we gain
                    if "x" in san:
                        if val_moved > val_captured:
                            is_blunder = True
                            comment = f"Blunder: {color} traded a {chess.piece_name(piece_moved.piece_type)} for a {chess.piece_name(piece_captured.piece_type)} without compensation!"
                    # If it wasn't a capture and it's hung
                    elif val_moved >= 3:
                        is_blunder = True
                        comment = f"Blunder: {color} left a {chess.piece_name(piece_moved.piece_type)} hanging!"
            
            # 2. Check if the move left ANOTHER piece hanging (that wasn't the one that moved)
            if not is_blunder:
                for square in chess.SQUARES:
                    if square == to_square: continue # Already checked the piece that moved
                    
                    piece = board.piece_at(square)
                    if piece and piece.color == (not board.turn): # Side that just moved
                        if board.is_attacked_by(board.turn, square):
                            defenders = board.attackers(not board.turn, square)
                            if not defenders:
                                val = self.get_piece_value(piece)
                                if val >= 3:
                                    is_blunder = True
                                    comment = f"Blunder: {color} left a {chess.piece_name(piece.piece_type)} hanging!"
                                    break

            if is_blunder:
                alerts.append("BLUNDER")
                blunders += 1
            
            if board.is_checkmate():
                comment = f"Checkmate! {color} wins."
                is_excellent = True
                alerts.append("CHECKMATE")
                excellent += 1
            elif not is_blunder and board.is_check():
                comment = f"{color} gives check."
                alerts.append("CHECK")
            
            if not is_blunder and not is_excellent and "x" in san:
                comment = f"{color} captures a piece."
                alerts.append("CAPTURE")
            
            moves_data.append({
                "move_index": i + 1,
                "move_number": move_number,
                "move_color": color,
                "san": san,
                "is_blunder": is_blunder,
                "is_excellent": is_excellent,
                "alerts": alerts,
                "comment": comment
            })

        return {
            "white": white_player,
            "black": black_player,
            "result": result,
            "opening": opening,
            "total_moves": len(moves_data),
            "blunders": blunders,
            "mistakes": mistakes,
            "excellent": excellent,
            "moves": moves_data
        }
