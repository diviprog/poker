import random

numbers = '23456789TJQKA'
suits = 'SHDC'

class Deck:
    def __init__(self):
        self.deck = [Card(i + j) for i in numbers for j in suits]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)

    def choose_card(self):
        return self.deck.pop()
    
    def show(self):
        return [card.show() for card in self.deck]
    
    def return_card(self,card):
        self.deck.append(card)

class Card:
    def __init__(self, card):
        self.card = card
        self.number = card[0]
        self.suit = card[1]

    def show(self):
        return self.card