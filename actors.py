class Actor:
    def __init__(self, stack, table):
        self.hole_cards = []
        self.stack = stack
        self.active = True
        self.position = ""
        self.amount_in_round = 0
        self.acted = True
        self.groups = {}
        self.table = table

    def get_card(self, card): # assigns a card to the actor
        self.hole_cards.append(card)

    def give_position(self, position): # assigned a position to the actor
        self.position = position

    def cards(self):
        cards = []
        if len(self.hole_cards) != 0:
            for card in self.hole_cards:
                cards.append(card.show())
        else:
            for groups in self.groups.values():
                group = [card.show() for card in groups]
                cards.append(group)
        return cards
    
    def make_preflop_choice(self,variation):
        if variation == 'regret':
            print("Choose 2 from : ", self.cards())
            for i in range(3):
                valid_choice = False
                while not valid_choice:
                    pair = input("Enter your pair " + str(i+1) + " (1,2 for 1st and 2nd card): ")
                    pair = pair.split(",")
                    pair = [self.hole_cards[int(pair[0])-1], self.hole_cards[int(pair[1])-1]]
                    if (pair[0] in self.hole_cards) and (pair[1] in self.hole_cards):
                        self.groups['pair' + str(i+1)] = pair
                        self.hole_cards.remove(pair[0])
                        self.hole_cards.remove(pair[1])
                        valid_choice = True
                    else:
                        print("Invalid pair selected. Please try again.")
                    if i!=2:
                        print("Choose 2 from : ", self.cards())
            print()
                        
    def action(self, actions, high_bet):
        action = ""
        print(self.cards())
        print(self.position, self.stack)
        print(actions)
        while not action or action[0] not in actions:
            action = input("Enter your action: ")
        print()

        if action[0] == "F":
            return self.fold()
        elif action[0] == "B" or action[0] == "R":
            return self.bet(int(action[2:]) - self.amount_in_round)
        elif action[0] == "C":
            return self.bet(high_bet - self.amount_in_round)
        else:
            return 0

    def fold(self):
        self.active = False
        return 0

    def bet(self, amount):
        self.stack -= amount
        return amount

class Player(Actor):
    def __init__(self, stack, table):
        super().__init__(stack, table)
        self.id = "player"

class Bot(Actor):
    def __init__(self, stack, table):
        super().__init__(stack, table)
        self.id = "bot"