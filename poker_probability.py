import poker_besthand
from functools import reduce
import operator as op
from itertools import combinations

import poker_comparehands


def betterhand_probability(hole_cards, community_cards, full_deck):
    remaining_deck = []
    for i in full_deck:
        if not(i in hole_cards):
            remaining_deck.append(i)

    player_hand = hole_cards + community_cards

    other_hands = list(combinations(remaining_deck, 2))

    all_other_hands = []
    for i in other_hands:
        all_other_hands.append(list(i) + community_cards)

    number_beaten = 0
    number_beats = 0
    for i in all_other_hands:
        answer = poker_comparehands.compare_hands(player_hand, i)
        if answer == 1:
            number_beats += 1
        elif answer == 2:
            number_beaten += 1

    probability_beats = number_beats/len(other_hands)
    probability_beaten = number_beaten/len(other_hands)

    return probability_beats, probability_beaten


def ncr(n, r):
    r = min(n-r, r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, 1+r), 1)
    return numer // denom


def besthand_probability(open_cards, current_deck):

    total_possibilities = ncr(len(current_deck), 7-len(open_cards))
    all_possibilities = list(combinations(current_deck, 7-len(open_cards)))

    besthand_counter = {'High Card': 0, 'Pair': 0, 'Two Pair': 0, 'Three of a Kind': 0, 'Straight': 0, 'Flush': 0, 'Full House': 0, 'Four of a Kind': 0, 'Straight Flush': 0, 'Royal Flush': 0}
    besthand_probabilities = {'High Card': 0, 'Pair': 0, 'Two Pair': 0, 'Three of a Kind': 0, 'Straight': 0, 'Flush': 0,
                        'Full House': 0, 'Four of a Kind': 0, 'Straight Flush': 0, 'Royal Flush': 0}

    for i in all_possibilities:
        cards = []
        cards.extend(open_cards)
        cards.extend(list(i))
        answer = poker_besthand.besthand(cards)
        besthand_counter[answer['hand']] += 1

    for i in list(besthand_counter.keys()):
        besthand_probabilities[i] = besthand_counter[i]/total_possibilities*100

    return besthand_probabilities

def return_besthandprobability(besthand_probabilities):

    high_hand = ""
    high_probability = 0
    for key in besthand_probabilities:
        if besthand_probabilities[key] > high_probability:
            high_probability = besthand_probabilities[key]
            high_hand = key

    return high_hand, high_probability

def besthandprobability_test():
    hole_cards = ['3C', '9D']
    value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    suits = ['S', 'H', 'D', 'C']
    full_deck = []
    for i in suits:
        for j in value:
            card = j + i
            full_deck.append(card)
    current_deck = []
    for i in full_deck:
        if not(i in hole_cards):
            current_deck.append(i)

    besthand_probability(hole_cards, current_deck)

def betterhandprobability_test():
    hole_cards = ['AS', 'AD']
    community_cards = ['2C', '3S', '6S', 'QS', 'AH']
    value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    suits = ['S', 'H', 'D', 'C']
    full_deck = []
    for i in suits:
        for j in value:
            card = j + i
            full_deck.append(card)

    print(betterhand_probability(hole_cards, community_cards, full_deck))