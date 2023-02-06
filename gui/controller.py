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
from ai import Ai
import pygame as pg

from game import C, R, S

# Controller reacts to events and modifies model (Board)

# Model holds information and logic on how states change

class Board:
    def __init__(self):
        self.needs_redraw = False
        self.discard = False
        self.play_wonder = False
        self.all_cards = False
        self.highlight_card_index = -1
        self.game_over = False

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

        self.ai_dict = self.assign_ais()

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
        current_player = self.game.current_player()
        if not self.board.all_cards:
            hand = self.game.current_player_hand()
            del hand[selected_card_number]
            current_player.give_moneys_for_discard()
            self.on_end_turn()
            if self.board.game_over:
                return
            self.game.current_player_finished()
            self.board.discard = False
            self.board.request_redraw()
            if self.game.current_player().bot:
                self.on_bot_turn()
            else:
                self.ai_debugs()
            

    def build_wonder(self, selected_card_number):
        if not self.board.all_cards:
            current_player = self.game.current_player()
            wonder_card = current_player.wonder.layers_list[current_player.wonder_level + 1]
            if current_player.play_card(wonder_card, current_player.bot) or current_player.bot:
                hand = self.game.current_player_hand()
                del hand[selected_card_number]
                current_player.wonder_level += 1
                hand = self.game.current_player_hand()
                if wonder_card.icon:
                    wonder_card.icon.on_played(current_player, self.game.players)
                self.on_end_turn()
                if self.board.game_over:
                    return
                self.game.current_player_finished()
                self.board.play_wonder = False
                self.board.request_redraw()
                if self.game.current_player().bot:
                    self.on_bot_turn()
                else:
                    self.ai_debugs()

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
        current_player = self.game.current_player()
        if not self.board.all_cards:
            if not self.board.discard:
                if current_player.wonder_level < len(current_player.wonder.layers_list) - 1:
                    self.board.play_wonder = True
                    self.board.request_redraw()

    def reset_side(self, side, current_player):
        if side == "l":
            for b_res in current_player.bought_resources:
                if b_res[0][0] < 600:
                    current_player.bought_resources.remove(b_res)
        else:
            for b_res in current_player.bought_resources:
                if b_res[0][0] > 600:
                    current_player.bought_resources.remove(b_res)

    def on_resource_selected(self, side, resource_map, selected_resource):
        if not self.board.all_cards:
            current_player = self.game.current_player()

            self.reset_side(side, current_player)

            if side == "r":
                current_player.spent_money_r = 0
            elif side == "l":
                current_player.spent_money_l = 0

            for resource_tuple in resource_map:
                for resource in resource_tuple:
                    if resource[0][0] < 600:
                        res_side = "l"
                        if resource[1].is_raw():
                            cost = current_player.left_cost_r
                        else:
                            cost = current_player.left_cost_m
                    else:
                        res_side = "r"
                        if resource[1].is_raw():
                            cost = current_player.right_cost_r
                        else:
                            cost = current_player.right_cost_m
                    
                    if current_player.spent_money_l + current_player.spent_money_r + cost <= current_player.money:
                        if resource[2]:
                            current_player.bought_resources.append(resource)
                            # maybe should be side not res_side
                            if res_side == "l":
                                current_player.spent_money_l += cost
                            else:
                                current_player.spent_money_r += cost

            self.board.request_redraw()

    def on_wonder_board_selected(self):
        current_player = self.game.current_player()
        if current_player.wonder_action:
            if current_player.wonder_selected:
                current_player.wonder_selected = False
                current_player.wonder_action.on_activated(current_player)
            else:
                current_player.wonder_selected = True
                current_player.wonder_action.on_activated(current_player)
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
            current_player = self.game.current_player()
            hand = self.game.current_player_hand()
            card = hand[selected_card_number]
            selected_card = card

            # WARNING TO FUTURE SELF: BOT IGNORES CAN PLAY FUNCTION - ANY AI LOGIG BUG WILL ALLOW IT TO PLAY CARDS FOR FREE
            if current_player.play_card(selected_card, current_player.bot) or current_player.play_for_free:
                if card.icon:
                    card.icon.on_played(current_player, self.game.players)
                del hand[selected_card_number]
                self.on_end_turn()
                if self.board.game_over:
                    return
                self.game.current_player_finished()
                self.board.request_redraw()
                if self.game.current_player().bot:
                    self.on_bot_turn()
                else:
                    self.ai_debugs()

    def on_all_cards_button_pressed(self):
        if not self.board.all_cards:
            self.board.all_cards = True
            self.view.all_cards_view.player_index  = self.game.current_player_index
            self.board.request_redraw()

    def on_back_button_pressed(self):
        self.board.all_cards = False
        self.board.request_redraw()

    def assert_wonders(self, current_player):
        stages = current_player.wonder.layers_list
        stage_set = set(stages)
        if len(stages) != len(stage_set):
            print("uh oh")

    def on_end_turn(self):
        current_player = self.game.current_player()

        self.assert_wonders(current_player)

        left_player, right_player = self.game.left_right_players(current_player)
        current_player.money += (-current_player.spent_money_l - current_player.spent_money_r)
        left_player.money += current_player.spent_money_l
        right_player.money += current_player.spent_money_r

        if len(self.game.current_player_hand()) <= 1:
            if current_player.player_number == len(self.game.players) - 1 and not (current_player.play_last_card and len(self.game.current_player_hand()) == 1):
                if self.game.age == 3:
                    self.game.end_game()
                    self.board.game_over = True
                    print("ITS OVER")
                else:
                    self.game.next_age()
     
        current_player.spent_money_l = 0
        current_player.spent_money_r = 0

        # pretty janky code to make sure that view resets the resource map after each turn
        if not current_player.bot:
            current_player.bought_resources = []
        else:
            current_player.bought_resources = ["turn ended"]

        if current_player.play_for_free:
            current_player.play_for_free = False
            current_player.wonder_action = None
        current_player.wonder_selected = False

        self.board.request_redraw()

        current_player.current_score = self.game.score_player(current_player)

        if current_player.money < 0:
            print("uh oh")

    def reset_game(self):
        print("reset function")
        self.game = Game()
        self.ai_dict = self.assign_ais()
        self.board.game_over = False


    def assign_ais(self):
        player_list = self.game.players

        ais = {}
        for player in player_list:
            # commented out for debuggging to test ai on human player
            # if player.bot:
            ais[player] = Ai(player, self.game.players)

        return ais

    def on_bot_turn(self):
        current_player = self.game.current_player()
        ai = self.ai_dict[current_player]
        selected_card, action, cost = ai.evaluate(self.game.current_player_hand(), self.game.age)
        selected_card_index = self.game.current_player_hand().index(selected_card)
        if action == "play":
            self.select_card(selected_card_index)
            left_player, right_player = self.game.left_right_players(current_player)
            left_player.money += cost[0]
            right_player.money += cost[1]
            current_player.money -= cost[0] + cost[1]
        elif action == "wonder":
            self.build_wonder(selected_card_index)
        elif action == "discard":
            self.discard_card(selected_card_index)

    def ai_debugs(self):
        print()
        print()
        print("PLAYER DEBUG")
        current_player = self.game.current_player()
        if not current_player.bot:
            ai = self.ai_dict[current_player]
            # for printing
            selected_card, action, cost = ai.evaluate(self.game.current_player_hand(), self.game.age)
        print()

    def test_ai(self, num_games):
        point_total = 0
        individual_point_total = [0 for i in range(len(self.game.players))]
        avg_wonder_stages = [0 for i in range(len(self.game.players))]
        win_totals = [0 for i in range(len(self.game.players))]
        wonder_wins = {}
        bias_totals = [0, 0]
        best_score = 0
        winning_avg = 0
        for i in range(num_games):
            print("reseting")
            self.reset_game()
            self.on_bot_turn()
            win_index = None
            best_points = -99
            for p, player in enumerate(self.game.players):
                player_score = self.game.score_player(player)
                individual_point_total[p] += player_score
                avg_wonder_stages[p] += player.wonder_level
                point_total += player_score
                if player_score > best_points:
                    best_points = player_score
                    win_index = p
                    if best_points > best_score:
                        best_score = best_points
                        best_cards = self.game.players[win_index].cards
                        

            print("player number", win_index, "won with", best_points)
            print("Player number {} won game {} with a score of {}".format(win_index, i, best_points))
            winner = self.game.players[win_index]
            win_totals[win_index] += 1
            winning_wonder = winner.wonder.name
            winning_avg += best_points
            if winning_wonder in wonder_wins:
                wonder_wins[winning_wonder] += 1
            else:
                wonder_wins[winning_wonder] = 1
            winning_ai = self.ai_dict[self.game.players[p]]
            bias_totals[0] += winning_ai.bias_dict[C.SCIENCE]
            bias_totals[1] += winning_ai.bias_dict[C.MILITARY]

        point_avg = point_total / num_games / len(self.game.players)

        for i in range(len(individual_point_total)):
            individual_point_total[i] /= num_games
            avg_wonder_stages[i] /= num_games

        for i in range(len(bias_totals)):
            bias_totals[i] /= num_games

        winning_avg /= num_games

        print()
        print("win totals:", win_totals)
        print("average points:", point_avg)
        print("individiual point averages:", individual_point_total)
        print("avg wonder stages:", avg_wonder_stages)
        print("avg winning biases:", bias_totals)
        print("single highest score of", best_score)
        print("Average winning score of", winning_avg)
        print(wonder_wins)

        print()
        print("best card list:")
        print("--------------------")
        [print(card.name) for card in best_cards]

            
