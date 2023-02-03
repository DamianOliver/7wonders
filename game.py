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

NUM_PLAYERS = 6
NUM_BOTS = NUM_PLAYERS
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
        print("initiallizing game")
        self.turn = 0
        self.current_player_index = 0
        self.age = 1    
        self.players = []
        
        for i in range(NUM_PLAYERS):
            if i < NUM_BOTS:
                self.players.append(Player(i, True))
            else:
                self.players.append(Player(i, False))

        self.assign_wonders(self.create_wonder_list())
        for player in self.players:
            player.play_card(player.wonder.layers_list[0])

        self.hands = []
        self.deck = self.create_deck()
        self.hands = self.create_hands(self.deck)

    def current_player_finished(self):
        # there is a PURELY GRAPHICAL glitch where a highlighted bought resource remains highlighted after the first card has been bought when playing the last two cards. maybe fix that some day
        if len(self.current_player_hand()) == 1 and self.current_player().play_last_card:
            return
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
        # print()
        # print("calculating score")
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
                if len(card.provides_sciences[0]) == 1:
                    available_science.append(card.provides_sciences[0])
                else:
                    science_tuples.append(card.provides_sciences[0])

        total_score += civic_points + icon_points

        # print("civic gave", civic_points)
        # print("icons gave", icon_points)

        war_points = 0
        for token in player.war_tokens:
            war_points += token

        total_score += war_points

        # print("war gave", war_points)

        total_score += player.money // 3

        # print("money gave", player.money // 3)

        totals_list = [0, 0, 0]
        for science in available_science:
            if science[0] == S.COG:
                totals_list[0] += 1
            elif science[0] == S.COMPASS:
                totals_list[1] += 1
            elif science[0] == S.TABLET:
                totals_list[2] += 1
            else:
                print("Error: unknown science symbol - could not calculate total")

        science_points = self.science_minimax(totals_list, science_tuples)
        total_score += science_points

        # print("science gave", science_points)

        # print("total:", total_score)

        return total_score

    # TODO - move this out of game class to pure function
    def science_minimax(self, totals_list, science_tuples):
        if not science_tuples:
            return self.score_science(totals_list)

        else:
            best_option = None
            best_points = -1
            for option in science_tuples[0]:
                if option == S.COG:
                    new_index = 0
                elif option == S.COMPASS:
                    new_index = 1
                elif option == S.TABLET:
                    new_index = 2
                else:
                    print("Error: unknown science symbol - could not find index")
    
                totals_list[new_index] += 1
                new_points = self.science_minimax(totals_list, science_tuples[1:])
                totals_list[new_index] -= 1

                if new_points > best_points:
                    best_points = new_points
                    best_option = option

            # print("using", best_option, "-", best_points)
            return best_points


    def score_science(self, totals_list):
        total_points = 0
        for total in totals_list:
            total_points += total ** 2

        total_points += min(totals_list) * 7

        # print("[Cog, Compass, Tablet]")
        # print("total of", total_points, "with", totals_list)

        return total_points


    def create_deck(self):
        if self.age == 1:
            deck = [
                Card("BATHS", C.CIVIC, points = 3, provides_coupons = ["AQUEDUCT"], cost = [R.STONE], num_players = 3),
                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 3),
                Card("CLAY PIT", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)], money_cost = 1, num_players = 3),
                Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [R.SILK], num_players = 3),
                Card("SCRIPTORIUM", C.SCIENCE, provides_sciences = [(S.TABLET,)], provides_coupons = ["COURTHOUSE", "LIBRARY"], cost = [R.PAPYRUS], num_players = 3),
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
                Card("WORKSHOP", C.SCIENCE, provides_sciences = [(S.COG,)], provides_coupons = ["ARCHERY RANGE", "LABORATORY"], cost = [R.GLASS], num_players = 3),
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
                Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [R.SILK], num_players = 5),
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
                Card("WORKSHOP", C.SCIENCE, provides_sciences = [(S.COG,)], provides_coupons = ["ARCHERY RANGE", "LABORATORY"], cost = [R.GLASS], num_players = 7),
                Card("TAVERN", C.COMMERCIAL, provides_money = 5, num_players = 7),
                Card("WEST TRADING POST", C.COMMERCIAL, icon = LeftRawDiscount(), provides_coupons = ["FORUM"], num_players = 7),
                Card("BATHS", C.CIVIC, points = 3, provides_coupons = ["AQUEDUCT"], cost = [R.STONE], num_players = 7),  
                Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD], num_players = 7)
                ]

        elif self.age == 2:
            deck = [
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
                Card("LIBRARY", C.SCIENCE, provides_sciences = [(S.TABLET,)], provides_coupons = ["SENATE", "UNIVERSITY"], cost = [R.STONE, R.STONE, R.SILK], num_players = 3),
                Card("LABORATORY", C.SCIENCE, provides_sciences = [(S.COG,)], provides_coupons = ["SIEGE WORKSHOP", "OBSERVATORY"], cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 3),
                Card("DISPENSARY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], provides_coupons = ["ARENA", "LODGE"], cost = [R.ORE, R.ORE, R.GLASS], num_players = 3),
                Card("SCHOOL", C.SCIENCE, provides_sciences = [(S.TABLET,)], provides_coupons = ["ACADEMY", "STUDY"], cost = [R.WOOD, R.PAPYRUS], num_players = 3),

                Card("FOUNDRY", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,)], money_cost = 1, num_players = 4),
                Card("SAWMILL", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,)], money_cost = 1, num_players = 4),
                Card("BRICKYARD", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,)], money_cost = 1,num_players = 4),
                Card("QUARRY", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,)], money_cost = 1, num_players = 4),
                Card("BAZAR", C.COMMERCIAL, icon = TwoGoldForMfc(), num_players = 4),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 4),
                Card("DISPENSARY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], provides_coupons = ["ARENA", "LODGE"], cost = [R.ORE, R.ORE, R.GLASS], num_players = 4),

                Card("GLASSWORKS", C.MFG_R, provides_resources = [(R.GLASS,)], num_players = 5),
                Card("PRESS", C.MFG_R, provides_resources = [(R.PAPYRUS,)], num_players = 5),
                Card("LOOM", C.MFG_R, provides_resources = [(R.SILK,)], num_players = 5),
                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], provides_coupons = ["LIGHT HOUSE"], cost = [R.WOOD, R.WOOD], num_players = 4),
                Card("COURTHOUSE", C.CIVIC, points = 4, cost = [R.BRICK, R.BRICK, R.SILK], num_players = 5),
                Card("STABLES", C.MILITARY, num_shields = 2, cost = [R.BRICK, R.WOOD, R.ORE], num_players = 5),
                Card("LABORATORY", C.SCIENCE, provides_sciences = [(S.COG,)], provides_coupons = ["SIEGE WORKSHOP", "OBSERVATORY"], cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 5),

                Card("CARAVANSERY", C.COMMERCIAL, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], provides_coupons = ["LIGHT HOUSE"], cost = [R.WOOD, R.WOOD], num_players = 6),
                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], provides_coupons = ["HAVEN"], cost = [R.BRICK, R.BRICK], num_players = 6),
                Card("VINEYARD", C.COMMERCIAL, icon = OneGoldForRaw(), num_players = 6),
                Card("TEMPLE", C.CIVIC, points = 3, cost = [R.WOOD, R.BRICK, R.GLASS], provides_coupons = ["PANTHEON"], num_players = 6),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 6),
                Card("ARCHERY RANGE", C.MILITARY, num_shields = 2, cost = [R.WOOD, R.WOOD, R.ORE], num_players = 6),
                Card("LIBRARY", C.SCIENCE, provides_sciences = [(S.TABLET,)], provides_coupons = ["SENATE", "UNIVERSITY"], cost = [R.STONE, R.STONE, R.SILK], num_players = 6),

                Card("FORUM", C.COMMERCIAL, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], provides_coupons = ["HAVEN"], cost = [R.BRICK, R.BRICK], num_players = 7),
                Card("BAZAR", C.COMMERCIAL, icon = TwoGoldForMfc(), num_players = 7),
                Card("STATUE", C.CIVIC, points = 4, cost = [R.ORE, R.ORE, R.WOOD], provides_coupons = ["GARDENS"], num_players = 7),
                Card("AQUEDUCT", C.CIVIC, points = 5, cost = [R.STONE, R.STONE, R.STONE], num_players = 7),
                Card("TRAINING GROUND", C.MILITARY, num_shields = 2, cost = [R.ORE, R.ORE, R.WOOD], num_players = 7),
                Card("WALLS", C.MILITARY, num_shields = 2, cost = [R.STONE, R.STONE, R.STONE], num_players = 7),
                Card("SCHOOL", C.SCIENCE, provides_sciences = [(S.TABLET,)], provides_coupons = ["ACADEMY", "STUDY"], cost = [R.WOOD, R.PAPYRUS], num_players = 7)
                ]

        elif self.age == 3:
            deck = [
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
                Card("UNIVERSITY", C.SCIENCE, provides_sciences = [(S.TABLET,)], cost = [R.WOOD, R.WOOD, R.PAPYRUS, R.GLASS], num_players = 3),
                Card("LODGE", C.SCIENCE, provides_sciences = [(S.COMPASS,)], cost = [R.BRICK, R.BRICK, R.PAPYRUS, R.SILK], num_players = 3),
                Card("ACADEMY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], cost = [R.STONE, R.STONE, R.STONE, R.GLASS], num_players = 3),
                Card("OBSERVATORY", C.SCIENCE, provides_sciences = [(S.COG,)], cost = [R.ORE, R.ORE, R.GLASS, R.SILK], num_players = 3),
                Card("STUDY", C.SCIENCE, provides_sciences = [(S.COG,)], cost = [R.WOOD, R.PAPYRUS, R.SILK], num_players = 3),
                
                Card("HAVEN", C.COMMERCIAL, icon = OneGoldPointForRaw(), cost = [R.WOOD, R.ORE, R.SILK], num_players = 4),
                Card("COMMERCE CHAMBER", C.COMMERCIAL, icon = TwoPointForMfc(), cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 4),
                Card("GARDENS", C.CIVIC, points = 5, cost = [R.BRICK, R.BRICK, R.WOOD], num_players = 4),
                Card("ARSENAL", C.MILITARY, num_shields = 3, cost = [R.WOOD, R.WOOD, R.ORE, R.SILK], num_players = 4),
                Card("CIRCUS", C.MILITARY, num_shields = 3, cost = [R.STONE, R.STONE, R.STONE, R.ORE], num_players = 4),
                Card("UNIVERSITY", C.SCIENCE, provides_sciences = [(S.TABLET,)], cost = [R.WOOD, R.WOOD, R.PAPYRUS, R.GLASS], num_players = 4),

                Card("ARENA", C.COMMERCIAL, icon = ThreeGoldPointForWonder(), cost = [R.STONE, R.STONE, R.ORE], num_players = 5),
                Card("SENATE", C.CIVIC, points = 6, cost = [R.WOOD, R.WOOD, R.STONE, R.ORE], num_players = 5),
                Card("TOWN HALL", C.CIVIC, points = 6, cost = [R.STONE, R.STONE, R.ORE, R.GLASS], num_players = 5),
                Card("SIEGE WORKSHOP", C.MILITARY, num_shields = 3, cost = [R.BRICK, R.BRICK, R.BRICK, R.WOOD], num_players = 5),
                Card("CIRCUS", C.MILITARY, num_shields = 3, cost = [R.STONE, R.STONE, R.STONE, R.ORE], num_players = 5),
                Card("STUDY", C.SCIENCE, provides_sciences = [(S.COG,)], cost = [R.WOOD, R.PAPYRUS, R.SILK], num_players = 5),

                Card("COMMERCE CHAMBER", C.COMMERCIAL, icon = TwoPointForMfc(), cost = [R.BRICK, R.BRICK, R.PAPYRUS], num_players = 6),
                Card("LIGHTHOUSE", C.COMMERCIAL, icon = OneGoldPointForCommercial(), cost = [R.STONE, R.GLASS], num_players = 6),
                Card("TOWN HALL", C.CIVIC, points = 6, cost = [R.STONE, R.STONE, R.ORE, R.GLASS], num_players = 6),
                Card("PANTHEON", C.CIVIC, points = 7, cost = [R.BRICK, R.BRICK, R.ORE, R.GLASS, R.PAPYRUS, R.SILK], num_players = 6),
                Card("CIRCUS", C.MILITARY, num_shields = 3, cost = [R.STONE, R.STONE, R.STONE, R.ORE], num_players = 6),
                Card("LODGE", C.SCIENCE, provides_sciences = [(S.COMPASS,)], cost = [R.BRICK, R.BRICK, R.PAPYRUS, R.SILK], num_players = 6),

                Card("ARENA", C.COMMERCIAL, icon = ThreeGoldPointForWonder(), cost = [R.STONE, R.STONE, R.ORE], num_players = 7),
                Card("PALACE", C.CIVIC, points = 8, cost = [R.STONE, R.ORE, R.WOOD, R.BRICK, R.GLASS, R.PAPYRUS, R.SILK], num_players = 7),
                Card("FORTIFICATIONS", C.MILITARY, num_shields = 3, cost = [R.ORE, R.ORE, R.ORE, R.STONE], num_players = 7),
                Card("ARSENAL", C.MILITARY, num_shields = 3, cost = [R.WOOD, R.WOOD, R.ORE, R.SILK], num_players = 7),
                Card("ACADEMY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], cost = [R.STONE, R.STONE, R.STONE, R.GLASS], num_players = 7),
                Card("OBSERVATORY", C.SCIENCE, provides_sciences = [(S.COG,)], cost = [R.ORE, R.ORE, R.GLASS, R.SILK], num_players = 7),
            ]

            guild_list = [
                Card("Workers Guild", C.GUILD, icon = PointForRaw(), cost = [R.ORE, R.ORE, R.BRICK, R.STONE, R.WOOD]),
                Card("Craftmens Guild", C.GUILD, icon = TwoPointForMfc(), cost = [R.ORE, R.ORE, R.STONE, R.STONE]),
                Card("Traders Guild", C.GUILD, icon = OnePointForCommercial(), cost = [R.GLASS, R.SILK, R.PAPYRUS]),
                Card("Magistrates Guild", C.GUILD, icon = OnePointForCivic(), cost = [R.WOOD, R.WOOD, R.WOOD, R.STONE, R.SILK]),
                Card("Spies Guild", C.GUILD, icon = OnePointForMilitary(), cost = [R.BRICK, R.BRICK, R.BRICK, R.GLASS]),
                Card("Philosophers Guild", C.GUILD, icon = OnePointForScience(), cost = [R.BRICK, R.BRICK, R.BRICK, R.PAPYRUS, R.SILK]),
                Card("Shipowners Guild", C.GUILD, icon = PointForRawMfcGuild(), cost = [R.WOOD, R.WOOD, R.WOOD, R.GLASS, R.PAPYRUS]),
                Card("Strategists Guild", C.GUILD, icon = LeftRightPointForMinusTokens(), cost = [R.ORE, R.ORE, R.STONE, R.SILK]),
                Card("Builder's Guild", C.GUILD, icon = PointForWonder(), cost = [R.STONE, R.STONE, R.BRICK, R.BRICK, R.GLASS]),
                Card("Scientists Guild", C.GUILD, icon = ScienceOptions(), provides_sciences = [(S.TABLET, S.COG, S.COMPASS)], cost = [R.WOOD, R.WOOD, R.ORE, R.ORE, R.PAPYRUS]),
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


# Commented out create deck functions are for test decks

    # def create_deck(self):
    #     deck = [
    #         Card("CLAY PIT", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)], money_cost = 1, num_players = 3),
    #         Card("CLAY POOL", C.RAW_R, provides_resources = [(R.BRICK,)], num_players = 3),
    #         Card("LUMBER YARD", C.RAW_R, provides_resources = [(R.WOOD,)], num_players = 3),
    #         Card("ORE VEIN", C.RAW_R, provides_resources = [(R.ORE,)], num_players = 3),
    #         Card("EAST TRADING POST", C.COMMERCIAL, icon = RightRawDiscount(), provides_coupons = ["FORUM"], num_players = 3),
    #         Card("TIMBER YARD", C.RAW_R, provides_resources = [(R.STONE, R.WOOD)], money_cost = 1, num_players = 3),
    #         Card("STOCKADE", C.MILITARY, num_shields = 1, cost = [R.WOOD, R.WOOD], num_players = 3),
    #         Card("BARRACKS", C.MILITARY, num_shields = 1, cost = [R.ORE, R.ORE], num_players = 3),
    #         ]

    #     return deck

    # def create_deck(self):
    #     deck = [
    #         Card("Workers Guild", C.GUILD, icon = PointForRaw(), cost = [R.ORE, R.ORE, R.BRICK, R.STONE, R.WOOD]),
    #         Card("Workers Guild", C.GUILD, icon = PointForRaw(), cost = []),
    #         Card("Craftmens Guild", C.GUILD, icon = TwoPointForMfc(), cost = [R.ORE, R.ORE, R.STONE, R.STONE]),
    #         Card("Traders Guild", C.GUILD, icon = OnePointForCommercial(), cost = [R.GLASS, R.SILK, R.PAPYRUS]),
    #         Card("Magistrates Guild", C.GUILD, icon = OnePointForCivic(), cost = [R.WOOD, R.WOOD, R.WOOD, R.STONE, R.SILK]),
    #         Card("Spies Guild", C.GUILD, icon = OnePointForMilitary(), cost = [R.BRICK, R.BRICK, R.BRICK, R.GLASS]),
    #         Card("Philosophers Guild", C.GUILD, icon = OnePointForScience(), cost = [R.BRICK, R.BRICK, R.BRICK, R.PAPYRUS, R.SILK]),
    #         Card("Shipowners Guild", C.GUILD, icon = PointForRawMfcGuild(), cost = [R.WOOD, R.WOOD, R.WOOD, R.GLASS, R.PAPYRUS]),
    #         Card("Strategists Guild", C.GUILD, icon = LeftRightPointForMinusTokens(), cost = [R.ORE, R.ORE, R.STONE, R.SILK]),
    #         Card("Builders Guild", C.GUILD, icon = PointForWonder(), cost = [R.STONE, R.STONE, R.BRICK, R.BRICK, R.GLASS]),
    #         Card("Scientists Guild", C.GUILD, icon = ScienceOptions(), cost = [R.WOOD, R.WOOD, R.ORE, R.ORE, R.PAPYRUS]),
    #         ]

    #     return deck

    # def create_deck(self):
    #     deck = [
    #         Card("Scientists Guild", C.GUILD, icon = ScienceOptions(), provides_sciences = [(S.TABLET, S.COG, S.COMPASS)], cost = []),
    #         Card("Scientists Guild", C.GUILD, icon = ScienceOptions(), provides_sciences = [(S.TABLET, S.COG, S.COMPASS)], cost = []),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [], num_players = 3),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.COG,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [], num_players = 3),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.TABLET,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [], num_players = 3),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.COG,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [], num_players = 3),
    #         Card("APOTHECARY", C.SCIENCE, provides_sciences = [(S.COMPASS,)], provides_coupons = ["STABLES", "DISPENSARY"], cost = [], num_players = 3),
    #         ]

    #     return deck

    # def create_deck(self):
    #     deck = [
    #         Card("Resources", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,), (R.BRICK,), (R.BRICK,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,), (R.WOOD,), (R.WOOD,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,), (R.STONE,), (R.STONE,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,), (R.ORE,), (R.ORE,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,), (R.BRICK,), (R.BRICK,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,), (R.WOOD,), (R.WOOD,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,), (R.STONE,), (R.STONE,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,), (R.BRICK,), (R.BRICK,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.WOOD,), (R.WOOD,), (R.WOOD,), (R.WOOD,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.STONE,), (R.STONE,), (R.STONE,), (R.STONE,)]),
    #         Card("Resources", C.RAW_R, provides_resources = [(R.ORE,), (R.ORE,), (R.ORE,), (R.ORE,)]),
    #         ]

    #     return deck

    # def create_deck(self):
    #     deck = [
    #         Card("Resources 1", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)]),
    #         Card("Resources 2", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,)]),
    #         Card("Resources 3", C.RAW_R, provides_resources = [(R.STONE,)]),
    #         Card("Resources 4", C.RAW_R, provides_resources = [(R.BRICK, R.ORE)]),
    #         Card("Resources 5", C.RAW_R, provides_resources = [(R.BRICK,), (R.BRICK,)]),
    #         Card("Resources 6", C.RAW_R, provides_resources = [(R.STONE,)]),
    #         Card("Resources 7", C.RAW_R, provides_resources = [(R.WOOD,)]),
    #         ]

    #     return deck

    # def create_deck(self):
    #     deck = [
    #         Card("Alexandria Start A", C.WONDER_START, provides_resources = [(R.GLASS,)]), 
    #         Card("Alexandria One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), 
    #         Card("Alexandria Two", C.WONDER_C, provides_resources = [(R.BRICK, R.ORE, R.WOOD, R.STONE)], cost = [R.ORE, R.ORE]), 
    #         Card("Alexandria Three", C.WONDER_C, points = 7, cost = [R.GLASS, R.GLASS]),
    #         Card("Alexandria Start B", C.WONDER_START, provides_resources = [(R.GLASS,)]), 
    #         Card("Alexandria One", C.WONDER_C, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], cost = [R.BRICK, R.BRICK]), 
    #         Card("Alexandria Two", C.WONDER_C, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], cost = [R.WOOD, R.WOOD]), 
    #         Card("Alexandria Three", C.WONDER_C, points = 7, cost = [R.STONE, R.STONE, R.STONE]),
    #         Card("Babylon Start A", C.WONDER_START, provides_resources = [(R.BRICK,)]), 
    #         Card("Babylon One", C.WONDER_C, points = 3, cost = [R.BRICK, R.BRICK]), 
    #         Card("Babylon Two", C.WONDER_C, icon = ScienceOptions(), provides_sciences = [(S.TABLET, S.COG, S.COMPASS)], cost = [R.WOOD, R.WOOD, R.WOOD]), 
    #         Card("Babylon Three", C.WONDER_C, points = 7, cost = [R.BRICK, R.BRICK, R.BRICK, R.BRICK]),
    #         Card("Babylon Start B", C.WONDER_START, provides_resources = [(R.BRICK,)]), 
    #         Card("Babylon One", C.WONDER_C, points = 3, cost = [R.SILK, R.BRICK]), 
    #         Card("Babylon Two", C.WONDER_C, icon = PlayLastCard(), cost = [R.WOOD, R.WOOD, R.GLASS]), 
    #         Card("Babylon Three", C.WONDER_C, provides_sciences = [(S.TABLET, S.COMPASS, S.COG)], cost = [R.BRICK, R.BRICK, R.BRICK, R.PAPYRUS]),
    #         Card("Ghiza Start A", C.WONDER_START, provides_resources = [(R.STONE,)]), 
    #         Card("Ghiza One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), 
    #         Card("Ghiza Two", C.WONDER_C, points = 5, cost = [R.WOOD, R.WOOD, R.WOOD]), 
    #         Card("Ghiza Three", C.WONDER_C, points = 7, cost = [R.STONE, R.STONE, R.STONE, R.STONE]),
    #         Card("Ephesos Start A", C.WONDER_START, provides_resources = [(R.PAPYRUS,)]), 
    #         Card("Ephesos One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), 
    #         Card("Ephesos Two", C.WONDER_C, provides_money = 9, cost = [R.WOOD, R.WOOD]), 
    #         Card("Ephesos Three", C.WONDER_C, points = 7, cost = [R.PAPYRUS, R.PAPYRUS]),
    #         Card("Ephesos Start B", C.WONDER_START, provides_resources = [(R.PAPYRUS,)]), 
    #         Card("Ephesos One", C.WONDER_C, points = 2, provides_money = 4, icon = TwoPointFourGold(), cost = [R.STONE, R.STONE]), 
    #         Card("Ephesos Two", C.WONDER_C, points = 3, provides_money = 4, icon = ThreePointFourGold(), cost = [R.WOOD, R.WOOD]), 
    #         Card("Ephesos Three", C.WONDER_C, points = 5, provides_money = 4, icon = FivePointFourGold(), cost = [R.PAPYRUS, R.SILK, R.GLASS]),
    #         Card("Rhodos Start A", C.WONDER_START, provides_resources = [(R.ORE,)]), 
    #         Card("Rhodos One", C.WONDER_C, points = 3, cost = [R.WOOD, R.WOOD]), 
    #         Card("Rhodos Two", C.WONDER_C, num_shields = 2, cost = [R.BRICK, R.BRICK, R.BRICK]), 
    #         Card("Rhodos Three", C.WONDER_C, points = 7, cost = [R.ORE, R.ORE, R.ORE, R.ORE]),
    #         Card("Olympia Start A", C.WONDER_START, provides_resources = [(R.WOOD,)]), 
    #         Card("Olympia One", C.WONDER_C, points = 3, cost = [R.WOOD, R.WOOD]), \
    #         Card("Olympia Two", C.WONDER_C, icon = GiveFreeCard(), cost = [R.STONE, R.STONE]), 
    #         Card("Olympia Three", C.WONDER_C, points = 7, cost = [R.ORE, R.ORE]),
    #         Card("Olympia Start B", C.WONDER_START, provides_resources = [(R.WOOD,)]), 
    #         Card("Olympia One", C.WONDER_C, icon = RawDiscount(), cost = [R.WOOD, R.WOOD]), 
    #         Card("Olympia Two", C.WONDER_C, points = 5, cost = [R.STONE, R.STONE]), 
    #         Card("Olympia Three", C.WONDER_C, icon = CopyGuild(), cost = [R.ORE, R.ORE, R.SILK])
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
            for card in player.cards:
                if card.icon:
                    card.icon.on_next_age(player, self.players)
            player.current_score = self.score_player(player)

    def end_game(self):
        self.war()

        winners = []
        best_score = -1
        for player in self.players:
            player.current_score = self.score_player(player)
            if player.current_score > best_score:
                winners = [player.player_number]
                best_score = player.current_score
            elif player.current_score == best_score:
                winners.append(player.player_number)
        if len(winners) == 1:
            print("Player number", winners[0], "wins!")
        else:
            print("A tie!")
            print("List of winners: ")
            print("--------")
            for winner in winners:
                print(winner)
            print("--------")


    def create_wonder_list(self):
        alexandria_a_card_list = [Card("Alexandria Start A", C.WONDER_START, provides_resources = [(R.GLASS,)]), \
                                    Card("Alexandria One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), \
                                    Card("Alexandria Two", C.WONDER_C, provides_resources = [(R.BRICK, R.ORE, R.WOOD, R.STONE)], cost = [R.ORE, R.ORE]), \
                                    Card("Alexandria Three", C.WONDER_C, points = 7, cost = [R.GLASS, R.GLASS])]
        alexandria_b_card_list = [Card("Alexandria Start B", C.WONDER_START, provides_resources = [(R.GLASS,)]), \
                                    Card("Alexandria One", C.WONDER_C, provides_resources = [(R.WOOD, R.STONE, R.ORE, R.BRICK)], cost = [R.BRICK, R.BRICK]), \
                                    Card("Alexandria Two", C.WONDER_C, provides_resources = [(R.GLASS, R.SILK, R.PAPYRUS)], cost = [R.WOOD, R.WOOD]), \
                                    Card("Alexandria Three", C.WONDER_C, points = 7, cost = [R.STONE, R.STONE, R.STONE])]
        babylon_a_card_list = [Card("Babylon Start A", C.WONDER_START, provides_resources = [(R.BRICK,)]), \
                                Card("Babylon One", C.WONDER_C, points = 3, cost = [R.BRICK, R.BRICK]), \
                                Card("Babylon Two", C.WONDER_C, icon = ScienceOptions(), provides_sciences = [(S.TABLET, S.COG, S.COMPASS)], cost = [R.WOOD, R.WOOD, R.WOOD]), \
                                Card("Babylon Three", C.WONDER_C, points = 7, cost = [R.BRICK, R.BRICK, R.BRICK, R.BRICK])]
        babylon_b_card_list = [Card("Babylon Start B", C.WONDER_START, provides_resources = [(R.BRICK,)]), \
                                Card("Babylon One", C.WONDER_C, points = 3, cost = [R.SILK, R.BRICK]), \
                                Card("Babylon Two", C.WONDER_C, icon = PlayLastCard(), cost = [R.WOOD, R.WOOD, R.GLASS]), \
                                Card("Babylon Three", C.WONDER_C, provides_sciences = [(S.TABLET, S.COMPASS, S.COG)], icon = ScienceOptions(), cost = [R.BRICK, R.BRICK, R.BRICK, R.PAPYRUS])]
        ghiza_a_card_list = [Card("Ghiza Start A", C.WONDER_START, provides_resources = [(R.STONE,)]), \
                                Card("Ghiza One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), \
                                Card("Ghiza Two", C.WONDER_C, points = 5, cost = [R.WOOD, R.WOOD, R.WOOD]), \
                                Card("Ghiza Three", C.WONDER_C, points = 7, cost = [R.STONE, R.STONE, R.STONE, R.STONE])]
        ghiza_b_card_list = [Card("Ghiza Start B", C.WONDER_START, provides_resources = [(R.STONE,)]), \
                                Card("Ghiza One", C.WONDER_C, points = 3, cost = [R.WOOD, R.WOOD]), \
                                Card("Ghiza Two", C.WONDER_C, points = 5, cost = [R.STONE, R.STONE, R.STONE]), \
                                Card("Ghiza Three", C.WONDER_C, points = 5, cost = [R.BRICK, R.BRICK, R.BRICK]), \
                                Card("Ghiza Four", C.WONDER_C, points = 7, cost = [R.STONE, R.STONE, R.STONE, R.STONE, R.PAPYRUS])]
        ephesos_a_card_list = [Card("Ephesos Start A", C.WONDER_START, provides_resources = [(R.PAPYRUS,)]), \
                                Card("Ephesos One", C.WONDER_C, points = 3, cost = [R.STONE, R.STONE]), \
                                Card("Ephesos Two", C.WONDER_C, provides_money = 9, cost = [R.WOOD, R.WOOD]), \
                                Card("Ephesos Three", C.WONDER_C, points = 7, cost = [R.PAPYRUS, R.PAPYRUS])]
        ephesos_b_card_list = [Card("Ephesos Start B", C.WONDER_START, provides_resources = [(R.PAPYRUS,)]), \
                                Card("Ephesos One", C.WONDER_C, points = 2, provides_money = 4, icon = TwoPointFourGold(), cost = [R.STONE, R.STONE]), \
                                Card("Ephesos Two", C.WONDER_C, points = 3, provides_money = 4, icon = ThreePointFourGold(), cost = [R.WOOD, R.WOOD]), \
                                Card("Ephesos Three", C.WONDER_C, points = 5, provides_money = 4, icon = FivePointFourGold(), cost = [R.PAPYRUS, R.SILK, R.GLASS])]
        rhodos_a_card_list = [Card("Rhodos Start A", C.WONDER_START, provides_resources = [(R.ORE,)]), \
                                Card("Rhodos One", C.WONDER_C, points = 3, cost = [R.WOOD, R.WOOD]), \
                                Card("Rhodos Two", C.WONDER_C, num_shields = 2, cost = [R.BRICK, R.BRICK, R.BRICK]), \
                                Card("Rhodos Three", C.WONDER_C, points = 7, cost = [R.ORE, R.ORE, R.ORE, R.ORE])]
        rhodos_b_card_list = [Card("Rhodos Start B", C.WONDER_START, provides_resources = [(R.ORE,)]), \
                                Card("Rhodos One", C.WONDER_C, num_shields = 1, points = 3, provides_money = 3, icon = OneShieldThreePointThreeGold(), cost = [R.STONE, R.STONE, R.STONE]), \
                                Card("Rhodos Two", C.WONDER_C, num_shields = 1, points = 4, provides_money = 4, icon = OneShieldFourPointFourGold(), cost = [R.ORE, R.ORE, R.ORE, R.ORE])]
        olympia_a_card_list = [Card("Olympia Start A", C.WONDER_START, provides_resources = [(R.WOOD,)]), \
                                Card("Olympia One", C.WONDER_C, points = 3, cost = [R.WOOD, R.WOOD]), \
                                Card("Olympia Two", C.WONDER_C, icon = GiveFreeCard(), cost = [R.STONE, R.STONE]), \
                                Card("Olympia Three", C.WONDER_C, points = 7, cost = [R.ORE, R.ORE])]
        olympia_b_card_list = [Card("Olympia Start B", C.WONDER_START, provides_resources = [(R.WOOD,)]), \
                                Card("Olympia One", C.WONDER_C, icon = RawDiscount(), cost = [R.WOOD, R.WOOD]), \
                                Card("Olympia Two", C.WONDER_C, points = 5, cost = [R.STONE, R.STONE]), \
                                Card("Olympia Three", C.WONDER_C, icon = CopyGuild(), cost = [R.ORE, R.ORE, R.SILK])]

        alexandria_a = Wonder("Alexandria", pg.image.load("Images/Wonders/alexandria_a.png"), alexandria_a_card_list)
        alexandria_b = Wonder("Alexandria", pg.image.load("Images/Wonders/alexandria_b.png"), alexandria_b_card_list)
        alexandria = [alexandria_a, alexandria_b]

        babylon_a = Wonder("Babylon", pg.image.load("Images/Wonders/babylon_a.png"), babylon_a_card_list)
        babylon_b = Wonder("Babylon", pg.image.load("Images/Wonders/babylon_b.png"), babylon_b_card_list)
        babylon = [babylon_a, babylon_b]

        ghiza_a = Wonder("Ghiza", pg.image.load("Images/Wonders/ghiza_a.png"), ghiza_a_card_list)
        ghiza_b = Wonder("Ghiza", pg.image.load("Images/Wonders/ghiza_b.png"), ghiza_b_card_list)
        ghiza = [ghiza_a, ghiza_b]

        ephesos_a = Wonder("Ephesos", pg.image.load("Images/Wonders/ephesos_a.png"), ephesos_a_card_list)
        ephesos_b = Wonder("Ephesos", pg.image.load("Images/Wonders/ephesos_b.png"), ephesos_b_card_list)
        ephesos = [ephesos_a, ephesos_b]

        rhodos_a = Wonder("Rhodos", pg.image.load("Images/Wonders/rhodos_a.png"), rhodos_a_card_list)
        rhodos_b = Wonder("Rhodos", pg.image.load("Images/Wonders/rhodos_b.png"), rhodos_b_card_list)
        rhodos = [rhodos_a, rhodos_b]

        olympia_a = Wonder("Olympia", pg.image.load("Images/Wonders/olympia_a.png"), olympia_a_card_list)
        olympia_b = Wonder("Olympia", pg.image.load("Images/Wonders/olympia_b.png"), olympia_b_card_list)
        olympia = [olympia_a, olympia_b]

        wonder_list = [alexandria, rhodos, babylon, ghiza, ephesos, olympia]
        random.shuffle(wonder_list)
        return wonder_list

        # BUG WITH THE THE DRAWING OF PRETTY MUCH EVERYTHING IN BABYLON B

    def assign_wonders(self, wonder_list):
        for i, player in enumerate(self.players):
            if not player.bot:
                print("You have selected {}!".format(wonder_list[i][0].name))
                # first one is for debug to always give player the desired wonder
                # the 2 length is for debuging and will skip the choosing a side part
                # if len(wonder_list[i]) == 1 or len(wonder_list[i]) == 2:
                # player.wonder = wonder_list[5][1]
                # continue
                if len(wonder_list[i]) == 1:
                    player.wonder = wonder_list[i][0]
                    continue
                player_choice = input("Would you like side A or side B? ")
                while True:
                    if player_choice == "a" or player_choice == "A":
                        player.wonder = wonder_list[i][0]
                        break
                    elif player_choice == "b" or player_choice == "B":
                        player.wonder = wonder_list[i][1]
                        break
                    print("Invalid Response Recieved")
                    player_choice = input("Please enter A or B")
            else:
                player.wonder = wonder_list[i][random.randrange(0, len(wonder_list[i]))]
                # player.wonder = wonder_list[i][0]
                    

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
    def __init__(self, player_number, bot):
        self.player_number = player_number
        self.wonder = None
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

        self.wonder_action = None
        self.wonder_selected = False
        self.play_last_card = False
        self.play_for_free = False
        
        self.bot = bot

    def give_moneys_for_discard(self):
        self.money += 3

    def play_card(self, selected_card, can_play = False):
        if self.can_play_card(selected_card) or can_play:
            self.money -= selected_card.money_cost
            self.num_shields += selected_card.num_shields
            self.money += selected_card.provides_money
            self.cards.append(selected_card)
            return True
        else:
            return False

    def can_play_card(self, card):
        resource_tuples = self.available_resources_tuples(self.cards)

        for player_card in self.cards:
            if card.name == player_card.name:
                return False

        for player_card in self.cards:
            for coupon in player_card.provides_coupons:
                if coupon == card.name:
                    return True 

        if self.has_resources_for_card(card.cost, resource_tuples) and self.money - self.spent_money_l - self.spent_money_r >= card.money_cost:
            return True
        if self.play_for_free:
            return True
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
    def __init__(self, image = pg.image.load("Images/image_not_found.png"), size = [50, 50]):
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

    def on_next_age(self, player, player_list):
        return

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

class RawDiscount(DiscountIcon):
    # 951 by 300
    def __init__(self):
        # image does not currently exist because I think this is only on a wonder
        image = pg.image.load("Images/raw_discount.png")
        super().__init__("both", "raw", 1, image, [100, 32])

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

        # print("icon score provided", total * self.provides[1])
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

    def total(self, player, player_list):
        left_player, right_player = self.left_right_players(player, player_list)
        total = 0

        if "left" in self.directions:
            total += left_player.wonder_level

        if "right" in self.directions:
            total += right_player.wonder_level

        if "down" in self.directions:
            total += player.wonder_level

        return total

    def on_played(self, current_player, player_list):
        current_player.money += self.total(current_player, player_list) * self.provides[0]

    def score(self, player, player_list):
        return self.total(player, player_list) * self.provides[1]

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

    def total(self, player, player_list):
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

        return total

    def score(self, player, player_list):
        return self.total(player, player_list) * self.provides[1]

class LeftRightPointForMinusTokens(StuffForMilitaryTokens):
    def __init__(self):
        # 435 by 241
        image = pg.image.load("Images/left_right_point_for_minus_tokens.png")
        super().__init__(["left", "right"], [0, 1], -1, image, [81, 45])


class ScienceOptions(Icon):
    # dummy icon, only used for image
    def __init__(self):
        # 745 by 190
        image = pg.image.load("Images/science_options.png")
        super().__init__(image, [100, 26])

class PlayLastCard(Icon):
    def __init__(self):
        image = pg.image.load("Images/play_last_card.png")
        # 385 / 244
        super().__init__(image, [65, 41])

    def on_played(self, current_player, player_list):
        # potential bug here where playing this icon as the last card will then allow another card to be played. I think I'm calling that a feature though
        current_player.play_last_card = True

class GiveFreeCard(Icon):
    # 258 by 240
    def __init__(self):
        image = pg.image.load("Images/free_card.png")
        super().__init__(image, [54, 50])

    def on_played(self, current_player, player_list):
        current_player.wonder_action = FreeCard()

    def on_next_age(self, player, player_list):
        player.wonder_action = FreeCard()

class CopyGuild(Icon):
    # 447 by 214
    def __init__(self):
        image = pg.image.load("Images/copy_guild.png")

        super().__init__(image, [75, 36])

    def score(self, current_player, player_list):
        left_player, right_player = self.left_right_players(current_player, player_list)
        neighbor_cards = left_player.cards + right_player.cards

        best_score = 0
        best_card = None
        
        for card in neighbor_cards:
            if card.card_type == C.GUILD:
                score = card.icon.score(current_player, player_list)
                if score > best_score:
                    best_score = score
                    best_card = card.name

        # print("best copy option was", best_card, "giving", best_score, "points")
        return best_score

# dummy icons because I can't be bothered to draw shields, coins, and points on the same card

class TwoPointFourGold(Icon):
    def __init__(self):
        image = pg.image.load("Images/Multi/two_point_four_gold.png")
        super().__init__(image, [80, 40])

class ThreePointFourGold(Icon):
    def __init__(self):
        image = pg.image.load("Images/Multi/three_point_four_gold.png")
        super().__init__(image, [80, 40])

class FivePointFourGold(Icon):
    def __init__(self):
        image = pg.image.load("Images/Multi/five_point_four_gold.png")
        super().__init__(image, [80, 40])

class OneShieldThreePointThreeGold(Icon):
    def __init__(self):
        # 633 by 207
        image = pg.image.load("Images/Multi/one_shield_three_point_three_gold.png")
        super().__init__(image, [90, 29])

class OneShieldFourPointFourGold(Icon):
    def __init__(self):
        image = pg.image.load("Images/Multi/one_shield_four_point_four_gold.png")
        super().__init__(image, [90, 29])

class OneShieldSevenPointsSevenGold(Icon):
    def __init__(self):
        image = pg.image.load("Images/Multi/one_shield_seven_point_seven_gold.png")
        super().__init__(image, [90, 29])



class WonderFunction():
    def __init__(self, active = False):
        self.active = active

    def on_activated(self, player):
        if self.active:
            print("Error: No wonder activation function found")
            return
        else:
            print("Error: No wonder deactivation function found")
            return

# maybe one day draw these icons in the all cards view

class FreeCard(WonderFunction):
    def __init__(self):
        super().__init__(False)

    def on_activated(self, player):
        print("ACTIVATED")
        if self.active:
            print("False")
            player.play_for_free = False
            self.active = False
        else:
            print("True")
            player.play_for_free = True
            self.active = True

    

    

