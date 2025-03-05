from collections import Counter
from itertools import combinations

def bubble_sort(hand):
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    n = len(hand)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if translation[hand[j][0]] < translation[hand[j + 1][0]]:
                hand[j], hand[j + 1] = hand[j + 1], hand[j]
    return hand

def value_counter(cards):
    return Counter([card[0] for card in cards])

def suit_counter(cards):
    return Counter([card[-1] for card in cards])

def straight_collector(cards):
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    values = []
    for card in cards:
        values.append(translation[card[0]])
        if card[0] == 'A':
            values.append(1)
    values = list(set(values))
    values.sort()
    for i in range(len(values) - 4):
        if values[i:i+5] == list(range(values[i], values[i] + 5)):
            return True, values[i:i+5]
    return False, []

def check_pair(cards):
    value_count = value_counter(cards)
    pairs = [key for key, count in value_count.items() if count == 2]
    if pairs:
        # Sort pairs by value (highest first)
        translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        pairs.sort(key=lambda x: translation[x], reverse=True)
        pair_value = pairs[0]
        
        # Get the pair cards
        pair_cards = [card for card in cards if card[0] == pair_value]
        
        # Get remaining cards sorted by value
        remaining = [card for card in cards if card[0] != pair_value]
        remaining = bubble_sort(remaining)
        
        # Form best 5-card hand: pair + top 3 kickers
        hand = pair_cards + remaining[:3]
        return {'check': True, 'hand': hand}
    return {'check': False}

def check_trips(cards):
    value_count = value_counter(cards)
    trips = [key for key, count in value_count.items() if count == 3]
    if trips:
        translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        trips.sort(key=lambda x: translation[x], reverse=True)
        trips_value = trips[0]
        
        trips_cards = [card for card in cards if card[0] == trips_value]
        remaining = [card for card in cards if card[0] != trips_value]
        remaining = bubble_sort(remaining)
        
        hand = trips_cards + remaining[:2]
        return {'check': True, 'hand': hand}
    return {'check': False}

def check_quads(cards):
    value_count = value_counter(cards)
    quads = [key for key, count in value_count.items() if count == 4]
    if quads:
        quads_value = quads[0]
        quads_cards = [card for card in cards if card[0] == quads_value]
        remaining = [card for card in cards if card[0] != quads_value]
        remaining = bubble_sort(remaining)
        
        hand = quads_cards + remaining[:1]
        return {'check': True, 'hand': hand}
    return {'check': False}

def check_twopair(cards):
    value_count = value_counter(cards)
    pairs = [key for key, count in value_count.items() if count == 2]
    if len(pairs) >= 2:
        translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        pairs.sort(key=lambda x: translation[x], reverse=True)
        pair1_value = pairs[0]
        pair2_value = pairs[1]
        
        pair1_cards = [card for card in cards if card[0] == pair1_value]
        pair2_cards = [card for card in cards if card[0] == pair2_value]
        remaining = [card for card in cards if card[0] != pair1_value and card[0] != pair2_value]
        remaining = bubble_sort(remaining)
        
        hand = pair1_cards + pair2_cards + remaining[:1]
        return {'check': True, 'hand': hand}
    return {'check': False}

def check_flush(cards):
    suit_count = suit_counter(cards)
    flush_suits = [suit for suit, count in suit_count.items() if count >= 5]
    if flush_suits:
        flush_suit = flush_suits[0]
        flush_cards = [card for card in cards if card[-1] == flush_suit]
        flush_cards = bubble_sort(flush_cards)
        
        return {'check': True, 'hand': flush_cards[:5]}
    return {'check': False}

def check_fullhouse(cards):
    value_count = value_counter(cards)
    trips = [key for key, count in value_count.items() if count >= 3]
    pairs = [key for key, count in value_count.items() if count >= 2]
    
    if not trips:
        return {'check': False}
    
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    trips.sort(key=lambda x: translation[x], reverse=True)
    trips_value = trips[0]
    
    # Filter out the trips value from pairs
    valid_pairs = [p for p in pairs if p != trips_value]
    
    if not valid_pairs:
        return {'check': False}
    
    valid_pairs.sort(key=lambda x: translation[x], reverse=True)
    pair_value = valid_pairs[0]
    
    trips_cards = [card for card in cards if card[0] == trips_value][:3]
    pair_cards = [card for card in cards if card[0] == pair_value][:2]
    
    hand = trips_cards + pair_cards
    return {'check': True, 'hand': hand}

def check_straight(cards):
    checker, straight_values = straight_collector(cards)
    if checker:
        translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        hand = []
        
        # Need to handle Ace-low straight (A-2-3-4-5)
        if 14 in straight_values and 2 in straight_values:  # This means A-2-3-4-5
            values_needed = [14, 2, 3, 4, 5]
        else:
            values_needed = sorted(straight_values, reverse=True)[:5]
        
        for value in values_needed:
            for card in cards:
                curr_value = translation[card[0]]
                if curr_value == value and card not in hand:
                    hand.append(card)
                    break
                if card[0] == 'A' and value == 1 and card not in hand:  # Handle Ace as 1
                    hand.append(card)
                    break
        
        return {'check': True, 'hand': hand}
    return {'check': False}

def check_straightflush(cards):
    # First check if there's a flush
    flush_result = check_flush(cards)
    if not flush_result['check']:
        return {'check': False}
    
    # Now check if those flush cards form a straight
    flush_cards = flush_result['hand']
    straight_result = check_straight(flush_cards)
    
    if straight_result['check']:
        return {'check': True, 'hand': straight_result['hand']}
    
    return {'check': False}

def check_royalflush(cards):
    straightflush_result = check_straightflush(cards)
    if not straightflush_result['check']:
        return {'check': False}
    
    # Check if it's a royal flush (10-J-Q-K-A of same suit)
    hand = straightflush_result['hand']
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    values = [translation[card[0]] for card in hand]
    
    if sorted(values) == [10, 11, 12, 13, 14]:
        return {'check': True, 'hand': hand}
    
    return {'check': False}

def check_highcard(cards):
    sorted_cards = bubble_sort(cards)
    return {'check': True, 'hand': sorted_cards[:5]}

def tex_besthand(cards):
    # Evaluate all possible 5-card combinations
    best_hand_type = 0
    best_hand_value = []
    
    hand_ranking = {
        'High Card': 1,
        'Pair': 2,
        'Two Pair': 3,
        'Three of a Kind': 4,
        'Straight': 5,
        'Flush': 6,
        'Full House': 7,
        'Four of a Kind': 8,
        'Straight Flush': 9,
        'Royal Flush': 10
    }
    
    hand_checks = [
        ('Royal Flush', check_royalflush),
        ('Straight Flush', check_straightflush),
        ('Four of a Kind', check_quads),
        ('Full House', check_fullhouse),
        ('Flush', check_flush),
        ('Straight', check_straight),
        ('Three of a Kind', check_trips),
        ('Two Pair', check_twopair),
        ('Pair', check_pair),
        ('High Card', check_highcard)
    ]
    
    for hand_name, check_func in hand_checks:
        result = check_func(cards)
        if result['check']:
            return {'hand': hand_name, 'besthand': result['hand']}
    
    # Fallback to high card
    high_card_result = check_highcard(cards)
    return {'hand': 'High Card', 'besthand': high_card_result['hand']}

def omaha_besthand(hole_cards, community_cards):
    best_hand_type = 0
    best_hand = None
    
    hand_ranking = {
        'High Card': 1,
        'Pair': 2,
        'Two Pair': 3,
        'Three of a Kind': 4,
        'Straight': 5,
        'Flush': 6,
        'Full House': 7,
        'Four of a Kind': 8,
        'Straight Flush': 9,
        'Royal Flush': 10
    }
    
    # Try all combinations of 2 hole cards and 3 community cards
    for hole_combo in combinations(hole_cards, 2):
        for comm_combo in combinations(community_cards, 3):
            cards = list(hole_combo) + list(comm_combo)
            current_hand = tex_besthand(cards)
            
            if best_hand is None or hand_ranking[current_hand['hand']] > hand_ranking.get(best_hand['hand'], 0):
                best_hand = current_hand
            elif hand_ranking[current_hand['hand']] == hand_ranking.get(best_hand['hand'], 0):
                # Compare same hand types
                # This is a simplified comparison - ideally, use compare_hands
                if current_hand['besthand'] > best_hand['besthand']:
                    best_hand = current_hand
    
    return best_hand

def regret_besthand(hole_cards, community_cards):
    best_hand_type = 0
    best_hand = None
    
    hand_ranking = {
        'High Card': 1,
        'Pair': 2,
        'Two Pair': 3,
        'Three of a Kind': 4,
        'Straight': 5,
        'Flush': 6,
        'Full House': 7,
        'Four of a Kind': 8,
        'Straight Flush': 9,
        'Royal Flush': 10
    }
    
    # Process each pair in hole_cards
    for pair in hole_cards:
        current_hand = omaha_besthand(pair, community_cards)
        
        if best_hand is None or hand_ranking[current_hand['hand']] > hand_ranking.get(best_hand['hand'], 0):
            best_hand = current_hand
    
    return best_hand