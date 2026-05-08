"""
Checkers (Draughts) Game - Board representation and game logic.
Implements an 8x8 board with standard capture and kinging rules.
"""

class Piece:
    """Represents a single piece on the board."""
    
    RED = 'red'
    BLACK = 'black'
    RED_KING = 'red_king'
    BLACK_KING = 'black_king'
    
    def __init__(self, color):
        self.color = color
        self.is_king = False
    
    def promote(self):
        """Promote piece to king."""
        if self.color == Piece.RED and not self.is_king:
            self.is_king = True
        elif self.color == Piece.BLACK and not self.is_king:
            self.is_king = True
    
    def __repr__(self):
        if self.is_king:
            return f"{self.color}_king"
        return self.color
    
    def to_char(self):
        """Return character representation for display."""
        if self.color == Piece.RED:
            return 'r' if not self.is_king else 'R'
        else:
            return 'b' if not self.is_king else 'B'


class Board:
    """8x8 Checkers board with piece management."""
    
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = Piece.RED
        self.red_pieces = 12
        self.black_pieces = 12
        self._setup_board()
    
    def _setup_board(self):
        """Set up initial board position with pieces on dark squares."""
        # Black pieces on rows 0-2 (top)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece(Piece.BLACK)
        
        # Red pieces on rows 5-7 (bottom)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Piece(Piece.RED)
    
    def display(self):
        """Display the board with row/column labels."""
        print("\n  a b c d e f g h")
        for row in range(8):
            print(f"{row + 1} ", end='')
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    # Show dark/light squares
                    if (row + col) % 2 == 1:
                        print(". ", end='')
                    else:
                        print("_ ", end='')
                else:
                    print(f"{piece.to_char()} ", end='')
            print(f"{row + 1}")
        print("  a b c d e f g h")
    
    def get_piece(self, row, col):
        """Get piece at position (row, col)."""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """Set piece at position (row, col)."""
        if 0 <= row < 8 and 0 <= col < 8:
            self.board[row][col] = piece
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds."""
        return 0 <= row < 8 and 0 <= col < 8
    
    def is_dark_square(self, row, col):
        """Check if position is a dark (playable) square."""
        return (row + col) % 2 == 1
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for piece at position."""
        piece = self.get_piece(row, col)
        if piece is None:
            return [], []
        
        moves = []  # (to_row, to_col) for simple moves
        captures = []  # (to_row, to_col, captured_row, captured_col)
        
        directions = []
        if piece.color == Piece.RED or piece.is_king:
            directions.append((-1, -1))  # up-left
            directions.append((-1, 1))   # up-right
        if piece.color == Piece.BLACK or piece.is_king:
            directions.append((1, -1))   # down-left
            directions.append((1, 1))    # down-right
        
        for dr, dc in directions:
            # Check simple move (one step)
            nr, nc = row + dr, col + dc
            if self.is_valid_position(nr, nc) and self.board[nr][nc] is None:
                moves.append((nr, nc))
            
            # Check capture (jump over opponent)
            jr, jc = row + 2 * dr, col + 2 * dc
            if self.is_valid_position(jr, jc) and self.board[jr][jc] is None:
                mr, mc = row + dr, col + dc  # Middle square
                middle_piece = self.get_piece(mr, mc)
                if middle_piece is not None and middle_piece.color != piece.color:
                    captures.append((jr, jc, mr, mc))
        
        return moves, captures
    
    def get_all_valid_moves(self, color):
        """Get all valid moves for all pieces of given color."""
        all_moves = {}
        
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == color:
                    moves, captures = self.get_valid_moves(row, col)
                    if moves or captures:
                        all_moves[(row, col)] = (moves, captures)
        
        return all_moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """
        Make a move from (from_row, from_col) to (to_row, to_col).
        Returns True if move was successful, False otherwise.
        """
        piece = self.get_piece(from_row, from_col)
        if piece is None:
            return False
        
        moves, captures = self.get_valid_moves(from_row, from_col)
        is_capture = (to_row, to_col) in [c[0:2] for c in captures]
        
        if (to_row, to_col) not in moves and not is_capture:
            return False
        
        # Check for mandatory captures (if any capture is available, must take it)
        all_moves = self.get_all_valid_moves(piece.color)
        has_capture = any(
            len(captures) > 0 
            for moves, captures in all_moves.values()
        )
        
        if has_capture and not is_capture:
            return False  # Must capture if available
        
        # Execute move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Handle capture
        if is_capture:
            for move_to_row, move_to_col, captured_row, captured_col in captures:
                if (move_to_row, move_to_col) == (to_row, to_col):
                    self.board[captured_row][captured_col] = None
                    if piece.color == Piece.RED:
                        self.black_pieces -= 1
                    else:
                        self.red_pieces -= 1
                    break
        
        # Handle kinging
        if piece.color == Piece.RED and to_row == 0:
            piece.promote()
        elif piece.color == Piece.BLACK and to_row == 7:
            piece.promote()
        
        return True
    
    def switch_turn(self):
        """Switch turn to other player."""
        self.turn = Piece.BLACK if self.turn == Piece.RED else Piece.RED
    
    def check_winner(self):
        """Check if there's a winner. Returns color of winner or None."""
        if self.red_pieces == 0:
            return Piece.BLACK
        if self.black_pieces == 0:
            return Piece.RED
        
        # Check if current player has any valid moves
        all_moves = self.get_all_valid_moves(self.turn)
        if not all_moves:
            return Piece.BLACK if self.turn == Piece.RED else Piece.RED
        
        return None
    
    def to_dict(self):
        """Convert board state to dictionary for serialization."""
        return {
            'board': [
                [p.to_char() if p else '_' for p in row]
                for row in self.board
            ],
            'turn': self.turn,
            'red_pieces': self.red_pieces,
            'black_pieces': self.black_pieces
        }


def parse_move(move_str):
    """
    Parse move string in format like '5a-9e' or '5-9'.
    Returns (from_row, from_col, to_row, to_col) or None if invalid.
    """
    move_str = move_str.strip().lower()
    
    # Try parsing formats like "5a-9e" or "5-9"
    if '-' not in move_str:
        return None
    
    parts = move_str.split('-')
    if len(parts) != 2:
        return None
    
    def parse_position(pos):
        """Parse a position like '5a' or '5'."""
        pos = pos.strip()
        
        # Handle format like '5a' (row column)
        if len(pos) >= 2 and pos[0].isdigit() and pos[1].isalpha():
            row = int(pos[0]) - 1
            col = ord(pos[1].lower()) - ord('a')
            return row, col
        
        # Handle format like '5' (just row number)
        if pos.isdigit():
            row = int(pos) - 1
            return row, None
        
        return None
    
    from_pos = parse_position(parts[0])
    to_pos = parse_position(parts[1])
    
    if from_pos is None or to_pos is None:
        return None
    
    if from_pos[1] is not None and to_pos[1] is not None:
        # Both have column specifications
        return (*from_pos, *to_pos)
    
    return None
