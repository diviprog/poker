def make_deck():
    value = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    suits = ['S', 'H', 'D', 'C']
    full_deck = []
    for i in suits:
        for j in value:
            card = j + i
            full_deck.append(card)

    return full_deck