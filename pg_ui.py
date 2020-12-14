from game import *
import pygame as pg
import random

screen_dimension = (1000, 700)
screen = pg.display.set_mode((screen_dimension), pg.RESIZABLE)
BACKRGOUND_COLOR = (110, 60, 40)
MILITARY_COLOR = (220, 50, 50)
SCIENCE_COLOR = (50, 230, 50)
RAW_RESOURCE_COLOR = (0,0,0)

HAND_MARGIN = screen_dimension[0]/10
HAND_CARD_SIZE = (screen_dimension[0]/4, screen_dimension[1]/3)
HAND_SPACING = screen_dimension[0]/20

class PgUi:
    def __init__(self):
        self.game = Game()

    def play(self):
        global screen_dimension
        for i in range(len(self.game.players)):
                player = self.game.players[i]
                hand = self.game.hands[(i + self.game.turn) % len(self.game.hands)] 
        self.draw_board(hand)
        pg.display.update()
        print("I made it")
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.VIDEORESIZE:
                    screen_dimension = (screen.get_width, screen.get_height)
                    print(screen_dimension)
                    self.draw_board(hand)
                    pg.display.update()

    def draw_rounded_rect(self, height, width, round_distance, location_x, location_y, color):
        pg.draw.rect(screen, color, (location_x, location_y, width, height))
        pg.draw.rect(screen, color, [location_x, location_y, width, height], round_distance)
        pg.draw.ellipse(screen, color, (location_x - round_distance/2, location_y - round_distance/2, round_distance, round_distance))
        pg.draw.ellipse(screen, color, (location_x - round_distance/2, location_y + height - round_distance/2, round_distance, round_distance))
        pg.draw.ellipse(screen, color, (location_x - round_distance/2 + width, location_y - round_distance/2, round_distance, round_distance))
        pg.draw.ellipse(screen, color, (location_x + width - round_distance/2, location_y + height - round_distance/2, round_distance, round_distance))
   
    def draw_board(self, hand_cards):
        print("drawing stuff")
        screen.fill(BACKRGOUND_COLOR   )
        for i in range(len(hand_cards)):
            if hand_cards[i].card_type == "Military":
                self.draw_rounded_rect(200, 50, 20, HAND_MARGIN + i * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2, MILITARY_COLOR)
            elif hand_cards[i].card_type == "Science":
                self.draw_rounded_rect(200, 50, 20, HAND_MARGIN + i * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2, SCIENCE_COLOR)
            else:
                self.draw_rounded_rect(200, 50, 20, HAND_MARGIN + i * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2, SCIENCE_COLOR)
