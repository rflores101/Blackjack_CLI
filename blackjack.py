import os
import random
import time

os.system("clear")

## GLOBAL VARS
MIN_BET = 15
MAX_BET = 1000

## FUNCTIONS
def create_balance():
    while True:
        balance = input("Enter your starting balance: $")
        if balance.isdigit():
            balance = int(balance)
            if balance > MIN_BET:
                break
            else:
                os.system("clear")
                print(f"You must have at least ${MIN_BET} to play here.\n")
        else:
            os.system("clear")
            print("Enter a valid dollar amount.\n")
    return balance

def set_bet(balance):
    while True:
        bet = input("How much would you like to bet for this hand? $")
        if bet.isdigit():
            bet = int(bet)
            print()
            if bet % 5 != 0:
                print("Bets must be in $5 increments.\n")
            elif bet > balance:
                print(f"You cannot bet more than your balance of ${balance}.\n")
            elif bet < MIN_BET:
                print(f"Minimum bet is ${MIN_BET}.\n")
            elif bet > MAX_BET:
                print(f"Maximum bet is ${MAX_BET}.\n")
            else:
                break
        else:
            print("Enter a valid dollar amount.")
    return bet

def get_card_value(card: str):
    # Ace is treated as 11 until needed to be lowered
    facecard_value = {
        "A": 11,
        "K": 10,
        "Q": 10,
        "J": 10
    }
    # NOTE: Emojis had a blank space at the end of the string
    value = card[-3]
    if not value.isdigit():
        value = facecard_value[value]
    elif value == "0":
        value = "10"
    
    value = int(value)
    return value

def game_over(balance):
    print(f"Thanks for playing! Your ending balance was ${balance}\n")
    print("See you again soon...\n")

def empty_balance():
    print("All out of money...")
    print("Come back again soon...\n\n")


##CLASSES
class Dealer:
    def __init__(self):
        self.hand = []
        self.hand_total = 0

    def get_new_card(self, card):
        self.hand.append(card)
        self.hand_total += get_card_value(card)

    def get_hand_total(self):
        hand = self.reveal_hand()
        cur_total = self.hand_total

        # Evaluate aces to stay in the game
        ace_count = 0
        changed_aces = 0
        for card in hand:
            if card[0] == "A":
                ace_count += 1
        while (cur_total > 21) and (changed_aces < ace_count):
            cur_total -= 10
            changed_aces += 1

        return cur_total
    
    def get_hand(self):
        return self.hand[1:]
    
    def reveal_hand(self):
        return self.hand
            
    
class Player:
    def __init__(self):
        self.hand = []
        self.hand_total = 0

    def get_new_card(self, card):
        self.hand.append(card)
        self.hand_total += get_card_value(card)

    def get_hand_total(self):
        hand = self.get_hand()
        cur_total = self.hand_total

        # Evaluate aces to stay in the game
        ace_count = 0
        changed_aces = 0
        for card in hand:
            if card[0] == "A":
                ace_count += 1
        while (cur_total > 21) and (changed_aces < ace_count):
            cur_total -= 10
            changed_aces += 1

        return cur_total
    
    def get_hand(self):
        return self.hand
    

class Deck:
    def __init__(self):
        card_values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        card_suits = ["♠️", "♦️", "♥️", "♣️"]

        deck = []
        for val in card_values:
            for suit in card_suits:
                deck.append(val+suit)
        self._original = deck
        self.running = deck.copy()

    def deal_card(self):
        random_card = random.choice(self.running)
        self.running.remove(random_card)
        return random_card
    
    def get_running(self):
        return self.running
    
    def reset_deck(self):
        self.running = self._original.copy()


class Game:
    def __init__(self, player: Player, dealer: Dealer, deck: Deck, balance, bet):
        self.messages = {
            "busted": "BUSTED! Tough luck.",
            "tie": "Tie! Congrats, you get your bet back.",
            "player_won": "Winner! Well done.",
            "dealer_won": "Dealer wins. Better luck next time.",
            "player_turn": "Your move.",
            "dealer_turn": "Dealer's move.",
            "game_over": "Thanks for playing!"
        }
        self.player = player
        self.dealer = dealer
        self.deck = deck
        self.balance = balance
        self.bet = bet

    def get_message(self, message):
        return self.messages[message]
    
    def print_game_status_player(self):
        print(f"Balance: ${self.balance}")
        print(f"Bet: ${self.bet}\n")
        print("DEALER: " + " ".join(self.dealer.get_hand()) + "\n")
        print("HAND: " + " ".join(self.player.get_hand()) + "\n")

    def print_game_status_dealer(self):
        print(f"Balance: ${self.balance}")
        print(f"Bet: ${self.bet}\n")
        print("DEALER: " + " ".join(self.dealer.reveal_hand()) + "\n")
        print("HAND: " + " ".join(self.player.get_hand()) + "\n")

    def player_turn(self):
        while True:
            choice = input("Hit (h) or Stay (s)? ")
            choice = choice.lower()

            if choice == "h":
                self.player.get_new_card(self.deck.deal_card())
                os.system("clear")
                self.print_game_status_player()
                if self.player.get_hand_total() > 21:
                    print(str(self.player.get_hand_total()) + "! " + self.get_message("busted") + "\n")
                    return "LOST"
            elif choice == "s":
                return "DEALER_TURN"
            else:
                print("Please enter a valid choice.")
        
    def dealer_turn(self):
        while True:
            dealer_total = self.dealer.get_hand_total()
            player_total = self.player.get_hand_total()

            os.system("clear")
            self.print_game_status_dealer()
            if dealer_total > 21:
                print("_____________________\n\n")
                print(f"Dealer busts!...\n{self.get_message('player_won')}\n")
                return "WON"
            elif dealer_total == player_total:
                print("_____________________\n\n")
                print(f"{player_total} vs Dealer's {dealer_total}...\n{self.get_message('tie')}\n")
                return "TIE"
            elif dealer_total > player_total:
                print("_____________________\n\n")
                print(f"{player_total} vs Dealer's {dealer_total}...\n{self.get_message('dealer_won')}\n")
                return "LOST"
            else:
                print("Dealer playing...")
                time.sleep(1) # Mimic dealing card
                self.dealer.get_new_card(self.deck.deal_card())
        

## MAIN
def main():
    balance = create_balance()
    
    play_game = True

    while play_game:
        print(f"Balance: ${balance}")
        bet = set_bet(balance)
        deck = Deck()
        dealer = Dealer()
        player = Player()

        # STARTING HANDS
        for _ in range(2):
            dealer.get_new_card(deck.deal_card())
            player.get_new_card(deck.deal_card())
        
        # START THE GAME
        os.system("clear")
        game = Game(player, dealer, deck, balance, bet)
        game.print_game_status_player()

        # PLAYER'S TURN
        players_turn = game.player_turn()
        dealers_turn = None
        if players_turn == "DEALER_TURN":
            # IF PLAYER DOES NOT BUST -> DEALER'S TURN
            dealers_turn = game.dealer_turn()

        # UPDATE BALANCE BASED ON RESULT
        if players_turn == "LOST" or dealers_turn == "LOST":
            balance -= bet
        elif dealers_turn == "WON":
            balance += bet

        print("_____________________\n\n")
        print(f"New Balance: ${balance}")        
        
        if balance > 0:
        # ASK TO PLAY AGAIN
            while True:
                replay_ask = input("Another round [y/n]? ")
                replay_ask = replay_ask.lower()

                if replay_ask == "n":
                    play_game = False
                    os.system("clear")
                    game_over(balance)
                    break
                elif replay_ask == "y":
                    os.system("clear")
                    break
                else:
                    print("Please enter a valid response.\n")
        else:
            play_game = False
            print()
            empty_balance()

    


    
main()
