from game import *
from gui.controller import GameController, Board
from gui.view import *
import pygame as pg
import random

i = 0
hand = Game().hands[(i + Game().turn) % len(Game().hands)]

DISCARD_BUTTON_SIZE = (100, 50)
DISCARD_BUTTON_COLOR = (240, 20, 20)
DISCARD_BUTTON_ROUND_DISTANCE = 8
DISCARD_BUTTON_MARGIN = (20, 0)
DISCARD_FONT_SIZE = 20

HAND_CARD_SIZE = (144, 250)
HAND_SPACING = 20
HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*NUM_CARDS_PER_PLAYER + HAND_SPACING)/2

LAST_CARD_LOCATION = ((HAND_MARGIN + (NUM_CARDS_PER_PLAYER - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
DISCARD_BUTTON_LOCATION = (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1])

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
        global discard
        global LAST_CARD_LOCATION
        global DISCARD_BUTTON_LOCATION

        # draw initial hand
        self.draw_game()
        self.run_event_loop()

    def run_event_loop(self):
        global HAND_MARGIN
        global DISCARD_BUTTON_LOCATION
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
                    HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
                    LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
                    print("hand margin: ", HAND_MARGIN)
                    DISCARD_BUTTON_LOCATION = (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1])
                    print(screen_dimension)
                    self.draw_game()
                    pg.display.update()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.is_event_inside_discard_button():
                        if discard:
                            discard = False
                            self.draw_discard_button()
                        else:
                            discard = True
                            self.draw_discard_button()
                    hand = self.game.current_player_hand()

    def is_event_inside_discard_button(self):
        return \
            pg.mouse.get_pos()[0] > DISCARD_BUTTON_LOCATION[0] and \
            pg.mouse.get_pos()[0] < DISCARD_BUTTON_LOCATION[0] + DISCARD_BUTTON_SIZE[0] and \
            pg.mouse.get_pos()[1] > DISCARD_BUTTON_LOCATION[1] and \
            pg.mouse.get_pos()[1] < DISCARD_BUTTON_LOCATION[1] + DISCARD_BUTTON_SIZE[1]

    # def draw_money(self, money)

    def draw_game(self):
        print("drawing stuff")
        screen.fill(BACKRGOUND_COLOR)
        self.game_view.draw()
        self.draw_discard_button()

    def draw_discard_button(self):
        if not discard:
            pg.draw.rect(screen, pg.Color(DISCARD_BUTTON_COLOR), pg.Rect(DISCARD_BUTTON_LOCATION, DISCARD_BUTTON_SIZE), border_radius=int(DISCARD_BUTTON_ROUND_DISTANCE))
            discard_font = pg.font.SysFont("georgia", DISCARD_FONT_SIZE)
            discard_text = discard_font.render("Discard", True, (0, 0, 0))
            discard_text_rect = discard_text.get_rect(center = (DISCARD_BUTTON_LOCATION[0] + DISCARD_BUTTON_SIZE[0]/2, DISCARD_BUTTON_LOCATION[1] + DISCARD_BUTTON_SIZE[1]/2))
            screen.blit(discard_text, discard_text_rect)
            pg.display.update()
        else:
            self.draw_cancel_button()


    def draw_cancel_button(self):
        global CANCEL_BUTTON_LOCATION
        CANCEL_BUTTON_LOCATION = DISCARD_BUTTON_LOCATION
        pg.draw.rect(screen, pg.Color(CANCEL_BUTTON_COLOR), pg.Rect(CANCEL_BUTTON_LOCATION, CANCEL_BUTTON_SIZE), border_radius=int(CANCEL_BUTTON_ROUND_DISTANCE))
        cancel_font = pg.font.SysFont("georgia", CANCEL_FONT_SIZE)
        cancel_text = cancel_font.render("Cancel", True, (0, 0, 0))
        cancel_text_rect = cancel_text.get_rect(center = (CANCEL_BUTTON_LOCATION[0] + CANCEL_BUTTON_SIZE[0]/2, CANCEL_BUTTON_LOCATION[1] + CANCEL_BUTTON_SIZE[1]/2))
        screen.blit(cancel_text, cancel_text_rect)
        pg.display.update()
