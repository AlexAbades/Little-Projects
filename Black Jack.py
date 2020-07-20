import random
from time import sleep
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
values = {
    'ace': 11,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'jack': 10,
    'queen': 10,
    'king': 10
}
on_game = True
count = 0

class Card:

    def __init__(self, rank, suit):
        self.rank = rank.capitalize()
        self.suit = suit.capitalize()
        self.value = values[self.rank.lower()]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def __str__(self):
        return f'I have {len(self.all_cards)} cards'


class Hand:

    def __init__(self):
        self.hand = []
        self.aces = 0
        self.points = 0

    def add_card(self, card):
        self.hand.append(card)
        self.points += card.value
        if card.rank.lower() == 'ace':
            self.aces += 1

    def foll_aces(self):
        while self.points > 21 and self.aces:
            self.points -= 10
            self.aces -= 1


class Bank:

    def __init__(self, amount=100):
        self.amount = amount
        self.bet = 0

    def win(self):
        self.amount += self.bet

    def loose(self):
        self.amount -= self.bet

    def __str__(self):
        return f'Your current bank amount is {self.amount}€'


def bet(bank_player=None):
    """

    :type bank_player: Object of  Bank class
    """
    while True:
        try:
            bank_player.bet = int(input('\nHow much do you want to bet? '))
        except ValueError:
            print('Please select a valid amount.')
        else:
            if bank_player.bet > bank_player.amount:
                print('You do not have enough money...')
            else:
                break


def hit(deck, hand):
    """

    :param deck: Object, class Deck
    :param hand: Object, class Hand
    :return: Nothing
    """
    hand.add_card(deck.deal_one())
    hand.foll_aces()


def hit_or_stay(deck, hand):
    global on_game
    while on_game:
        try:
            player_choice = input("\nWould you like to hit or stay? Press 'h' to hit & 's' to stay: ")

            if player_choice[0].lower() == 'h':
                hit(deck, hand)
                on_game = True

            elif player_choice[0].lower() == 's':
                print('\nPlayer stands, Dealer is playing... \n')
                sleep(1)
                on_game = False

            else:
                print('I do not recognise what do you want to do...')
                pass
            break
        except IndexError:
            print('Please select hit or stay...')


def show_first(player, dealer):
    print('\nThe Dealer hand is: ')
    print('<Hidden card> &',dealer.hand[1], '\n')
    print('The player hand is:', *player.hand,sep='\n')  # The asterisk * symbol is used to print every item in a
    # collection, and the sep='\n ' argument prints each item on a separate line. The problem it's tjat it allways let
    # a space in the first item


def show_hands(player, dealer):
    print('The Dealer hand is:\n', *dealer.hand, sep='\n')
    print('The total points of the dealer are: ', dealer.points)
    print('\nThe Player hand is,\n', *player.hand, sep='\n')
    print('The total point os the player are: ', player.points)


def show_dealer(dealer):
    print('The Dealer hand is:', *dealer.hand, sep='\n')


def player_busts(bank, player):
    sleep(1)
    print('Player busts, your total point are ', player.points)
    bank.loose()


def player_wins(bank):
    sleep(1)
    print('\n\nPlayer wins')
    bank.win()


def dealer_busts(bank):
    sleep(1)
    print('\n\nDealer busts ')
    bank.win()


def dealer_win(bank):
    sleep(1)
    print('\n\nDealer wins')
    bank.loose()


def tie():
    sleep(1)
    print('\n\nIt is a tie')


player_bank = Bank()  # Default 100€

while True and player_bank.amount != 0:

    if count == 0:
        print('Hello, welcome to Black Jack, \nTry to reach 21, or the closest as you can \n'
              'Aces count 11 or 1, be carefully!')
    # We create a new deck and we shuffle it
    my_deck = Deck()
    my_deck.shuffle()

    # We instantiate a player and a dealer hand.
    player_hand = Hand()
    dealer_hand = Hand()

    # We deal one card to each one starting with the player
    player_hand.add_card(my_deck.deal_one())
    dealer_hand.add_card(my_deck.deal_one())
    # 2nd card of the game
    player_hand.add_card(my_deck.deal_one())
    dealer_hand.add_card(my_deck.deal_one())

    # We ask the player what does it want to do
    print('\nYour current bank amount is: ', player_bank.amount, '€')
    bet(player_bank)

    # Show to the player his cards and the second one from the dealer
    show_first(player_hand, dealer_hand)

    # We start the game
    while on_game:
        # We ask the player is he want to hit or stay
        hit_or_stay(my_deck, player_hand)

        # We show him his cards
        if on_game:
            show_first(player_hand, dealer_hand)
            print('')

        if player_hand.points > 21:
            player_busts(player_bank, player_hand)
            break

    # If the player doesn't bust, we keep playing
    if player_hand.points <= 21:
        # We show the dealer cards
        # show_dealer(dealer_hand)

        # If the dealer doesn't have 17 or more, we continue adding cards.
        while dealer_hand.points < 17:
            dealer_hand.add_card(my_deck.deal_one())

        # Once The dealer has 17 or more, we show all the cards
        show_hands(player_hand, dealer_hand)

        # We check the different scenarios.
        if dealer_hand.points > 21:
            dealer_busts(player_bank)
        elif dealer_hand.points > player_hand.points:
            dealer_win(player_bank)
        elif dealer_hand.points < player_hand.points:
            player_wins(player_bank)
        else:
            tie()

    # We show the player his bank
    print(str(player_bank))  # As we defined a str function in the Bank class, if we
    # want to print it, we have to call the str function

    # We ask the player if he wants to continue playing
    sleep(1)

    while player_bank.amount != 0:
        try:
            keep_playing = input('\nDo you want to keep playing? (Y) or (N): ')

            if keep_playing[0].lower() == 'y' and keep_playing != '':
                on_game = True
                break
            elif keep_playing[0].lower() == 'n' and keep_playing != '':
                print('See you latter!')
                count = 0
                break
            else:
                print("Please select yer or no...")
        except IndexError:
            print('Please select yer or no...')

    count += 1
    player_hand.points = 0



# Reset the tota points of the player! player_hand.points = 0 at the end