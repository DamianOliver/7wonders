import random


NUM_CARDS_PER_PLAYER = 7
NUM_TURNS = NUM_CARDS_PER_PLAYER - 1

class Game:
    def __init__(self):
        self.turn = 0
        self.players = [Player(1), Player(2)]
        self.hands = []
        for i in range(len(self.players)):
           self.hands.append([Card() for i in range(NUM_CARDS_PER_PLAYER)]) 

    def next_turn(self):
        self.turn += 1

    def play(self):
        while self.turn < NUM_TURNS:

            print("turn {}".format(self.turn))

            for i in range(len(self.players)):
                player = self.players[i]
                hand = self.hands[(i + self.turn) % len(self.hands)]
                print("  Player {}".format(player.player_number))
                player.select_card(hand)

            self.turn += 1

        self.print_player_cards()

    def print_player_cards(self):
        for player in self.players:
            print("  Player {} Cards: ".format(player.player_number))
            player.print_cards()


class Player:
    def __init__(self, player_number):
        self.player_number = player_number
        self.cards = []

    def select_card(self, hand_cards):
        self.print_cards()
        selected_card_number = self.ask_for_card_selection(hand_cards)
        self.cards.append(hand_cards[selected_card_number])
        del hand_cards[selected_card_number]

    def ask_for_card_selection(self, hand_cards):
        for i in range(len(hand_cards)):
            print("Card {}: Points = {}".format(i, hand_cards[i].points))
        while True:
            try:
                index = int(input("  Select a card: "))
                if index >= 0 and index < len(hand_cards):
                    return index
            except ValueError: 
                pass
                
            print("Enter a number from 0 to {}".format(len(hand_cards) - 1))

    def print_cards(self):
        for card in self.cards:
            print("    {}".format(card.points))


class Card:
    def __init__(self):
        self.points = random.randrange(0,6)



Game().play()
