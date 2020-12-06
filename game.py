

NUM_TURNS = 6

class Game:
    def __init__(self):
        self.turn = 0
        self.players = [Player(1), Player(2)]
        self.cards = [Card(), Card(), Card()]

    def next_turn(self):
        self.turn += 1

    def play(self):
        while self.turn < NUM_TURNS:
            print("turn {}".format(self.turn))

            for player in self.players:
                print("  Player {}".format(player.player_number))
                player.select_card([])

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
        input = raw_input("  Select a card: ")
        selected_card_number = int(input)
        self.cards.append(selected_card_number)

    def print_cards(self):
        for card in self.cards:
            print("    {}".format(card))


class Card:
    def __init__(self):
        self.points = 1

    def print_card(self):



Game().play()
