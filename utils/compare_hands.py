from itertools import combinations
from collections import Counter

def compare_hands(hole_cards1, hole_cards2, community_cards, variation='texas'):
    """
    Compare two poker hands and determine which is better.
    
    Args:
        hole_cards1: List of player 1's hole cards (strings like '2H', 'AS', etc.)
        hole_cards2: List of player 2's hole cards (strings like '2H', 'AS', etc.)
        community_cards: List of community cards (strings like '2H', 'AS', etc.)
        variation: String indicating the poker variant (default: 'texas')
        
    Returns:
        1 if player 1's hand is better
        2 if player 2's hand is better
        0 if both hands are equal
    """
    # print(f"\nComparing hands in {variation} mode:")
    # print(f"Player 1 hole cards: {hole_cards1}")
    # print(f"Player 2 hole cards: {hole_cards2}")
    # print(f"Community cards: {community_cards}")
    
    # Determine the best hand for each player based on variation
    if variation.lower() in ['texas', 'tex', 'holdem', 'discard']:
        best_hand1 = get_best_texas_hand(hole_cards1, community_cards)
        best_hand2 = get_best_texas_hand(hole_cards2, community_cards)
    elif variation.lower() == 'omaha':
        best_hand1 = get_best_omaha_hand(hole_cards1, community_cards)
        best_hand2 = get_best_omaha_hand(hole_cards2, community_cards)
    else:
        raise ValueError(f"Unsupported variation: {variation}")
    
    # print(f"Player 1 best hand: {best_hand1['hand_name']} - {best_hand1['cards']}")
    # print(f"Player 2 best hand: {best_hand2['hand_name']} - {best_hand2['cards']}")
    
    # Compare hand ranks first
    hand_ranks = {
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
    
    if hand_ranks[best_hand1['hand_name']] > hand_ranks[best_hand2['hand_name']]:
        #print(f"Player 1 wins with {best_hand1['hand_name']} vs {best_hand2['hand_name']}")
        return 1
    elif hand_ranks[best_hand1['hand_name']] < hand_ranks[best_hand2['hand_name']]:
        #print(f"Player 2 wins with {best_hand2['hand_name']} vs {best_hand1['hand_name']}")
        return 2
    
    # If ranks are equal, compare cards within each hand
    result = compare_same_hands(best_hand1, best_hand2)
    # if result == 1:
    #     print(f"Player 1 wins with better {best_hand1['hand_name']}")
    # elif result == 2:
    #     print(f"Player 2 wins with better {best_hand2['hand_name']}")
    # else:
    #     print("It's a tie!")
    
    return result

def get_card_rank(card):
    """Convert card value to numeric rank for comparison."""
    ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
             '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return ranks[card[0]]

def get_best_texas_hand(hole_cards, community_cards):
    """Find the best 5-card hand in Texas Hold'em."""
    all_cards = hole_cards + community_cards
    
    # Check each possible 5-card combination
    best_hand = {'hand_name': 'High Card', 'hand_rank': 1, 'cards': [], 'values': []}
    
    for combo in combinations(all_cards, 5):
        hand = evaluate_hand(list(combo))
        
        # Update if this hand is better
        if hand['hand_rank'] > best_hand['hand_rank']:
            best_hand = hand
        elif hand['hand_rank'] == best_hand['hand_rank']:
            # Compare same rank hands by their card values
            if is_better_same_rank(hand, best_hand):
                best_hand = hand
    
    return best_hand

def get_best_omaha_hand(hole_cards, community_cards):
    """Find the best 5-card hand in Omaha (must use exactly 2 hole and 3 community cards)."""
    best_hand = {'hand_name': 'High Card', 'hand_rank': 1, 'cards': [], 'values': []}
    
    # Try all combinations of 2 hole cards and 3 community cards
    for hole_combo in combinations(hole_cards, 2):
        for comm_combo in combinations(community_cards, 3):
            combo = list(hole_combo) + list(comm_combo)
            hand = evaluate_hand(combo)
            
            # Update if this hand is better
            if hand['hand_rank'] > best_hand['hand_rank']:
                best_hand = hand
            elif hand['hand_rank'] == best_hand['hand_rank']:
                # Compare same rank hands by their card values
                if is_better_same_rank(hand, best_hand):
                    best_hand = hand
    
    return best_hand

def is_better_same_rank(hand1, hand2):
    """Determine if hand1 is better than hand2 when they have the same rank."""
    if len(hand1['values']) != len(hand2['values']):
        return False
    
    for i in range(len(hand1['values'])):
        if hand1['values'][i] > hand2['values'][i]:
            return True
        elif hand1['values'][i] < hand2['values'][i]:
            return False
    
    return False  # Hands are equal

def evaluate_hand(cards):
    """Evaluate a 5-card poker hand and return its rank and value."""
    # Sort cards by rank (highest to lowest)
    sorted_cards = sorted(cards, key=get_card_rank, reverse=True)
    
    # Check for each hand type in descending order
    royal_flush = check_royal_flush(sorted_cards)
    if royal_flush['is_valid']:
        return royal_flush
    
    straight_flush = check_straight_flush(sorted_cards)
    if straight_flush['is_valid']:
        return straight_flush
        
    four_kind = check_four_of_a_kind(sorted_cards)
    if four_kind['is_valid']:
        return four_kind
        
    full_house = check_full_house(sorted_cards)
    if full_house['is_valid']:
        return full_house
        
    flush = check_flush(sorted_cards)
    if flush['is_valid']:
        return flush
        
    straight = check_straight(sorted_cards)
    if straight['is_valid']:
        return straight
        
    three_kind = check_three_of_a_kind(sorted_cards)
    if three_kind['is_valid']:
        return three_kind
        
    two_pair = check_two_pair(sorted_cards)
    if two_pair['is_valid']:
        return two_pair
        
    pair = check_pair(sorted_cards)
    if pair['is_valid']:
        return pair
    
    # If no other hand, return high card
    return {
        'hand_name': 'High Card',
        'hand_rank': 1,
        'is_valid': True,
        'cards': sorted_cards,
        'values': [get_card_rank(card) for card in sorted_cards]
    }

def check_royal_flush(cards):
    """Check for a royal flush (A-K-Q-J-10 of the same suit)."""
    # First check for a straight flush
    straight_flush = check_straight_flush(cards)
    if not straight_flush['is_valid']:
        return {'is_valid': False}
    
    # Check if the high card is an Ace
    if get_card_rank(straight_flush['cards'][0]) == 14:  # Ace
        return {
            'hand_name': 'Royal Flush',
            'hand_rank': 10,
            'is_valid': True,
            'cards': straight_flush['cards'],
            'values': [14]  # Only need Ace value as all royal flushes are equal
        }
    
    return {'is_valid': False}

def check_straight_flush(cards):
    """Check for a straight flush (five cards in sequence, all of the same suit)."""
    # Check for a flush
    flush = check_flush(cards)
    if not flush['is_valid']:
        return {'is_valid': False}
    
    # Check for a straight with the flush cards
    straight = check_straight(flush['cards'])
    if straight['is_valid']:
        return {
            'hand_name': 'Straight Flush',
            'hand_rank': 9,
            'is_valid': True,
            'cards': straight['cards'],
            'values': straight['values']
        }
    
    return {'is_valid': False}

def check_four_of_a_kind(cards):
    """Check for four of a kind (four cards of the same rank)."""
    # Count card ranks
    rank_counter = Counter([card[0] for card in cards])
    
    # Check if any rank appears 4 times
    for rank, count in rank_counter.items():
        if count == 4:
            # Get the four matching cards
            quads = [card for card in cards if card[0] == rank]
            
            # Get the kicker (remaining card)
            kickers = [card for card in cards if card[0] != rank]
            
            # Form the hand: four matching cards + kicker
            quad_cards = quads + kickers
            
            return {
                'hand_name': 'Four of a Kind',
                'hand_rank': 8,
                'is_valid': True,
                'cards': quad_cards,
                'values': [get_card_rank(quads[0]), get_card_rank(kickers[0])]
            }
    
    return {'is_valid': False}

def check_full_house(cards):
    """Check for a full house (three of a kind and a pair)."""
    # Count card ranks
    rank_counter = Counter([card[0] for card in cards])
    
    # Look for a rank that appears 3 times
    trips_rank = None
    for rank, count in rank_counter.items():
        if count == 3:
            trips_rank = rank
            break
    
    if not trips_rank:
        return {'is_valid': False}
    
    # Look for a rank that appears 2 times
    pair_rank = None
    for rank, count in rank_counter.items():
        if count == 2 and rank != trips_rank:
            pair_rank = rank
            break
    
    if not pair_rank:
        return {'is_valid': False}
    
    # Get the three matching cards
    trips = [card for card in cards if card[0] == trips_rank]
    
    # Get the pair
    pair = [card for card in cards if card[0] == pair_rank]
    
    # Form the hand: three matching cards + pair
    full_house_cards = trips + pair
    
    return {
        'hand_name': 'Full House',
        'hand_rank': 7,
        'is_valid': True,
        'cards': full_house_cards,
        'values': [get_card_rank(trips[0]), get_card_rank(pair[0])]
    }

def check_flush(cards):
    """Check for a flush (five cards of the same suit)."""
    # Count card suits
    suit_counter = Counter([card[1] for card in cards])
    
    # Check if any suit appears 5 times
    for suit, count in suit_counter.items():
        if count >= 5:
            # Get the five cards of the same suit
            flush_cards = [card for card in cards if card[1] == suit]
            flush_cards = sorted(flush_cards, key=get_card_rank, reverse=True)[:5]
            
            return {
                'hand_name': 'Flush',
                'hand_rank': 6,
                'is_valid': True,
                'cards': flush_cards,
                'values': [get_card_rank(card) for card in flush_cards]
            }
    
    return {'is_valid': False}

def check_straight(cards):
    """Check for a straight (five cards in sequence)."""
    # Get unique ranks, sorted high to low
    ranks = sorted(set(get_card_rank(card) for card in cards), reverse=True)
    
    # Check for A-5-4-3-2 (Ace-low straight)
    if 14 in ranks and 2 in ranks and 3 in ranks and 4 in ranks and 5 in ranks:
        # Find the actual cards for the straight
        ace = next(card for card in cards if card[0] == 'A')
        two = next(card for card in cards if card[0] == '2')
        three = next(card for card in cards if card[0] == '3')
        four = next(card for card in cards if card[0] == '4')
        five = next(card for card in cards if card[0] == '5')
        
        straight_cards = [five, four, three, two, ace]
        
        return {
            'hand_name': 'Straight',
            'hand_rank': 5,
            'is_valid': True,
            'cards': straight_cards,
            'values': [5]  # The high card in a 5-high straight
        }
    
    # Check for regular straights
    for i in range(len(ranks) - 4):
        if ranks[i] - ranks[i+4] == 4:
            # We found 5 consecutive ranks
            straight_values = ranks[i:i+5]
            
            # Find the actual cards for the straight
            straight_cards = []
            for value in straight_values:
                for card in cards:
                    if get_card_rank(card) == value and card not in straight_cards:
                        straight_cards.append(card)
                        break
            
            return {
                'hand_name': 'Straight',
                'hand_rank': 5,
                'is_valid': True,
                'cards': straight_cards,
                'values': [straight_values[0]]  # The high card in the straight
            }
    
    return {'is_valid': False}

def check_three_of_a_kind(cards):
    """Check for three of a kind (three cards of the same rank)."""
    # Count card ranks
    rank_counter = Counter([card[0] for card in cards])
    
    # Check if any rank appears 3 times
    for rank, count in rank_counter.items():
        if count == 3:
            # Get the three matching cards
            trips = [card for card in cards if card[0] == rank]
            
            # Get the kickers (remaining cards)
            kickers = [card for card in cards if card[0] != rank]
            kickers = sorted(kickers, key=get_card_rank, reverse=True)[:2]
            
            # Form the hand: three matching cards + kickers
            hand_cards = trips + kickers
            
            return {
                'hand_name': 'Three of a Kind',
                'hand_rank': 4,
                'is_valid': True,
                'cards': hand_cards,
                'values': [get_card_rank(trips[0])] + [get_card_rank(k) for k in kickers]
            }
    
    return {'is_valid': False}

def check_two_pair(cards):
    """Check for two pair (two different pairs)."""
    # Count card ranks
    rank_counter = Counter([card[0] for card in cards])
    
    # Find all ranks that appear 2 times
    pairs = [rank for rank, count in rank_counter.items() if count == 2]
    
    if len(pairs) >= 2:
        # Sort pairs by rank (highest first)
        pairs.sort(key=lambda rank: get_card_rank(rank + 'S'), reverse=True)
        pair1_rank = pairs[0]
        pair2_rank = pairs[1]
        
        # Get the two pairs
        pair1 = [card for card in cards if card[0] == pair1_rank]
        pair2 = [card for card in cards if card[0] == pair2_rank]
        
        # Get the kicker (remaining card)
        kickers = [card for card in cards if card[0] != pair1_rank and card[0] != pair2_rank]
        kickers = sorted(kickers, key=get_card_rank, reverse=True)[:1]
        
        # Form the hand: two pairs + kicker
        hand_cards = pair1 + pair2 + kickers
        
        return {
            'hand_name': 'Two Pair',
            'hand_rank': 3,
            'is_valid': True,
            'cards': hand_cards,
            'values': [get_card_rank(pair1[0]), get_card_rank(pair2[0]), get_card_rank(kickers[0])]
        }
    
    return {'is_valid': False}

def check_pair(cards):
    """Check for a pair (two cards of the same rank)."""
    # Count card ranks
    rank_counter = Counter([card[0] for card in cards])
    
    # Check if any rank appears 2 times
    for rank, count in rank_counter.items():
        if count == 2:
            # Get the pair
            pair = [card for card in cards if card[0] == rank]
            
            # Get the kickers (remaining cards)
            kickers = [card for card in cards if card[0] != rank]
            kickers = sorted(kickers, key=get_card_rank, reverse=True)[:3]
            
            # Form the hand: pair + kickers
            hand_cards = pair + kickers
            
            return {
                'hand_name': 'Pair',
                'hand_rank': 2,
                'is_valid': True,
                'cards': hand_cards,
                'values': [get_card_rank(pair[0])] + [get_card_rank(k) for k in kickers]
            }
    
    return {'is_valid': False}

def compare_same_hands(hand1, hand2):
    """Compare two hands of the same type."""
    # Compare the hand values in order
    for i in range(min(len(hand1['values']), len(hand2['values']))):
        if hand1['values'][i] > hand2['values'][i]:
            return 1
        elif hand1['values'][i] < hand2['values'][i]:
            return 2
    
    # If all values are equal, it's a tie
    return 0

# hand1 = ['AH', 'AS']
# hand2 = ['KH', 'KS']
# community = ['2H', '2S', '2C', '3H', '3S']
# variation = 'texas'
# print(compare_hands(hand1, hand2, community, variation))