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
    if 2 in value_count.values():
        pair_value = [key for key, count in value_count.items() if count == 2][0]
        hand = [card for card in cards if card[0] == pair_value]
        remaining = [card for card in cards if card[0] != pair_value]
        hand.extend(check_highcard(remaining)['hand'])
        return {'check': True, 'hand': hand[:5]}
    return {'check': False}

def check_trips(cards):
    value_count = value_counter(cards)
    if 3 in value_count.values():
        trips_value = [key for key, count in value_count.items() if count == 3][0]
        hand = [card for card in cards if card[0] == trips_value]
        remaining = [card for card in cards if card[0] != trips_value]
        hand.extend(check_highcard(remaining)['hand'])
        return {'check': True, 'hand': hand[:5]}
    return {'check': False}

def check_quads(cards):
    value_count = value_counter(cards)
    if 4 in value_count.values():
        quads_value = [key for key, count in value_count.items() if count == 4][0]
        hand = [card for card in cards if card[0] == quads_value]
        remaining = [card for card in cards if card[0] != quads_value]
        hand.extend(check_highcard(remaining)['hand'])
        return {'check': True, 'hand': hand[:5]}
    return {'check': False}

def check_twopair(cards):
    value_count = value_counter(cards)
    pairs = [key for key, count in value_count.items() if count == 2]
    if len(pairs) > 1:
        hand = [card for card in cards if card[0] in pairs]
        remaining = [card for card in cards if card[0] not in pairs]
        hand.extend(check_highcard(remaining)['hand'])
        hand = bubble_sort(hand[:4]) + [hand[-1]]
        return {'check': True, 'hand': hand}
    return {'check': False}

def check_flush(cards):
    suit_count = suit_counter(cards)
    if 5 in suit_count.values():
        flush_suit = [key for key, count in suit_count.items() if count == 5][0]
        hand = [card for card in cards if card[-1] == flush_suit]
        return {'check': True, 'hand': bubble_sort(hand)[:5]}
    return {'check': False}

def check_fullhouse(cards):
    result_trips = check_trips(cards)
    result_pair = check_pair(cards)
    if result_pair['check'] and result_trips['check']:
        return {'check': True, 'hand': result_trips['hand'][:3] + result_pair['hand'][:2]}
    return {'check': False}

def check_straight(cards):
    checker, straight_values = straight_collector(cards)
    if checker:
        translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        hand = []
        for value in straight_values:
            for card in cards:
                if translation[card[0]] == value:
                    hand.append(card)
                    break
        return {'check': True, 'hand': bubble_sort(hand)}
    return {'check': False}

def check_straightflush(cards):
    checker, straight_values = straight_collector(cards)
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    if checker:
        flush_check = [card for card in cards if any(translation[card[0]] == val for val in straight_values)]
        return_flushcheck = check_flush(flush_check)
        if return_flushcheck['check']:
            return {'check': True, 'hand': return_flushcheck['hand']}
    return {'check': False}

def check_royalflush(cards):
    return_straightflushcheck = check_straightflush(cards)
    if return_straightflushcheck['check'] and return_straightflushcheck['hand'][0][0] == 'A' and return_straightflushcheck['hand'][1][0] == 'K':
        return {'check': True, 'hand': return_straightflushcheck['hand']}
    return {'check': False}

def check_highcard(cards):
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    values = [translation[card[0]] for card in cards]
    values.sort(reverse=True)
    hand = []
    for value in values[:5]:
        for card in cards:
            if translation[card[0]] == value:
                hand.append(card)
                break
    return {'check': True, 'hand': hand}

def tex_besthand(cards):
    best_hand = {'hand': 'High Card', 'besthand': check_highcard(cards)['hand']}
    hand_ranking_order = [
        ('Royal Flush', check_royalflush),
        ('Straight Flush', check_straightflush),
        ('Four of a Kind', check_quads),
        ('Full House', check_fullhouse),
        ('Flush', check_flush),
        ('Straight', check_straight),
        ('Three of a Kind', check_trips),
        ('Two Pair', check_twopair),
        ('Pair', check_pair)
    ]

    for comb in combinations(cards, 5):
        for hand_name, hand_check_function in hand_ranking_order:
            check_result = hand_check_function(comb)
            if check_result['check']:
                best_hand = {'hand': hand_name, 'besthand': check_result['hand']}
                break
            else:
                continue

    return best_hand

def omaha_besthand(hole_cards, community_cards):
    hand_ranking_index = {
        'Royal Flush':1,
        'Straight Flush':2,
        'Four of a Kind':3,
        'Full House':4,
        'Flush':5,
        'Straight':6,
        'Three of a Kind':7,
        'Two Pair':8,
        'Pair':9,
        'High Card':10
    }

    best_hand = {'hand':'High Card'}
    for hole_comb in combinations(hole_cards, 2):
        for community_comb in combinations(community_cards, 3):
            combined_cards = list(hole_comb) + list(community_comb)
            current_best = tex_besthand(combined_cards)
            if hand_ranking_index[current_best['hand']] < hand_ranking_index[best_hand['hand']]:
                best_hand['besthand'] = current_best
    return best_hand['besthand']

def regret_besthand(hole_cards, community_cards):
    hand_ranking_index = {
        'Royal Flush':1,
        'Straight Flush':2,
        'Four of a Kind':3,
        'Full House':4,
        'Flush':5,
        'Straight':6,
        'Three of a Kind':7,
        'Two Pair':8,
        'Pair':9,
        'High Card':10
    }
    best_hand = {'hand':'High Card'}
    for pair in hole_cards:
        current_best = omaha_besthand(pair, community_cards)
        if hand_ranking_index[current_best['hand']] < hand_ranking_index[best_hand['hand']]:
                best_hand['besthand'] = current_best
    return best_hand['besthand']