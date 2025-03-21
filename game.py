from table import Table
from actors import Player, Bot

class Game:
    def __init__(self, pvp_or_bots, variation, num_players, small, big, stack):
        self.pvp_or_bots = pvp_or_bots
        self.num_players = num_players
        self.small = small
        self.big = big
        self.stack = stack
        self.actors = []
        self.variation = variation

        self.table = Table(self.variation, self.actors, self.small, self.big)

        if self.pvp_or_bots == "pvp":
            for _ in range(self.num_players):
                self.actors.append(Player(stack, self.table))
        elif self.pvp_or_bots == "bots":
            self.actors.append(Player(stack, self.table))
            for _ in range(self.num_players - 1):
                self.actors.append(Bot(stack, self.table))

    def add_player(self, player):
        self.actors.append(player)

    def remove_player(self, player):
        self.actors.remove(player)

    def start_game(self):
        self.table.play_round()
        while input("Continue? (y/n) ") == "y":
            self.table.round_number += 1
            self.table.play_round()