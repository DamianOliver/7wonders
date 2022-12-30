# Copyright 2020 Damian Piech
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from gui.view import GameView
from game import Game
import pygame as pg

# Controller reacts to events and modifies model (Board)

# Model holds information and logic on how states change

class Board:
    def __init__(self):
        self.needs_redraw = False
        self.discard = False
        self.play_wonder = False
        self.all_cards = False
        self.highlight_card_index = -1

    def request_redraw(self):
        self.needs_redraw = True

    def is_hand_card_highlighted(self, card_index):
        return self.highlight_card_index == card_index

    def update_hand_card_highlight(self, card_index):
        if self.highlight_card_index != card_index:
            self.highlight_card_index = card_index
            self.needs_redraw = True

class GameController:
    def __init__(self, game, board, view):
        self.game = game
        self.board = board
        self.view = view

    def on_hand_card_mouse_over(self, hand_card_index):
        if not self.board.all_cards:
            self.board.update_hand_card_highlight(hand_card_index)

    def on_hand_card_mouse_down(self, hand_card_index):
        if not self.board.all_cards:
            if self.board.discard:
                self.discard_card(hand_card_index)
            elif self.board.play_wonder:
                self.build_wonder(hand_card_index)
            else:
                self.select_card(hand_card_index)
            return

    def discard_card(self, selected_card_number):
        if not self.board.all_cards:
            hand = self.game.current_player_hand()
            del hand[selected_card_number]
            self.game.current_player().give_moneys_for_discard()
            self.on_end_turn()
            self.game.current_player_finished()
            self.board.discard = False
            self.board.request_redraw()

    def build_wonder(self, selected_card_number):
        if not self.board.all_cards:
            current_player = self.game.current_player()
            if current_player.play_card(current_player.wonder.layers_list[current_player.wonder_level + 1]):
                hand = self.game.current_player_hand()
                del hand[selected_card_number]
                current_player.wonder_level += 1
                hand = self.game.current_player_hand()
                self.on_end_turn()
                self.game.current_player_finished()
                self.board.play_wonder = False
                self.board.request_redraw()

    def on_discard_button_pressed(self):
        if not self.board.all_cards:
            if not self.board.discard and not self.board.play_wonder:
                self.board.discard = True
                self.board.request_redraw()
            else:
                self.board.discard = False
                self.board.play_wonder = False
                self.board.request_redraw()

    def on_wonder_button_pressed(self):
        if not self.board.all_cards:
            if not self.board.discard:
                if self.game.current_player().wonder_level < len(self.game.current_player().wonder.layers_list) - 1:
                    self.board.play_wonder = True
                    self.board.request_redraw()

    def reset_side(self, side, current_player):
        if side == "l":
            for b_res in current_player.bought_resources:
                print("b_res:", b_res)
                if b_res[0][0] < 600:
                    # print("b_res:", b_res, b_res[0][0][0])
                    current_player.bought_resources.remove(b_res)
                    print("reset something")
        else:
            for b_res in current_player.bought_resources:
                if b_res[0][0] > 600:
                    print("reset something")
                    current_player.bought_resources.remove(b_res)

    def on_resource_selected(self, side, resource_map, selected_resource):
        if not self.board.all_cards:
            current_player = self.game.current_player()

            self.reset_side(side, current_player)

            current_player.spent_money_l = 0
            current_player.spent_money_r = 0
            # if side == "l":
            #     if selected_resource[1].is_raw():
            #         selected_cost = current_player.left_cost_r
            #     else:
            #         selected_cost = current_player.left_cost_m
            #     if current_player.money >= selected_cost:
            #         current_player.spent_money_l = 0

            #         for resource_tuple in resource_map:
            #             for resource in resource_tuple:
            #                 if resource[2]:
            #                     current_player.bought_resources.append(resource)
            #                     if resource[1].is_raw():
            #                         current_player.spent_money_l += current_player.right_cost_r
            #                     else:
            #                         current_player.spent_money_l += current_player.right_cost_m

            # else:
            #     if selected_resource[1].is_raw():
            #         selected_cost = current_player.right_cost_r
            #     else:
            #         selected_cost = current_player.right_cost_m
            #     if current_player.money >= selected_cost:
            #         current_player.spent_money_r = 0
            #         for resource_tuple in resource_map:
            #             for resource in resource_tuple:
            #                 if resource[2]:
            #                     current_player.bought_resources.append(resource)
            #                     if resource[1].is_raw():
            #                         current_player.spent_money_r += current_player.right_cost_r
            #                     else:
            #                         current_player.spent_money_r += current_player.right_cost_m

            print("bought resources", current_player.bought_resources)
            print()
            for resource_tuple in resource_map:
                for resource in resource_tuple:
                    # print("resource:", resource)
                    if resource[0][0] < 600:
                        # print("< 600")
                        res_side = "l"
                        if resource[1].is_raw():
                            cost = current_player.left_cost_r
                        else:
                            cost = current_player.left_cost_m
                    else:
                        # print("> 600")
                        res_side = "r"
                        if resource[1].is_raw():
                            cost = current_player.right_cost_r
                        else:
                            cost = current_player.right_cost_m
                    
                    if current_player.spent_money_l + current_player.spent_money_r + cost <= current_player.money:
                        if resource[2]:
                            # print("true")
                            current_player.bought_resources.append(resource)
                            # maybe should be side not res_side
                            if res_side == "l":
                                current_player.spent_money_l += cost
                            else:
                                current_player.spent_money_r += cost
                        # else:
                        #     print("false")
                            

                # print("left:", current_player.spent_money_l, "right:", current_player.spent_money_r)
                print("bought:", current_player.bought_resources)

            

            self.board.request_redraw()

    def on_player_view_selected(self, index):
        if not self.board.all_cards:
            self.board.all_cards = True
            self.view.all_cards_view.player_index = index
            self.board.request_redraw()
            return True
        return False

    def select_card(self, selected_card_number):
        if not self.board.all_cards:
            hand = self.game.current_player_hand()
            card = hand[selected_card_number]
            selected_card = card

            if self.game.current_player().play_card(selected_card):
                if card.icon:
                    card.icon.on_played(self.game.current_player(), self.game.players)
                del hand[selected_card_number]
                self.on_end_turn()
                self.game.current_player_finished()
                self.board.request_redraw()

    def on_all_cards_button_pressed(self):
        if not self.board.all_cards:
            self.board.all_cards = True
            self.view.all_cards_view.player_index  = self.game.current_player_index
            self.board.request_redraw()

    def on_back_button_pressed(self):
        self.board.all_cards = False
        self.board.request_redraw()

    def on_end_turn(self):
        current_player = self.game.current_player()
        left_player, right_player = self.game.left_right_players(current_player)
        current_player.money += (-current_player.spent_money_l - current_player.spent_money_r)
        left_player.money += current_player.spent_money_l
        right_player.money += current_player.spent_money_r

        if len(self.game.current_player_hand()) <= 1:
            if current_player.player_number == len(self.game.players) - 1:
                if self.game.age == 3:
                    print("game over")
                else:
                    self.game.next_age()
     
        current_player.spent_money_l = 0
        current_player.spent_money_r = 0

        current_player.current_score = self.game.score_player(current_player)
