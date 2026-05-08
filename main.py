#!/usr/bin/env python3
"""
Checkers (Draughts) CLI Game
A command-line Checkers game with 8x8 board, turn-based play,
standard capture and kinging rules, and move notation input.
"""

import sys
from checkers import Board, Piece, parse_move


def print_board(board):
    """Print the board with helpful labels."""
    print("\n" + "=" * 50)
    print("Current Board State:")
    print("=" * 50)
    print("\n  a b c d e f g h")
    for row in range(8):
        print(f"{row + 1} ", end='')
        for col in range(8):
            piece = board.board[row][col]
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
    print(f"\nRed pieces remaining: {board.red_pieces}")
    print(f"Black pieces remaining: {board.black_pieces}")
    print(f"\nCurrent turn: {board.turn}")


def get_move_input(board, player_color):
    """Get move input from player."""
    while True:
        print(f"\n{player_color.upper()}'s turn")
        print("Enter move in format 'rowcol-rowcol' (e.g., '5a-4b' or '5-4')")
        print("Type 'quit' to exit, 'board' to redisplay board")
        
        move_str = input("Your move: ").strip().lower()
        
        if move_str == 'quit':
            return None
        elif move_str == 'board':
            print_board(board)
            continue
        
        # Try to parse the move
        result = parse_move(move_str)
        if result is None:
            print("Invalid move format. Please use format like '5a-4b'")
            continue
        
        from_row, from_col, to_row, to_col = result
        
        # Validate positions
        if not (0 <= from_row < 8 and 0 <= from_col < 8):
            print(f"Invalid from position: ({from_row + 1}, {chr(ord('a') + from_col)})")
            continue
        
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            print(f"Invalid to position: ({to_row + 1}, {chr(ord('a') + to_col)})")
            continue
        
        # Try to make the move
        success = board.make_move(from_row, from_col, to_row, to_col)
        if not success:
            print("Invalid move! Checkers rules apply:")
            print("- Pieces move diagonally forward")
            print("- Kings can move diagonally in any direction")
            print("- Captures are mandatory when available")
            print("- Must land on a dark square")
            continue
        
        return (from_row, from_col, to_row, to_col)


def play_game():
    """Main game loop."""
    print("=" * 50)
    print("Welcome to Checkers!")
    print("=" * 50)
    print("\nRules:")
    print("- Red moves first")
    print("- Pieces move diagonally forward one square")
    print("- Kings can move diagonally in any direction")
    print("- Captures are made by jumping over opponent pieces")
    print("- Captures are mandatory when available")
    print("- Reach the opposite end to become a King")
    print("- Win by capturing all opponent pieces or blocking them")
    print("\nMove format: 'rowcol-rowcol' (e.g., '5a-4b')")
    print("Example: '5a' means row 5, column a")
    
    board = Board()
    
    while True:
        print_board(board)
        
        # Check for winner
        winner = board.check_winner()
        if winner:
            print_board(board)
            print(f"\n{'=' * 50}")
            print(f"GAME OVER! {winner.upper()} WINS!")
            print(f"{'=' * 50}")
            break
        
        # Get player move
        current_player = board.turn
        move = get_move_input(board, current_player)
        
        if move is None:
            print("\nGame quit by player.")
            print("Thanks for playing!")
            break
        
        # Switch turn
        board.switch_turn()
        
        print(f"\nMove: ({move[0] + 1}{chr(ord('a') + move[1])}) to ({move[2] + 1}{chr(ord('a') + move[3])})")
    
    print("\nGame session ended.")


def main():
    """Entry point."""
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        print("Thanks for playing!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
