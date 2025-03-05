from game import Game

if __name__ == "__main__":
    game = Game("pvp", variation='texas', num_players=3, small=10, big=20, stack=1000)
    game.start_game()