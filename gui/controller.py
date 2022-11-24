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
    def __init__(self, game, board):
        self.game = game
        self.board = board

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
            self.game.current_player_finished()
            self.board.discard = False
            self.board.request_redraw()

    def build_wonder(self, selected_card_number):
        if not self.board.all_cards:
            if self.game.current_player().play_card(self.game.current_player().wonder.layers_list[self.game.current_player().wonder_level + 1]):
                hand = self.game.current_player_hand()
                del hand[selected_card_number]
                self.game.current_player().wonder_level += 1
                hand = self.game.current_player_hand()
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

    def select_card(self, selected_card_number):
        if not self.board.all_cards:
            hand = self.game.current_player_hand()
            selected_card = hand[selected_card_number]

            if self.game.current_player().play_card(selected_card):
                del hand[selected_card_number]
                self.game.current_player_finished()
                self.board.request_redraw()

    def on_all_cards_button_pressed(self):
        if self.board.all_cards == False:
            self.board.all_cards = True
        self.board.request_redraw()

    def on_back_button_pressed(self):
        self.board.all_cards = False
        self.board.request_redraw()