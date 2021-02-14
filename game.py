import random
from enum import Enum

NUM_PLAYERS = 2
NUM_CARDS_PER_PLAYER = 7
NUM_TURNS = NUM_CARDS_PER_PLAYER - 1

class R(Enum):
    BRICK = "brick"
    SILK = "silk"
    STONE = "stone"
    ORE = "ore"
    WOOD = "wood"
    GLASS = "glass"
    PAPYRUS = "papyrus"

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

class C(Enum):
    SCIENCE = "Science"
    MFG_R = "Manufactored Resource"
    RAW_R = "Raw Resource"
    COMMERCIAL = "Commercial"
    MILITARY = "Military"
    CIVIC = "Civic"

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

class Game:
    def __init__(self):
        self.turn = 0
        self.current_player_index = 0
        self.players = [Player(i) for i in range(NUM_PLAYERS)]
        self.hands = []
        self.deck = self.create_deck()
        self.hands = self.create_hands(self.deck)

    def current_player_finished(self):
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.turn += 1
            self.current_player_index = self.current_player_index % len(self.players)

    def current_player_hand(self):
        # Change starting index in hands array with every turn, so that players get a diffent hand
        # on each turn.
        return self.hands[(self.current_player_index + self.turn) % len(self.hands)]

    def player_right_left(self, player_index):
        if player_index == 0:
            player_right = self.players[player_index + 1]
            player_left = self.players[len(self.players)]
        elif player_index == len(self.players):
            player_right = self.players[0]
            player_left = self.players[player_index - 1]
        else:
            player_right = self.players[player_index + 1]
            player_left = self.players[player_index - 1]
        return player_right, player_left

    def current_player(self):
        return self.players[self.current_player_index]

    def print_player_cards(self):
        for player in self.players:
            print("  Player {} Cards: ".format(player.player_number))
            player.print_cards()

    def create_deck(self):
        deck = [ \
            Card("Tavern", C.COMMERCIAL, provides_resources = [(R.BRICK, R.STONE, R.WOOD, R.ORE)]),
            Card("Stones 'r' Us", C.RAW_R, provides_resources = [(R.STONE, R.STONE, R.STONE, R.STONE)], cost = [R.SILK]),
            Card("Stones + Bricks 'r' Us", C.RAW_R, provides_resources = [(R.STONE, R.BRICK)]),
            Card("Tavern", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], cost = [R.SILK]),
            Card("Quarry", C.RAW_R, provides_resources = [(R.STONE,)]),
            Card("Quarry", C.RAW_R, provides_resources = [(R.STONE,),(R.STONE,)]),
            Card("Guard Tower", C.MILITARY, num_shields = 2, money_cost = 1),
            Card("Guard Tower", C.MILITARY, num_shields = 1, cost = [R.STONE]),
            Card("University", C.SCIENCE, provides_sciences = ["science_symbol", "science_symbol"], cost = [R.BRICK, R.SILK]),
            Card("Towel Factory", C.MFG_R, provides_resources = [(R.SILK,),(R.SILK,)]),
            Card("Temple", C.CIVIC, points = 4, cost = [R.ORE]),
            Card("Scriptorium", C.SCIENCE, provides_sciences = ["science_symbol"]),
            Card("Scriptorium", C.SCIENCE, provides_sciences = ["science_symbol"]),
            Card("Towel Factory", C.MFG_R, provides_resources = [(R.SILK,), (R.SILK,)]),
            Card("Palace", C.CIVIC, points = 8, cost = [R.STONE, R.STONE])]
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
        self.money = 0

    def give_moneys_for_discard(self):
        self.money += 3

    def play_card(self, selected_card):
        resource_tuples = self.available_resources_tuples(self.cards)

        if self.has_resources(selected_card.cost, resource_tuples):
            self.cards.append(selected_card)
            print("self.cards: ", self.cards)
            return True
        elif selected_card.money_cost > 0:
            if self.money >= selected_card.money_cost:
                self.money -= selected_card.money_cost
            else:
                return False
        else:
            return False

    def available_resources_tuples(self, cards):
        resource_tuples = []
        for card in cards:
            for resource_tuple in card.provides_resources:
                resource_tuples.append(resource_tuple)
        return resource_tuples

    def has_resources(self, cost, resource_tuples):
        if len(cost) == 0:
            return True
        elif len(resource_tuples) == 0:
            return False
        elif len(resource_tuples[0]) == 0:
            return self.has_resources(cost, resource_tuples[1:])
        else:
            for resource_option in resource_tuples[0]:
                cost_copy = cost.copy()
                try:
                    cost_copy.remove(resource_option)
                except:
                    pass
                if self.has_resources(cost_copy, resource_tuples[1:]):
                    return True
            # No matches found
            return False

    def print_cards(self):
        self.total_science_symbols = 0
        self.total_score = 0
        for card in self.cards:
            if card.card_type == C.SCIENCE:
                for i in range(0, len(card.provides_resources)):
                    self.total_science_symbols += 1
        print("total science symbols: ", self.total_science_symbols)
        for card in self.cards:
            if card.card_type == C.SCIENCE:
                card.points = 0
                for i in range(len(card.provides_resources)):
                    card.points += self.total_science_symbols
            if card.points > 0 and len(card.provides_resources) > 0:
                print("    {30} - Provides {:>20} Points - {:>4} Cost - {:>20}".format(card.name, card.provides_resources, card.points, card.cost))
            elif card.points > 0:
                print("    {} - {} points Cost - {}".format(card.name, card.points, card.cost))
            else:
                print("    {} - Provides {} Cost - {}".format(card.name, card.provides_resources, card.cost))
            self.total_score += card.points
        print("Total Score: ", self.total_score)

    # def buy_resource(self, player_index):
    #     player_right_available_resources = []
    #     player_left_available_resources = []
    #     player_right_index, player_left_index = Game.player_right_left(player_index)
    #     right_player = Game.players[player_right_index]
    #     left_player = Game.players[player_left_index]
    #     for card in right_player.cards:
    #         if card.type == C.MFG_R or card.type == C.RAW_R:
    #             player_right_available_resources.append(card)
    #             print(card.provides_resources)

class Card:
    def __init__( self, name, card_type, points = 0, provides_resources = [], cost = [], provides_sciences = [], num_shields = 0, money_cost = 0):
        self.cost = cost
        self.points = points
        self.card_type = card_type
        self.name = name
        self.provides_resources = provides_resources
        self.provides_sciences = provides_sciences
        self.num_shields = num_shields
        self.money_cost = money_cost

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}: Card Type: {}  Points = {}, Resources = {}, Science = {}, Shields = {}, Cost {}".format(
            self.name, self.card_type, self.points, self.provides_resources, self.provides_sciences, self.num_shields, self.cost)
