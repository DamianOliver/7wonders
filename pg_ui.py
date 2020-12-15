from game import *
import pygame as pg
import random

pg.init()

screen_dimension = (1440, 1024)
screen = pg.display.set_mode((screen_dimension), pg.RESIZABLE)

BACKRGOUND_COLOR = (110, 60, 40)
MILITARY_COLOR = (220, 50, 50)
SCIENCE_COLOR = (50, 150, 30)
RAW_RESOURCE_COLOR = (70, 35, 25)
MANUFACTORED_RESOURCE_COLOR = (125,125,125)
COMMERCIAL_COLOR = (200, 170, 20)
CIVIC_COLOR = (0, 0, 200)
CARD_NAME_COLOR = (255, 255, 255)

HAND_CARD_TEXT_MARGIN = 10
HAND_CARD_NAME_FONT_SIZE = 20

HAND_CARD_PROVIDES_MARGIN = 15

HAND_CARD_SIZE = (144, 250)
hand_spacing = screen_dimension[0]/30

class PgUi:
    def __init__(self):
        self.game = Game()

    def play(self):
        global screen_dimension
        for i in range(len(self.game.players)):
                player = self.game.players[i]
                hand = self.game.hands[(i + self.game.turn) % len(self.game.hands)] 
        self.draw_game(hand)
        pg.display.update()
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.VIDEORESIZE:
                    screen_dimension = pg.display.get_surface().get_size()
                    print(screen_dimension)
                    self.draw_game(hand)
                    pg.display.update()
   
    def draw_game(self, hand_cards):
        print("drawing stuff")
        screen.fill(BACKRGOUND_COLOR)
        self.draw_hand(hand_cards)

    def draw_hand(self, hand_cards):
        for i in range(len(hand_cards)):

            round_distance = HAND_CARD_SIZE[0] / 17
            hand_spacing = screen_dimension[0]/30
            hand_margin = (screen_dimension[0] - (hand_spacing + HAND_CARD_SIZE[0])*len(hand_cards) + hand_spacing)/2
            card_location = ((hand_margin + i * (hand_spacing + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
            print(hand_cards[i].card_type)
            if hand_cards[i].card_type == "Military":
                pg.draw.rect(screen, pg.Color(MILITARY_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
                for i in range(hand_cards[i].num_sheilds):
                    print("mIlLiTAry")
                    shield = pg.image.load('C:\\Users\Damian\\7wonders\\Images\\shield.png')
                    shield = pg.transform.scale(shield, (50, 50))
                    shield_pos = (((card_location[0] / hand_cards[i].num_sheilds) * i) + shield.get_size()[0]/2, card_location[1] + HAND_CARD_PROVIDES_MARGIN)
                    screen.blit(shield, (shield_pos[0], shield_pos[1]))
                    print(shield_pos[0])
                    print(card_location[0])
            elif hand_cards[i].card_type == "Science":
                pg.draw.rect(screen, pg.Color(SCIENCE_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
            elif hand_cards[i].card_type == "Raw Resource":
                pg.draw.rect(screen, pg.Color(RAW_RESOURCE_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
            elif hand_cards[i].card_type == "Commercial":
                pg.draw.rect(screen, pg.Color(COMMERCIAL_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
            elif hand_cards[i].card_type == "Manufactored Resource":
                pg.draw.rect(screen, pg.Color(MANUFACTORED_RESOURCE_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
            elif hand_cards[i].card_type == "Civic":
                pg.draw.rect(screen, pg.Color(CIVIC_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
            else:
                pg.draw.rect(screen, pg.Color(0, 0, 0), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(round_distance))
            
            hand_card_name_font = pg.font.Font(None, HAND_CARD_NAME_FONT_SIZE)
            hand_card_name_text = hand_card_name_font.render(hand_cards[i].name, True, (255, 255, 255))
            hand_card_name_text = pg.transform.rotate(hand_card_name_text, 90)
            hand_card_name_text_length = hand_card_name_text.get_size()
            hand_card_name_location = (card_location[0] + HAND_CARD_TEXT_MARGIN, card_location[1] + HAND_CARD_SIZE[1] - HAND_CARD_TEXT_MARGIN - hand_card_name_text_length[1])
            screen.blit(hand_card_name_text, (hand_card_name_location[0], hand_card_name_location[1]))