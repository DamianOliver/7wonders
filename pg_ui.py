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


card_highlighted = 1
discard = False

class PgUi:
    def __init__(self):
        self.game = Game()

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
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.VIDEORESIZE:
                    screen_dimension = pg.display.get_surface().get_size()
                    HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
                    LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
                    DISCARD_BUTTON_LOCATION = (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1])
                    print(screen_dimension)
                    self.draw_game()
                    pg.display.update()
                    pg.display.update()
                elif event.type == pg.MOUSEMOTION:
                    self.highlight_card()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pos()[0] > DISCARD_BUTTON_LOCATION[0] and pg.mouse.get_pos()[0] < DISCARD_BUTTON_LOCATION[0] + DISCARD_BUTTON_SIZE[0] and pg.mouse.get_pos()[1] > DISCARD_BUTTON_LOCATION[1] and pg.mouse.get_pos()[1] < DISCARD_BUTTON_LOCATION[1] + DISCARD_BUTTON_SIZE[1]:
                        if discard:
                            discard = False
                            self.draw_discard_button()
                        else:
                            discard = True
                            self.draw_discard_button()
                    hand = self.game.current_player_hand()
                    for i in range(len(hand)):
                        card_location = ((HAND_MARGIN + i * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
                        if pg.mouse.get_pos()[0] > card_location[0] and pg.mouse.get_pos()[0] < card_location[0] + HAND_CARD_SIZE[0] and pg.mouse.get_pos()[1] > card_location[1] and pg.mouse.get_pos()[1] < card_location[1] + HAND_CARD_SIZE[1]:
                            if discard:
                                self.discard_card(i)
                                #self.draw_game()
                                self.highlight_card()
                                print("BREAK")
                                break
                            else:
                                self.select_card(i)
                                #self.draw_game()
                                self.highlight_card()
                                print("BREAK")
                                break
                break
        print("pls pls give much help")

    # def draw_money(self, money)


    def highlight_card(self):
        global card_highlighted
        global HIGHLIGHT_COLOR
        card_fails = 0
        hand = self.game.current_player_hand()
        for i in range(len(hand)):
            card_location = ((HAND_MARGIN + i * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
            if pg.mouse.get_pos()[0] > card_location[0] and pg.mouse.get_pos()[0] < card_location[0] + HAND_CARD_SIZE[0] and pg.mouse.get_pos()[1] > card_location[1] and pg.mouse.get_pos()[1] < card_location[1] + HAND_CARD_SIZE[1]:
                if hand[i] != card_highlighted:
                    if discard:
                        HIGHLIGHT_COLOR = DISCARD_HIGHLIGHT_COLOR
                    else:
                        HIGHLIGHT_COLOR = PLAY_HIGHLIGHT_COLOR
                    self.draw_game()
                    card_highlighted = hand[i]
                    pg.draw.rect(screen, pg.Color(HIGHLIGHT_COLOR), pg.Rect((card_location[0] - HIGHLIGHT_DISTANCE/2, card_location[1] - HIGHLIGHT_DISTANCE/2), (HAND_CARD_SIZE[0] + HIGHLIGHT_DISTANCE, HAND_CARD_SIZE[1] + HIGHLIGHT_DISTANCE)), border_radius=int(HIGHLIGHT_ROUND_DISTANCE))
                    self.draw_card(hand[i], i, hand)
                    pg.display.update((card_location[0] - HIGHLIGHT_DISTANCE/2, card_location[1] - HIGHLIGHT_DISTANCE/2), (HAND_CARD_SIZE[0] + HIGHLIGHT_DISTANCE, HAND_CARD_SIZE[1] + HIGHLIGHT_DISTANCE))
            else:
                card_fails += 1
                if card_fails == len(hand):
                    if card_highlighted != 1:
                        self.draw_game()
                        card_highlighted = 1
                        pg.display.update()

    def draw_game(self):
        print("drawing stuff")
        screen.fill(BACKRGOUND_COLOR)
        self.draw_hand()
        self.draw_discard_button()

    def draw_discard_button(self):
        if not discard:
            pg.draw.rect(screen, pg.Color(DISCARD_BUTTON_COLOR), pg.Rect((DISCARD_BUTTON_LOCATION[0], DISCARD_BUTTON_LOCATION[1]), (DISCARD_BUTTON_SIZE[0], DISCARD_BUTTON_SIZE[1])), border_radius=int(DISCARD_BUTTON_ROUND_DISTANCE))
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
        pg.draw.rect(screen, pg.Color(CANCEL_BUTTON_COLOR), pg.Rect((CANCEL_BUTTON_LOCATION[0], CANCEL_BUTTON_LOCATION[1]), (CANCEL_BUTTON_SIZE[0], CANCEL_BUTTON_SIZE[1])), border_radius=int(CANCEL_BUTTON_ROUND_DISTANCE))
        cancel_font = pg.font.SysFont("georgia", CANCEL_FONT_SIZE)
        cancel_text = cancel_font.render("Cancel", True, (0, 0, 0))
        cancel_text_rect = cancel_text.get_rect(center = (CANCEL_BUTTON_LOCATION[0] + CANCEL_BUTTON_SIZE[0]/2, CANCEL_BUTTON_LOCATION[1] + CANCEL_BUTTON_SIZE[1]/2))
        screen.blit(cancel_text, cancel_text_rect)
        pg.display.update()

    def draw_hand_card_background(self, card, card_location):
        print(card.card_type)
        if card.card_type == C.MILITARY:
            pg.draw.rect(screen, pg.Color(MILITARY_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))
        elif card.card_type == C.SCIENCE:
            pg.draw.rect(screen, pg.Color(SCIENCE_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))
        elif card.card_type == C.RAW_R:
            pg.draw.rect(screen, pg.Color(RAW_RESOURCE_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))
        elif card.card_type == C.COMMERCIAL:
            pg.draw.rect(screen, pg.Color(COMMERCIAL_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))
        elif card.card_type == C.MFG_R:
            pg.draw.rect(screen, pg.Color(MANUFACTORED_RESOURCE_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))
        elif card.card_type == C.CIVIC:
            pg.draw.rect(screen, pg.Color(CIVIC_COLOR), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))
        else:
            pg.draw.rect(screen, pg.Color(0, 0, 0), pg.Rect((card_location[0], card_location[1]), (HAND_CARD_SIZE[0], HAND_CARD_SIZE[1])), border_radius=int(ROUND_DISTANCE))

    def draw_hand_card_name(self, name, card_location):
        hand_card_name_font = pg.font.SysFont('georgia', HAND_CARD_NAME_FONT_SIZE)
        hand_card_name_text = hand_card_name_font.render(name, True, (255, 255, 255))
        hand_card_name_text = pg.transform.rotate(hand_card_name_text, 90)
        hand_card_name_text_length = hand_card_name_text.get_size()
        hand_card_name_location = (card_location[0] + HAND_CARD_TEXT_MARGIN, card_location[1] + HAND_CARD_SIZE[1] - HAND_CARD_TEXT_MARGIN - hand_card_name_text_length[1])
        screen.blit(hand_card_name_text, (hand_card_name_location[0], hand_card_name_location[1]))

    def draw_hand_card_provides(self, card_location, card):
        if len(card.cost) == 0 and card.money_cost == 0:
            hand_resource_margin = 0
        else:
            hand_resource_margin = 20
        if card.card_type == C.MILITARY:
            for i in range(card.num_shields):
                print("mIlLiTAry")
                shield = pg.image.load('Images/shield.png')
                shield = pg.transform.scale(shield, SHIELD_SIZE)
                shield_pos = (card_location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / card.num_shields*(i+1/2) - SHIELD_SIZE[0]/2, card_location[1])
                screen.blit(shield, (shield_pos[0], shield_pos[1]))
                print(shield_pos[0])
                print(card_location[0])
                print(HAND_CARD_SIZE[0]/2)
        elif card.card_type == C.SCIENCE:
            for i in range(len(card.provides_sciences)):
                print("science")
                tablet = pg.image.load('Images/tablet.png')
                tablet = pg.transform.scale(tablet, SCIENCE_SYMBOL_SIZE)
                tablet_pos = (card_location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / len(card.provides_sciences)*(i+1/2) - SCIENCE_SYMBOL_SIZE[0]/2, card_location[1])
                screen.blit(tablet, (tablet_pos[0], tablet_pos[1]))
        elif card.card_type == C.CIVIC:
            points_image = pg.image.load('Images/civic_points.png')
            points_image = pg.transform.scale(points_image, CIVIC_POINTS_SIZE)
            points_image_pos = (card_location[0] + HAND_CARD_SIZE[0]/2 - CIVIC_POINTS_SIZE[0]/2, card_location[1])
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
                        if resource_tuple[i] == R.STONE:
                            resource_image = pg.image.load('Images/stone.png')
                        elif resource_tuple[i] == R.BRICK:
                            resource_image = pg.image.load('Images/brick.png')
                        elif resource_tuple[i] == R.ORE:
                            resource_image = pg.image.load('Images/ore.png')
                        elif resource_tuple[i] == R.WOOD:
                            resource_image = pg.image.load('Images/wood.png')
                        elif resource_tuple[i] == R.SILK:
                            resource_image = pg.image.load('Images/silk.png')
                        elif resource_tuple[i] == R.GLASS:
                            resource_image = pg.image.load('Images/glass.png')
                        elif resource_tuple[i] == R.PAPYRUS:
                            resource_image = pg.image.load('Images/papyrus.png')

                        resource_image = pg.transform.scale(resource_image, choice_resource_hand_size)
                        resource_image_pos = (HAND_CARD_PROVIDES_MARGIN[0] + card_location[0] + (choice_resource_hand_size[0] + slash_size[0])*i, card_location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                        screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
                        if i != len(resource_tuple) - 1:
                            slash = pg.image.load('Images/slash.png')
                            slash = pg.transform.scale(slash, (int(slash_size[0]), int(slash_size[1])))
                            slash_pos = (resource_image_pos[0] + choice_resource_hand_size[0], card_location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                            screen.blit(slash, (slash_pos[0], slash_pos[1]))

                else:
                    if card.provides_resources[a] == (R.STONE,):
                        resource_image = pg.image.load('Images/stone.png')
                    elif card.provides_resources[a] == (R.BRICK,):
                        resource_image = pg.image.load('Images/brick.png')
                    elif card.provides_resources[a] == (R.ORE,):
                        resource_image = pg.image.load('Images/ore.png')
                    elif card.provides_resources[a] == (R.WOOD,):
                        resource_image = pg.image.load('Images/wood.png')
                    elif card.provides_resources[a] == (R.SILK,):
                        resource_image = pg.image.load('Images/silk.png')
                    elif card.provides_resources[a] == (R.GLASS,):
                        resource_image = pg.image.load('Images/glass.png')
                    elif card.provides_resources[a] == (R.PAPYRUS,):
                        resource_image = pg.image.load('Images/papyrus.png')
                    else:
                        return
                    resource_image = pg.transform.scale(resource_image, PROVIDES_RESOURCE_ICON_SIZE)
                    resource_image_pos = (card_location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / len(card.provides_resources)*(a+1/2) - PROVIDES_RESOURCE_ICON_SIZE[0]/2, card_location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                    screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))

    def draw_hand_card_cost(self, card, card_location):
        if len(card.cost) > 0:
            rect_size = (HAND_RESOURCE_COST_SIZE[0]/2, (HAND_RESOURCE_COST_SIZE[1] + HAND_RESOURCE_COST_SPACING)*len(card.cost) + 3)
            rect_location = (card_location[0] + HAND_RESOURCE_COST_SIZE[0]/2, card_location[1])
            pg.draw.rect(screen, pg.Color(220, 200, 210), pg.Rect((rect_location), (rect_size)))
            for i in range(len(card.cost)):
                cost = card.cost[i]
                cost_pos = (card_location[0] + HAND_RESOURCE_COST_MARGIN[0], card_location[1] + HAND_RESOURCE_COST_MARGIN[1] + (HAND_RESOURCE_COST_SPACING + HAND_RESOURCE_COST_SIZE[1]) * i)
                if cost == R.STONE:
                    cost_image = pg.image.load('Images/stone.png')
                elif cost == R.ORE:
                    cost_image = pg.image.load('Images/ore.png')
                elif cost == R.BRICK:
                    cost_image = pg.image.load('Images/brick.png')
                elif cost == R.WOOD:
                    cost_image = pg.image.load('Images/wood.png')
                elif cost == R.GLASS:
                    cost_image = pg.image.load('Images/glass.png')
                elif cost == R.SILK:
                    cost_image = pg.image.load('Images/silk.png')
                elif cost == R.PAPYRUS:
                    cost_image = pg.image.load('Images/papyrus.png')
                cost_image = pg.transform.scale(cost_image, HAND_RESOURCE_COST_SIZE)
                screen.blit(cost_image, cost_pos)

    def draw_card(self, card, i, hand_cards):
        card_location = ((HAND_MARGIN + i * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2))
        self.draw_hand_card_background(card, card_location)
        self.draw_hand_card_name(card.name ,card_location)
        self.draw_hand_card_provides(card_location, card)
        self.draw_hand_card_cost(card, card_location)

    def draw_hand(self):
        hand_cards = self.game.current_player_hand()
        for i in range(len(hand_cards)):
            self.draw_card(hand_cards[i], i, hand_cards)

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
