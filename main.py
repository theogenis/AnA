from board_setup import setup_board
from turn_manager import TurnManager

# Setup the board
players, territories = setup_board()

# Define unit prices
unit_prices = {
    "Infantry": 3,
    "Tank": 5,
    "Fighter": 10,
    "Bomber": 15
}

# Create TurnManager
turn_manager = TurnManager(players, territories, unit_prices)

# Start game loop
turn_manager.play_game()