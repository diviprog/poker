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
        self.mainpot = 0
        self.sidepots = []
        self.full_deck = Deck()
        self.variation = variation
        self.num_hole_cards, self.preflop_choice, self.discard = self.get_variation(self.variation)

    def get_variation(self, variation):
        return variations[variation]

    def assign_positions(self):
        self.players = len(self.actors)
        player_positions = positions[str(self.players) + 'p']
        for i in range(self.players):
            self.actors[i].give_position(player_positions[(i - self.round_number + 1) % self.players])

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

    # This is the fixed version of the play_round method in your Table class
    # The issue is in how winning indices are extracted and used

    def play_round(self):
        self.full_deck.shuffle()
        self.community_cards = []
        self.assign_positions()
        self.make_players_active()
        self.pot = 0
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

        hands = [[list(map(lambda card: card.show(), self.actors[i].hole_cards if len(self.actors[i].hole_cards) != 0 else self.actors[i].groups.values())), i] for i in range(self.players) if self.actors[i].active]
        
        if hands:
            winning_hands_and_indices = self.find_winner(hands)
            
            # FIX: Extract winning hands and indices correctly
            winning_hands = []
            winning_indices = []
            
            for winner in winning_hands_and_indices:
                # Each winner should be a list of [hand, player_index]
                winning_hands.append(winner[0])
                winning_indices.append(winner[1])  # This is now an integer, not a list
            
            print("Winning hands:", [" ".join(hand) for hand in winning_hands])
            
            # Distribute winnings
            winnings = self.pot // len(winning_indices)
            for index in winning_indices:
                self.actors[index].stack += winnings

            # Display final stacks
            for i in range(self.players):
                print(f"Player {i+1} stack: {self.actors[i].stack}")

        self.return_hole_cards()

    # If needed, here's the updated find_winner method to ensure it returns the correct structure:

    def find_winner(self, hands):
        """
        Find the winning hand(s) among active players.
        
        Args:
            hands: List of [hole_cards, player_index] pairs
                
        Returns:
            List of [hand, player_index] pairs for winning hands
        """
        if not hands:
            return []
        
        # If only one player remains, they win automatically
        if len(hands) == 1:
            return [hands[0]]
        
        # Convert community cards to strings
        community = [card.show() for card in self.community_cards]
        
        # First, compare player 1 vs player 2
        winners = []
        if len(hands) >= 2:
            result = compare_hands(hands[0][0], hands[1][0], community, self.variation)
            if result == 1:
                winners = [hands[0]]  # Player 1 wins
            elif result == 2:
                winners = [hands[1]]  # Player 2 wins
            else:
                winners = [hands[0], hands[1]]  # Tie
        
        # If there are more than 2 players, compare the current winner against each remaining player
        for i in range(2, len(hands)):
            # If we have multiple winners (tie), compare each winner against the new player
            if len(winners) > 1:
                # Compare first winner against new player
                result = compare_hands(winners[0][0], hands[i][0], community, self.variation)
                if result == 1:
                    # Current winner beats new player, keep current winners
                    continue
                elif result == 2:
                    # New player beats all current winners
                    winners = [hands[i]]
                else:
                    # New player ties with current winners
                    winners.append(hands[i])
            else:
                # Compare the single current winner against new player
                result = compare_hands(winners[0][0], hands[i][0], community, self.variation)
                if result == 1:
                    # Current winner beats new player
                    continue
                elif result == 2:
                    # New player beats current winner
                    winners = [hands[i]]
                else:
                    # New player ties with current winner
                    winners.append(hands[i])
        
        return winners


    def betting_round(self, high_bet=0, preflop=False):
        check_actions = 'KBF'
        call_actions = 'CRF'
        self.initialize_player_amount_in_round()

        # Handle blinds for preflop
        if preflop:
            small_blind = (self.round_number - 1) % self.players
            big_blind = self.round_number % self.players
            self.actors[small_blind].amount_in_round = min(self.small, self.actors[small_blind].stack)
            sb_amount = self.actors[small_blind].bet(self.small)
            self.pot += sb_amount
            self.actors[small_blind].total_contribution += sb_amount
            
            self.actors[big_blind].amount_in_round = min(self.big, self.actors[big_blind].stack)
            bb_amount = self.actors[big_blind].bet(self.big)
            self.pot += bb_amount
            self.actors[big_blind].total_contribution += bb_amount
            high_bet = self.actors[big_blind].amount_in_round

        # Initialize all players as not having acted
        self.reset_acted()
        
        # Keep track of betting rounds to prevent infinite loops
        max_rounds = 10  # Safety limit
        betting_rounds = 0
        
        # In preflop, action starts after big blind
        start_pos = (self.round_number + 1) % self.players if preflop else (self.round_number - 1) % self.players
        
        # Count active players
        active_count = self.count_active()
        if active_count <= 1:
            return  # Only one player active, no need for betting
        
        # Main betting loop
        while not self.check_betting_over(high_bet) and betting_rounds < max_rounds:
            betting_rounds += 1
            print(f"Betting round {betting_rounds}, high bet: {high_bet}")
            
            # Track if any player raised this round
            any_action_taken = False
            
            # Go around the table once
            for i in range(self.players):
                # Calculate position, starting from appropriate position
                pos = (start_pos + i) % self.players
                actor = self.actors[pos]
                
                # Skip inactive players or those who've already acted and don't need to act again
                if not actor.active or (actor.acted and actor.amount_in_round == high_bet):
                    continue
                    
                print(f"Action to {actor.position} (Player {pos+1})")

                # Calculate max possible bet (limited by stack)
                max_additional_bet = actor.stack
                current_high_bet = min(high_bet, actor.amount_in_round + max_additional_bet)
            
                # Determine actions based on current bet
                if high_bet == 0 or high_bet == actor.amount_in_round:
                    # Can check or bet
                    if max_additional_bet == 0:
                        # Player can only check (no chips left)
                        amount = 0
                        actor.acted = True
                    else:
                        amount = actor.action(check_actions, high_bet)
                        self.pot += amount
                        actor.amount_in_round += amount
                        actor.total_contribution += amount
                else:
                    # Facing a bet
                    if max_additional_bet < (high_bet - actor.amount_in_round):
                        # Not enough to call - can only fold or go all-in
                        print(f"Not enough to call full amount. Can fold or call for {max_additional_bet}")
                        action_input = input("Enter F to fold or C to call all-in: ")
                        if action_input.upper().startswith('F'):
                            actor.fold()
                            amount = 0
                        else:
                            # All-in call
                            amount = actor.bet(max_additional_bet)
                            self.pot += amount
                            actor.amount_in_round += amount
                            actor.total_contribution += amount
                            print(f"Player {pos+1} is all-in for {actor.amount_in_round}")
                    else:
                        # Can call, raise, or fold
                        amount = actor.action(call_actions, high_bet)
                        self.pot += amount
                        actor.amount_in_round += amount
                        actor.total_contribution += amount
                
                # Mark player as having acted
                actor.acted = True
                
                # Handle all-in raises
                if actor.all_in and actor.amount_in_round > high_bet:
                    high_bet = actor.amount_in_round
                    # Reset acted status for players who haven't matched this new bet
                    for other_actor in self.actors:
                        if other_actor.active and not other_actor.all_in and other_actor.amount_in_round < high_bet:
                            other_actor.acted = False
                    
                    any_action_taken = True
                # Handle normal raises
                elif actor.amount_in_round > high_bet:
                    high_bet = actor.amount_in_round
                    # Reset acted status for players who haven't matched this new bet
                    for other_actor in self.actors:
                        if other_actor.active and not other_actor.all_in and other_actor.amount_in_round < high_bet:
                            other_actor.acted = False
                    
                    any_action_taken = True
                
                # Check if only one player remains active
                if self.count_active() <= 1:
                    return
            
            # If no action was taken this round, break to prevent infinite loop
            if not any_action_taken and betting_rounds > 1:
                print("No action taken this round, ending betting")
                break
        
        # Safety check for infinite loops
        if betting_rounds >= max_rounds:
            print("Maximum betting rounds reached, ending betting")

    def check_betting_over(self, high_bet):
        """
        Check if the current betting round is over.
        
        Returns:
            True if all active players have acted and bet the same amount
        """
        active_players = [actor for actor in self.actors if actor.active]
        
        # No active players or only one active player
        if len(active_players) <= 1:
            return True
        
        # Check if all active players have acted and matched the high bet
        for actor in active_players:
            if not actor.acted:
                return False
            if actor.amount_in_round != high_bet:
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
    
    def _find_best_hands(self, hands):
        """
        Find the best hand(s) among the given hands.
        
        Args:
            hands: List of [hole_cards, player_index] pairs
            
        Returns:
            List of winning [hole_cards, player_index] pairs
        """
        if len(hands) == 1:
            return [hands[0]]
        
        # Convert community cards to strings
        community = [card.show() for card in self.community_cards]
        
        # First, compare player 1 vs player 2
        winners = []
        if len(hands) >= 2:
            result = compare_hands(hands[0][0], hands[1][0], community, self.variation)
            if result == 1:
                winners = [hands[0]]  # Player 1 wins
            elif result == 2:
                winners = [hands[1]]  # Player 2 wins
            else:
                winners = [hands[0], hands[1]]  # Tie
        
        # If there are more than 2 players, compare the current winner against each remaining player
        for i in range(2, len(hands)):
            # If we have multiple winners (tie), compare each winner against the new player
            if len(winners) > 1:
                # Compare first winner against new player
                result = compare_hands(winners[0][0], hands[i][0], community, self.variation)
                if result == 1:
                    # Current winner beats new player, keep current winners
                    continue
                elif result == 2:
                    # New player beats all current winners
                    winners = [hands[i]]
                else:
                    # New player ties with current winners
                    winners.append(hands[i])
            else:
                # Compare the single current winner against new player
                result = compare_hands(winners[0][0], hands[i][0], community, self.variation)
                if result == 1:
                    # Current winner beats new player
                    continue
                elif result == 2:
                    # New player beats current winner
                    winners = [hands[i]]
                else:
                    # New player ties with current winner
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

    def initialize_player_amount_in_round(self):
        """Reset the amount each player has bet in this round."""
        for actor in self.actors:
            actor.amount_in_round = 0

    def reset_acted(self):
        """Reset the acted flag for all active players."""
        for actor in self.actors:
            if actor.active:
                actor.acted = False

    def calculate_sidepots(self):
        """
        Calculate sidepots based on all-in players and their bet amounts.
        """
        # If no all-in players, just use the main pot
        all_in_players = [actor for actor in self.actors if actor.active and actor.all_in]
        if not all_in_players:
            return
        
        # Sort all-in players by their total contribution (lowest first)
        all_in_players.sort(key=lambda x: x.total_contribution)
        
        # Reset sidepots
        self.sidepots = []
        
        # Calculate sidepots
        previous_amount = 0
        for all_in_player in all_in_players:
            current_amount = all_in_player.total_contribution
            
            # Skip if this player contributed the same as the previous player
            if current_amount == previous_amount:
                continue
            
            # Calculate this pot level
            pot_amount = 0
            eligible_players = []
            
            for actor in self.actors:
                if actor.active:
                    # How much does this player contribute to this pot level
                    contribution = min(current_amount, actor.total_contribution) - previous_amount
                    if contribution > 0:
                        pot_amount += contribution
                        eligible_players.append(actor)
            
            # Add this sidepot
            if pot_amount > 0:
                self.sidepots.append({
                    'amount': pot_amount,
                    'eligible_players': eligible_players.copy()
                })
            
            previous_amount = current_amount
        
        # Display sidepots information
        if self.sidepots:
            print("\nSidepots:")
            for i, pot in enumerate(self.sidepots):
                eligible_indices = [self.actors.index(player) for player in pot['eligible_players']]
                print(f"Pot {i+1}: ${pot['amount']} - Eligible players: {[idx+1 for idx in eligible_indices]}")
            print()

    def reset_player_states(self):
        """Reset player states after a hand."""
        for actor in self.actors:
            actor.all_in = False
            actor.total_contribution = 0