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

from game import Game, C, R, NUM_CARDS_PER_PLAYER
import pygame as pg
from gui.controller import GameController, Board

# display only and takes events

screen = pg.display.set_mode(( (1440, 1000)), pg.RESIZABLE)

pg.init()

BACKRGOUND_COLOR = (110, 60, 40)
MILITARY_COLOR = (220, 50, 50)
SCIENCE_COLOR = (50, 150, 30)
RAW_RESOURCE_COLOR = (70, 35, 25)
MANUFACTORED_RESOURCE_COLOR = (125,125,125)
COMMERCIAL_COLOR = (200, 170, 20)
CIVIC_COLOR = (0, 0, 200)
CARD_NAME_COLOR = (255, 255, 255)
PLAY_HIGHLIGHT_COLOR = (255, 255, 0)
DISCARD_HIGHLIGHT_COLOR = (255, 40, 40)
HIGHLIGHT_COLOR = PLAY_HIGHLIGHT_COLOR
DISCARD_BUTTON_COLOR = (230, 20, 20)

CARD_COLORS = {
    C.MILITARY: MILITARY_COLOR,
    C.SCIENCE: SCIENCE_COLOR,
    C.RAW_R: RAW_RESOURCE_COLOR,
    C.COMMERCIAL: COMMERCIAL_COLOR,
    C.CIVIC: CIVIC_COLOR,
    C.MFG_R: MANUFACTORED_RESOURCE_COLOR,
}

HAND_CARD_TEXT_MARGIN = 10
HAND_CARD_NAME_FONT_SIZE = 20

HAND_CARD_PROVIDES_MARGIN = (25, 4)

ROUND_DISTANCE = 5

# for hand
SHIELD_SIZE = (40, 40)
SCIENCE_SYMBOL_SIZE = (50, 50)
PROVIDES_RESOURCE_ICON_SIZE = (50, 50)
CIVIC_POINTS_SIZE = (50, 50)

HAND_CIVIC_POINTS_FONT_SIZE = 30

HAND_RESOURCE_COST_MARGIN = (3, 3)
HAND_RESOURCE_COST_SPACING = 4
HAND_RESOURCE_COST_SIZE = (17, 17)

HAND_CARD_SIZE = (144, 250)
HAND_SPACING = 20

DISCARD_BUTTON_SIZE = (100, 50)
DISCARD_BUTTON_COLOR = (240, 20, 20)
DISCARD_BUTTON_ROUND_DISTANCE = 8
DISCARD_BUTTON_MARGIN = (20, 0)
DISCARD_FONT_SIZE = 20

MONEY_MARGIN = (20, 0)
MONEY_IMAGE_SIZE = (60, 60)
MONEY_FONT_SIZE = 30

CANCEL_BUTTON_COLOR = (250, 0, 0)
CANCEL_BUTTON_SIZE = DISCARD_BUTTON_SIZE
CANCEL_BUTTON_ROUND_DISTANCE = DISCARD_BUTTON_ROUND_DISTANCE
CANCEL_FONT_SIZE = 20
CANCEL_BUTTON_MARGIN = (20, 0)

HIGHLIGHT_DISTANCE = 10
HIGHLIGHT_ROUND_DISTANCE = 4

MONEY_COST_FONT_SIZE = 10

RESOURCE_IMAGE_FILE_NAMES = {
    R.STONE: 'Images/stone.png',
    R.ORE: 'Images/ore.png',
    R.BRICK: 'Images/brick.png',
    R.WOOD: 'Images/wood.png',
    R.GLASS: 'Images/glass.png',
    R.SILK: 'Images/silk.png',
    R.PAPYRUS: 'Images/papyrus.png'
}

class View:
    def __init__(self, game, board, controller):
        self.game = game
        self.board = board
        self.controller = controller
        self.children = []

    def layout(self, screen_dimension):
        for child in self.children:
            child.layout(screen_dimension)

    def set_children(self, children):
        self.children = children

    def handle_event(self, event):
        for child in self.children:
            if child.handle_event(event):
                return True
        return False

    def draw(self):
        for child in self.children:
            child.draw()

class GameView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.hand_view = HandView(game, board, controller)
        self.discard_button_view = DiscardButtonView(game, board, controller)
        self.money_view = MoneyView(game, board, controller)
        self.set_children([self.hand_view, self.discard_button_view, self.money_view])

class MoneyView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.location = (0, 0)

    def calc_location(self, screen_dimension):
        hand = self.game.current_player_hand()
        HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
        LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
        return (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + MONEY_MARGIN[0], LAST_CARD_LOCATION[1] + MONEY_MARGIN[1] + DISCARD_BUTTON_SIZE[1] * 2)

    def draw(self):
        money_image = pg.image.load('Images/money_image.png')
        money_image = pg.transform.scale(money_image, MONEY_IMAGE_SIZE)
        screen.blit(money_image, self.location)

        money_font = pg.font.SysFont("timesnewroman", MONEY_FONT_SIZE)
        money_text = money_font.render(str(self.game.current_player().money), True, (0, 0, 0))
        money_text_rect = money_text.get_rect(center = (self.location[0] + MONEY_IMAGE_SIZE[0]/2, self.location[1] + MONEY_IMAGE_SIZE[1]/2))
        screen.blit(money_text, money_text_rect)

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

class HandView(View):
    def __init__(self, game, board, controller, max_num_cards=NUM_CARDS_PER_PLAYER):
        super().__init__(game, board, controller)
        
        #self.card_views = [CardView(game, board, controller, i) for i in range(max_num_cards)]
        self.card_views = []
        for i in range(max_num_cards):
            card_view = CardView(game, board, controller, i)
            self.card_views.append(card_view)

        self.set_children(self.card_views)
        
    def draw(self):
        hand_cards = self.game.current_player_hand()
        for i in range(len(hand_cards)):
            self.card_views[i].draw()

    def handle_event(self, event):
        hand_cards = self.game.current_player_hand()
        for i in range(len(hand_cards)):
            if self.card_views[i].handle_event(event):
                return True

        if event.type == pg.MOUSEMOTION:
            # None of the cards consumed the mouse-motion event, so the event
            # was outside of any cards bounds.  And should reset the highlight
            # card.
            self.controller.on_hand_card_mouse_over(-1)
            return True
        return False

class CardView(View):
    def __init__(self, game, board, controller, hand_card_index):
        super().__init__(game, board, controller)
        self.hand_card_index = hand_card_index
        self.location = (0, 0)

    def calc_location(self, screen_dimension):
        hand = self.game.current_player_hand()
        HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
        return ((HAND_MARGIN + self.hand_card_index * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))

    def handle_event(self, event):
        if self.is_event_inside_card():
            if event.type == pg.MOUSEMOTION:
                self.controller.on_hand_card_mouse_over(self.hand_card_index)
                return True
            elif event.type == pg.MOUSEBUTTONUP:
                self.controller.on_hand_card_mouse_down(self.hand_card_index)
                return True
        return False

    def is_event_inside_card(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + HAND_CARD_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + HAND_CARD_SIZE[1]

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

    def draw(self):
        card = self.game.current_player_hand()[self.hand_card_index]
        if self.board.is_hand_card_highlighted(self.hand_card_index):
            self.draw_highlight()
        self.draw_hand_card_background(card)
        self.draw_hand_card_name(card.name)
        self.draw_hand_card_provides(card)
        self.draw_hand_card_cost(card)

    def draw_hand_card_background(self, card):
        print(card.card_type)
        color = CARD_COLORS.get(card.card_type, (0, 0, 0))
        pg.draw.rect(screen, pg.Color(color), pg.Rect(self.location, HAND_CARD_SIZE), border_radius=int(ROUND_DISTANCE))

    def draw_hand_card_name(self, name):
        hand_card_name_font = pg.font.SysFont('georgia', HAND_CARD_NAME_FONT_SIZE)
        hand_card_name_text = hand_card_name_font.render(name, True, (255, 255, 255))
        hand_card_name_text = pg.transform.rotate(hand_card_name_text, 90)
        hand_card_name_text_length = hand_card_name_text.get_size()
        hand_card_name_location = (self.location[0] + HAND_CARD_TEXT_MARGIN, self.location[1] + HAND_CARD_SIZE[1] - HAND_CARD_TEXT_MARGIN - hand_card_name_text_length[1])
        screen.blit(hand_card_name_text, (hand_card_name_location[0], hand_card_name_location[1]))

    def draw_hand_card_provides(self, card):
        if len(card.cost) == 0 and card.money_cost == 0:
            hand_resource_margin = 0
        else:
            hand_resource_margin = 20
        if card.card_type == C.MILITARY:
            for i in range(card.num_shields):
                print("mIlLiTAry")
                shield = pg.image.load('Images/shield.png')
                shield = pg.transform.scale(shield, SHIELD_SIZE)
                shield_pos = (self.location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / card.num_shields*(i+1/2) - SHIELD_SIZE[0]/2, self.location[1])
                screen.blit(shield, (shield_pos[0], shield_pos[1]))
                print(shield_pos[0])
                print(self.location[0])
                print(HAND_CARD_SIZE[0]/2)
        elif card.card_type == C.SCIENCE:
            for i in range(len(card.provides_sciences)):
                print("science")
                tablet = pg.image.load('Images/tablet.png')
                tablet = pg.transform.scale(tablet, SCIENCE_SYMBOL_SIZE)
                tablet_pos = (self.location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / len(card.provides_sciences)*(i+1/2) - SCIENCE_SYMBOL_SIZE[0]/2, self.location[1])
                screen.blit(tablet, (tablet_pos[0], tablet_pos[1]))
        elif card.card_type == C.CIVIC:
            points_image = pg.image.load('Images/civic_points.png')
            points_image = pg.transform.scale(points_image, CIVIC_POINTS_SIZE)
            points_image_pos = (self.location[0] + HAND_CARD_SIZE[0]/2 - CIVIC_POINTS_SIZE[0]/2, self.location[1])
            screen.blit(points_image, points_image_pos)

            points_font = pg.font.SysFont('timesnewroman', HAND_CIVIC_POINTS_FONT_SIZE)
            points_text = points_font.render(str(card.points), True, (255, 255, 255))
            points_text_size = points_text.get_size()
            points_text_pos = (points_image_pos[0] + CIVIC_POINTS_SIZE[0]/2 - points_text_size[0]/2, points_image_pos[1] + CIVIC_POINTS_SIZE[1]/2 - points_text_size[1]/2 - 3)
            screen.blit(points_text, points_text_pos)

        elif card.card_type == C.RAW_R or card.card_type == C.MFG_R or card.card_type == C.COMMERCIAL:
            for a in range(len(card.provides_resources)):
                if len(card.provides_resources[a]) > 1:
                    choice_resource_hand_size = (60 - len(card.provides_resources[a])*10, 60 - len(card.provides_resources[a])*10)
                    print("size: ", choice_resource_hand_size)
                    slash_size = (choice_resource_hand_size[0]/2.5, choice_resource_hand_size[1])
                    resource_tuple = card.provides_resources[a]
                    for i in range(len(resource_tuple)):
                        resource_image = self.load_resource_image(resource=resource_tuple[i])
                        resource_image = pg.transform.scale(resource_image, choice_resource_hand_size)
                        resource_image_pos = (HAND_CARD_PROVIDES_MARGIN[0] + self.location[0] + (choice_resource_hand_size[0] + slash_size[0])*i, self.location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                        screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
                        if i != len(resource_tuple) - 1:
                            slash = pg.image.load('Images/slash.png')
                            slash = pg.transform.scale(slash, (int(slash_size[0]), int(slash_size[1])))
                            slash_pos = (resource_image_pos[0] + choice_resource_hand_size[0], self.location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                            screen.blit(slash, (slash_pos[0], slash_pos[1]))
                else:
                    resource_image = self.load_resource_image(resource=card.provides_resources[a][0])
                    resource_image = pg.transform.scale(resource_image, PROVIDES_RESOURCE_ICON_SIZE)
                    resource_image_pos = (self.location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / len(card.provides_resources)*(a+1/2) - PROVIDES_RESOURCE_ICON_SIZE[0]/2, self.location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                    screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))

    def draw_hand_card_cost(self, card):
        if len(card.cost) > 0:
            rect_size = (HAND_RESOURCE_COST_SIZE[0]/2, (HAND_RESOURCE_COST_SIZE[1] + HAND_RESOURCE_COST_SPACING)*len(card.cost) + 3)
            rect_location = (self.location[0] + HAND_RESOURCE_COST_SIZE[0]/2, self.location[1])
            pg.draw.rect(screen, pg.Color(220, 200, 210), pg.Rect((rect_location), (rect_size)))
            for i in range(len(card.cost)):
                cost = card.cost[i]
                cost_pos = (self.location[0] + HAND_RESOURCE_COST_MARGIN[0], self.location[1] + HAND_RESOURCE_COST_MARGIN[1] + (HAND_RESOURCE_COST_SPACING + HAND_RESOURCE_COST_SIZE[1]) * i)
                cost_image = self.load_resource_image(resource=cost)
                cost_image = pg.transform.scale(cost_image, HAND_RESOURCE_COST_SIZE)
                screen.blit(cost_image, cost_pos)
        elif card.money_cost > 0:
            rect_size = (HAND_RESOURCE_COST_SIZE[0]/2, (HAND_RESOURCE_COST_SIZE[1] + 3))
            rect_location = (self.location[0] + HAND_RESOURCE_COST_SIZE[0]/2, self.location[1])
            cost_pos = (self.location[0] + HAND_RESOURCE_COST_MARGIN[0], self.location[1] + HAND_RESOURCE_COST_MARGIN[1])
            pg.draw.rect(screen, pg.Color(220, 200, 210), pg.Rect((rect_location), (rect_size)))
            cost_image = pg.image.load('Images/money_image.png')
            cost_image = pg.transform.scale(cost_image, HAND_RESOURCE_COST_SIZE)
            screen.blit(cost_image, cost_pos)

            money_cost_font = pg.font.SysFont("timesnewroman", MONEY_COST_FONT_SIZE)
            money_cost_text = money_cost_font.render(str(card.money_cost), True, (0, 0, 0))
            money_cost_text_rect = money_cost_text.get_rect(center = (cost_pos[0] + HAND_RESOURCE_COST_SIZE[0]/2, cost_pos[1] + HAND_RESOURCE_COST_SIZE[1]/2))
            screen.blit(money_cost_text, money_cost_text_rect)


    def draw_highlight(self):
        highlight_color = DISCARD_HIGHLIGHT_COLOR if self.board.discard else PLAY_HIGHLIGHT_COLOR
        highlight_rect_bounds = (self.location[0] - HIGHLIGHT_DISTANCE/2, self.location[1] - HIGHLIGHT_DISTANCE/2), \
                                 (HAND_CARD_SIZE[0] + HIGHLIGHT_DISTANCE, HAND_CARD_SIZE[1] + HIGHLIGHT_DISTANCE)
        pg.draw.rect(screen,
                     pg.Color(highlight_color),
                     pg.Rect(highlight_rect_bounds),
                     border_radius=int(HIGHLIGHT_ROUND_DISTANCE))

    def load_resource_image(self, resource):
        return pg.image.load(RESOURCE_IMAGE_FILE_NAMES[resource])

class DiscardButtonView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.set_children([])
        self.location = (0, 0)

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

    def calc_location(self, screen_dimension):
        hand = self.game.current_player_hand()
        HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
        LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
        return (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1])

    def draw(self):
        if not self.board.discard:
            self.draw_discard_button()
        else:
            self.draw_cancel_button()

    def draw_discard_button(self):
        pg.draw.rect(screen, pg.Color(DISCARD_BUTTON_COLOR), pg.Rect(self.location, DISCARD_BUTTON_SIZE), border_radius=int(DISCARD_BUTTON_ROUND_DISTANCE))
        discard_font = pg.font.SysFont("georgia", DISCARD_FONT_SIZE)
        discard_text = discard_font.render("Discard", True, (0, 0, 0))
        discard_text_rect = discard_text.get_rect(center = (self.location[0] + DISCARD_BUTTON_SIZE[0]/2, self.location[1] + DISCARD_BUTTON_SIZE[1]/2))
        screen.blit(discard_text, discard_text_rect)

    def draw_cancel_button(self):
        pg.draw.rect(screen, pg.Color(CANCEL_BUTTON_COLOR), pg.Rect(self.location, CANCEL_BUTTON_SIZE), border_radius=int(CANCEL_BUTTON_ROUND_DISTANCE))
        cancel_font = pg.font.SysFont("georgia", CANCEL_FONT_SIZE)
        cancel_text = cancel_font.render("Cancel", True, (0, 0, 0))
        cancel_text_rect = cancel_text.get_rect(center = (self.location[0] + CANCEL_BUTTON_SIZE[0]/2, self.location[1] + CANCEL_BUTTON_SIZE[1]/2))
        screen.blit(cancel_text, cancel_text_rect)

    def is_event_inside_discard_button(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + DISCARD_BUTTON_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + DISCARD_BUTTON_SIZE[1]
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONUP:
            if self.is_event_inside_discard_button():
                self.controller.on_discard_button_pressed()
                return True
        return False