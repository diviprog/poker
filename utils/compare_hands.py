from utils.best_hand import tex_besthand, omaha_besthand, regret_besthand
import inspect

def compare_hands(hand1, hand2, community_cards, variation):
    conversion = {'High Card': 1, 
                  'Pair': 2, 
                  'Two Pair': 3, 
                  'Three of a Kind': 4, 
                  'Straight': 5, 
                  'Flush': 6, 
                  'Full House': 7, 
                  'Four of a Kind': 8, 
                  'Straight Flush': 9, 
                  'Royal Flush': 10}
    translation = {'2': 2, 
                   '3': 3, 
                   '4': 4, 
                   '5': 5, 
                   '6': 6, 
                   '7': 7, 
                   '8': 8, 
                   '9': 9, 
                   'T': 10, 
                   'J': 11, 
                   'Q': 12, 
                   'K': 13,
                   'A': 14}
    variations = {
        'tex':tex_besthand,
        'omaha':omaha_besthand,
        'regret':regret_besthand,
    }

    num_positional_args = len(inspect.signature(variations[variation]).parameters)
    if num_positional_args == 1:
        answer1 = variations[variation](hand1)
        answer2 = variations[variation](hand2)
    elif num_positional_args == 2:
        answer1 = variations[variation](hand1, community_cards)
        answer2 = variations[variation](hand2, community_cards)

    if conversion[answer1['hand']] > conversion[answer2['hand']]:
        return 1
    elif conversion[answer1['hand']] < conversion[answer2['hand']]:
        return 2
    else:
        if answer1['hand'] == 'Royal Flush':
            return 0
        elif answer1['hand'] == 'Straight Flush':
            if translation[answer1['besthand'][0][0]] > translation[answer2['besthand'][0][0]]:
                return 1
            elif translation[answer1['besthand'][0][0]] < translation[answer2['besthand'][0][0]]:
                return 2
            else:
                return 0
        elif answer1['hand'] == 'Four of a Kind':
            if translation[answer1['besthand'][-1][0]] > translation[answer2['besthand'][-1][0]]:
                return 1
            elif translation[answer1['besthand'][-1][0]] < translation[answer2['besthand'][-1][0]]:
                return 2
            else :
                return 0
        elif answer1['hand'] == 'Full House':
            if max(translation[answer1['besthand'][0][0]], translation[answer1['besthand'][3][0]]) > max(translation[answer2['besthand'][0][0]], translation[answer2['besthand'][3][0]]):
                return 1
            elif max(translation[answer1['besthand'][0][0]], translation[answer1['besthand'][3][0]]) < max(translation[answer2['besthand'][0][0]], translation[answer2['besthand'][3][0]]):
                return 2
            elif min(translation[answer1['besthand'][0][0]], translation[answer1['besthand'][3][0]]) > min(translation[answer2['besthand'][0][0]], translation[answer2['besthand'][3][0]]):
                return 1
            elif min(translation[answer1['besthand'][0][0]], translation[answer1['besthand'][3][0]]) < min(translation[answer2['besthand'][0][0]], translation[answer2['besthand'][3][0]]):
                return 2
            else:
                return 0
        elif answer1['hand'] == 'Flush':
            for i in range(5):
                if translation[answer1['besthand'][i][0]] > translation[answer2['besthand'][i][0]]:
                    return 1
                elif translation[answer1['besthand'][i][0]] < translation[answer2['besthand'][i][0]]:
                    return 2
            return 0
        elif answer1['hand'] == 'Straight':
            if translation[answer1['besthand'][0][0]] > translation[answer2['besthand'][0][0]]:
                return 1
            elif translation[answer1['besthand'][0][0]] < translation[answer2['besthand'][0][0]]:
                return 2
            else:
                return 0
        elif answer1['hand'] == 'Three of a Kind':
            if translation[answer1['besthand'][0][0]] > translation[answer2['besthand'][0][0]]:
                return 1
            elif translation[answer1['besthand'][0][0]] < translation[answer2['besthand'][0][0]]:
                return 2
            else:
                for i in range(2):
                    if translation[answer1['besthand'][i+3][0]] > translation[answer2['besthand'][i+3][0]]:
                        return 1
                    elif translation[answer1['besthand'][i+3][0]] < translation[answer2['besthand'][i+3][0]]:
                        return 2
                return 0
        elif answer1['hand'] == 'Two Pair':
            for i in range(0, 5, 2):
                if translation[answer1['besthand'][i][0]] > translation[answer2['besthand'][i][0]]:
                    return 1
                elif translation[answer1['besthand'][i][0]] > translation[answer2['besthand'][i][0]]:
                    return 2
            return 0
        elif answer1['hand'] == 'Pair':
            if translation[answer1['besthand'][0][0]] > translation[answer2['besthand'][0][0]]:
                return 1
            elif translation[answer1['besthand'][0][0]] < translation[answer2['besthand'][0][0]]:
                return 2
            else:
                for i in range(3):
                    if translation[answer1['besthand'][i + 2][0]] > translation[answer2['besthand'][i + 2][0]]:
                        return 1
                    elif translation[answer1['besthand'][i + 2][0]] < translation[answer2['besthand'][i + 2][0]]:
                        return 2
                return 0
        else:
            for i in range(5):
                if translation[answer1['besthand'][i][0]] > translation[answer2['besthand'][i][0]]:
                    return 1
                elif translation[answer1['besthand'][i][0]] > translation[answer2['besthand'][i][0]]:
                    return 2
            return 0

'''
hole_cards1 = ['2S', 'AD']
hole_cards2 = ['2H', 'AS']
community_cards = ['2C', '3S', '6S', 'QS', 'AH']
cards1 = hole_cards1 + community_cards
cards2 = hole_cards2 + community_cards

print(cards1, cards2, compare_hands(cards1, cards2))
'''