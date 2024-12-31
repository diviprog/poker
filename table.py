from cards import Deck
from utils.positions import positions
from utils.variations import variations
from utils.compare_hands import compare_hands

class Table:
    def __init__(self, variation, actors, small, big):
        self.actors = actors
        self.round_number = 1
        self.flop = []
        self.turn = ""
        self.river = ""
        self.community_cards = []
        self.small = small
        self.big = big
        self.pot = 0
        self.full_deck = Deck()
        self.variation = variation
        self.num_hole_cards, self.preflop_choice, self.discard = self.get_variation(self.variation)

        self.play_round()
        while input("Continue? (y/n) ") == "y":
            self.round_number += 1
            self.play_round()

    def get_variation(self, variation):
        return variations[variation]

    def assign_positions(self):
        self.players = len(self.actors)
        player_positions = positions[str(self.players) + 'p']
        for i in range(self.players):
            self.actors[i].give_position(player_positions[(i + self.round_number - 1) % self.players])

    def initialize_player_amount_in_round(self):
        for actor in self.actors:
            actor.amount_in_round = 0

    def distribute_hole_cards(self):
        for _ in range(self.num_hole_cards):
            for actor in self.actors:
                actor.get_card(self.full_deck.choose_card())

    def reset_acted(self):
        for actor in self.actors:
            if actor.active:
                actor.acted = False

    def play_round(self):
        self.full_deck.shuffle()
        self.community_cards = []
        self.assign_positions()
        self.make_players_active()
        self.distribute_hole_cards()
        
        # Discard before preflop if necessary
        if self.variation == 'discard':
            self.discard_phase("preflop")
        
        self.preflop = 1
        if self.preflop_choice:
            for actor in self.actors:
                actor.make_preflop_choice(self.variation)
        self.betting_round(self.big, preflop=True)
        self.preflop = 0
        
        if self.count_active() > 1:
            self.show_flop()
            
            # Discard after flop for both 'regret' and 'discard'
            if self.variation in ['regret', 'discard']:
                self.discard_phase("flop")
                
            self.betting_round()

        if self.count_active() > 1:
            self.show_turn()
            
            # Discard after turn for both 'regret' and 'discard'
            if self.variation in ['regret', 'discard']:
                self.discard_phase("turn")
                
            self.betting_round()

        if self.count_active() > 1:
            self.show_river()
            self.betting_round()

        hands = [[list(map(lambda card: card.show(), self.actors[i].hole_cards if len(self.actors[i].hole_cards) != 0 else self.actors[i].groups.values())),i] for i in range(self.players) if self.actors[i].active]
        
        if hands:
            winning_hands_and_indices = self.find_winner(hands)
            winning_hands = [item[0] for item in winning_hands_and_indices]
            winning_indices = [item[1] for item in winning_hands_and_indices]
            print("Winning hands:", [" ".join(hand) for hand in winning_hands])

            winnings = self.pot // len(winning_indices)
            for index in winning_indices:
                self.actors[index].stack += winnings

            for i in range(self.players):
                print(f"Player {i+1} stack: {self.actors[i].stack}")

        self.return_hole_cards()


    def betting_round(self, high_bet=0, preflop=False):
        check_actions = 'KBF'
        call_actions = 'CRF'
        self.initialize_player_amount_in_round()

        if preflop:
            small_blind = (self.round_number - 1) % self.players
            big_blind = self.round_number % self.players
            self.actors[small_blind].amount_in_round = self.small
            self.pot += self.actors[small_blind].bet(self.small)
            self.actors[big_blind].amount_in_round = self.big
            self.pot += self.actors[big_blind].bet(self.big)
            high_bet = self.big

        self.reset_acted()

        while not self.check_betting_over(high_bet):
            for i in range(self.players):
                actor = self.actors[(i + self.round_number - 1 + self.preflop * 2) % self.players]
                if actor.active and not actor.acted:
                    if high_bet == 0 or high_bet == actor.amount_in_round:
                        amount = actor.action(check_actions, high_bet)
                        self.pot += amount
                        actor.amount_in_round += amount
                    else:
                        amount = actor.action(call_actions, high_bet)
                        self.pot += amount
                        actor.amount_in_round += amount
                    if high_bet < amount:
                        high_bet = actor.amount_in_round
                        self.reset_acted()
                    actor.acted = True

    def check_betting_over(self, high_bet):
        for actor in self.actors:
            if actor.active and not actor.acted:
                return False
            if actor.active and actor.amount_in_round != high_bet:
                return False
        return True

    def show_flop(self):
        self.full_deck.choose_card() # burn card
        self.flop = [self.full_deck.choose_card() for _ in range(3)]
        self.community_cards.extend(self.flop)
        print("Flop:", [card.show() for card in self.flop])
        print("Community Cards are: ", self.show_community_cards())
        print("Pot size is", self.pot)
        print()

    def show_turn(self):
        self.full_deck.choose_card()
        self.turn = self.full_deck.choose_card()
        self.community_cards.append(self.turn)
        print("Turn:", self.turn.show())
        print("Community Cards are: ", self.show_community_cards())
        print("Pot size is", self.pot)
        print()

    def show_river(self):
        self.full_deck.choose_card()
        self.river = self.full_deck.choose_card()
        self.community_cards.append(self.river)
        print("River:", self.river.show())
        print("Community Cards are: ", self.show_community_cards())
        print("Pot size is", self.pot)
        print()

    def show_community_cards(self):
        return [card.show() for card in self.community_cards]

    def make_players_active(self):
        for actor in self.actors:
            actor.active = True

    def count_active(self):
        return sum(actor.active for actor in self.actors)

    def find_winner(self, hands):
        if not hands:
            return []

        winners = [hands[0]]

        for i in range(1, len(hands)):
            result = compare_hands(winners[0][0], hands[i][0], [card.show() for card in self.community_cards], self.variation)
            if result == 1:
                continue
            elif result == 2:
                winners = [hands[i]]
            else:
                winners.append(hands[i])

        return winners
    
    def return_hole_cards(self):
        for actor in self.actors:
            for card in actor.hole_cards:
                self.full_deck.return_card(card)
            actor.hole_cards = []

    def discard_phase(self, phase):
        for actor in self.actors:
            if actor.active:
                print(f"{actor.position} - Time to discard during {phase}. Current cards: {actor.cards()}")

                if self.variation == 'regret':
                    # Discard a pair from actor.groups
                    if actor.groups:
                        print("Available pairs to discard:")
                        for idx, (key, group) in enumerate(actor.groups.items(), start=1):
                            print(f"{idx}: {key} - {[card.show() for card in group]}")
                        pair_index = int(input("Enter the index of the pair to discard: ")) - 1
                        key_to_remove = list(actor.groups.keys())[pair_index]
                        discarded_pair = actor.groups.pop(key_to_remove)
                        for card in discarded_pair:
                            self.full_deck.return_card(card)
                        print(f"Discarded pair: {[card.show() for card in discarded_pair]}")
                    else:
                        print("No pairs available to discard.")
                    print()
                    
                elif self.variation == 'discard':
                    # Discard a single card from self.hole_cards
                    num_discards = int(input(f"How many cards to discard (0-{len(actor.hole_cards)}): "))
                    for _ in range(num_discards):
                        card_index = int(input("Enter the index of the card to discard (starting from 1): ")) - 1
                        discarded_card = actor.hole_cards.pop(card_index)
                        self.full_deck.return_card(discarded_card)
                        print(f"Discarded {discarded_card.show()}. Remaining cards: {actor.cards()}")
                    print()