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
    WONDER_START = "Wonder Start"

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
        self.age = 1

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

    def score_player(self, player):
        print()
        print("calculating score")
        total_score = 0
        available_science = []
        science_tuples = []

        civic_points = 0
        icon_points = 0
        for card in player.cards:
            civic_points += card.points
            if card.icon:
                icon_points += card.icon.score(player, self.players)

            if card.provides_sciences:
                if len(card.provides_sciences) == 1:
                    available_science.append(card.provides_sciences[0])
                else:
                    science_tuples.append(card.provides_sciences[0])

        total_score += civic_points + icon_points

        print("civic gave", civic_points)
        print("icons gave", icon_points)

        war_points = 0
        for token in player.war_tokens:
            war_points += token

        total_score += war_points

        print("war gave", war_points)

        total_score += player.money // 3

        print("money gave", player.money // 3)

        totals_list = [0, 0, 0]
        for science in available_science:
            if science == S.COG:
                totals_list[0] += 1
            elif science == S.COMPASS:
                totals_list[1] += 1
            else:
                totals_list[2] += 1

        science_points = self.science_minimax(totals_list, science_tuples)
        total_score += science_points

        print("science gave", science_points)

        print("total:", total_score)

        return total_score

    def science_minimax(self, totals_list, science_tuples):
        if not science_tuples:
            return self.score_science(totals_list)

        else:
            best_option = None
            best_points = -1
            for option in science_tuples:
                if option == S.COG:
                    new_index = 0
                elif option == S.COMPASS:
                    new_index = 1
                else:
                    new_index = 2
    
                totals_list[new_index] += 1
                new_points = self.science_minimax(totals_list, science_tuples[1:])
                totals_list[new_index] -= 1

                if new_points > best_points:
                    best_points = new_points
                    best_option = option

            return best_points


    def score_science(self, totals_list):
        total_points = 0
        for total in totals_list:
            total_points += total ** 2

        total_points += min(totals_list) * 7

        return total_points


    def create_deck(self):
        if self.age == 1:
            deck = [ \
                Card("BATHS", C.CIVIC, points = 3, provides_coupons = ["AQUEDUCT"], cost = [R.STONE], num_players = 3),
                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 3),
                Card("CLAY PIT", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)], money_cost = 1, num_players = 3),
                Card("APOTHECARY", C.SCIENCE, provides_sciences = [S.COMPASS], provides_coupons = ["STABLES", "DISPENSARY"], cost = [R.SILK], num_players = 3),
                Card("SCRIPTORIUM", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.PAPYRUS], num_players = 3),
                Card("CLAY POOL", C.RAW_R, provides_resources = [(R.BRICK,)], num_players = 3),
                Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
                Card("ORE VEIN", C.RAW_R, provides_resources = [(R.ORE,)], num_players = 3),
                Card("EAST TRADING POST", C.COMMERCIAL, icon = RightRawDiscount(), provides_coupons = ["FORUM"], num_players = 3),
                Card("ALTAR", C.CIVIC, points = 2, provides_coupons = ["TEMPLE"], num_players = 3),
                Card("TIMBER YARD", C.RAW_R, provides_resources = [(R.STONE, R.WOOD)], money_cost = 1, num_players = 3),
                Card("GUARD TOWER", C.MILITARY, num_shields = 1, cost = [R.BRICK], num_players = 3),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 3),
                Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD], num_players = 3),
                Card("BARRACKS", C.MILITARY, num_shields = 1, cost = [R.ORE], num_players = 3),
                Card("WORKSHOP", C.SCIENCE, provides_sciences = [S.COG], provides_coupons = ["ARCHERY RANGE", "LABORATORY"], cost = [R.GLASS], num_players = 3),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 3),
                Card("STONE PIT", C.RAW_R, provides_resources = [(R.STONE,)], num_players = 3),
                Card("MARKETPLACE", C.COMMERCIAL, icon = ManufactoredDiscount(), provides_coupons = ["CARAVANSERY"], num_players = 3),
                Card("WEST TRADING POST", C.COMMERCIAL, icon = LeftRawDiscount(), provides_coupons = ["FORUM"], num_players = 3),
                Card("THEATER", C.CIVIC, points = 2, provides_coupons = ["STATUE"], num_players = 3),

                Card("THEATER", C.CIVIC, points = 2, provides_coupons = ["STATUE"], num_players = 4),
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
                Card("ALTAR", C.CIVIC, points = 2, provides_coupons = ["TEMPLE"], num_players = 5),
                Card("APOTHECARY", C.SCIENCE, provides_sciences = [S.COMPASS], provides_coupons = ["STABLES", "DISPENSARY"], cost = [R.SILK], num_players = 5),
                Card("FOREST CAVE", C.RAW_R, provides_resources = [(R.WOOD, R.ORE)], money_cost = 1, num_players = 5),

                Card("MARKETPLACE", C.COMMERCIAL, icon = ManufactoredDiscount(), provides_coupons = ["CARAVANSERY"], num_players = 6),
                Card("TREE FARM", C.RAW_R, provides_resources = [(R.WOOD, R.BRICK)], money_cost = 1, num_players = 6),
                Card("MINE", C.RAW_R, provides_resources = [(R.STONE, R.ORE)], money_cost = 1, num_players = 6),
                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 6),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 6),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 6),
                Card("THEATER", C.CIVIC, points = 2,  provides_coupons = ["STATUE"], num_players = 6),

                Card("EAST TRADING POST", C.COMMERCIAL, icon = RightRawDiscount(), provides_coupons = ["FORUM"], num_players = 7),
                Card("PAWNSHOP", C.CIVIC, points = 3, num_players = 7),
                Card("WORKSHOP", C.SCIENCE, provides_sciences = [S.COG], provides_coupons = ["ARCHERY RANGE", "LABORATORY"], cost = [R.GLASS], num_players = 7),
                Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 7),
                Card("WEST TRADING POST", C.COMMERCIAL, icon = LeftRawDiscount(), provides_coupons = ["FORUM"], num_players = 7),
                Card("BATHS", C.CIVIC, points = 3, provides_coupons = ["AQUEDUCT"], cost = [R.STONE], num_players = 7),  
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
                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], provides_coupons = ["LIGHT HOUSE"], cost = [R.WOOD, R.WOOD], num_players = 3),
                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], provides_coupons = ["HAVEN"], cost = [R.BRICK, R.BRICK], num_players = 3),
                Card("VINEYARD", C.COMMERCIAL, icon = OneGoldForRaw(), num_players = 3),
                Card("TEMPLE", C.CIVIC, points = 3, cost = [R.WOOD, R.BRICK, R.GLASS], provides_coupons = ["PANTHEON"], num_players = 3),
                Card("COURTHOUSE", C.CIVIC, points = 4, cost = [R.BRICK, R.BRICK, R.SILK], num_players = 3),
                Card("STATUE", C.CIVIC, points = 4, cost = [R.ORE, R.ORE, R.WOOD], provides_coupons = ["GARDENS"], num_players = 3),
                Card("AQUEDUCT", C.CIVIC, points = 5, cost = [R.STONE, R.STONE, R.STONE],num_players = 3),
                Card("STABLES", C.MILITARY, num_shields = 2, cost = [R.BRICK, R.WOOD, R.ORE], num_players = 3),
                Card("ARCHERY RANGE", C.MILITARY, num_shields = 2, cost = [R.WOOD, R.WOOD, R.ORE], num_players = 3),
                Card("WALLS", C.MILITARY, num_shields = 2, cost = [R.STONE, R.STONE, R.STONE], num_players = 3),
                Card("LIBRARY", C.SCIENCE, provides_sciences = [S.TABLET], provides_coupons = ["SENATE", "UNIVERSITY"], cost = [R.STONE, R.STONE, R.SILK], num_players = 3),
                Card("LABORATORY", C.SCIENCE, provides_sciences = [S.COG], provides_coupons = ["SIEGE WORKSHOP", "OBSERVATORY"], cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 3),
                Card("DISPENSARY", C.SCIENCE, provides_sciences = [S.COMPASS], provides_coupons = ["ARENA", "LODGE"], cost = [R.ORE, R.ORE, R.GLASS], num_players = 3),
                Card("SCHOOL", C.SCIENCE, provides_sciences = [S.TABLET], provides_coupons = ["ACADEMY", "STUDY"], cost = [R.WOOD, R.PAPYRUS], num_players = 3),

                Card("FOUNDRY", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,)], money_cost = 1, num_players = 4),
                Card("SAWMILL", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,)], money_cost = 1, num_players = 4),
                Card("BRICKYARD", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,)], money_cost = 1,num_players = 4),
                Card("QUARRY", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,)], money_cost = 1, num_players = 4),
                Card("BAZAR", C.COMMERCIAL, icon = TwoGoldForMfc(), num_players = 4),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 4),
                Card("DISPENSARY", C.SCIENCE, provides_sciences = [S.COMPASS], provides_coupons = ["ARENA", "LODGE"], cost = [R.ORE, R.ORE, R.GLASS], num_players = 4),

                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 5),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 5),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 5),
                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], provides_coupons = ["LIGHT HOUSE"], cost = [R.WOOD, R.WOOD], num_players = 4),
                Card("COURTHOUSE", C.CIVIC, points = 4, cost = [R.BRICK, R.BRICK, R.SILK], num_players = 5),
                Card("STABLES", C.MILITARY, num_shields = 2, cost = [R.BRICK, R.WOOD, R.ORE], num_players = 5),
                Card("LABORATORY", C.SCIENCE, provides_sciences = [S.COG], provides_coupons = ["SIEGE WORKSHOP", "OBSERVATORY"], cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 5),

                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], provides_coupons = ["LIGHT HOUSE"], cost = [R.WOOD, R.WOOD], num_players = 6),
                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], provides_coupons = ["HAVEN"], cost = [R.BRICK, R.BRICK], num_players = 6),
                Card("VINEYARD", C.COMMERCIAL, icon = OneGoldForRaw(), num_players = 6),
                Card("TEMPLE", C.CIVIC, points = 3, cost = [R.WOOD, R.BRICK, R.GLASS], provides_coupons = ["PANTHEON"], num_players = 6),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 6),
                Card("ARCHERY RANGE", C.MILITARY, num_shields = 2, cost = [R.WOOD, R.WOOD, R.ORE], num_players = 6),
                Card("LIBRARY", C.SCIENCE, provides_sciences = [S.TABLET], provides_coupons = ["SENATE", "UNIVERSITY"], cost = [R.STONE, R.STONE, R.SILK], num_players = 6),

                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], provides_coupons = ["HAVEN"], cost = [R.BRICK, R.BRICK], num_players = 7),
                Card("BAZAR", C.COMMERCIAL, icon = TwoGoldForMfc(), num_players = 7),
                Card("STATUE", C.CIVIC, points = 4, cost = [R.ORE, R.ORE, R.WOOD], provides_coupons = ["GARDENS"], num_players = 7),
                Card("AQUEDUCT", C.CIVIC, points = 5, cost = [R.STONE, R.STONE, R.STONE], num_players = 7),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 7),
                Card("WALLS", C.MILITARY, num_shields = 2, cost = [R.STONE, R.STONE, R.STONE], num_players = 7),
                Card("SCHOOL", C.SCIENCE, provides_sciences = [S.TABLET], provides_coupons = ["ACADEMY", "STUDY"], cost = [R.WOOD, R.PAPYRUS], num_players = 7)
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
                
                Card("HAVEN", C.COMMERCIAL, icon = OneGoldPointForRaw(), cost = [R.WOOD, R.ORE, R.SILK], num_players = 4),
                Card("COMMERCE CHAMBER", C.COMMERCIAL, icon = TwoPointForMfc(), cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 4),
                Card("GARDENS", C.CIVIC, points = 5, cost = [R.BRICK, R.BRICK, R.WOOD], num_players = 4),
                Card("ARSENAL", C.MILITARY, num_shields = 3, cost = [R.WOOD, R.WOOD, R.ORE, R.SILK], num_players = 4),
                Card("CIRCUS", C.MILITARY, num_shields = 3, cost = [R.STONE, R.STONE, R.STONE, R.ORE], num_players = 4),
                Card("UNIVERSITY", C.SCIENCE, provides_sciences = [S.TABLET], cost = [R.WOOD, R.WOOD, R.PAPYRUS, R.GLASS], num_players = 4),

                Card("ARENA", C.COMMERCIAL, icon = ThreeGoldPointForWonder(), cost = [R.STONE, R.STONE, R.ORE], num_players = 5),
                Card("SENATE", C.CIVIC, points = 6, cost = [R.WOOD, R.WOOD, R.STONE, R.ORE], num_players = 5),
                Card("TOWN HALL", C.CIVIC, points = 6, cost = [R.STONE, R.STONE, R.ORE, R.GLASS], num_players = 5),
                Card("SIEGE WORKSHOP", C.MILITARY, num_shields = 3, cost = [R.BRICK, R.BRICK, R.BRICK, R.WOOD], num_players = 5),
                Card("CIRCUS", C.MILITARY, num_shields = 3, cost = [R.STONE, R.STONE, R.STONE, R.ORE], num_players = 5),
                Card("STUDY", C.SCIENCE, provides_sciences = [S.COG], cost = [R.WOOD, R.PAPYRUS, R.SILK], num_players = 5),

                Card("COMMERCE CHAMBER", C.COMMERCIAL, icon = TwoPointForMfc(), cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 6),
                Card("LIGHTHOUSE", C.COMMERCIAL, icon = OneGoldPointForCommercial(), cost = [R.STONE, R.GLASS], num_players = 6),
                Card("TOWN HALL", C.CIVIC, points = 6, cost = [R.STONE, R.STONE, R.ORE, R.GLASS], num_players = 6),
                Card("PANTHEON", C.CIVIC, points = 7, cost = [R.BRICK, R.BRICK, R.ORE, R.GLASS, R.PAPYRUS, R.SILK], num_players = 6),
                Card("CIRCUS", C.MILITARY, num_shields = 3, cost = [R.STONE, R.STONE, R.STONE, R.ORE], num_players = 6),
                Card("LODGE", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.BRICK, R.BRICK, R.PAPYRUS, R.SILK], num_players = 6),

                Card("ARENA", C.COMMERCIAL, icon = ThreeGoldPointForWonder(), cost = [R.STONE, R.STONE, R.ORE], num_players = 7),
                Card("PALACE", C.CIVIC, points = 8, cost = [R.STONE, R.ORE, R.WOOD, R.BRICK, R.GLASS, R.PAPYRUS, R.SILK], num_players = 7),
                Card("FORTIFICATIONS", C.MILITARY, num_shields = 3, cost = [R.ORE, R.ORE, R.ORE, R.STONE], num_players = 7),
                Card("ARSENAL", C.MILITARY, num_shields = 3, cost = [R.WOOD, R.WOOD, R.ORE, R.SILK], num_players = 7),
                Card("ACADEMY", C.SCIENCE, provides_sciences = [S.COMPASS], cost = [R.STONE, R.STONE, R.STONE, R.GLASS], num_players = 7),
                Card("OBSERVATORY", C.SCIENCE, provides_sciences = [S.COG], cost = [R.ORE, R.ORE, R.GLASS, R.SILK], num_players = 7),
            ]

            guild_list = [ \
                Card("Workers Guild", C.GUILD, icon = PointForRaw(), cost = [R.ORE, R.ORE, R.BRICK, R.STONE, R.WOOD]),
                Card("Craftmens Guild", C.GUILD, icon = TwoPointForMfc(), cost = [R.ORE, R.ORE, R.STONE, R.STONE]),
                Card("Traders Guild", C.GUILD, icon = OnePointForCommercial(), cost = [R.GLASS, R.SILK, R.PAPYRUS]),
                Card("Magistrates Guild", C.GUILD, icon = OnePointForCivic(), cost = [R.WOOD, R.WOOD, R.WOOD, R.STONE, R.SILK]),
                Card("Spies Guild", C.GUILD, icon = OnePointForMilitary(), cost = [R.BRICK, R.BRICK, R.BRICK, R.GLASS]),
                Card("Philosophers Guild", C.GUILD, icon = OnePointForScience(), cost = [R.BRICK, R.BRICK, R.BRICK, R.PAPYRUS, R.SILK]),
                Card("Shipowners Guild", C.GUILD, icon = PointForRawMfcGuild(), cost = [R.WOOD, R.WOOD, R.WOOD, R.GLASS, R.PAPYRUS]),
                Card("Strategists Guild", C.GUILD, icon = LeftRightPointForMinusTokens(), cost = [R.ORE, R.ORE, R.STONE, R.SILK]),
                Card("Builder's Guild", C.GUILD, icon = PointForWonder(), cost = [R.STONE, R.STONE, R.BRICK, R.BRICK, R.GLASS]),
                ]

        length_of_deck = len(deck)

        i = 0

        while i < length_of_deck:
            if deck[i].num_players > 3 and deck[i].num_players > NUM_PLAYERS:
                del deck[i]
                length_of_deck -= 1
            else:
                i += 1

        if self.age == 3:
            random.shuffle(guild_list)
            for i in range(NUM_PLAYERS + 2):
                deck.append(guild_list[i])

        random.shuffle(deck)
        return deck

    # def create_deck(self):
    #     deck = [ \
    #         Card("Glass 6", C.RAW_R, provides_resources=[(R.BRICK,)], cost = [R.GLASS, R.GLASS, R.GLASS, R.GLASS, R.GLASS, R.GLASS]),
    #         Card("Glass 3", C.RAW_R, provides_resources=[(R.BRICK,)], cost = [R.GLASS, R.GLASS, R.GLASS]),
    #         Card("Glass 2", C.RAW_R, provides_resources=[(R.BRICK,)], cost = [R.GLASS, R.GLASS]),
    #         Card("Glass 1", C.RAW_R, provides_resources=[(R.BRICK,)], cost = [R.GLASS]),
    #         Card("Brick 3", C.MFG_R, provides_resources=[(R.GLASS,)], cost = [R.BRICK, R.BRICK, R.BRICK]),
    #         Card("Brick 2", C.MFG_R, provides_resources=[(R.GLASS,)], cost = [R.BRICK, R.BRICK]),
    #         Card("Brick 1", C.MFG_R, provides_resources=[(R.GLASS,)], cost = [R.BRICK]),
    #     ]

    #     return deck

    # def create_deck(self):
    #     deck = [ \
    #         Card("EAST TRADING POST", C.COMMERCIAL, icon = RightRawDiscount(), provides_coupons = ["FORUM"], num_players = 3),
    #         Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
    #         Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
    #         Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
    #         Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 3),
    #         Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 3),
    #         Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 3),
    #         ]

    #     return deck

    # def create_deck(self):
    #     deck = [ \
    #         Card("Workers Guild", C.GUILD, icon = PointForRaw(), cost = [R.ORE, R.ORE, R.BRICK, R.STONE, R.WOOD]),
    #         Card("Workers Guild", C.GUILD, icon = PointForRaw(), cost = []),
    #         Card("Craftmens Guild", C.GUILD, icon = TwoPointForMfc(), cost = [R.ORE, R.ORE, R.STONE, R.STONE]),
    #         Card("Traders Guild", C.GUILD, icon = OnePointForCommercial(), cost = [R.GLASS, R.SILK, R.PAPYRUS]),
    #         Card("Magistrates Guild", C.GUILD, icon = OnePointForCivic(), cost = [R.WOOD, R.WOOD, R.WOOD, R.STONE, R.SILK]),
    #         Card("Spies Guild", C.GUILD, icon = OnePointForMilitary(), cost = [R.BRICK, R.BRICK, R.BRICK, R.GLASS]),
    #         Card("Philosophers Guild", C.GUILD, icon = OnePointForScience(), cost = [R.BRICK, R.BRICK, R.BRICK, R.PAPYRUS, R.SILK]),
    #         Card("Shipowners Guild", C.GUILD, icon = PointForRawMfcGuild(), cost = [R.WOOD, R.WOOD, R.WOOD, R.GLASS, R.PAPYRUS]),
    #         Card("Strategists Guild", C.GUILD, icon = LeftRightPointForMinusTokens(), cost = [R.ORE, R.ORE, R.STONE, R.SILK]),
    #         Card("Builder's Guild", C.GUILD, icon = PointForWonder(), cost = [R.STONE, R.STONE, R.BRICK, R.BRICK, R.GLASS]),
    #         ]

    #     return deck

    def create_hands(self, deck):
        hands = []
        for i in range(NUM_PLAYERS):
            start = i * NUM_CARDS_PER_PLAYER
            end = (i + 1) * NUM_CARDS_PER_PLAYER
            hands.append(deck[start:end])
        return hands

    def next_age(self):
        print("next age!")
        self.war()
        self.age += 1
        self.deck = self.create_deck()
        self.hands = self.create_hands(self.deck)

        for player in self.players:
            player.current_score = self.score_player(player)

    def assign_wonders(self):
        alexandria_card_list = [Card("Alexandria Start", C.WONDER_START, provides_resources = [(R.GLASS,)]), Card("Alexandria One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), Card("Alexandria Two", C.WONDER_C, provides_resources = [(R.BRICK, R.ORE, R.WOOD, R.STONE)], cost = [R.ORE, R.ORE]), Card("Alexandria Three", C.WONDER_C, points = 7, cost = [R.GLASS, R.GLASS])]

        Alexandria = Wonder("Alexandria", pg.image.load("Images/Alexandria.png"), alexandria_card_list)
        wonder_list = [Alexandria, Alexandria, Alexandria, Alexandria, Alexandria, Alexandria, Alexandria]
        random.shuffle(wonder_list)
        return wonder_list

    def left_right_players(self, player):
        player_index = player.player_number

        if player_index == 0:
            left_player = self.players[len(self.players) - 1]
        else:
            left_player = self.players[player_index - 1]

        if player_index == len(self.players) - 1:
            right_player = self.players[0]
        else:
            right_player = self.players[player_index + 1]

        return left_player, right_player

    def war(self):
        for player in self.players:
            left_player, right_player = self.left_right_players(player)
            wins = 0
            if left_player.num_shields > player.num_shields:
                player.war_tokens.append(-1)
            elif left_player.num_shields < player.num_shields:
                wins += 1

            if right_player.num_shields > player.num_shields:
                player.war_tokens.append(-1)
            elif right_player.num_shields < player.num_shields:
                wins += 1

            for i in range(wins):
                if self.age == 1:
                    player.war_tokens.append(1)
                elif self.age == 2:
                    player.war_tokens.append(3)
                else:
                    player.war_tokens.append(5)

                

class Player:
    def __init__(self, player_number, wonder):
        self.player_number = player_number
        self.wonder = wonder
        self.cards = []
        self.money = 3
        self.num_shields = 0
        self.wonder_level = 0
        self.bought_resources = []
        self.left_cost_m = 2
        self.left_cost_r = 2
        self.right_cost_m = 2
        self.right_cost_r = 2
        self.spent_money_l = 0
        self.spent_money_r = 0
        self.war_tokens = []
        self.current_score = 1

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
        # if card.name == "Glass 3":
        #     print("checking 3")
        # if card.name == "Glass 2":
        #     print("checking 2")
        resource_tuples = self.available_resources_tuples(self.cards)

        for player_card in self.cards:
            for coupon in player_card.provides_coupons:
                if coupon == card.name:
                    return True

        if self.has_resources_for_card(card.cost, resource_tuples) and self.money - self.spent_money_l - self.spent_money_r >= card.money_cost:
            return True
        else:
            return False

    def can_play_wonder(self):
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
        for resource in self.bought_resources:
            resource_tuples.append((resource[1],))
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
    def __init__(self, name, card_type, points = 0, provides_resources = [], cost = [], provides_sciences = [], provides_money = 0, icon = None, num_shields = 0, money_cost = 0, provides_coupons = [], num_players = 3):
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
        self.provides_coupons = provides_coupons
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
        return

    def score(self, player, player_list):
        return 0

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

    def score(self, current_player, player_list):
        left_player, right_player = self.left_right_players(current_player, player_list)
        total = 0

        if "down" in self.directions:
            player = current_player
            total += self.total_cards(player.cards)

        if "left" in self.directions:
            total += self.total_cards(left_player.cards)

        if "right" in self.directions:
            total += self.total_cards(right_player.cards)

        print("icon score provided", total * self.provides[1])
        return total * self.provides[1]

        

class OneGoldForRaw(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_gold_for_raw.png")
        # 437 by 341
        super().__init__(["left", "right", "down"], C.RAW_R, [1, 0], image, [64, 50])

class TwoGoldForMfc(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/two_gold_for_mfc.png")
        super().__init__(["left", "right", "down"], C.MFG_R, [2, 0], image, [64, 50])

class TwoGoldPointForMfc(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/two_gold_point_for_mfc.png")
        super().__init__(["down"], C.MFG_R, [2, 2], image, [49, 50])

# guilds - 390 by 215

class PointForRaw(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_point_for_raw.png")
        super().__init__(["left", "right"], C.RAW_R, [0, 1], image, [91, 50])

class TwoPointForMfc(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/two_point_for_mfc.png")
        super().__init__(["left", "right"], C.MFG_R, [0, 2], image, [91, 50])

class OnePointForCommercial(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_point_for_commercial.png")
        super().__init__(["left", "right"], C.COMMERCIAL, [0, 1], image, [91, 50])

class OnePointForCivic(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_point_for_civic.png")
        super().__init__(["left", "right"], C.CIVIC, [0, 1], image, [91, 50])

class OnePointForMilitary(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_point_for_military.png")
        super().__init__(["left", "right"], C.MILITARY, [0, 1], image, [91, 50])

class OnePointForScience(StuffPerCard):
    def __init__(self):
        image = pg.image.load("Images/one_point_for_science.png")
        super().__init__(["left", "right"], C.SCIENCE, [0, 1], image, [91, 50])



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

class PointForRawMfcGuild(Icon):
    def __init__(self):
        # 521 by 214
        image = pg.image.load("Images/point_for_raw_mfc_guild.png")
        super().__init__(image, [98, 40])

    def score(self, player, player_list):
        total = 0
        for card in player.cards:
            if card.card_type == C.RAW_R or card.card_type == C.MFG_R or card.card_type == C.GUILD:
                total += 1

        return total


class StuffForWonderStage(Icon):
    def __init__(self, directions, provides, image, size):
        self.directions = directions
        self.provides = provides
        super().__init__(image, size)

    def on_played(self, current_player, player_list):
        left_player, right_player = self.left_right_players(current_player, player_list)
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

class PointForWonder(StuffForWonderStage):
    def __init__(self):
        image = pg.image.load("Images/point_for_wonder.png")
        # 222 by 148
        super().__init__(["left", "right", "down"], [3, 1], image, [80, 53])


class StuffForMilitaryTokens(Icon):
    def __init__(self, directions, provides, token_type, image, size):
        self.directions = directions
        self.provides = provides
        self.token_type = token_type
        super().__init__(image, size)

    def score(self, player, player_list):
        left_player, right_player = self.left_right_players(player, player_list)
        total = 0
        if "left" in self.directions:
            for token in left_player.war_tokens:
                if token == self.token_type:
                    total += 1
        if "right" in self.directions:
            for token in right_player.war_tokens:
                if token == self.token_type:
                    total += 1
        if "down" in self.directions:
            if token == self.token_type:
                total += 1

        return total * self.provides[1]

class LeftRightPointForMinusTokens(StuffForMilitaryTokens):
    def __init__(self):
        # 435 by 241
        image = pg.image.load("Images/left_right_point_for_minus_tokens.png")
        super().__init__(["left", "right"], [0, 1], -1, image, [81, 45])

