Poker Game Project

Overview

This project is a command-line implementation of a customizable poker game. It supports various poker variations, allows for both player-vs-player and player-vs-bots modes, and includes features like betting, community cards, and hand evaluation. The game is written in Python and is structured for modularity and scalability.

Features
	•	Multiple Poker Variations: Texas Hold’em, Omaha, and other custom modes.
	•	Player Modes: Supports Player-vs-Player (PvP) and Player-vs-Bots.
	•	Betting System: Implements small and big blinds, betting rounds, and pot management.
	•	Community Cards: Flop, Turn, and River phases are included.
	•	Hand Comparison: Determines the winner based on the best poker hand.

Prerequisites
	•	Python 3.7 or above

Installation
	1.	Clone the repository:

git clone https://github.com/your-username/poker-game.git


	2.	Navigate to the project directory:

cd poker-game


	3.	Install any dependencies (if needed):

pip install -r requirements.txt

How to Run
	1.	Navigate to the project directory.
	2.	Run the main script:

python main.py


	3.	Follow the on-screen instructions to play the game.

Project Structure

poker/
├── main.py                # Entry point for the game
├── actors.py              # Actor classes: Player, Bot, and Actor
├── cards.py               # Card and Deck management
├── table.py               # Table and game round logic
├── game.py                # Game initialization and setup
├── utils/
│   ├── variations.py      # Definitions for poker variations
│   ├── positions.py       # Player position mappings
│   └── hand_comparator.py # Hand comparison logic
└── README.md              # Project documentation

Gameplay Instructions
	1.	Starting the Game:
	•	Choose the game mode (PvP or Bots).
	•	Select the poker variation (e.g., Texas Hold’em, Omaha).
	•	Specify the number of players and initial stack sizes.
	2.	During the Game:
	•	Players are assigned positions (e.g., SB, BB, UTG).
	•	Cards are dealt, and betting rounds proceed (preflop, flop, turn, river).
	•	Players can choose actions like fold, bet, or call.
	3.	Winning:
	•	The player(s) with the best hand(s) win the pot.
	•	Hands are compared using poker hand rankings.

Customization

Adding New Variations
	1.	Open utils/variations.py.
	2.	Add a new variation to the dictionary:

variations['new_variation'] = [number_of_hole_cards, preflop_choice_required, discard_allowed]



Adding New Positions
	1.	Open utils/positions.py.
	2.	Update the positions dictionary with new mappings.

Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Future Enhancements
	•	Add graphical user interface (GUI).
	•	Implement more advanced AI for bots.
	•	Support for additional poker variations.
	•	Save and load game states.

Enjoy the game! 😊