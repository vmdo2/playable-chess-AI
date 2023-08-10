import chess.pgn
import re
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

# Define the number of unique pieces and positions on the board
num_pieces = 6  # Pawn, Knight, Bishop, Rook, Queen, King
num_positions = 64  # 8x8 board

# Regular expression pattern to extract evaluation and best move
eval_pattern = re.compile(r"[%]eval:\s+([-+]?\d+)")
best_move_pattern = re.compile(r"[%]best_move:\s+(\S+)")

# Load PGN data from a single file
train_pgn_file = "c:/Users/vince/Downloads/magnus_evalv2.pgn"

# Load PGN data using python-chess
pgn = open(train_pgn_file)
games = []
max_moves = 0
while True:
    game = chess.pgn.read_game(pgn)
    if game is None:
        break

    # Count the number of moves in the game
    num_moves = sum(1 for _ in game.mainline_moves())

    # TODO update max moves
    # Update max_moves if necessary
    if num_moves > max_moves:
        max_moves = num_moves

    games.append(game)

pgn.close()
print(max_moves)

def move_to_numeric(move):
    # Convert algebraic notation to a one-hot encoded array

    # Define the alphabet for the chess squares (a-h)
    alphabet = 'abcdefgh'

    # Get source and target squares from the move object
    source_square = move.from_square
    target_square = move.to_square

    # Create a one-hot encoded array for the move
    move_numeric = [0] * (num_positions * 2)  # Two positions for source and target squares
    move_numeric[source_square] = 1
    move_numeric[num_positions + target_square] = 1

    return move_numeric

# Process training data and prepare inputs and ground truth
x_train, y_train_eval, y_train_move = [], [], []

for game in games:
    board = game.board()
    for move_number, move in enumerate(game.mainline_moves()):
        fen = board.fen()

        # Extract evaluation from PGN data
        eval_match = eval_pattern.search(str(move))
        if eval_match:
            evaluation = int(eval_match.group(1))
        else:
            evaluation = 0  # Default evaluation if not found

        # Extract best move from PGN data
        best_move_match = best_move_pattern.search(str(move))
        if best_move_match:
            best_move = best_move_match.group(1)
        else:
            best_move = None  # Default best move if not found

        # Append data to lists
        x_train.append(move_to_numeric(move))
        y_train_eval.append(evaluation / 100.0)  # Normalize evaluation to [-1, 1]
        y_train_move.append(1.0 if best_move else 0.0)

# Convert lists to NumPy arrays
x_train = np.array(x_train)
y_train_eval = np.array(y_train_eval)
y_train_move = np.array(y_train_move)

# Create a feedforward neural network model
def create_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='linear'),  # Output layer for evaluation prediction
        layers.Dense(1, activation='sigmoid')  # Output layer for best move prediction
    ])
    return model

# Custom loss function for chess move prediction
def custom_chess_loss(y_true, y_pred):
    # Split y_pred into evaluation predictions and best move predictions
    eval_pred = y_pred[:, 0]
    move_pred = y_pred[:, 1]

    # Split y_true into actual evaluations and best move indicators
    actual_eval = y_true[:, 0]
    best_move_indicators = y_true[:, 1]

    # Calculate mean squared error for evaluation predictions
    mse_eval = keras.losses.mean_squared_error(actual_eval, eval_pred)

    # Calculate binary cross-entropy for best move predictions
    bce_move = keras.losses.binary_crossentropy(best_move_indicators, move_pred)

    # Combine the two loss components with appropriate weights
    total_loss = mse_eval + bce_move

    return total_loss

# Define input shape based on the number of features in your input data
num_moves = max_moves
input_shape = (num_moves * (num_pieces + num_positions) + 1,)

# Create and compile the model
model = create_model(input_shape)
model.compile(optimizer='adam', loss=custom_chess_loss, metrics=['mae'])

# Define callbacks for early stopping and learning rate scheduling
early_stopping = EarlyStopping(patience=10, restore_best_weights=True)
def lr_scheduler(epoch, lr):
    if epoch < 30:
        return lr
    else:
        return lr * tf.math.exp(-0.1)
learning_rate_scheduler = LearningRateScheduler(lr_scheduler)

# Train the model with callbacks
batch_size = 32
num_epochs = 50
history = model.fit(
    x_train, [y_train_eval, y_train_move], batch_size=batch_size, epochs=num_epochs,
    validation_split=0.2, callbacks=[early_stopping, learning_rate_scheduler]
)

# Save the trained model
model.save('trained_chess_model.h5')

# -----------------------
# Testing the trained model

# Load the trained model
model = keras.models.load_model('trained_chess_model.h5')

# Load PGN data from your test PGN file
test_pgn_file = "c:/Users/vince/Downloads/GM_games_eval.pgn.pgn"

# Load PGN data using python-chess
pgn = open(test_pgn_file)
games = []

while True:
    game = chess.pgn.read_game(pgn)
    if game is None:
        break
    games.append(game)

pgn.close()

# Process test data and prepare inputs and ground truth
x_test, y_test_eval, y_test_move = [], [], []

for game in games:
    board = game.board()
    for move_number, move in enumerate(game.mainline_moves()):
        fen = board.fen()

        # Extract evaluation from PGN data
        eval_match = eval_pattern.search(str(move))
        if eval_match:
            evaluation = int(eval_match.group(1))
        else:
            evaluation = 0  # Default evaluation if not found

        # Extract best move from PGN data
        best_move_match = best_move_pattern.search(str(move))
        if best_move_match:
            best_move = best_move_match.group(1)
        else:
            best_move = None  # Default best move if not found

        # Append data to lists
        x_test.append(move_to_numeric(move))
        y_test_eval.append(evaluation / 100.0)  # Normalize evaluation to [-1, 1]
        y_test_move.append(1.0 if best_move else 0.0)

# Convert lists to NumPy arrays
x_test = np.array(x_test)
y_test_eval = np.array(y_test_eval)
y_test_move = np.array(y_test_move)

# Predict using the model
predictions = model.predict(x_test)

# Extract predicted evaluation scores and best move indicators
predicted_evaluations = predictions[:, 0]
predicted_best_moves = (predictions[:, 1] > 0.5).astype(int)

# Evaluate model performance
eval_mse = np.mean((y_test_eval - predicted_evaluations)**2)
move_accuracy = np.mean(np.equal(y_test_move, predicted_best_moves))

# Display results
print("Evaluation MSE:", eval_mse)
print("Move Accuracy:", move_accuracy)