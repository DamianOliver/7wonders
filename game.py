# Copyright 2020 Damian Piech

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from enum import Enum

NUM_PLAYERS = 1
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
    GUILD = "Guild"

class S(Enum):
    TABLET = "Tablet"
    COG = "Cog"
    COMPASS = "Compass"

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

    # def create_deck(self):
    #     deck = [ \
    #         Card("BATHS", C.CIVIC, points = 3, cost = [R.STONE], num_players = 3),
    #         Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 3),
    #         Card("CLAY PIT", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)], money_cost = 1, num_players = 3),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.SILK], num_players = 3),
    #         Card("SCRIPTORIUM", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.PAPYRUS], num_players = 3),
    #         Card("CLAY POOL", C.RAW_R, provides_resources = [(R.BRICK,)], num_players = 3),
    #         Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
    #         Card("ORE VEIN", C.RAW_R, provides_resources = [(R.ORE,)], num_players = 3),
    #         Card("EAST TRADING POST", C.COMMERCIAL, num_players = 3),
    #         Card("ALTAR", C.CIVIC, points = 2, num_players = 3),
    #         Card("TIMBER YARD", C.RAW_R, provides_resources = [(R.STONE, R.WOOD)], money_cost = 1, num_players = 3),
    #         Card("GUARD TOWER", C.MILITARY, num_shields = 1, cost = [R.BRICK], num_players = 3),
    #         Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 3),
    #         Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD], num_players = 3),
    #         Card("BARRACKS", C.MILITARY, num_shields = 1, cost = [R.ORE], num_players = 3),
    #         Card("WORKSHOP", C.SCIENCE, provides_sciences = [S.COG], cost = [R.GLASS], num_players = 3),
    #         Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 3),
    #         Card("STONE PIT", C.RAW_R, provides_resources = [(R.STONE,)], num_players = 3),
    #         Card("MARKETPLACE", C.COMMERCIAL, num_players = 3),
    #         Card("WEST TRADING POST", C.COMMERCIAL, num_players = 3),
    #         Card("THEATER", C.CIVIC, points = 2, num_players = 3),
    #         # Card("", C., ),
    #         Card("THEATER", C.CIVIC, points = 2, num_players = 4),
    #         Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 4),
    #         Card("EXCAVATION", C.RAW_R, provides_resources = [(R.STONE, R.BRICK)], money_cost = 1, num_players = 4),
    #         Card("ORE VEIN", C.RAW_R, provides_resources = [(R.ORE,)], num_players = 4),
    #         Card("PAWNSHOP", C.CIVIC, points = 3, num_players = 4),
    #         Card("GUARD TOWER", C.MILITARY, num_shields = 1, cost = [R.BRICK], num_players = 4),
    #         Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 4),

    #         Card("BARRACKS", C.MILITARY, num_shields = 1, cost = [R.ORE], num_players = 5),
    #         Card("STONE PIT", C.RAW_R, provides_resources = [(R.STONE,)], num_players = 5),
    #         Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 5),
    #         Card("CLAY POOL", C.RAW_R, provides_resources = [(R.BRICK,)], num_players = 5),
    #         Card("ALTAR", C.CIVIC, points = 2, num_players = 5),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.SILK], num_players = 5),
    #         Card("FOREST CAVE", C.RAW_R, provides_resources = [(R.WOOD, R.ORE)], money_cost = 1, num_players = 5),

    #         Card("MARKETPLACE", C.COMMERCIAL, num_players = 6),
    #         Card("TREE FARM", C.RAW_R, provides_resources = [(R.WOOD, R.BRICK)], money_cost = 1, num_players = 6),
    #         Card("MINE", C.RAW_R, provides_resources = [(R.STONE, R.ORE)], money_cost = 1, num_players = 6),
    #         Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 6),
    #         Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 6),
    #         Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 6),
    #         Card("THEATER", C.CIVIC, points = 2, num_players = 6),

    #         Card("EAST TRADING POST", C.COMMERCIAL, num_players = 7),
    #         Card("PAWNSHOP", C.CIVIC, points = 3, num_players = 7),
    #         Card("WORKSHOP", C.SCIENCE, provides_sciences = [S.COG], cost = [R.GLASS], num_players = 7),
    #         Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 7),
    #         Card("WEST TRADING POST", C.COMMERCIAL, num_players = 7),
    #         Card("BATHS", C.CIVIC, points = 3, cost = [R.STONE], num_players = 7),  
    #         Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD], num_players = 7)]

    #     length_of_deck = len(deck)
    #     i = 0

    #     while i < length_of_deck:
    #         if deck[i].num_players > 3 and deck[i].num_players > NUM_PLAYERS:
    #             del deck[i]
    #             length_of_deck -= 1
    #         else:
    #             i += 1

    #     random.shuffle(deck)
    #     return deck

    def create_deck(self):
        deck = [ \
            Card("RAINFOREST", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,), (R.WOOD,), (R.WOOD,)], num_players = 7),
            Card("BIG MINE", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,), (R.ORE,)], cost = [R.WOOD], num_players = 7),
            Card("PAPER HOUSE", C.MFG_R, provides_resources = [(R.PAPYRUS,), (R.PAPYRUS,)], cost = [R.WOOD], num_players = 7),
            Card("TOWEL HOUSE", C.MFG_R, provides_resources = [(R.SILK,), (R.SILK,)], cost = [R.WOOD], num_players = 7),
            Card("PAPER HOUSE", C.MFG_R, provides_resources = [(R.PAPYRUS,), (R.PAPYRUS,)], cost = [R.WOOD], num_players = 7),
            Card("RAINFOREST", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,), (R.WOOD,), (R.WOOD,)], num_players = 7),
            Card("BIG MINE", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,), (R.ORE,)], cost = [R.WOOD], num_players = 7),
            Card("RAINFOREST", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,), (R.WOOD,), (R.WOOD,)], num_players = 7),
            Card("BIG MINE", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,), (R.ORE,)], cost = [R.WOOD], num_players = 7),
            Card("TOWEL HOUSE", C.MFG_R, provides_resources = [(R.SILK,), (R.SILK,)], cost = [R.WOOD], num_players = 7)]
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
        self.num_shields = 0

    def give_moneys_for_discard(self):
        self.money += 3

    def play_card(self, selected_card):
        resource_tuples = self.available_resources_tuples(self.cards)

        if self.can_play_card(selected_card):
            self.money -= selected_card.money_cost
            self.num_shields += selected_card.num_shields
            self.money += selected_card.provides_money
            print("added: ", self.num_shields)
            self.cards.append(selected_card)
            print("self.cards: ", self.cards)
            return True
        else:
            return False

    def can_play_card(self, card):
        resource_tuples = self.available_resources_tuples(self.cards)

        if self.has_resources_for_card(card.cost, resource_tuples) and self.money >= card.money_cost:
            return True
        else:
            return False

    # def has_money_for_card(self, )

    def available_resources_tuples(self, cards):
        resource_tuples = []
        for card in cards:
            for resource_tuple in card.provides_resources:
                resource_tuples.append(resource_tuple)
        return resource_tuples

    def has_resources_for_card(self, cost, resource_tuples):
        if len(cost) == 0:
            return True
        elif len(resource_tuples) == 0:
            return False
        elif len(resource_tuples[0]) == 0:
            return self.has_resources_for_card(cost, resource_tuples[1:])
        else:
            for resource_option in resource_tuples[0]:
                cost_copy = cost.copy()
                try:
                    cost_copy.remove(resource_option)
                except:
                    pass
                if self.has_resources_for_card(cost_copy, resource_tuples[1:]):
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
    def __init__(self, name, card_type, points = 0, provides_resources = [], cost = [], provides_sciences = [], provides_money = 0, num_shields = 0, money_cost = 0, num_players = 3):
        self.cost = cost
        self.points = points
        self.card_type = card_type
        self.name = name
        self.provides_resources = provides_resources
        self.provides_sciences = provides_sciences
        self.num_shields = num_shields
        self.money_cost = money_cost
        self.provides_money = provides_money
        self.num_players = num_players

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}: Card Type: {}  Points = {}, Resources = {}, Science = {}, Shields = {}, Cost {}".format(
            self.name, self.card_type, self.points, self.provides_resources, self.provides_sciences, self.num_shields, self.cost)
