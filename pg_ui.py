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


from game import *
from gui.controller import GameController, Board
from gui.view import *
from ai import Ai
import pygame as pg
import random

i = 0

screen_dimension = (1440, 1000)
pg.display.set_caption("7 Wonders")

DISCARD_BUTTON_SIZE = (100, 50)
DISCARD_BUTTON_COLOR = (240, 20, 20)
DISCARD_BUTTON_ROUND_DISTANCE = 8
DISCARD_BUTTON_MARGIN = (20, 0)
DISCARD_FONT_SIZE = 20

HAND_CARD_SIZE = (144, 250)


card_highlighted = 1
discard = False

class PgUi:
    def __init__(self):
        self.game = Game()
        # self.hand = self.game().hands[(i + self.game().turn) % len(self.game().hands)]
        self.board = Board()
        self.controller = GameController(self.game, self.board, "placeholder")
        self.game_view = GameView(self.game, self.board, self.controller)
        self.controller.view = self.game_view
        self.game_view.controller = self.controller
        self.screen_dimension = (1440, 1000)
        self.background_image = pg.image.load("Images/wood_background.png")
        

        # self.init_views()

    # def init_views(self):
    #     self.game_view = GameView(self.game, self.board, self.controller)

    def play(self):
        global card_highlighted
        global screen_dimension

        # draw initial hand

        if not self.game.players[0].bot:
            self.game_view.layout(screen_dimension)
            self.draw_game()
            pg.display.update()
        else:
            self.controller.on_bot_turn()
        self.run_event_loop()

        # self.controller.test_ai(200)

    def run_event_loop(self):
        global screen_dimension
        global discard

        while True:
            events = pg.event.get()
            for event in events:
                if self.game_view.handle_event(event):
                    if self.board.needs_redraw:
                        if not self.game.current_player().bot:
                            self.game_view.layout(self.screen_dimension)
                            self.draw_game()
                            pg.display.update()
                            self.board.needs_redraw = False
                    continue
                elif event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.VIDEORESIZE:
                    screen_dimension = pg.display.get_surface().get_size()
                    self.game_view.layout(screen_dimension)
                    self.screen_dimension = screen_dimension
                    self.draw_game()
                    pg.display.update()

    def draw_game(self):
        # scaled_image = pg.transform.scale(self.background_image, self.screen_dimension)
        # screen.blit(scaled_image, (0, 0))
        screen.fill(BACKRGOUND_COLOR)
        self.game_view.draw()

    