from collections import Counter


def bubble_sort(hand):
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13,
                   'A': 14}
    n = len(hand)
    swapped = False
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if translation[hand[j][0]] < translation[hand[j + 1][0]]:
                swapped = True
                hand[j], hand[j + 1] = hand[j + 1], hand[j]

    return hand

def value_counter(cards):
    values = []
    for i in cards:
        values.append(i[0])

    return Counter(values)


def suit_counter(cards):
    suits = []
    for i in cards:
        suits.append(i[-1])

    return Counter(suits)


def straight_collector(cards):
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13}

    values = []
    for i in cards:
        if i[0] == 'A':
            values.extend([1, 14])
        else:
            values.append(translation[i[0]])

    values = list(set(values))
    values.sort(reverse=True)

    is_straight = False
    window = [0]
    for i in range(len(values) - 4):
        window = values[i:i + 5]
        if sorted(window) == list(range(min(window), max(window) + 1)):
            is_straight = True
            break

    return is_straight, window


def check_pair(cards):
    answer = {}
    value_count = value_counter(cards)
    if 2 in value_count.values():
        answer['check'] = True
        value = {i for i in value_count if value_count[i] == 2}

        hand = []
        remaining = []
        for i in cards:
            if i[0] == list(value)[0]:
                hand.append(i)
            else:
                remaining.append(i)
        hand.extend(check_highcard(remaining)['hand'])

        answer['hand'] = hand
    else:
        answer['check'] = False

    return answer


def check_trips(cards):
    answer = {}
    value_count = value_counter(cards)
    if 3 in value_count.values():
        answer['check'] = True
        value = {i for i in value_count if value_count[i] == 3}

        hand = []
        remaining = []
        for i in cards:
            if i[0] == list(value)[0]:
                hand.append(i)
            else:
                remaining.append(i)
        hand.extend(check_highcard(remaining)['hand'])

        answer['hand'] = hand
    else:
        answer['check'] = False

    return answer


def check_quads(cards):
    answer = {}
    value_count = value_counter(cards)
    if 4 in value_count.values():
        answer['check'] = True
        value = {i for i in value_count if value_count[i] == 4}

        hand = []
        remaining = []
        for i in cards:
            if i[0] == list(value)[0]:
                hand.append(i)
            else:
                remaining.append(i)
        hand.extend(check_highcard(remaining)['hand'])

        answer['hand'] = hand
    else:
        answer['check'] = False

    return answer


def check_twopair(cards):
    answer = {}
    value_count = value_counter(cards)
    if Counter(value_count.values())[2] > 1:
        answer['check'] = True

        values = []
        dict_values = list(value_count.values())
        dict_keys = list(value_count.keys())
        for i in range(len(dict_keys)):
            if dict_values[i] == 2:
                values.append(dict_keys[i])

        hand = []
        remaining = []
        for i in cards:
            if i[0] in values:
                hand.append(i)
            else:
                remaining.append(i)

        hand.extend(check_highcard(remaining)['hand'])

        hand = bubble_sort(hand[:4]) + [hand[-1]]
        answer['hand'] = hand

    else:
        answer['check'] = False

    return answer


def check_flush(cards):
    answer = {}
    suit_count = suit_counter(cards)
    if 5 in suit_count.values():
        answer['check'] = True
        suit = {i for i in suit_count if suit_count[i] == 5}

        hand = []
        for i in cards:
            if i[-1] == list(suit)[0]:
                hand.append(i)

        answer['hand'] = hand

    else:
        answer['check'] = False

    return answer


def check_fullhouse(cards):
    answer = {}
    result_trips = check_trips(cards)
    result_pair = check_pair(cards)
    if result_pair['check'] and result_trips['check']:
        answer['check'] = True
        answer['hand'] = result_trips['hand'][:3] + result_pair['hand'][:2]
    else:
        answer ['check'] = False

    return answer


def check_straight(cards):
    answer = {}
    checker, straight_values = straight_collector(cards)
    if checker:
        answer['check'] = True

        translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        hand = []
        for i in cards:
            if translation[i[0]] in straight_values:
                hand.append(i)
                straight_values.remove(translation[i[0]])

        hand = bubble_sort(hand)

        answer['hand'] = hand

    else:
        answer['check'] = False

    return answer


def check_straightflush(cards):
    answer = {}
    checker, straight_values = straight_collector(cards)
    if checker:

        translation = {1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        flush_check = []
        for i in range(1, 6):
            for j in cards:
                if j[0] == translation[straight_values[0]-i+1]:
                    flush_check.append(j)

        return_flushcheck = check_flush(flush_check)
        if return_flushcheck['check']:
            answer['check'] = True
            answer['hand'] = return_flushcheck['hand']
        else:
            answer['check'] = False
    else:
        answer['check'] = False

    return answer


def check_royalflush(cards):
    answer = {}
    return_straightflushcheck = check_straightflush(cards)
    if return_straightflushcheck['check'] and  return_straightflushcheck['hand'][0][0] == 'A' and return_straightflushcheck['hand'][1][0] == 'K':
        answer['check'] = True
        answer['hand'] = return_straightflushcheck['hand']
    else:
        answer['check'] = False

    return answer


def check_highcard(cards):
    translation = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    answer = {'check': True}

    values = []
    for i in cards:
        values.append(translation[i[0]])
    values.sort()
    values = values[2:]

    hand = []
    for i in cards:
        for j in values:
            if translation[i[0]] == j:
                hand.append(i)

    hand = bubble_sort(hand)

    answer['hand'] = hand

    return answer


def besthand(cards):

    best_hand = {}
    if check_royalflush(cards)['check']:
        best_hand['hand'] = 'Royal Flush'
        best_hand['besthand'] = check_royalflush(cards)['hand']
    elif check_straightflush(cards)['check']:
        best_hand['hand'] = 'Straight Flush'
        best_hand['besthand'] = check_straightflush(cards)['hand']
    elif check_quads(cards)['check']:
        best_hand['hand'] = 'Four of a Kind'
        best_hand['besthand'] = check_quads(cards)['hand']
    elif check_fullhouse(cards)['check']:
        best_hand['hand'] = 'Full House'
        best_hand['besthand'] = check_fullhouse(cards)['hand']
    elif check_flush(cards)['check']:
        best_hand['hand'] = 'Flush'
        best_hand['besthand'] = check_flush(cards)['hand']
    elif check_straight(cards)['check']:
        best_hand['hand'] = 'Straight'
        best_hand['besthand'] = check_straight(cards)['hand']
    elif check_trips(cards)['check']:
        best_hand['hand'] = 'Three of a Kind'
        best_hand['besthand'] = check_trips(cards)['hand']
    elif check_twopair(cards)['check']:
        best_hand['hand'] = 'Two Pair'
        best_hand['besthand'] = check_twopair(cards)['hand']
    elif check_pair(cards)['check']:
        best_hand['hand'] = 'Pair'
        best_hand['besthand'] = check_pair(cards)['hand']
    else:
        best_hand['hand'] = 'High Card'
        best_hand['besthand'] = check_highcard(cards)['hand']

    return best_hand
