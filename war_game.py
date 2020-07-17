"""
File to define a card Class
"""

# random.sguffle doesn't return anything, it does it in place!

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
values = {
    'ace': 14,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'jack': 11,
    'queen': 12,
    'king': 13


}


class Card:

    def __init__(self, suit, rank):

        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
        self.value = values[self.rank.lower()]

    def __str__(self):
        return self.rank + ' of ' + self.suit



class Deck:

    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # Create the Card Object
                self.all_cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

    def __str__(self):
        return 'I am a deck, I have 52 cards'


class Player:

    def __init__(self, name):

        self.name = name
        self.all_cards = []

    def remove_one(self):
        return self.all_cards.pop(0)  # from the beginning of the list, that's why we specify the index 0

    def add_cards(self, new_cards):
        if type(new_cards) == list:
            self.all_cards.extend(new_cards)
        else:
            self.all_cards.append(new_cards)
        # What happens if it doesn't pass a valid card

    def __str__(self):
        return f'Player {self.name} has {len(self.all_cards)}'


def game():


    # GAME SET UP
    player_one = Player('Player One')
    player_two = Player('Player Two')

    new_deck = Deck()
    new_deck.shuffle()

    for x in range(26):
        player_one.add_cards(new_deck.deal_one())
        player_two.add_cards(new_deck.deal_one())

    game_on = True
    round_num = 0

    while game_on:
        round_num += 1
        print(f'Round {round_num}')

        if len(player_one.all_cards) == 0:
            print('Player One out of cards, Player two wins!')
            game_on = False
            break

        if len(player_two.all_cards) == 0:
            print('Player two out of cards, Player one wins!')
            game_on = False
            break

        # START A NEW ROUND
        player_one_cards = []   # The card that are on the table, or in play in that particular round
        player_one_cards.append(player_one.remove_one())


        player_two_cards = []  # The card that are on the table, or in play in that particular round
        player_two_cards.append(player_two.remove_one())

        at_war = True

        while at_war:
            if player_one_cards[-1].value > player_two_cards[-1].value:  # We specify the last position with the -1, because if we
                # go to war, the cards on that list will increase, and we'll allways want to select the last one
                player_one.add_cards(player_two_cards)
                player_one.add_cards(player_one_cards)

                at_war = False

            elif player_two_cards[-1].value > player_one_cards[-1].value:
                player_two.add_cards(player_two_cards)
                player_two.add_cards(player_one_cards)

                at_war = False

            else:
                print('WAR!')
                if len(player_one.all_cards) < 5:
                    print('Player one can not play, insufficient cards')
                    print('PLAYER TWO WINS')
                    game_on = False
                    break

                elif len(player_two.all_cards) < 5:
                    print('Player two can not play, insufficient cards')
                    print('PLAYER ONE WINS')
                    game_on = False
                    break

                else:
                    for num in range(3):
                        player_one_cards.append(player_one.remove_one())
                        player_two_cards.append(player_two.remove_one())


game()
