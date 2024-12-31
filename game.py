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

        if self.pvp_or_bots == "pvp":
            for _ in range(self.num_players):
                self.actors.append(Player(stack))
        elif self.pvp_or_bots == "bots":
            self.actors.append(Player(stack))
            for _ in range(self.num_players - 1):
                self.actors.append(Bot(stack))

        self.table = Table(self.variation, self.actors, self.small, self.big)

    def add_player(self, player):
        self.actors.append(player)

    def remove_player(self, player):
        self.actors.remove(player)