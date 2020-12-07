import random

NUM_PLAYERS = 2
NUM_CARDS_PER_PLAYER = 7
NUM_TURNS = NUM_CARDS_PER_PLAYER - 1

class Game:
    def __init__(self):
        self.turn = 0
        self.players = [Player(i) for i in range(NUM_PLAYERS)]
        self.hands = []
        self.deck = self.create_deck()
        self.hands = self.create_hands(self.deck)

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
                print("hand cards: ", len(hand))
                print(hand)

            self.turn += 1

        self.print_player_cards()

    def print_player_cards(self):
        for player in self.players:
            print("  Player {} Cards: ".format(player.player_number))
            player.print_cards()

    def create_deck(self):
        deck = [ \
            Card("Tavern", 3, "Commercial"), 
            Card("Tavern", 3, "Commercial"), 
            Card("Temple", 4, "Civic"), 
            Card("Temple", 4, "Civic"), 
            Card("Scriptorium", 1, "Science"), 
            Card("Scriptorium", 1, "Science"), 
            Card("Quarry", 0, "Raw Rescource"),
            Card("Quarry", 0, "Raw Resource"), 
            Card("Towel Factory", 0, "Manufactored Resource"), 
            Card("Towel Factory", 0, "Manufactored Resource"), 
            Card("Guard Tower", 3, "Military"), 
            Card("Guard Tower", 3, "Military"), 
            Card("University", 8, "Science"), 
            Card("Palace", 8, "Civic")]
        random.shuffle(deck)
        return deck

    def create_hands(self, deck):
        hands = []
        for i in range(NUM_PLAYERS):
            deck_len = len(deck)
            start = i * NUM_CARDS_PER_PLAYER
            end = (i + 1) * NUM_CARDS_PER_PLAYER
            hands.append(self.deck[start:end])
        return hands

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
            print("Number: {} {}".format(i, hand_cards[i].__str__()))
        while True:
            try:
                index = int(input("  Select a card: "))
                if index >= 0 and index < len(hand_cards):
                    return index
            except ValueError: 
                pass
                
            print("Enter a number from 0 to {}".format(len(hand_cards) - 1))
            print("hand cards", len(hand_cards))
            print("hand: ", hand_cards)

    def print_cards(self):
        self.total_score = 0
        for card in self.cards:
            print("    {} - {} points".format(card.name, card.points))
            self.total_score += card.points
        print("Total Score: ", self.total_score)


class Card:
    def __init__( self, name, points, card_type):
        self.points = points
        self.card_type = card_type
        self.name = name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}: Card Type: {}  Points = {}".format(self.name, self.card_type, self.points)



Game().play()
