import tkinter as tk
import math
import time

# Create the main application window
root = tk.Tk()
root.title("Tic Tac Toe")

# Set the dimensions of the game window
WIDTH = 500
HEIGHT = 500
LINE_WIDTH = 15
BOARD_SIZE = 3
SQUARE_SIZE = WIDTH // BOARD_SIZE

# Define colors
BG_COLOR = "#b09f93"
LINE_COLOR = "#000000"
O_COLOR = "#00FF00"
X_COLOR = "#FFFFFF"

# Create the canvas for drawing the game board
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
canvas.pack()

# Create the game board
board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# Define the players
HUMAN = "X"
COMPUTER = "O"
current_player = HUMAN

# Flag to indicate if the game is over
game_over = False

# Flag to indicate if the game is in the home page
home_page = True

# Flag to indicate if it's AI vs AI mode
ai_vs_ai_mode = False

# Function to start the game
def start_game():
    """Starts a new game between a human and AI."""
    global home_page, ai_vs_ai_mode
    home_page = False
    ai_vs_ai_mode = False
    canvas.delete("all")
    draw_lines()
    draw_figures()
    result_label.config(text="")
    root.update()

# Function to start AI vs AI mode
def start_ai_vs_ai():
    """Starts an AI vs AI game mode."""
    global home_page, ai_vs_ai_mode
    home_page = False
    ai_vs_ai_mode = True
    canvas.delete("all")
    draw_lines()
    play_ai_vs_ai()
    result = get_board_score()
    if result == 1:
        result_label.config(text="AI O wins!")
    elif result == -1:
        result_label.config(text="AI X wins!")
    else:
        result_label.config(text="It's a draw!")
    root.update()

# Create the home page frame and options
home_frame = tk.Frame(root)
home_frame.pack()

label = tk.Label(home_frame, text="Select an Option", font=("Helvetica", 24))
label.pack()

# Create the "Human vs AI" button
human_vs_ai_button = tk.Button(
    home_frame, text="Human vs AI", font=("Helvetica", 18), command=start_game,
    borderwidth=5, relief="ridge", width=15
)
human_vs_ai_button.pack()

# Create the "AI vs AI" button
ai_vs_ai_button = tk.Button(
    home_frame, text="AI vs AI", font=("Helvetica", 18), command=start_ai_vs_ai,
    borderwidth=5, relief="ridge", width=15
)
ai_vs_ai_button.pack()

# Function to change the button color when clicked
def button_click_effect(button):
    """Changes the button's background color temporarily when clicked."""
    button.config(bg="#FF5733")  # Change the background color to blue when clicked
    root.update()
    root.after(100, lambda: button.config(bg="#FFFFFF"))  # Reset the color after 100ms

# Bind the click effect to the buttons
human_vs_ai_button.bind("<Button-1>", lambda event, button=human_vs_ai_button: button_click_effect(button))
ai_vs_ai_button.bind("<Button-1>", lambda event, button=ai_vs_ai_button: button_click_effect(button))

# Function to reset the game
def reset_game():
    """Resets the game board and flags for a new game."""
    global board, current_player, game_over
    board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    current_player = HUMAN
    game_over = False
    canvas.delete("all")
    draw_lines()
    result_label.config(text="")
    root.update()

def handle_mouse_click(event):
    """Handles mouse clicks during the game."""
    global current_player, game_over, home_page

    if home_page or ai_vs_ai_mode:
        return

    if game_over:
        reset_game()
        return

    if current_player == HUMAN:
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if board[row][col] is None:
            mark_square(row, col, current_player)
            draw_figures()
            print_move(row, col)
            root.update()

            if is_winner(current_player):
                show_game_over(get_board_score())
                game_over = True
                return

            if is_draw():
                show_game_over(0)
                game_over = True
                return

            current_player = COMPUTER

            # Handle computer's move
            row, col = get_best_move()
            mark_square(row, col, current_player)
            draw_figures()
            print_move(row, col)
            root.update()

            if is_winner(current_player):
                show_game_over(get_board_score())
                game_over = True
                return

            if is_draw():
                show_game_over(0)
                game_over = True
                return
            time.sleep(1)
            current_player = HUMAN

def print_move(row, col):
    """Prints a move made by a player to the console."""
    print_board()
    print(f"Player {current_player} moved to row {row}, col {col}")

def print_board():
    """Prints the current state of the game board to the console."""
    for row in board:
        print(" ".join([player if player else "-" for player in row]))
    print()

def draw_lines():
    """Draws the game board grid lines on the canvas."""
    # Draw the horizontal lines
    for i in range(1, BOARD_SIZE):
        canvas.create_line(0, i * SQUARE_SIZE, WIDTH, i * SQUARE_SIZE, fill=LINE_COLOR, width=LINE_WIDTH)

    # Draw the vertical lines
    for i in range(1, BOARD_SIZE):
        canvas.create_line(i * SQUARE_SIZE, 0, i * SQUARE_SIZE, HEIGHT, fill=LINE_COLOR, width=LINE_WIDTH)

def draw_figures():
    """Draws X and O symbols on the canvas."""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == COMPUTER:
                canvas.create_oval(col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4,
                                   (col + 1) * SQUARE_SIZE - SQUARE_SIZE // 4, (row + 1) * SQUARE_SIZE - SQUARE_SIZE // 4,
                                   outline=X_COLOR, width=LINE_WIDTH)
            elif board[row][col] == HUMAN:
                canvas.create_line(col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4,
                                   (col + 1) * SQUARE_SIZE - SQUARE_SIZE // 4, (row + 1) * SQUARE_SIZE - SQUARE_SIZE // 4,
                                   fill=X_COLOR, width=LINE_WIDTH)
                canvas.create_line((col + 1) * SQUARE_SIZE - SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4,
                                   col * SQUARE_SIZE + SQUARE_SIZE // 4, (row + 1) * SQUARE_SIZE - SQUARE_SIZE // 4,
                                   fill=X_COLOR, width=LINE_WIDTH)

def mark_square(row, col, player):
    """Marks a square on the game board with the player's symbol."""
    board[row][col] = player

def available_moves():
    """Returns a list of available moves on the game board."""
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] is None:
                moves.append((row, col))
    return moves

def is_winner(player):
    """Checks if the given player has won the game."""
    # Check rows
    for row in range(BOARD_SIZE):
        if all(board[row][col] == player for col in range(BOARD_SIZE)):
            return True

    # Check columns
    for col in range(BOARD_SIZE):
        if all(board[row][col] == player for row in range(BOARD_SIZE)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_SIZE)):
        return True

    if all(board[i][BOARD_SIZE - i - 1] == player for i in range(BOARD_SIZE)):
        return True

    return False

def is_draw():
    """Checks if the game is a draw (no more available moves)."""
    return all(board[row][col] is not None for row in range(BOARD_SIZE) for col in range(BOARD_SIZE))

def get_board_score():
    """Determines the current score of the game board."""
    if is_winner(COMPUTER):
        return 1
    elif is_winner(HUMAN):
        return -1
    else:
        return 0

def minimax(board, depth, alpha, beta, maximizing_player):
    """Implements the minimax algorithm to find the best move for the computer player."""
    if depth == 0 or is_winner(HUMAN) or is_winner(COMPUTER) or is_draw():
        return get_board_score()

    if maximizing_player:
        max_eval = float("-inf")
        for move in available_moves():
            row, col = move
            board[row][col] = COMPUTER
            evaluation = minimax(board, depth - 1, alpha, beta, False)
            board[row][col] = None
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in available_moves():
            row, col = move
            board[row][col] = HUMAN
            evaluation = minimax(board, depth - 1, alpha, beta, True)
            board[row][col] = None
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval

def get_best_move():
    """Finds the best move for the computer player using the minimax algorithm."""
    best_score = float("-inf")
    best_move = None
    for move in available_moves():
        row, col = move
        board[row][col] = COMPUTER
        score = minimax(board, BOARD_SIZE ** 2, float("-inf"), float("inf"), False)
        board[row][col] = None
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def print_result(result):
    """Returns a text description of the game result."""
    if result == 1:
        return "Computer wins!"
    elif result == -1:
        return "You win!"
    else:
        return "It's a draw!"

def show_game_over(result):
    """Displays the game result on the GUI."""
    if ai_vs_ai_mode:
        if result == 1:
            if current_player == COMPUTER:
                result_label.config(text="AI X wins!")
            else:
                result_label.config(text="AI O wins!")
        elif result == -1:
            if current_player == COMPUTER:
                result_label.config(text="AI O wins!")
            else:
                result_label.config(text="AI X wins!")
        else:
            result_label.config(text="It's a draw!")
    else:
        result_label.config(text=print_result(result))

def play_ai_vs_ai():
    """Implements the AI vs AI game mode."""
    AI="X"

    global current_player, game_over
    current_player = AI
    while not game_over and ai_vs_ai_mode:
        # AI vs AI game loop
        time.sleep(1)  # Delay between AI moves for visibility
        if current_player == AI:
            row, col = get_best_move()
            mark_square(row, col, current_player)
            draw_figures()
            print_move(row, col)
            root.update()
            if is_winner(current_player):
                show_game_over(get_board_score())
                game_over = True
            elif is_draw():
                show_game_over(0)
                game_over = True
            current_player = COMPUTER
        else:
            row, col = get_best_move()
            mark_square(row, col, current_player)
            draw_figures()
            print_move(row, col)
            root.update()
            if is_winner(current_player):
                show_game_over(get_board_score())
                game_over = True
            elif is_draw():
                show_game_over(0)
                game_over = True
            current_player = AI

draw_lines()

canvas.bind("<Button-1>", handle_mouse_click)

result_label = tk.Label(root, text="", font=("Helvetica", 24))
result_label.pack()

root.mainloop()