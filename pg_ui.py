from game import *
from gui.controller import GameController, Board
from gui.view import *
import pygame as pg
import random

i = 0
hand = Game().hands[(i + Game().turn) % len(Game().hands)]

screen_dimension = (1440, 1000)



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
        self.board = Board()
        self.controller = GameController(self.game, self.board)
        self.init_views()

    def init_views(self):
        self.game_view = GameView(self.game, self.board, self.controller)

    def play(self):
        global card_highlighted
        global screen_dimension
        global HAND_MARGIN
        global LAST_CARD_LOCATION

        # draw initial hand
        self.game_view.layout(screen_dimension)
        self.draw_game()
        pg.display.update()
        self.run_event_loop()

    def run_event_loop(self):
        global HAND_MARGIN
        global screen_dimension
        global discard

        while True:
            events = pg.event.get()
            for event in events:
                if self.game_view.handle_event(event):
                    if self.board.needs_redraw:
                        self.draw_game()
                        pg.display.update()
                        self.board.needs_redraw = False

                    continue
                elif event.type == pg.QUIT:
                    pg.quit()
                    print("NO DON'T QUIT")
                    return
                elif event.type == pg.WINDOWEVENT and event.__dict__["event"] == pg.WINDOWEVENT_CLOSE:
                    pg.quit()
                    print("NO DON'T QUIT")
                    return
                elif event.type == pg.VIDEORESIZE:
                    print("pls resize")
                    screen_dimension = pg.display.get_surface().get_size()
                    print(screen_dimension)
                    self.game_view.layout(screen_dimension)
                    self.draw_game()
                    pg.display.update()

    # def draw_money(self, money)

    def draw_game(self):
        print("drawing stuff")
        screen.fill(BACKRGOUND_COLOR)
        self.game_view.draw()

    