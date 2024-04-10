import random
from poker_probability import besthand_probability, return_besthandprobability

def texas_holdem(full_deck):

    # initialising the table
    current_deck = full_deck
    num_players = 5

    # initialising hole cards
    hole_cards = {'player': []}

    # distributing hole cards to the player
    for i in range(2):
        chosen_card = random.choice(current_deck)
        hole_cards['player'].append(chosen_card)
        current_deck.remove(chosen_card)

    # distributing hole cards to the bots
    for i in range(num_players-1):
        bot_name = 'bot'+str(i+1)
        bot_hand = []
        for j in range(2):
            chosen_card = random.choice(current_deck)
            bot_hand.append(chosen_card)
            current_deck.remove(chosen_card)
        hole_cards[bot_name] = bot_hand

    print("Your hole cards are : ", hole_cards['player'])
    besthand_probabilities = besthand_probability(hole_cards['player'],current_deck)
    besthand, besthandprobability = return_besthandprobability(besthand_probabilities)
    print("Your most probable hand is", besthand, "with a probability of", round(besthandprobability,2),"%")
    print()

    # initialising the community cards
    community_cards = []

    # laying out the flop
    flop = []
    for i in range(3):
        chosen_card = random.choice(current_deck)
        flop.append(chosen_card)
        current_deck.remove(chosen_card)

    print("And the flop comes out as : ", flop)

    community_cards.extend(flop)
    print("Current community cards are : ", community_cards)
    besthand_probabilities = besthand_probability(hole_cards['player'], current_deck)
    besthand, besthandprobability = return_besthandprobability(besthand_probabilities)
    print("Your most probable hand now is", besthand, "with a probability of", round(besthandprobability, 2), "%")
    print()

    # laying out the turn
    turn = random.choice(current_deck)
    current_deck.remove(turn)
    print("And the turn comes out as : ", turn)

    community_cards.append(turn)
    print("Current community cards are : ", community_cards)
    besthand_probabilities = besthand_probability(hole_cards['player'], current_deck)
    besthand, besthandprobability = return_besthandprobability(besthand_probabilities)
    print("Your most probable hand now is", besthand, "with a probability of", round(besthandprobability, 2), "%")
    print()

    # laying out the river
    river = random.choice(current_deck)
    current_deck.remove(river)
    print("And the river comes out as : ", river)

    community_cards.append(river)
    print("Current community cards are : ", community_cards)
    besthand_probabilities = besthand_probability(hole_cards['player'], current_deck)
    besthand, besthandprobability = return_besthandprobability(besthand_probabilities)
    print("You have a", besthand)