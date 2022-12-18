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
import pygame as pg
from enum import Enum

NUM_PLAYERS = 3
NUM_CARDS_PER_PLAYER = 7
NUM_TURNS = NUM_CARDS_PER_PLAYER - 1

class R(Enum):
    BRICK = "brick"
    STONE = "stone"
    ORE = "ore"
    WOOD = "wood"
    GLASS = "glass"
    PAPYRUS = "papyrus"
    SILK = "silk"
   
    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def is_raw(self):
        raw_resources = [R.BRICK, R.STONE, R.ORE, R.WOOD]
        if self in raw_resources:
            return True
        return False
    
class C(Enum):
    SCIENCE = "Science"
    MFG_R = "Manufactored Resource"
    RAW_R = "Raw Resource"
    COMMERCIAL = "Commercial"
    MILITARY = "Military"
    CIVIC = "Civic"
    GUILD = "Guild"
    WONDER_C = "Wonder"

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
        self.age = 3

        wonder_list = self.assign_wonders()
        self.players = []
        
        for i in range(NUM_PLAYERS):
            self.players.append(Player(i, wonder_list[i]))
            self.players[i].play_card(wonder_list[i].layers_list[0])

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
        if self.age == 1:
            deck = [ \
                Card("BATHS", C.CIVIC, points = 3, cost = [R.STONE], num_players = 3),
                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 3),
                Card("CLAY PIT", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)], money_cost = 1, num_players = 3),
                Card("APOTHECARY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.SILK], num_players = 3),
                Card("SCRIPTORIUM", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.PAPYRUS], num_players = 3),
                Card("CLAY POOL", C.RAW_R, provides_resources = [(R.BRICK,)], num_players = 3),
                Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
                Card("ORE VEIN", C.RAW_R, provides_resources = [(R.ORE,)], num_players = 3),
                Card("EAST TRADING POST", C.COMMERCIAL, icon = RightRawDiscount(), num_players = 3),
                Card("ALTAR", C.CIVIC, points = 2, num_players = 3),
                Card("TIMBER YARD", C.RAW_R, provides_resources = [(R.STONE, R.WOOD)], money_cost = 1, num_players = 3),
                Card("GUARD TOWER", C.MILITARY, num_shields = 1, cost = [R.BRICK], num_players = 3),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 3),
                Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD], num_players = 3),
                Card("BARRACKS", C.MILITARY, num_shields = 1, cost = [R.ORE], num_players = 3),
                Card("WORKSHOP", C.SCIENCE, provides_sciences = [S.COG], cost = [R.GLASS], num_players = 3),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 3),
                Card("STONE PIT", C.RAW_R, provides_resources = [(R.STONE,)], num_players = 3),
                Card("MARKETPLACE", C.COMMERCIAL, icon = ManufactoredDiscount(), num_players = 3),
                Card("WEST TRADING POST", C.COMMERCIAL, icon = LeftRawDiscount(), cost = [R.WOOD], num_players = 3),
                Card("THEATER", C.CIVIC, points = 2, num_players = 3),

                Card("THEATER", C.CIVIC, points = 2, num_players = 4),
                Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 4),
                Card("EXCAVATION", C.RAW_R, provides_resources = [(R.STONE, R.BRICK)], money_cost = 1, num_players = 4),
                Card("ORE VEIN", C.RAW_R, provides_resources = [(R.ORE,)], num_players = 4),
                Card("PAWNSHOP", C.CIVIC, points = 3, num_players = 4),
                Card("GUARD TOWER", C.MILITARY, num_shields = 1, cost = [R.BRICK], num_players = 4),
                Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 4),

                Card("BARRACKS", C.MILITARY, num_shields = 1, cost = [R.ORE], num_players = 5),
                Card("STONE PIT", C.RAW_R, provides_resources = [(R.STONE,)], num_players = 5),
                Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 5),
                Card("CLAY POOL", C.RAW_R, provides_resources = [(R.BRICK,)], num_players = 5),
                Card("ALTAR", C.CIVIC, points = 2, num_players = 5),
                Card("APOTHECARY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.SILK], num_players = 5),
                Card("FOREST CAVE", C.RAW_R, provides_resources = [(R.WOOD, R.ORE)], money_cost = 1, num_players = 5),

                Card("MARKETPLACE", C.COMMERCIAL, num_players = 6),
                Card("TREE FARM", C.RAW_R, provides_resources = [(R.WOOD, R.BRICK)], money_cost = 1, num_players = 6),
                Card("MINE", C.RAW_R, provides_resources = [(R.STONE, R.ORE)], money_cost = 1, num_players = 6),
                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 6),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 6),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 6),
                Card("THEATER", C.CIVIC, points = 2, num_players = 6),

                Card("EAST TRADING POST", C.COMMERCIAL, icon = RightRawDiscount(), num_players = 7),
                Card("PAWNSHOP", C.CIVIC, points = 3, num_players = 7),
                Card("WORKSHOP", C.SCIENCE, provides_sciences = [S.COG], cost = [R.GLASS], num_players = 7),
                Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 7),
                Card("WEST TRADING POST", C.COMMERCIAL, icon = LeftRawDiscount(), cost = [R.WOOD], num_players = 7),
                Card("BATHS", C.CIVIC, points = 3, cost = [R.STONE], num_players = 7),  
                Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD], num_players = 7)
                ]

        elif self.age == 2:
            deck = [ \
                Card("SAWMILL", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,)], money_cost = 1, num_players = 3),
                Card("FOUNDRY", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,)], money_cost = 1, num_players = 3),
                Card("BRICKYARD", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,)], money_cost = 1,num_players = 3),
                Card("QUARRY", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,)], money_cost = 1, num_players = 3),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 3),
                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 3),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 3),
                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], cost = [R.WOOD, R.WOOD], num_players = 3),
                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], cost = [R.BRICK, R.BRICK], num_players = 3),
                Card("VINEYARD", C.COMMERCIAL, icon = OneGoldForRaw(), num_players = 3),
                Card("TEMPLE", C.CIVIC, points = 3, cost = [R.WOOD, R.BRICK, R.GLASS], coupon = ["ALTAR"], num_players = 3),
                Card("COURTHOUSE", C.CIVIC, points = 4, cost = [R.BRICK, R.BRICK, R.SILK], num_players = 3),
                Card("STATUE", C.CIVIC, points = 4, cost = [R.ORE, R.ORE, R.WOOD], coupon = ["THEATER"], num_players = 3),
                Card("AQUEDUCT", C.CIVIC, points = 5, cost = [R.STONE, R.STONE, R.STONE], num_players = 3),
                Card("STABLES", C.MILITARY, num_shields = 2, cost = [R.BRICK, R.WOOD, R.ORE], num_players = 3),
                Card("ARCHERY RANGE", C.MILITARY, num_shields = 2, cost = [R.WOOD, R.WOOD, R.ORE], num_players = 3),
                Card("WALLS", C.MILITARY, num_shields = 2, cost = [R.STONE, R.STONE, R.STONE], num_players = 3),
                Card("LIBRARY", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.STONE, R.STONE, R.SILK], num_players = 3),
                Card("LABRATORY", C.SCIENCE, provides_sciences = [S.COG], cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 3),
                Card("DISPENSARY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.ORE, R.ORE, R.GLASS], num_players = 3),
                Card("SCHOOL", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.WOOD, R.PAPYRUS], num_players = 3),

                Card("FOUNDRY", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,)], money_cost = 1, num_players = 4),
                Card("SAWMILL", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,)], money_cost = 1, num_players = 4),
                Card("BRICKYARD", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,)], money_cost = 1,num_players = 4),
                Card("QUARRY", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,)], money_cost = 1, num_players = 4),
                Card("BAZAR", C.COMMERCIAL, icon = TwoGoldForMfc(), num_players = 4),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 4),
                Card("DISPENSARY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.ORE, R.ORE, R.GLASS], num_players = 4),

                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 5),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 5),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 5),
                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], cost = [R.WOOD, R.WOOD], num_players = 4),
                Card("COURTHOUSE", C.CIVIC, points = 4, cost = [R.BRICK, R.BRICK, R.SILK], num_players = 5),
                Card("STABLES", C.MILITARY, num_shields = 2, cost = [R.BRICK, R.WOOD, R.ORE], num_players = 5),
                Card("LABRATORY", C.SCIENCE, provides_sciences = [S.COG], cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 5),

                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], cost = [R.WOOD, R.WOOD], num_players = 6),
                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], cost = [R.BRICK, R.BRICK], num_players = 6),
                Card("VINEYARD", C.COMMERCIAL, icon = OneGoldForRaw(), num_players = 6),
                Card("TEMPLE", C.CIVIC, points = 3, cost = [R.WOOD, R.BRICK, R.GLASS], coupon = ["ALTAR"], num_players = 6),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 6),
                Card("ARCHERY RANGE", C.MILITARY, num_shields = 2, cost = [R.WOOD, R.WOOD, R.ORE], num_players = 6),
                Card("LIBRARY", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.STONE, R.STONE, R.SILK], num_players = 6),

                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], cost = [R.BRICK, R.BRICK], num_players = 7),
                Card("BAZAR", C.COMMERCIAL, icon = TwoGoldForMfc(), num_players = 7),
                Card("STATUE", C.CIVIC, points = 4, cost = [R.ORE, R.ORE, R.WOOD], coupon = ["THEATER"], num_players = 7),
                Card("AQUEDUCT", C.CIVIC, points = 5, cost = [R.STONE, R.STONE, R.STONE], num_players = 7),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 7),
                Card("WALLS", C.MILITARY, num_shields = 2, cost = [R.STONE, R.STONE, R.STONE], num_players = 7),
                Card("SCHOOL", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.WOOD, R.PAPYRUS], num_players = 7)
                ]

        elif self.age == 3:
            deck = [ \
                Card("HAVEN", C.COMMERCIAL, icon = OneGoldPointForRaw(), cost = [R.WOOD, R.ORE, R.SILK], num_players = 3),
                Card("LIGHTHOUSE", C.COMMERCIAL, icon = OneGoldPointForCommercial(), cost = [R.STONE, R.GLASS], num_players = 3),
                Card("ARENA", C.COMMERCIAL, icon = ThreeGoldPointForWonder(), cost = [R.STONE, R.STONE, R.ORE], num_players = 3),
                Card("GARDENS", C.CIVIC, points = 5, cost = [R.BRICK, R.BRICK, R.WOOD], num_players = 3),
                Card("SENATE", C.CIVIC, points = 6, cost = [R.WOOD, R.WOOD, R.STONE, R.ORE], num_players = 3),
                Card("TOWN HALL", C.CIVIC, points = 6, cost = [R.STONE, R.STONE, R.ORE, R.GLASS], num_players = 3),
                Card("PANTHEON", C.CIVIC, points = 7, cost = [R.BRICK, R.BRICK, R.ORE, R.GLASS, R.PAPYRUS, R.SILK], num_players = 3),
                Card("PALACE", C.CIVIC, points = 8, cost = [R.STONE, R.ORE, R.WOOD, R.BRICK, R.GLASS, R.PAPYRUS, R.SILK], num_players = 3),
                Card("ARSENAL", C.MILITARY, num_shields = 3, cost = [R.WOOD, R.WOOD, R.ORE, R.SILK], num_players = 3),
                Card("SIEGE WORKSHOP", C.MILITARY, num_shields = 3, cost = [R.BRICK, R.BRICK, R.BRICK, R.WOOD], num_players = 3),
                Card("FORTIFICATIONS", C.MILITARY, num_shields = 3, cost = [R.ORE, R.ORE, R.ORE, R.STONE], num_players = 3),
                Card("UNIVERSITY", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.WOOD, R.WOOD, R.PAPYRUS, R.GLASS], num_players = 3),
                Card("LODGE", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.BRICK, R.BRICK, R.PAPYRUS, R.SILK], num_players = 3),
                Card("ACADEMY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.STONE, R.STONE, R.STONE, R.GLASS], num_players = 3),
                Card("OBSERVATORY", C.SCIENCE, provides_sciences = [S.COG], cost = [R.ORE, R.ORE, R.GLASS, R.SILK], num_players = 3),
                Card("STUDY", C.SCIENCE, provides_sciences = [S.COG], cost = [R.WOOD, R.PAPYRUS, R.SILK], num_players = 3),
                

            ]

        length_of_deck = len(deck)

        i = 0

        while i < length_of_deck:
            if deck[i].num_players > 3 and deck[i].num_players > NUM_PLAYERS:
                del deck[i]
                length_of_deck -= 1
            else:
                i += 1

        random.shuffle(deck)
        return deck

    # def create_deck(self):
    #     deck = [ \


    #     ]

        return deck

    def create_hands(self, deck):
        hands = []
        for i in range(NUM_PLAYERS):
            deck_len = len(deck)
            start = i * NUM_CARDS_PER_PLAYER
            end = (i + 1) * NUM_CARDS_PER_PLAYER
            hands.append(self.deck[start:end])
        return hands

    def next_age(self):
        print("next age!")
        self.age += 1
        self.deck = self.create_deck()
        self.hands = self.create_hands(self.deck)

    def assign_wonders(self):
        alexandria_card_list = [Card("Alexandria Start", C.WONDER_C, provides_resources = [(R.GLASS,)]), Card("Alexandria One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), Card("Alexandria Two", C.WONDER_C, provides_resources = [(R.BRICK, R.ORE, R.WOOD, R.STONE)], cost = [R.ORE, R.ORE]), Card("Alexandria Three", C.WONDER_C, points = 7, cost = [R.GLASS, R.GLASS])]

        Alexandria = Wonder("Alexandria", pg.image.load("Images/Alexandria.png"), alexandria_card_list)
        wonder_list = [Alexandria, Alexandria, Alexandria, Alexandria, Alexandria, Alexandria, Alexandria]
        random.shuffle(wonder_list)
        return wonder_list

class Player:
    def __init__(self, player_number, wonder):
        self.player_number = player_number
        self.wonder = wonder
        self.cards = []
        self.money = 13
        self.num_shields = 0
        self.wonder_level = 0
        self.bought_resources = []
        self.left_cost_m = 2
        self.left_cost_r = 2
        self.right_cost_m = 2
        self.right_cost_r = 2
        self.spent_money_l = 0
        self.spent_money_r = 0

    def give_moneys_for_discard(self):
        self.money += 3

    def play_card(self, selected_card):
        if self.can_play_card(selected_card):
            self.money -= selected_card.money_cost
            self.num_shields += selected_card.num_shields
            self.money += selected_card.provides_money
            self.cards.append(selected_card)
            return True
        else:
            return False

    def can_play_card(self, card):
        resource_tuples = self.available_resources_tuples(self.cards)

        if len(card.coupons) > 0:
            for coupon in card.coupons:
                for player_card in self.cards:
                    if player_card.name == coupon:
                        return True

        if self.has_resources_for_card(card.cost, resource_tuples) and self.money - self.spent_money_l - self.spent_money_r >= card.money_cost:
            return True
        else:
            return False

    def can_play_wonder(self):
        print(self.wonder_level)
        resource_tuples = self.available_resources_tuples(self.cards)
        card = self.wonder.layers_list[self.wonder_level + 1]

        if self.has_resources_for_card(card.cost, resource_tuples) and self.money - self.spent_money_l - self.spent_money_r >= card.money_cost:
            return True
        else:
            return False

    # def has_money_for_card(self, )

    def available_resources_tuples(self, cards):
        resource_tuples = []
        for card in cards:
            for resource_tuple in card.provides_resources:
                resource_tuples.append(resource_tuple)
        resource_tuples += self.bought_resources
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

class Card:
    def __init__(self, name, card_type, points = 0, provides_resources = [], cost = [], provides_sciences = [], provides_money = 0, icon = None, num_shields = 0, money_cost = 0, coupons = [], num_players = 3):
        self.cost = cost
        self.points = points
        self.card_type = card_type
        self.name = name
        self.provides_resources = provides_resources
        self.provides_sciences = provides_sciences
        self.num_shields = num_shields
        self.money_cost = money_cost
        self.provides_money = provides_money
        self.icon = icon
        self.coupons = coupons
        self.num_players = num_players

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}: Card Type: {}  Points = {}, Resources = {}, Science = {}, Shields = {}, Cost {}".format(
            self.name, self.card_type, self.points, self.provides_resources, self.provides_sciences, self.num_shields, self.cost)
    
class Wonder:
    def __init__(self, name, image, layers_list):
        self.name = name
        self.image = image
        self.layers_list = layers_list

# icon classes

# default discount is 827 by 299


class Icon():
    def __init__(self, image, size):
        self.image = image
        self.size = size

    def on_played(self, player, player_list):
        print("Error: on_played function not found")

    def left_right_players(self, player, player_list):
        player_index = player.player_number

        if player_index == 0:
            left_player = player_list[len(player_list) - 1]
        else:
            left_player = player_list[player_index - 1]

        if player_index == len(player_list) - 1:
            right_player = player_list[0]
        else:
            right_player = player_list[player_index + 1]

        return left_player, right_player

class DiscountIcon(Icon):
    def __init__(self, direction, type, new_cost, image, size):
        self.direction = direction
        self.new_cost = new_cost
        self.type = type
        super().__init__(image, size)

    def on_played(self, current_player, player_list):
        if self.direction == "left" or self.direction == "both":
            if self.type == "raw":
                current_player.left_cost_r = self.new_cost
            else:
                current_player.left_cost_m = self.new_cost
        if self.direction == "right" or self.direction == "both":
            if self.type == "raw":
                current_player.right_cost_r = self.new_cost
            else:
                current_player.right_cost_m = self.new_cost         

class LeftRawDiscount(DiscountIcon):
    def __init__(self):
        image = pg.image.load("Images/left_r_discount.png")
        super().__init__("left", "raw", 1, image, [100, 36])

class RightRawDiscount(DiscountIcon):
    def __init__(self):
        image = pg.image.load("Images/right_r_discount.png")
        super().__init__("right", "raw", 1, image, [100, 36])

class ManufactoredDiscount(DiscountIcon):
    def __init__(self):
        image = pg.image.load("Images/m_discount.png")
        super().__init__("both", "mfc", 1, image, [100, 36])


class StuffPerCard(Icon):
    def __init__(self, directions, card_type, provides, image, size):
        self.directions = directions
        self.card_type = card_type
        self.provides = provides
        super().__init__(image, size)

    def total_cards(self, cards_list):
        total = 0
        for card in cards_list:
            if card.card_type == self.card_type:
                total += 1
        return total

    def on_played(self, current_player, player_list):
        left_player, right_player = self.left_right_players(current_player, player_list)
        total = 0

        if "down" in self.directions:
            player = current_player
            total += self.total_cards(player.cards)

        if "left" in self.directions:
            total += self.total_cards(left_player.cards)

        if "right" in self.directions:
            total += self.total_cards(right_player.cards)

        current_player.money += total * self.provides[0]

        

class OneGoldForRaw(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_gold_for_raw.png")
        # 437 by 341
        super().__init__(["left", "right", "down"], C.RAW_R, [1, 0], image, [64, 50])

class TwoGoldForMfc(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/two_gold_for_mfc.png")
        super().__init__(["left", "right", "down"], C.MFG_R, [2, 0], image, [64, 50])

class OneGoldPointForRaw(StuffPerCard):
    def __init__(self):
        # 264 by 268
        image = pg.image.load("Images/one_gold_point_for_raw.png")
        super().__init__(["down"], C.RAW_R, [1, 1], image, [49, 50])

class OneGoldPointForCommercial(StuffPerCard):
    def __init__(self):
        # 264 by 268
        image = pg.image.load("Images/one_gold_point_for_commercial.png")
        super().__init__(["down"], C.COMMERCIAL, [1, 1], image, [49, 50])



class StuffForWonderStage(Icon):
    def __init__(self, directions, provides, image, size):
        self.directions = directions
        self.provides = provides
        self.image = image
        self.size = size

    def on_played(self, current_player, player_list):
        left_player, right_player = self.left_right_players
        total = 0

        if "left" in self.directions:
            total += left_player.wonder_level

        if "right" in self.directions:
            total += right_player.wonder_level

        if "down" in self.directions:
            total += current_player.wonder_level

        current_player.money += total * self.provides[0]

class ThreeGoldPointForWonder(StuffForWonderStage):
    def __init__(self):
        image = pg.image.load("Images/three_gold_point_for_wonder.png")
        # 337 by 246
        super().__init__(["down"], [3, 1], image, [69, 51])


