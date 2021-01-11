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
PLAY_HIGHLIGHT_COLOR = (255, 255, 0)
DISCARD_HIGHLIGHT_COLOR = (255, 40, 40)
HIGHLIGHT_COLOR = PLAY_HIGHLIGHT_COLOR
DISCARD_BUTTON_COLOR = (230, 20, 20)
WONDER_COLOR = (20, 20, 230)

CARD_COLORS = {
    C.MILITARY: MILITARY_COLOR,
    C.SCIENCE: SCIENCE_COLOR,
    C.RAW_R: RAW_RESOURCE_COLOR,
    C.COMMERCIAL: COMMERCIAL_COLOR,
    C.CIVIC: CIVIC_COLOR,
}

HAND_CARD_TEXT_MARGIN = 10
HAND_CARD_NAME_FONT_SIZE = 20

HAND_CARD_PROVIDES_MARGIN = (25, 4)

i = 0
hand = Game().hands[(i + Game().turn) % len(Game().hands)]

HAND_SPACING = screen_dimension[0]/30
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
HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2

DISCARD_BUTTON_SIZE = (100, 50)
DISCARD_BUTTON_COLOR = (240, 20, 20)
DISCARD_BUTTON_ROUND_DISTANCE = 8
DISCARD_BUTTON_MARGIN = (20, 0)
DISCARD_FONT_SIZE = 20

LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))

DISCARD_BUTTON_LOCATION = (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1])

CANCEL_BUTTON_COLOR = (250, 0, 0)
CANCEL_BUTTON_SIZE = DISCARD_BUTTON_SIZE
CANCEL_BUTTON_ROUND_DISTANCE = DISCARD_BUTTON_ROUND_DISTANCE
CANCEL_BUTTON_LOCATION = DISCARD_BUTTON_LOCATION
CANCEL_FONT_SIZE = 20
CANCEL_BUTTON_MARGIN = (20, 0)

HIGHLIGHT_DISTANCE = 10
HIGHLIGHT_ROUND_DISTANCE = 4

RESOURCE_IMAGE_FILE_NAMES = {
    R.STONE: 'Images/stone.png',
    R.ORE: 'Images/ore.png',
    R.BRICK: 'Images/brick.png',
    R.WOOD: 'Images/wood.png',
    R.GLASS: 'Images/glass.png',
    R.SILK: 'Images/silk.png',
    R.PAPYRUS: 'Images/papyrus.png'
}

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

class Board:
    def __init__(self):
        self.discard = False
        self.highlight_card_index = -1
        self.needs_redraw = False

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
        self.board.update_hand_card_highlight(hand_card_index)

    def on_hand_card_mouse_down(self, hand_card_index):
        if self.board.discard:
            self.discard_card(hand_card_index)
        else:
            self.select_card(hand_card_index)
        return

    def discard_card(self, selected_card_number):
        hand = self.game.current_player_hand()
        print("discarrrrrrrrrrrrrrrrd")
        del hand[selected_card_number]
        self.game.current_player_index.give_moneys_for_discard()
        print("MONEY: ", player.money)
        self.game.current_player_finished()

    def select_card(self, selected_card_number):
        hand = self.game.current_player_hand()
        print("selecting a card!!!")
        selected_card = hand[selected_card_number]

        if self.game.current_player().play_card(selected_card):
            del hand[selected_card_number]

        self.game.current_player_finished()


class GameView:
    def __init__(self, game, board, controller):
        self.hand_view = HandView(game, board, controller)

    def handle_event(self, event):
        return self.hand_view.handle_event(event)

    def draw(self):
        self.hand_view.draw()

class HandView:
    def __init__(self, game, board, controller, max_num_cards=NUM_CARDS_PER_PLAYER):
        self.game = game
        self.controller = controller
        self.card_views = [CardView(game, board, controller, i) for i in range(max_num_cards)]

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
            # None of the cards consumed the mouse-motiokn event, so the event
            # was outside of any cards bounds.  And should reset the highlight
            # card.
            self.controller.on_hand_card_mouse_over(-1)
            return True
        return False

class CardView:
    def __init__(self, game, board, controller, hand_card_index):
        self.game = game
        self.board = board
        self.controller = controller
        self.hand_card_index = hand_card_index
        self.location = self.calc_location(hand_card_index)

    def calc_location(self, card_index):
        return ((HAND_MARGIN + card_index * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))

    def handle_event(self, event):
        if self.is_event_inside_card():
            if event.type == pg.MOUSEMOTION:
                self.controller.on_hand_card_mouse_over(self.hand_card_index)
                return True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.controller.on_hand_card_mouse_down(self.hand_card_index)
                return True
        return False

    def is_event_inside_card(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + HAND_CARD_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + HAND_CARD_SIZE[1]

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
        card_rect = pg.Rect(self.location, HAND_CARD_SIZE)
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
