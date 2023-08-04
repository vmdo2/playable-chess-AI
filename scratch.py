import pygame
from PIL import Image
import chess
import chess_player

# Set up the Pygame window
pygame.init()
WINDOW_SIZE = 400
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Chessboard')
clock = pygame.time.Clock()

# Load the chessboard image from your computer
board_image_path = "C:/Users/vince/Downloads/pieces/board.png"  # Replace this with the file path to the downloaded chessboard image
image = Image.open(board_image_path)
image = image.resize((WINDOW_SIZE, WINDOW_SIZE))

# Convert the PIL image to a Pygame surface
mode = image.mode
size = image.size
data = image.tobytes()
chessboard_img = pygame.image.fromstring(data, size, mode)

# Initialize the chessboard and other variables
board = chess.Board()
selected_square = None
# Function to convert Pygame coordinates to chessboard coordinates
def to_chess_coords(pygame_coords):
    x, y = pygame_coords
    col = x // (WINDOW_SIZE // 8)
    row = 7 - y // (WINDOW_SIZE // 8)
    return chess.square(col, row)

# Function to convert chessboard coordinates to Pygame coordinates
def to_pygame_coords(chess_coords):
    col = chess.square_file(chess_coords)
    row = 7 - chess.square_rank(chess_coords)
    return col * (WINDOW_SIZE // 8), row * (WINDOW_SIZE // 8)

# Main loop for handling events and rendering
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
            x, y = event.pos
            square = to_chess_coords((x, y))
            piece = board.piece_at(square)
            if piece is not None:
                selected_square = square
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button release
            if selected_square is not None:
                x, y = event.pos
                target_square = to_chess_coords((x, y))
                move = chess.Move(selected_square, target_square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

    # Clear the screen and draw the chessboard image
    screen.fill((255, 255, 255))
    screen.blit(chessboard_img, (0, 0))

    # Draw the pieces on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            # Determine the color of the piece
            color_suffix = "_w" if piece.color == chess.WHITE else "_b"

            # Load the piece image based on the filename with color suffix
            piece_image = pygame.image.load(f"C:/Users/vince/Downloads/pieces/{piece.symbol()}{color_suffix}.png")
            piece_image = pygame.transform.scale(piece_image, (WINDOW_SIZE // 8, WINDOW_SIZE // 8))

            # Calculate the position to center the piece image on the square
            x, y = to_pygame_coords(square)
            piece_x = x + (WINDOW_SIZE // 8 - piece_image.get_width()) // 2
            piece_y = y + (WINDOW_SIZE // 8 - piece_image.get_height()) // 2

            screen.blit(piece_image, (piece_x, piece_y))

    # Update the display
    pygame.display.flip()

    # Check if it's the AI's turn and get its move
    if not board.is_game_over() and board.turn == chess.BLACK:
        ai_move = chess_player.get_best_move(board)
        board.push(ai_move)

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()