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

import pygame as pg
from game import NUM_CARDS_PER_PLAYER, C, R, S, Game

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
GUILD_COLOR = (75, 0, 130)
WONDER_C_COLOR = (0, 0, 0)
CARD_NAME_COLOR = (255, 255, 255)
PLAY_HIGHLIGHT_COLOR = (255, 255, 0)
DISCARD_HIGHLIGHT_COLOR = (255, 40, 40)
WONDER_HIGHLIGHT_COLOR = (0, 0, 255)
HIGHLIGHT_COLOR = PLAY_HIGHLIGHT_COLOR
DISCARD_BUTTON_COLOR = (230, 20, 20)
WONDER_BUTTON_COLOR = (255, 255, 20)
All_CARDS_VIEW_BUTTON_COLOR = (40, 200, 50)

BLAND_VALUE = 1

CARD_COLORS = {
    C.MILITARY: MILITARY_COLOR,
    C.SCIENCE: SCIENCE_COLOR,
    C.RAW_R: RAW_RESOURCE_COLOR,
    C.COMMERCIAL: COMMERCIAL_COLOR,
    C.CIVIC: CIVIC_COLOR,
    C.MFG_R: MANUFACTORED_RESOURCE_COLOR,
    C.GUILD: GUILD_COLOR,
    C.WONDER_C: WONDER_C_COLOR,
    C.WONDER_START: WONDER_C_COLOR
}

HAND_CARD_TEXT_MARGIN = 10
HAND_CARD_NAME_FONT_SIZE = 15

HAND_CARD_COUPON_MARGIN = [2, 10]
HAND_CARD_COUPON_FONT_SIZE = 12
COUPON_OFFSET = 3

HAND_CARD_PROVIDES_MARGIN = (25, 4)

ROUND_DISTANCE = 7

# for hand
SHIELD_SIZE = (40, 40)
SCIENCE_SYMBOL_SIZE = (50, 50)
PROVIDES_RESOURCE_ICON_SIZE = (50, 50)
CIVIC_POINTS_SIZE = (50, 50)
PROVIDES_MONEY_SIZE = (50, 50)
PROVIDES_MONEY_FONT_SIZE = 30

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

BUTTON_MARGIN = 10

WONDER_BUTTON_SIZE = (100, 50)
WONDER_BUTTON_COLOR = (50, 50, 255)
WONDER_BUTTON_ROUND_DISTANCE = 8
WONDER_BUTTON_MARGIN = (20, 0)
WONDER_FONT_SIZE = 20

WONDER_HIGHLIGHT_DISTANCE = 3

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

PLAYER_VIEW_BACKGROUND_COLOR = (128, 128, 128)
PLAYER_VIEW_BACKGROUND_SIZE = (300, 200)
PLAYER_VIEW_ROUND_DISTANCE = 8

SELF_FILE_HEIGHT = 20
SELF_LABEL_HEIGHT = 45
SELF_LABEL_FONT_SIZE = 20
SELF_FILE_FONT_SIZE = 15
NUM_FILES = 7
FILE_THICKNESS = 4
FILE_PROVIDES_IMAGE_SIZE = (17, 17)
FILE_SCIENCE_OPTIONS_IMAGE_SIZE = (67, 17)
FILE_PROVIDES_FONT_SIZE = 15
FILE_SLASH_SIZE = (8, 14)

ALL_CARDS_SIZE = (144, 250)
ALL_CARDS_SPACING = 10
ALL_CARDS_MARGIN = (30, 30)

# 176 by 225

WAR_TOKENS_OFFSET = (20, 20)
MINUS_TOKEN_SIZE = [40, 40]
ONE_TOKEN_SIZE = [39, 50]
THREE_TOKEN_SIZE = [47, 60]
FIVE_TOKEN_SIZE = [55, 70]

TOKEN_SPACING = 10

BACK_ARROW_SIZE = (50, 50)

NEIGHBOR_RESOURCE_SIZE = (40, 40)
NEIGHBOR_SLASH_SIZE = (19, 36)

ADJ_RAW_COST_SIZE = [120, 43]
ADJ_MFC_COST_SIZE = [100, 43]

ADJ_MONEY_OFFSET = (30, -80 - ADJ_RAW_COST_SIZE[1])
ADJ_MONEY_SIZE = (40, 40)
ADJ_MONEY_TEXT_SIZE = 23

WONDER_BOARD_SIZE = (800, 300)

ALL_CARDS_VIEW_BUTTON_SIZE = (WONDER_BOARD_SIZE[0] - 150, SELF_LABEL_HEIGHT - FILE_THICKNESS)

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
        self.wonder_button_view = WonderButtonView(game, board, controller)
        self.money_view = MoneyView(game, board, controller)
        self.self_view = SelfView(game, board, controller)
        self.adjacent_resource_view = AdjacentResourceView(game, board, controller)
        self.all_cards_view_button = AllCardsViewButton(game, board, controller)
        self.all_cards_view = AllCardsView(game, board, controller)

        location_index = 0
        player_view_list = []
        for i in range(len(self.game.players)):
            self.player_view = PlayerView(game, board, controller, location_index, i)
            player_view_list.append(self.player_view)
            location_index += 1

        self.set_children([self.hand_view, self.discard_button_view, self.wonder_button_view, self.money_view, self.self_view, self.adjacent_resource_view, self.all_cards_view_button])
        self.children += player_view_list
        self.children.append(self.all_cards_view)

    # def handle_event(self, event):
    #     #handle P
    #     return super().handle_event(event)

class SelfView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.location = (0, 0)
        self.player_index = self.game.current_player_index

    def bland(self, color):
        color_average = (color[0] + color[1] + color[2]) / 3
        bland_color = ((color[0] * BLAND_VALUE + color_average) / 2, (color[1] * BLAND_VALUE + color_average) / 2, (color[2] * BLAND_VALUE + color_average) / 2)
        return bland_color

    def draw(self):
        current_player = self.game.players[self.game.current_player_index]
        if current_player.wonder_selected:
            self.draw_wonder_board_highlight()
        self.draw_wonder_board(current_player)
        self.draw_raw_resources(current_player)
        self.draw_manufactored_resources(current_player)
        self.draw_military(current_player)
        self.draw_science(current_player)
        self.draw_civic(current_player)
        self.draw_commercial(current_player)
        self.draw_guilds(current_player)
        self.draw_labels()

    def draw_wonder_board(self, player):
        h_offset = 0
        if player.wonder_selected:
            h_offset = WONDER_HIGHLIGHT_DISTANCE
        # subract h offset from 
        board_image = player.wonder.image
        scaled_image = pg.transform.smoothscale(board_image, (WONDER_BOARD_SIZE[0], WONDER_BOARD_SIZE[1] - 2 * h_offset))

        screen.blit(scaled_image, (self.location[0], self.location[1] + WONDER_HIGHLIGHT_DISTANCE))

        shading_list = [[WONDER_BOARD_SIZE[0], 0], [WONDER_BOARD_SIZE[0], 282, 0], [WONDER_BOARD_SIZE[0], 530, 290, 0], [WONDER_BOARD_SIZE[0], 612, 393, 180, 0]]

        shading_value = shading_list[len(player.wonder.layers_list) - 2][player.wonder_level]

        shading_size = (shading_value - h_offset * 2, WONDER_BOARD_SIZE[1] - h_offset * 2)
        shading_location = (self.location[0] + WONDER_BOARD_SIZE[0] - shading_value + h_offset, self.location[1] + h_offset)

        greyout = pg.Surface(shading_size)
        greyout.set_alpha(190)
        greyout.fill((50, 50, 50))

        screen.blit(greyout, shading_location)

    def draw_wonder_board_highlight(self):
        highlight_size = [WONDER_BOARD_SIZE[0] + 2 * WONDER_HIGHLIGHT_DISTANCE, WONDER_BOARD_SIZE[1] + WONDER_HIGHLIGHT_DISTANCE]
        highlight_location = [self.location[0] - WONDER_HIGHLIGHT_DISTANCE, self.location[1]]

        pg.draw.rect(screen, HIGHLIGHT_COLOR, pg.Rect(highlight_location, highlight_size), border_radius=int(ROUND_DISTANCE))

    def is_event_inside_wonder_board(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + WONDER_BOARD_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + WONDER_BOARD_SIZE[1]

    def handle_event(self, event):
        if self.is_event_inside_wonder_board():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.controller.on_wonder_board_selected()
                return True
        return False

    def load_resource_image(self, resource):
        return pg.image.load(RESOURCE_IMAGE_FILE_NAMES[resource])

    def draw_labels(self):
        pg.draw.rect(screen, (10, 10, 10), ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - FILE_THICKNESS), (WONDER_BOARD_SIZE[0], FILE_THICKNESS)))
        pg.draw.rect(screen, (10, 10, 10), ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT - FILE_THICKNESS), (WONDER_BOARD_SIZE[0], FILE_THICKNESS)))
        pg.draw.rect(screen, (10, 10, 10), ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT - FILE_THICKNESS), (FILE_THICKNESS, SELF_LABEL_HEIGHT)))
        pg.draw.rect(screen, (10, 10, 10), ((self.location[0] + WONDER_BOARD_SIZE[0] - FILE_THICKNESS, self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT - FILE_THICKNESS), (FILE_THICKNESS, SELF_LABEL_HEIGHT)))
        pg.draw.rect(screen, (10, 10, 10), ((self.location[0] - FILE_THICKNESS + 80, self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT - FILE_THICKNESS), (FILE_THICKNESS, SELF_LABEL_HEIGHT + SELF_FILE_HEIGHT * NUM_FILES + FILE_THICKNESS)))
        pg.draw.rect(screen, (10, 10, 10), ((self.location[0] + WONDER_BOARD_SIZE[0] - 70, self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT - FILE_THICKNESS), (FILE_THICKNESS, SELF_LABEL_HEIGHT + SELF_FILE_HEIGHT * NUM_FILES + FILE_THICKNESS)))

        label_font_1 = pg.font.SysFont("timesnewroman", SELF_LABEL_FONT_SIZE)
        label_text_1 = label_font_1.render(("# of"), True, (0, 0, 0))
        label_text_1_rect = label_text_1.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT + SELF_FILE_HEIGHT / 2 + FILE_THICKNESS ))
        screen.blit(label_text_1, label_text_1_rect)

        label_font_2 = pg.font.SysFont("timesnewroman", SELF_LABEL_FONT_SIZE)
        label_text_2 = label_font_2.render(("cards"), True, (0, 0, 0))
        label_text_2_rect = label_text_2.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT + SELF_FILE_HEIGHT * 1.25 + FILE_THICKNESS))
        screen.blit(label_text_2, label_text_2_rect)

        label_font_3 = pg.font.SysFont("timesnewroman", SELF_LABEL_FONT_SIZE)
        label_text_3 = label_font_3.render(("total"), True, (0, 0, 0))
        label_text_3_rect = label_text_3.get_rect(center = (self.location[0] + WONDER_BOARD_SIZE[0] - 35, self.location[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT + SELF_LABEL_HEIGHT / 2))
        screen.blit(label_text_3, label_text_3_rect)

    def draw_raw_resources(self, player):
        bland_raw_resource_color = self.bland(RAW_RESOURCE_COLOR)
        pg.draw.rect(screen, bland_raw_resource_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * NUM_FILES), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        total_stone = 0
        total_ore = 0
        total_brick = 0
        total_wood = 0
        either_or_list = []
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.RAW_R:
                total_cards += 1
                for provides in card.provides_resources:
                    if provides == (R.STONE,):
                        total_stone += 1
                    elif provides == (R.ORE,):
                        total_ore += 1
                    elif provides == (R.BRICK,):
                        total_brick += 1
                    elif provides == (R.WOOD,):
                        total_wood += 1
                    elif len(provides) > 1:
                        either_or_list.append(card)
        
        for i in range(total_stone):
            stone_image = pg.image.load('Images/stone.png')
            stone_image = pg.transform.smoothscale(stone_image, FILE_PROVIDES_IMAGE_SIZE)
            stone_image_pos = (self.location[0] + 84 + (i * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - NUM_FILES * SELF_FILE_HEIGHT)
            screen.blit(stone_image, stone_image_pos)

        for i in range(total_ore):
            ore_image = pg.image.load('Images/ore.png')
            ore_image = pg.transform.smoothscale(ore_image, FILE_PROVIDES_IMAGE_SIZE)
            ore_image_pos = (self.location[0] + 84 + ((i + total_stone) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - NUM_FILES * SELF_FILE_HEIGHT)
            screen.blit(ore_image, ore_image_pos)

        for i in range(total_brick):
            brick_image = pg.image.load('Images/brick.png')
            brick_image = pg.transform.smoothscale(brick_image, FILE_PROVIDES_IMAGE_SIZE)
            brick_image_pos = (self.location[0] + 84 + ((i + total_stone + total_ore) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - NUM_FILES * SELF_FILE_HEIGHT)
            screen.blit(brick_image, brick_image_pos)

        for i in range(total_wood):
            wood_image = pg.image.load('Images/wood.png')
            wood_image = pg.transform.smoothscale(wood_image, FILE_PROVIDES_IMAGE_SIZE)
            wood_image_pos = (self.location[0] + 84 + ((i + total_stone + total_ore + total_brick) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - NUM_FILES * SELF_FILE_HEIGHT)
            screen.blit(wood_image, wood_image_pos)

        total_spacing = 0
        for card in either_or_list:
            if total_cards > 1:
                total_spacing += 10
            for i in range(len(card.provides_resources[0])):
                resource_image = self.load_resource_image(resource=card.provides_resources[0][i])
                resource_image = pg.transform.smoothscale(resource_image, FILE_PROVIDES_IMAGE_SIZE)
                resource_image_pos = (self.location[0] + 84 + ((total_stone + total_ore + total_brick + total_wood) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])) + total_spacing, self.location[1] - NUM_FILES * SELF_FILE_HEIGHT)
                screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
                total_spacing += (FILE_PROVIDES_IMAGE_SIZE[0] + 4)
                if i != len(card.provides_resources[0]) - 1:
                    slash = pg.image.load('Images/slash.png')
                    slash = pg.transform.smoothscale(slash, FILE_SLASH_SIZE)
                    slash_pos = (self.location[0] + 85 + ((total_stone + total_ore + total_brick + total_wood) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])) + total_spacing, self.location[1] - NUM_FILES * SELF_FILE_HEIGHT)
                    screen.blit(slash, (slash_pos[0], slash_pos[1]))
                    total_spacing += (FILE_SLASH_SIZE[0] + 2)
            


        total_cards_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_cards_font = total_cards_font.render((str(total_cards)), True, (255, 255, 255))
        total_cards_font_rect = total_cards_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 1) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_cards_font, total_cards_font_rect)

    def draw_manufactored_resources(self, player):
        bland_manufactored_resource_color = self.bland(MANUFACTORED_RESOURCE_COLOR)
        pg.draw.rect(screen, bland_manufactored_resource_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 1)), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        total_glass = 0
        total_papyrus = 0
        total_silk = 0
        either_or_list = []
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.MFG_R:
                total_cards += 1
                for provides in card.provides_resources:
                    if provides == (R.GLASS,):
                        total_glass += 1
                    elif provides == (R.PAPYRUS,):
                        total_papyrus += 1
                    elif provides == (R.SILK,):
                        total_silk += 1
                    elif len(provides) > 1:
                        either_or_list.append(card)
        
        for i in range(total_glass):
            glass_image = pg.image.load('Images/glass.png')
            glass_image = pg.transform.smoothscale(glass_image, FILE_PROVIDES_IMAGE_SIZE)
            glass_image_pos = (self.location[0] + 84 + (i * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - (NUM_FILES - 1) * SELF_FILE_HEIGHT)
            screen.blit(glass_image, glass_image_pos)

        for i in range(total_papyrus):
            papyrus_image = pg.image.load('Images/papyrus.png')
            papyrus_image = pg.transform.smoothscale(papyrus_image, FILE_PROVIDES_IMAGE_SIZE)
            papyrus_image_pos = (self.location[0] + 84 + ((i + total_glass) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - (NUM_FILES - 1) * SELF_FILE_HEIGHT)
            screen.blit(papyrus_image, papyrus_image_pos)

        for i in range(total_silk):
            silk_image = pg.image.load('Images/silk.png')
            silk_image = pg.transform.smoothscale(silk_image, FILE_PROVIDES_IMAGE_SIZE)
            silk_image_pos = (self.location[0] + 84 + ((i + total_glass + total_papyrus) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])), self.location[1] - (NUM_FILES - 1) * SELF_FILE_HEIGHT)
            screen.blit(silk_image, silk_image_pos)

        total_spacing = 0
        for card in either_or_list:
            if total_cards > 1:
                total_spacing += 10
            for i in range(len(card.provides_resources[0])):
                resource_image = self.load_resource_image(resource=card.provides_resources[0][i])
                resource_image = pg.transform.smoothscale(resource_image, FILE_PROVIDES_IMAGE_SIZE)
                resource_image_pos = (self.location[0] + 84 + ((total_glass + total_papyrus + total_silk) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])) + total_spacing, self.location[1] - (NUM_FILES - 1) * SELF_FILE_HEIGHT)
                screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
                total_spacing += (FILE_PROVIDES_IMAGE_SIZE[0] + 4)
                if i != len(card.provides_resources[0]) - 1:
                    slash = pg.image.load('Images/slash.png')
                    slash = pg.transform.smoothscale(slash, FILE_SLASH_SIZE)
                    slash_pos = (self.location[0] + 85 + ((total_glass + total_papyrus + total_silk) * (4 + FILE_PROVIDES_IMAGE_SIZE[0])) + total_spacing, self.location[1] - (NUM_FILES - 1) * SELF_FILE_HEIGHT)
                    screen.blit(slash, (slash_pos[0], slash_pos[1]))
                    total_spacing += (FILE_SLASH_SIZE[0] + 2)

        total_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_font = total_font.render((str(total_cards)), True, (0, 0, 0))
        total_font_3_rect = total_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 2) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_font, total_font_3_rect)

    def draw_military(self, player):
        bland_military_color = self.bland(MILITARY_COLOR)
        pg.draw.rect(screen, bland_military_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 2)), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.MILITARY:
                total_cards += 1

        for i in range(player.num_shields):
            shield = pg.image.load('Images/shield.png')
            shield = pg.transform.smoothscale(shield, FILE_PROVIDES_IMAGE_SIZE)
            shield_pos = (self.location[0] + 80 + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * i), self.location[1] - (SELF_FILE_HEIGHT * (NUM_FILES - 2)))
            screen.blit(shield, (shield_pos[0], shield_pos[1]))

        total_cards_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_cards_font = total_cards_font.render((str(total_cards)), True, (0, 0, 0))
        total_cards_font_rect = total_cards_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 3) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_cards_font, total_cards_font_rect)

        total_shields_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_shields_font = total_shields_font.render((str(player.num_shields)), True, (0, 0, 0))
        total_shields_font_rect = total_shields_font.get_rect(center = (self.location[0] + WONDER_BOARD_SIZE[0] - 35, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 3) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_shields_font, total_shields_font_rect)

    def draw_science(self, player):
        bland_science_color = self.bland(SCIENCE_COLOR)
        pg.draw.rect(screen, bland_science_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 3)), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        total_tablets = 0
        total_cogs = 0
        total_compasses = 0
        either_or_total = 0
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.SCIENCE or card.card_type == C.GUILD or card.card_type == C.WONDER_C:
                total_cards += 1
                for symbol in card.provides_sciences:
                    if len(symbol) == 1:
                        if symbol[0] == S.TABLET:
                            total_tablets += 1
                        elif symbol[0] == S.COG:
                            total_cogs += 1
                        elif symbol[0] == S.COMPASS:
                            total_compasses += 1
                        else:
                            print("Error: unrecognized science symbol -", card.provides_sciences[0], " ~ SelfView-draw_science")
                    else:
                        either_or_total += 1

        for i in range(total_tablets):
            tablet_image = pg.image.load('Images/tablet.png')
            tablet_image = pg.transform.smoothscale(tablet_image, FILE_PROVIDES_IMAGE_SIZE)
            tablet_image_pos = (self.location[0] + 83 + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * i), self.location[1] - (SELF_FILE_HEIGHT * (NUM_FILES - 3)))
            screen.blit(tablet_image, tablet_image_pos)

        for i in range(total_cogs):
            cog_image = pg.image.load('Images/cog.png')
            cog_image = pg.transform.smoothscale(cog_image, FILE_PROVIDES_IMAGE_SIZE)
            cog_image_pos = (self.location[0] + 83 + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * (i + total_tablets)), self.location[1] - (SELF_FILE_HEIGHT * (NUM_FILES - 3)))
            screen.blit(cog_image, cog_image_pos)

        for i in range(total_compasses):
            compass_image = pg.image.load('Images/compass.png')
            compass_image = pg.transform.smoothscale(compass_image, FILE_PROVIDES_IMAGE_SIZE)
            compass_image_pos = (self.location[0] + 83 + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * (i + total_tablets + total_cogs)), self.location[1] - (SELF_FILE_HEIGHT * (NUM_FILES - 3)))
            screen.blit(compass_image, compass_image_pos)

        for i in range(either_or_total):
            either_or_image = pg.image.load('Images/science_options.png')
            either_or_image = pg.transform.smoothscale(either_or_image, FILE_SCIENCE_OPTIONS_IMAGE_SIZE)
            either_or_image_pos = (self.location[0] + 83 + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * total_cards) + (i * (4 + FILE_SCIENCE_OPTIONS_IMAGE_SIZE[0])), self.location[1] - (SELF_FILE_HEIGHT * (NUM_FILES - 3)))

        total_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_font = total_font.render((str(total_cards)), True, (0, 0, 0))
        total_font_3_rect = total_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 4) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_font, total_font_3_rect)

    def draw_civic(self, player):
        bland_civic_color = self.bland(CIVIC_COLOR)
        pg.draw.rect(screen, bland_civic_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 4)), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        total_points = 0
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.CIVIC:
                points_image = pg.image.load('Images/civic_points.png')
                points_image = pg.transform.smoothscale(points_image, FILE_PROVIDES_IMAGE_SIZE)
                points_image_pos = (self.location[0] + 80 + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * total_cards), self.location[1] - (SELF_FILE_HEIGHT * (NUM_FILES - 4)))
                screen.blit(points_image, points_image_pos)

                points_font = pg.font.SysFont('timesnewroman', FILE_PROVIDES_FONT_SIZE)
                points_text = points_font.render(str(card.points), True, (255, 255, 255))
                points_text_rect = points_text.get_rect(center = (self.location[0] + 80 + 1 + (FILE_PROVIDES_IMAGE_SIZE[0] / 2) + ((4 + FILE_PROVIDES_IMAGE_SIZE[0]) * total_cards), self.location[1] + FILE_PROVIDES_IMAGE_SIZE[1] / 2 - 1 - (SELF_FILE_HEIGHT * (NUM_FILES - 4))))
                screen.blit(points_text, points_text_rect)
                total_cards += 1
                total_points += card.points

        total_cards_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_cards_font = total_cards_font.render((str(total_cards)), True, (255, 255, 255))
        total_cards_font_rect = total_cards_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 5) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_cards_font, total_cards_font_rect)

        total_shields_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_shields_font = total_shields_font.render((str(total_points)), True, (255, 255, 255))
        total_shields_font_rect = total_shields_font.get_rect(center = (self.location[0] + WONDER_BOARD_SIZE[0] - 35, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 5) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_shields_font, total_shields_font_rect)

    def draw_commercial(self, player):
        bland_commerical_color = self.bland(COMMERCIAL_COLOR)
        pg.draw.rect(screen, bland_commerical_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 5)), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        commercial_cards = []
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.COMMERCIAL:
                total_cards += 1
                commercial_cards.append(card)

        total_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_font = total_font.render((str(total_cards)), True, (0, 0, 0))
        total_font_3_rect = total_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 6) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_font, total_font_3_rect)

        total_spacing = 0
        drawn_cards = 0
        for card in commercial_cards:
            if drawn_cards > 1:
                total_spacing += 10
            if len(card.provides_resources) > 0:
                for k in range(len(card.provides_resources[0])):
                    drawn_cards += 1
                    resource_image = self.load_resource_image(resource=card.provides_resources[0][k])
                    resource_image = pg.transform.smoothscale(resource_image, FILE_PROVIDES_IMAGE_SIZE)
                    resource_image_pos = (self.location[0] + 84 + total_spacing, self.location[1] - (NUM_FILES - 5) * SELF_FILE_HEIGHT)
                    screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
                    total_spacing += (FILE_PROVIDES_IMAGE_SIZE[0] + 4)
                    if k != len(card.provides_resources[0]) - 1:
                        slash = pg.image.load('Images/slash.png')
                        slash = pg.transform.smoothscale(slash, FILE_SLASH_SIZE)
                        slash_pos = (self.location[0] + 85 + total_spacing, self.location[1] - (NUM_FILES - 5) * SELF_FILE_HEIGHT)
                        screen.blit(slash, (slash_pos[0], slash_pos[1]))
                        total_spacing += (FILE_SLASH_SIZE[0] + 2)

    def draw_guilds(self, player):
        bland_guild_color = self.bland(GUILD_COLOR)
        pg.draw.rect(screen, bland_guild_color, ((self.location[0], self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 6)), (WONDER_BOARD_SIZE[0], SELF_FILE_HEIGHT)))

        total_cards = 0
        for i in range(len(player.cards)):
            card = player.cards[i]
            if card.card_type == C.GUILD:
                total_cards += 1

        total_font = pg.font.SysFont("timesnewroman", SELF_FILE_FONT_SIZE)
        total_font = total_font.render((str(total_cards)), True, (0, 0, 0))
        total_font_3_rect = total_font.get_rect(center = (self.location[0] + 40, self.location[1] - SELF_FILE_HEIGHT * (NUM_FILES - 7) - (SELF_FILE_HEIGHT / 2)))
        screen.blit(total_font, total_font_3_rect)

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

    def calc_location(self, screen_dimension):
        return ((screen_dimension[0] - WONDER_BOARD_SIZE[0]) / 2, screen_dimension[1] - WONDER_BOARD_SIZE[1])

class AdjacentResourceView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.location = (0, 0)
        self.right_margin = 0
        self.resource_map_r = []
        self.resource_map_l = []

    def draw(self):
        left_margin = 10
        if len(self.game.players) > 2:
            if self.game.current_player_index == len(self.game.players) - 1:
                self.draw_resources(self.game.players[0], self.right_margin)
                self.draw_money(self.game.players[0], self.right_margin)
                self.draw_adjacent_costs(self.game.current_player(), self.right_margin)
            else:
                self.draw_resources(self.game.players[self.game.current_player_index + 1], self.right_margin)
                self.draw_money(self.game.players[self.game.current_player_index + 1], self.right_margin)
                self.draw_adjacent_costs(self.game.current_player(), self.right_margin)
            if self.game.current_player_index == 0:
                self.draw_resources(self.game.players[len(self.game.players) - 1], left_margin)
                self.draw_money(self.game.players[len(self.game.players) - 1], left_margin)
                self.draw_adjacent_costs(self.game.current_player(), left_margin)
            else:
                self.draw_resources(self.game.players[self.game.current_player_index - 1], left_margin)
                self.draw_money(self.game.players[self.game.current_player_index - 1], left_margin)
                self.draw_adjacent_costs(self.game.current_player(), left_margin)
        # self.draw_resources(self.game.players[self.game.current_player_index], left_margin)
        # self.draw_resources(self.game.players[self.game.current_player_index], self.right_margin)
        self.draw_left_right_highlight()
        
    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)
        self.right_margin = screen_dimension[0] - 10 - ((NEIGHBOR_RESOURCE_SIZE[0] + 4) * 5)
        # self.money_offset = 40
        # self.money_height = screen_dimension[1] / 2

    def load_resource_image(self, resource):
        return pg.image.load(RESOURCE_IMAGE_FILE_NAMES[resource])

    def draw_money(self, player, margin):
        money_location = [self.location[0] + ADJ_MONEY_OFFSET[0] + margin, self.location[1] + ADJ_MONEY_OFFSET[1]]

        money_image = pg.image.load('Images/money_image.png')
        money_image = pg.transform.smoothscale(money_image, ADJ_MONEY_SIZE)
        screen.blit(money_image, money_location)

        money_font = pg.font.SysFont("timesnewroman", ADJ_MONEY_TEXT_SIZE)
        money_text = money_font.render(str(player.money - player.spent_money_l - player.spent_money_r), True, (0, 0, 0))
        money_text_rect = money_text.get_rect(center = (money_location[0] + ADJ_MONEY_SIZE[0]/2, money_location[1] + ADJ_MONEY_SIZE[1]/2))
        screen.blit(money_text, money_text_rect)

    def draw_adjacent_costs(self, player, margin):
        if margin > 100:
            if player.right_cost_r == 1:
                raw_cost_image = pg.image.load("Images/right_r_discount.png")
            elif player.right_cost_r == 2:
                raw_cost_image = pg.image.load("Images/right_r_discount_2.png")
            else:
                print("Invalid Raw Cost - 100", player.right_cost_r)

            if player.right_cost_m == 1:
                mfc_cost_image = pg.image.load("Images/right_m_discount_702_299.png")
            elif player.right_cost_m == 2:
                mfc_cost_image = pg.image.load("Images/right_m_discount_2.png")
            else:
                print("Invalid Manufactored Cost - 100:", player.right_cost_m)
            side_offset = -20
        else:
            if player.left_cost_r == 1:
                raw_cost_image = pg.image.load("Images/left_r_discount.png")
            elif player.left_cost_r == 2:
                raw_cost_image = pg.image.load("Images/left_r_discount_2.png")
            else:
                print("Invalid Raw Cost - 0", player.right_cost_r)
            
            if player.left_cost_m == 1:
                mfc_cost_image = pg.image.load("Images/left_m_discount_702_299.png")
            elif player.left_cost_m == 2:
                mfc_cost_image = pg.image.load("Images/left_m_discount_2.png")
            else:
                print("Invalid Manufactored Cost - 100:", player.right_cost_m)

            side_offset = 0
        raw_cost_image = pg.transform.smoothscale(raw_cost_image, ADJ_RAW_COST_SIZE)
        mfc_cost_image = pg.transform.smoothscale(mfc_cost_image, ADJ_MFC_COST_SIZE)
        first_location = [self.location[0] + margin + side_offset, self.location[1] - ADJ_RAW_COST_SIZE[1] - 15]

        if margin > 100:
            screen.blit(raw_cost_image, first_location)
        else:
            screen.blit(mfc_cost_image, first_location)

        second_location = [first_location[0] + ADJ_RAW_COST_SIZE[0] + 15, first_location[1]]

        if margin > 100:
            screen.blit(mfc_cost_image, second_location)
        else:
            screen.blit(raw_cost_image, second_location)

    def draw_resources(self, player, margin):
        map_list = []
        total_stone = 0
        total_ore = 0
        total_brick = 0
        total_wood = 0
        total_glass = 0
        total_papyrus = 0
        total_silk = 0
        either_or_list = []
        for i, card in enumerate(player.cards):
            if card.card_type == C.RAW_R or card.card_type == C.MFG_R or card.card_type == C.WONDER_START:
                for resource in player.cards[i].provides_resources:
                    if resource == (R.STONE,):
                        total_stone += 1
                    elif resource == (R.ORE,):
                        total_ore += 1
                    elif resource == (R.BRICK,):
                        total_brick += 1
                    elif resource == (R.WOOD,):
                        total_wood += 1
                    elif resource == (R.GLASS,):
                        total_glass += 1
                    elif resource == (R.PAPYRUS,):
                        total_papyrus += 1
                    elif resource == (R.SILK,):
                        total_silk += 1
                    elif len(player.cards[i].provides_resources[0]) > 1:
                        either_or_list.append(player.cards[i])

        total_resources = total_stone + total_ore + total_brick + total_wood + total_glass + total_papyrus + total_silk

        for i in range(total_stone):
            stone_image = pg.image.load('Images/stone.png')
            stone_image = pg.transform.smoothscale(stone_image, NEIGHBOR_RESOURCE_SIZE)
            stone_image_pos = (self.location[0] + margin + ((i % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int(i / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(stone_image, stone_image_pos)
            map_list.append([[stone_image_pos, R.STONE, False]])

        for i in range(total_ore):
            ore_image = pg.image.load('Images/ore.png')
            ore_image = pg.transform.smoothscale(ore_image, NEIGHBOR_RESOURCE_SIZE)
            ore_image_pos = (self.location[0] + margin + (((i + total_stone) % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int((i + total_stone) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(ore_image, ore_image_pos)
            map_list.append([[ore_image_pos, R.ORE, False]])

        for i in range(total_brick):
            brick_image = pg.image.load('Images/brick.png')
            brick_image = pg.transform.smoothscale(brick_image, NEIGHBOR_RESOURCE_SIZE)
            brick_image_pos = (self.location[0] + margin + (((i + total_stone + total_ore) % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int((i + total_stone + total_ore) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(brick_image, brick_image_pos)
            map_list.append([[brick_image_pos, R.BRICK, False]])

        for i in range(total_wood):
            wood_image = pg.image.load('Images/wood.png')
            wood_image = pg.transform.smoothscale(wood_image, NEIGHBOR_RESOURCE_SIZE)
            wood_image_pos = (self.location[0] + margin + (((i + total_stone + total_ore + total_brick) % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int((i + total_stone + total_ore + total_brick) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(wood_image, wood_image_pos)
            map_list.append([[wood_image_pos, R.WOOD, False]])

        for i in range(total_glass):
            glass_image = pg.image.load('Images/glass.png')
            glass_image = pg.transform.smoothscale(glass_image, NEIGHBOR_RESOURCE_SIZE)
            glass_image_pos = (self.location[0] + margin + (((i + total_stone + total_ore + total_brick + total_wood) % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int((i + total_stone + total_ore + total_brick + total_wood) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(glass_image, glass_image_pos)
            map_list.append([[glass_image_pos, R.GLASS, False]])

        for i in range(total_papyrus):
            papyrus_image = pg.image.load('Images/papyrus.png')
            papyrus_image = pg.transform.smoothscale(papyrus_image, NEIGHBOR_RESOURCE_SIZE)
            papyrus_image_pos = (self.location[0] + margin + (((i + total_stone + total_ore + total_brick + total_wood + total_glass) % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int((i + total_stone + total_ore + total_brick + total_wood + total_glass) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(papyrus_image, papyrus_image_pos)
            map_list.append([[papyrus_image_pos, R.PAPYRUS, False]])

        for i in range(total_silk):
            silk_image = pg.image.load('Images/silk.png')
            silk_image = pg.transform.smoothscale(silk_image, NEIGHBOR_RESOURCE_SIZE)
            silk_image_pos = (self.location[0] + margin + (((i + total_stone + total_ore + total_brick + total_wood + total_glass + total_papyrus) % 5) * (4 + NEIGHBOR_RESOURCE_SIZE[0])), self.location[1] + ((int((i + total_stone + total_ore + total_brick + total_wood + total_glass + total_papyrus) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)))
            screen.blit(silk_image, silk_image_pos)
            map_list.append([[silk_image_pos, R.SILK, False]])
        
        height_spacing = (int((total_stone + total_ore + total_brick + total_wood + total_glass + total_papyrus + total_silk) / 5)) * (NEIGHBOR_RESOURCE_SIZE[1] + 4)

        if total_resources % 5 == 0:
            height_spacing -= NEIGHBOR_RESOURCE_SIZE[1] + 4

        tuple_spacing = 0
        last_pos = 0

        for i, card in enumerate(either_or_list):
            if i % 2 == 0:
                tuple_spacing += NEIGHBOR_RESOURCE_SIZE[1] + 4
                last_pos = margin
            for resource_tuple in card.provides_resources:
                slash_margin = 0
                location_list = []
                for r, resource in enumerate(resource_tuple):
                    resource_image = self.load_resource_image(resource=card.provides_resources[0][r])
                    resource_image = pg.transform.smoothscale(resource_image, NEIGHBOR_RESOURCE_SIZE)
                    resource_margin = r * (NEIGHBOR_RESOURCE_SIZE[0] + 0)
                    resource_location = [self.location[0] + resource_margin + slash_margin + last_pos, self.location[1] + height_spacing + tuple_spacing]
                    screen.blit(resource_image, resource_location)
                    location_list.append([resource_location, card.provides_resources[0][r], False])

                    if r != len(card.provides_resources[0]) - 1:
                        slash = pg.image.load('Images/slash.png')
                        slash = pg.transform.smoothscale(slash, NEIGHBOR_SLASH_SIZE)
                        slash_pos = (resource_location[0] + 0 + NEIGHBOR_RESOURCE_SIZE[0], resource_location[1] + 2)
                        screen.blit(slash, slash_pos)
                        slash_margin += NEIGHBOR_SLASH_SIZE[0] + 0
                last_pos = resource_location[0] + NEIGHBOR_RESOURCE_SIZE[0] + 10
                map_list.append(location_list)

        current_player = self.game.current_player()
        
        if margin > 100:
            # if current_player.spent_money_r == 0 and current_player.spent_money_l == 0:
            #     self.resource_map_r = map_list
            #     print("reset 1")
            if len(map_list) != len(self.resource_map_r):
                    self.resource_map_r = map_list
                    # print("reset 2")
                    self.controller.reset_side("l", current_player)
                    
            else:
                for r, resource_tuple in enumerate(map_list):
                    for i in range(len(resource_tuple)):
                        if resource_tuple[i][0] != self.resource_map_r[r][i][0]:
                            self.resource_map_r = map_list
                            # print("reset 3")
                            self.controller.reset_side("l", current_player)
                        elif resource_tuple[i][1] != self.resource_map_r[r][i][1]:
                            self.resource_map_r = map_list
                            # print("reset 4")
                            self.controller.reset_side("l", current_player)
        else:
            # if current_player.spent_money_l == 0 and current_player.spent_money_r == 0:
            #     self.resource_map_l = map_list
            #     print("reset 5")
            if len(map_list) != len(self.resource_map_l):
                    self.resource_map_l = map_list
                    # print("reset 6")
                    self.controller.reset_side("r", current_player)
            else:
                for r, resource_tuple in enumerate(map_list):
                    for i in range(len(resource_tuple)):
                        if resource_tuple[i][0] != self.resource_map_l[r][i][0]:
                            self.resource_map_l = map_list
                            # print("reset 7")
                            self.controller.reset_side("r", current_player)
                        elif resource_tuple[i][1] != self.resource_map_l[r][i][1]:
                            self.resource_map_l = map_list
                            # print("reset 8")
                            self.controller.reset_side("r", current_player)

    def draw_left_right_highlight(self):
        self.draw_image_highlights(self.resource_map_l)
        self.draw_image_highlights(self.resource_map_r)

    def draw_image_highlights(self, resource_list):
        for resource_tuple in resource_list:
            for resource in resource_tuple:
                if resource[2]:
                    center = (resource[0][0] + NEIGHBOR_RESOURCE_SIZE[0] / 2, resource[0][1] + NEIGHBOR_RESOURCE_SIZE[1] / 2)
                    pg.draw.circle(screen, PLAY_HIGHLIGHT_COLOR, center, NEIGHBOR_RESOURCE_SIZE[0] / 2 + 3)
                    resource_image = self.load_resource_image(resource=resource[1])
                    resource_image = pg.transform.smoothscale(resource_image, NEIGHBOR_RESOURCE_SIZE)
                    screen.blit(resource_image, resource[0])

    def calc_location(self, screen_dimension):
        return ((0, screen_dimension[1] - WONDER_BOARD_SIZE[1]))

    def is_event_inside_resource_map(self):
        for item in self.resource_map_l:
            if self.check_resource(item, "l", self.resource_map_l):
                return True
        for item in self.resource_map_r:
            if self.check_resource(item, "r", self.resource_map_r):
                return True
            
    def check_resource(self, item, side, resource_map):
        current_player = self.game.current_player()
        for resource in item:
            if pg.mouse.get_pos()[0] > resource[0][0] and \
                pg.mouse.get_pos()[0] < resource[0][0] + NEIGHBOR_RESOURCE_SIZE[0] and \
                pg.mouse.get_pos()[1] > resource[0][1] and \
                pg.mouse.get_pos()[1] < resource[0][1] + NEIGHBOR_RESOURCE_SIZE[1]:
                    if resource[2]:
                        resource[2] = False
                        # print("setting", resource, "to false")
                        self.controller.on_resource_selected(side, resource_map, resource)
                        self.controller.reset_side(side, current_player)
                        return True
                    else:
                        r_true = False
                        for r in item:
                            if r[2]:
                                r_true = True
                        # r is raw_resource and also right have fun - not at the same time though
                        remaining_money = current_player.money - current_player.spent_money_l - current_player.spent_money_r

                        if ((remaining_money >= current_player.left_cost_r and side == "l" and resource[1].is_raw) or \
                            (remaining_money >= current_player.left_cost_m and side == "l" and not resource[1].is_raw) or \
                            (remaining_money >= current_player.right_cost_r and side == "r" and resource[1].is_raw) or \
                            (remaining_money >= current_player.right_cost_m and side == "r" and not resource[1].is_raw)) or \
                            (len(item) > 1 and r_true):
                            for res in item:
                                res[2] = False
                                # print("setting", res, "to false")
                            resource[2] = True
                            self.controller.on_resource_selected(side, resource_map, resource)
                            return True

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.is_event_inside_resource_map():
                return True
        return False

class MoneyView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.location = (0, 0)

    def calc_location(self, screen_dimension):
        hand = self.game.current_player_hand()
        HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
        LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2 - screen_dimension[1] / 7))
        # return (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + MONEY_MARGIN[0], LAST_CARD_LOCATION[1] + MONEY_MARGIN[1] + DISCARD_BUTTON_SIZE[1] * 2)
        return (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + MONEY_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_SIZE[1] * 2 + BUTTON_MARGIN * 2)

    def draw(self):
        money_image = pg.image.load('Images/money_image.png')
        money_image = pg.transform.smoothscale(money_image, MONEY_IMAGE_SIZE)
        screen.blit(money_image, self.location)

        money_font = pg.font.SysFont("timesnewroman", MONEY_FONT_SIZE)
        money_text = money_font.render(str(self.game.current_player().money - self.game.current_player().spent_money_l - self.game.current_player().spent_money_r), True, (0, 0, 0))
        money_text_rect = money_text.get_rect(center = (self.location[0] + MONEY_IMAGE_SIZE[0]/2, self.location[1] + MONEY_IMAGE_SIZE[1]/2))
        screen.blit(money_text, money_text_rect)

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

class PlayerView(View):
    def __init__(self, game, board, controller, location_index, player_index):
        super().__init__(game, board, controller)
        self.location = [0, 0]
        self.location_index = location_index
        self.player_index = player_index
        self.size = [100, 100]

    # def calc_location(self, screen_dimension):

    def layout(self, screen_dimension):
        self.calc_size()
        self.location = self.calc_location(screen_dimension)

    def draw_player(self, player):
        self.draw_player_view_background()
        self.draw_left_or_right(self.player_index)
        self.draw_shield_num(self.game.players[self.player_index])
        self.draw_civic_image()
        self.draw_civic_num(self.game.players[self.player_index])
        self.draw_total_science(self.game.players[self.player_index])

    def draw_player_view_background(self):
        pg.draw.rect(screen, PLAYER_VIEW_BACKGROUND_COLOR, (self.location, self.size), border_radius=int(PLAYER_VIEW_ROUND_DISTANCE))

    def draw_left_or_right(self, player_index):
        if len(self.game.players) == 2:
            return
        elif self.is_left_of_current_player():
            left_or_right = "Left"
        elif self.is_right_of_current_player():
            left_or_right = "Right"
        else:
            return

        left_or_right_font_size = int(self.size[0] / 10)
        left_or_right_font = pg.font.SysFont(None, left_or_right_font_size)
        left_or_right_text = left_or_right_font.render(left_or_right, True, (30, 30, 30))
        left_or_right_text_rect = left_or_right_text.get_rect(center = (self.location[0] + self.size[0] / 2, self.location[1] + left_or_right_font_size / 2 + PLAYER_VIEW_ROUND_DISTANCE))
        screen.blit(left_or_right_text, left_or_right_text_rect)

    def is_left_of_current_player(self):
        return self.player_index == self.game.current_player_index - 1 or \
            ((self.player_index == (len(self.game.players) - 1)) and self.game.current_player_index == 0)

    def is_right_of_current_player(self):
        return self.player_index == self.game.current_player_index  + 1 or \
            (self.player_index == 0 and (self.game.current_player_index == len(self.game.players) - 1))

    def draw_shield_image(self):
        shield_size = (int(self.size[0] / 5), int(self.size[0] / 5))
        shield = pg.image.load('Images/shield.png')
        shield = pg.transform.smoothscale(shield, shield_size)
        shield_pos = (self.location[0] + self.size[0] - shield_size[0] - 10, self.location[1] + self.size[1] / 2 - shield_size[1] / 2)
        screen.blit(shield, (shield_pos[0], shield_pos[1]))

    def draw_shield_text(self, player):
        shield_size = (int(self.size[0] / 5), int(self.size[0] / 5))
        shield_pos = (self.location[0] + self.size[0] - shield_size[0] - 10, self.location[1] + self.size[1] / 2 - shield_size[1] / 2)

        num_shields_font_size = int(shield_size[0] / 2)
        num_shields_font = pg.font.SysFont('georgia', num_shields_font_size)
        num_shields_text = num_shields_font.render(str(player.num_shields), True, (30, 30, 30))
        num_shields_text_rect = num_shields_text.get_rect(center = (shield_pos[0] + shield_size[0] / 2, shield_pos[1] + shield_size[1] + self.size[1] / 15))
        screen.blit(num_shields_text, num_shields_text_rect)

    def draw_shield_num(self, player):
        self.draw_shield_image()
        self.draw_shield_text(player)

    def draw_civic_num(self, player):
        self.draw_civic_image()
        self.draw_civic_text(player)

    def draw_total_science(self, player):
        image_size = (int(self.size[0] / 5), int(self.size[0] / 5))
        image = pg.image.load("Images/science_total.png")
        image = pg.transform.smoothscale(image, image_size)
        image_pos = (self.location[0] + self.size[0] / 3 - image_size[0] - 10, self.location[1] + self.size[1] / 2 - image_size[1] / 2)
        screen.blit(image, image_pos)

        total_science = 0
        for card in player.cards:
            total_science += len(card.provides_sciences)

        science_font_size = image_size[0] // 2
        science_font = pg.font.SysFont('georgia', science_font_size)
        science_text = science_font.render(str(total_science), True, (30, 30, 30))
        science_text_rect = science_text.get_rect(center = (image_pos[0] + image_size[0] / 2, image_pos[1] + image_size[1] + self.size[1] / 15))
        screen.blit(science_text, science_text_rect)

    def draw_science_text(self, player):
        image_size = (int(self.size[0] / 5), int(self.size[0] / 5))
        text_pos = (self.location[0] + self.size[0] / 3 - 10, self.location[1] + self.size[1] / 2 - image_size[1] / 2)
        
    def draw_civic_image(self):
        civic_size = (int(self.size[0] / 5), int(self.size[0] / 5))
        civic = pg.image.load('Images/civic_points.png')
        civic = pg.transform.smoothscale(civic, civic_size)
        civic_pos = (self.location[0] + self.size[0] / 2 - civic_size[0] / 2, self.location[1] + self.size[1] / 2 - civic_size[1] / 2)
        screen.blit(civic, (civic_pos[0], civic_pos[1]))

    def draw_civic_text(self, player):
        # not actually civic anymore, but rather total current score
        # total_civic_points = 0
        # for card in player.cards:
        #     total_civic_points += card.points
        civic_size = (int(self.size[0] / 5), int(self.size[0] / 5))
        civic_pos = (self.location[0] + self.size[0] / 2, self.location[1] + self.size[1] / 2 - civic_size[1] / 2)

        num_civics_font_size = int(civic_size[0] / 2)
        num_civics_font = pg.font.SysFont('georgia', num_civics_font_size)
        num_civics_text = num_civics_font.render(str(player.current_score), True, (30, 30, 30))
        num_civics_text_rect = num_civics_text.get_rect(center = (civic_pos[0], civic_pos[1] + civic_size[1] + self.size[1] / 15))
        screen.blit(num_civics_text, num_civics_text_rect)

    def calc_size(self):
        # should probably be a dictionary
        if len(self.game.players) == 2:
            self.size = [380, 200]
        elif len(self.game.players) == 3:
            self.size = [300, 180]
        elif len(self.game.players) == 4:
            self.size = [250, 170]
        elif len(self.game.players) == 5:
            self.size = [250, 150]
        elif len(self.game.players) == 6:
            self.size = [220, 150]
        elif len(self.game.players) == 7:
            self.size = [190, 130]
        elif len(self.game.players) == 1:
            self.size = [380, 200]

    def calc_location(self, screen_dimension):
        # player_view_spacing = screen_dimension[0] / (len(self.game.players) - 1)
        player_view_spacing = (screen_dimension[0] - (self.size[0] * (len(self.game.players)))) / (len(self.game.players) + 1)
        location = [player_view_spacing + (player_view_spacing + self.size[0]) * self.location_index, PLAYER_VIEW_ROUND_DISTANCE * -1]
        return location

    def draw(self):
        # if self.game.players[self.player_index] != self.game.current_player():
        self.draw_player(self.game.players[self.player_index])

    def is_inside_player_view(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + self.size[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + self.size[1]

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.is_inside_player_view():
                if self.controller.on_player_view_selected(self.player_index):
                    return True
        return False

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
        return ((HAND_MARGIN + self.hand_card_index * (HAND_SPACING + HAND_CARD_SIZE[0]), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2 - screen_dimension[1] / 7))

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
            self.draw_highlight(card)
        self.draw_hand_card_background(card, self.location)
        self.draw_hand_card_name(card.name, self.location)
        self.draw_coupons(card.provides_coupons, self.location)
        self.draw_hand_card_provides(card, self.location)
        self.draw_hand_card_cost(card, self.location)
        if not self.board.discard:
            self.draw_hand_card_greyout(card)

    def draw_hand_card_greyout(self, card):
        current_player = self.game.current_player()
        if (not current_player.can_play_card(card) and not self.board.discard and not self.board.play_wonder) or \
            (self.board.play_wonder and not current_player.can_play_wonder()):
            greyout = pg.Surface((HAND_CARD_SIZE[0] + ROUND_DISTANCE * 2, HAND_CARD_SIZE[1] + ROUND_DISTANCE * 2))
            greyout.set_alpha(190)
            greyout.fill(BACKRGOUND_COLOR)
            screen.blit(greyout, (self.location[0] - ROUND_DISTANCE, self.location[1] - ROUND_DISTANCE))

    def draw_hand_card_background(self, card, location):
        color = CARD_COLORS.get(card.card_type, (0, 0, 0))
        pg.draw.rect(screen, pg.Color(color), pg.Rect(location, HAND_CARD_SIZE), border_radius=int(ROUND_DISTANCE))

    def draw_hand_card_name(self, name, location):
        hand_card_name_font = pg.font.SysFont('georgia', HAND_CARD_NAME_FONT_SIZE)
        hand_card_name_text = hand_card_name_font.render(name, True, (255, 255, 255))
        hand_card_name_text = pg.transform.rotate(hand_card_name_text, 90)
        hand_card_name_text_length = hand_card_name_text.get_size()
        hand_card_name_location = (location[0] + HAND_CARD_TEXT_MARGIN, location[1] + HAND_CARD_SIZE[1] - HAND_CARD_TEXT_MARGIN - hand_card_name_text_length[1])
        screen.blit(hand_card_name_text, (hand_card_name_location[0], hand_card_name_location[1]))

    def draw_coupons(self, coupons, location):
        for i, coupon in enumerate(coupons):
            hand_card_coupon_font = pg.font.SysFont('georgia', HAND_CARD_COUPON_FONT_SIZE)
            hand_card_coupon_text = hand_card_coupon_font.render(coupon, True, (255, 255, 255))
            hand_card_coupon_text = pg.transform.rotate(hand_card_coupon_text, 90)
            hand_card_coupon_text_length = hand_card_coupon_text.get_size()
            hand_card_coupon_location = (location[0] + HAND_CARD_SIZE[0] - COUPON_OFFSET - HAND_CARD_COUPON_MARGIN[0] * i - hand_card_coupon_text_length[0] * (i + 1), location[1] + HAND_CARD_SIZE[1] - HAND_CARD_COUPON_MARGIN[1] - hand_card_coupon_text_length[1])
            screen.blit(hand_card_coupon_text, hand_card_coupon_location)

    def draw_hand_card_provides(self, card, location):
            if len(card.cost) == 0 and card.money_cost == 0:
                hand_resource_margin = 0
            else:
                hand_resource_margin = 20
            if card.num_shields > 0 and not card.icon:
                for i in range(card.num_shields):
                    shield = pg.image.load('Images/shield.png')
                    shield = pg.transform.smoothscale(shield, SHIELD_SIZE)
                    shield_pos = (location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / card.num_shields*(i+1/2) - SHIELD_SIZE[0]/2, location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                    screen.blit(shield, (shield_pos[0], location[1] + HAND_CARD_PROVIDES_MARGIN[1]))
            if card.card_type == C.SCIENCE or card.card_type == C.WONDER_C and not card.icon:
                # this can't handle either or science cards
                for i in range(len(card.provides_sciences)):
                    if card.provides_sciences[0][i] == S.TABLET:
                        science_symbol_image = pg.image.load('Images/tablet.png')
                    elif card.provides_sciences[0][i] == S.COG:
                        science_symbol_image = pg.image.load('Images/cog.png')
                    elif card.provides_sciences[0][i] == S.COMPASS:
                        science_symbol_image = pg.image.load('Images/compass.png')
                    science_symbol_image = pg.transform.smoothscale(science_symbol_image, SCIENCE_SYMBOL_SIZE)
                    science_symbol_image_pos = (location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / len(card.provides_sciences)*(i+1/2) - SCIENCE_SYMBOL_SIZE[0]/2, location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                    screen.blit(science_symbol_image, (science_symbol_image_pos[0], location[1] + HAND_CARD_PROVIDES_MARGIN[1]))
            if card.points != 0 and not card.icon:
                points_image = pg.image.load('Images/civic_points.png')
                points_image = pg.transform.smoothscale(points_image, CIVIC_POINTS_SIZE)
                points_image_pos = (location[0] + HAND_CARD_SIZE[0]/2 - CIVIC_POINTS_SIZE[0]/2, location[1])
                screen.blit(points_image, points_image_pos)

                points_font = pg.font.SysFont('timesnewroman', HAND_CIVIC_POINTS_FONT_SIZE)
                points_text = points_font.render(str(card.points), True, (255, 255, 255))
                points_text_size = points_text.get_size()
                points_text_pos = (points_image_pos[0] + CIVIC_POINTS_SIZE[0]/2 - points_text_size[0]/2, points_image_pos[1] + CIVIC_POINTS_SIZE[1]/2 - points_text_size[1]/2 - 3)
                screen.blit(points_text, points_text_pos)

            if len(card.provides_resources) > 0:
                for a in range(len(card.provides_resources)):
                    if len(card.provides_resources[a]) > 1:
                        choice_resource_hand_size = (60 - len(card.provides_resources[a])*10, 60 - len(card.provides_resources[a])*10)
                        slash_size = (choice_resource_hand_size[0]/2.5, choice_resource_hand_size[1])
                        resource_tuple = card.provides_resources[a]
                        for i in range(len(resource_tuple)):
                            resource_image = self.load_resource_image(resource=resource_tuple[i])
                            resource_image = pg.transform.smoothscale(resource_image, choice_resource_hand_size)
                            resource_image_pos = (HAND_CARD_PROVIDES_MARGIN[0] + location[0] + (choice_resource_hand_size[0] + slash_size[0])*i, location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                            screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
                            if i != len(resource_tuple) - 1:
                                slash = pg.image.load('Images/slash.png')
                                slash = pg.transform.smoothscale(slash, (int(slash_size[0]), int(slash_size[1])))
                                slash_pos = (resource_image_pos[0] + choice_resource_hand_size[0], location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                                screen.blit(slash, (slash_pos[0], slash_pos[1]))
                    else:
                        resource_image = self.load_resource_image(resource=card.provides_resources[a][0])
                        resource_image = pg.transform.smoothscale(resource_image, PROVIDES_RESOURCE_ICON_SIZE)
                        resource_image_pos = (location[0] + hand_resource_margin + (HAND_CARD_SIZE[0] - hand_resource_margin) / len(card.provides_resources)*(a+1/2) - PROVIDES_RESOURCE_ICON_SIZE[0]/2, location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                        screen.blit(resource_image, (resource_image_pos[0], resource_image_pos[1]))
            if card.provides_money > 0 and not card.icon:
                money_pos = (location[0] + HAND_CARD_SIZE[0] / 2 - PROVIDES_MONEY_SIZE[0] / 2, location[1])
                money_image = pg.image.load('Images/money_image.png')
                money_image = pg.transform.smoothscale(money_image, PROVIDES_MONEY_SIZE)
                screen.blit(money_image, money_pos)

                money_font = pg.font.SysFont("timesnewroman", PROVIDES_MONEY_FONT_SIZE)
                money_text = money_font.render(str(card.provides_money), True, (0, 0, 0))
                money_text_rect = money_text.get_rect(center = (money_pos[0] + PROVIDES_MONEY_SIZE[0]/2, money_pos[1] + PROVIDES_MONEY_SIZE[1]/2))
                screen.blit(money_text, money_text_rect)

            if card.icon:
                image = pg.transform.smoothscale(card.icon.image, card.icon.size)
                image_pos = (location[0] + hand_resource_margin * 0.5 + HAND_CARD_SIZE[0] // 2 - card.icon.size[0] // 2, location[1] + HAND_CARD_PROVIDES_MARGIN[1])
                screen.blit(image, image_pos)

    def draw_hand_card_cost(self, card, location):
        if len(card.cost) > 0:
            rect_size = (HAND_RESOURCE_COST_SIZE[0]/2, (HAND_RESOURCE_COST_SIZE[1] + HAND_RESOURCE_COST_SPACING)*len(card.cost) + 3)
            rect_location = (location[0] + HAND_RESOURCE_COST_SIZE[0]/2, location[1])
            pg.draw.rect(screen, pg.Color(220, 200, 210), pg.Rect((rect_location), (rect_size)))
            for i in range(len(card.cost)):
                cost = card.cost[i]
                cost_pos = (location[0] + HAND_RESOURCE_COST_MARGIN[0], location[1] + HAND_RESOURCE_COST_MARGIN[1] + (HAND_RESOURCE_COST_SPACING + HAND_RESOURCE_COST_SIZE[1]) * i)
                cost_image = self.load_resource_image(resource=cost)
                cost_image = pg.transform.smoothscale(cost_image, HAND_RESOURCE_COST_SIZE)
                screen.blit(cost_image, cost_pos)
        elif card.money_cost > 0:
            rect_size = (HAND_RESOURCE_COST_SIZE[0]/2, (HAND_RESOURCE_COST_SIZE[1] + 3))
            rect_location = (location[0] + HAND_RESOURCE_COST_SIZE[0]/2, location[1])
            cost_pos = (location[0] + HAND_RESOURCE_COST_MARGIN[0], location[1] + HAND_RESOURCE_COST_MARGIN[1])
            pg.draw.rect(screen, pg.Color(220, 200, 210), pg.Rect((rect_location), (rect_size)))
            cost_image = pg.image.load('Images/money_image.png')
            cost_image = pg.transform.smoothscale(cost_image, HAND_RESOURCE_COST_SIZE)
            screen.blit(cost_image, cost_pos)

            money_cost_font = pg.font.SysFont("timesnewroman", MONEY_COST_FONT_SIZE)
            money_cost_text = money_cost_font.render(str(card.money_cost), True, (0, 0, 0))
            money_cost_text_rect = money_cost_text.get_rect(center = (cost_pos[0] + HAND_RESOURCE_COST_SIZE[0]//2, cost_pos[1] + HAND_RESOURCE_COST_SIZE[1]//2))
            screen.blit(money_cost_text, money_cost_text_rect)


    def draw_highlight(self, card):
        if (self.game.current_player().can_play_card(card) and not self.board.play_wonder) or self.board.discard or (self.board.play_wonder and self.game.current_player().can_play_wonder()):
            if self.board.discard:
                highlight_color = DISCARD_HIGHLIGHT_COLOR
            elif self.board.play_wonder:
                highlight_color = WONDER_HIGHLIGHT_COLOR
            else:
                highlight_color = PLAY_HIGHLIGHT_COLOR
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
        LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2 - screen_dimension[1] / 7))
        return (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1])

    def draw(self):
        if not self.board.discard and not self.board.play_wonder:
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
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.is_event_inside_discard_button():
                self.controller.on_discard_button_pressed()
                return True
        return False

class WonderButtonView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.set_children([])
        self.location = (0, 0)

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

    def calc_location(self, screen_dimension):
        # uses a lot of discard button stuff
        hand = self.game.current_player_hand()
        HAND_MARGIN = (screen_dimension[0] - (HAND_SPACING + HAND_CARD_SIZE[0])*len(hand) + HAND_SPACING)/2
        LAST_CARD_LOCATION = ((HAND_MARGIN + (len(hand) - 1) * (HAND_CARD_SIZE[0] + HAND_SPACING), screen_dimension[1]/2 - HAND_CARD_SIZE[1]/2 - screen_dimension[1] / 7))
        return (LAST_CARD_LOCATION[0] + HAND_CARD_SIZE[0] + DISCARD_BUTTON_MARGIN[0], LAST_CARD_LOCATION[1] + DISCARD_BUTTON_MARGIN[1] + DISCARD_BUTTON_SIZE[1] + BUTTON_MARGIN)

    def draw(self):
        if not self.board.play_wonder and not self.board.discard and self.game.current_player().wonder_level < len(self.game.current_player().wonder.layers_list) - 1:
            self.draw_wonder_button()

    def draw_wonder_button(self):
        pg.draw.rect(screen, pg.Color(WONDER_BUTTON_COLOR), pg.Rect(self.location, WONDER_BUTTON_SIZE), border_radius=int(WONDER_BUTTON_ROUND_DISTANCE))
        wonder_font = pg.font.SysFont("georgia", WONDER_FONT_SIZE)
        wonder_text = wonder_font.render("Wonder", True, (0, 0, 0))
        wonder_text_rect = wonder_text.get_rect(center = (self.location[0] + WONDER_BUTTON_SIZE[0]/2, self.location[1] + WONDER_BUTTON_SIZE[1]/2))
        screen.blit(wonder_text, wonder_text_rect)

    def is_event_inside_wonder_button(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + WONDER_BUTTON_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + WONDER_BUTTON_SIZE[1]
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.is_event_inside_wonder_button():
                self.controller.on_wonder_button_pressed()
                return True
        return False

class AllCardsViewButton(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.set_children([])
        self.location = (0, 0)

    def layout(self, screen_dimension):
        self.location = self.calc_location(screen_dimension)

    def calc_location(self, screen_dimension):
        return ((screen_dimension[0] - WONDER_BOARD_SIZE[0]) / 2 + 80, screen_dimension[1] - WONDER_BOARD_SIZE[1] - SELF_FILE_HEIGHT * NUM_FILES - SELF_LABEL_HEIGHT)

    def draw(self):
        pg.draw.rect(screen, pg.Color(All_CARDS_VIEW_BUTTON_COLOR), pg.Rect(self.location, ALL_CARDS_VIEW_BUTTON_SIZE))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.is_event_inside_all_cards_view_button():
                self.controller.on_all_cards_button_pressed()
                return True
        return False

    def is_event_inside_all_cards_view_button(self):
        return \
            pg.mouse.get_pos()[0] > self.location[0] and \
            pg.mouse.get_pos()[0] < self.location[0] + ALL_CARDS_VIEW_BUTTON_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.location[1] and \
            pg.mouse.get_pos()[1] < self.location[1] + ALL_CARDS_VIEW_BUTTON_SIZE[1]

class AllCardsView(View):
    def __init__(self, game, board, controller):
        super().__init__(game, board, controller)
        self.set_children([])
        self.location = (0, 0)
        self.back_button_location = (700, 100)
        self.num_per_row = 3
        self.background_size = (400, 400)
        self.player_index = self.game.current_player_index
        self.bottom_right = []

    def layout(self, screen_dimension):
        self.background_size = (screen_dimension[0], screen_dimension[1])
        self.num_per_row = self.calc_num_per_row(screen_dimension)
        self.back_button_location = (screen_dimension[0] - 80, 30)
        self.bottom_right = [screen_dimension[0], screen_dimension[1]]

    def calc_num_per_row(self, screen_dimension):
        if len(self.game.players[self.player_index].cards) == 0:
            return 10
        else:
            return int((screen_dimension[0] - ALL_CARDS_MARGIN[0]) / (ALL_CARDS_SIZE[0] + ALL_CARDS_SPACING))

    def draw(self):
        # Kinda makes it difficult for all the cards to fit but that was already a problem and I don't feel like fixing it - edit - kinda fixed it by making more cards fit
        if self.board.all_cards:
            pg.draw.rect(screen, (BACKRGOUND_COLOR), (self.location, self.background_size))
            player = self.game.players[self.player_index]
            self.draw_wonder_cards(player)
            order_list = [C.WONDER_START, C.WONDER_C, C.RAW_R, C.MFG_R, C.COMMERCIAL, C.MILITARY, C.CIVIC, C.SCIENCE, C.GUILD]
            num_drawn = -1
            wonders_drawn = -1

            num_drawn = -1
            for current_card_type in order_list:
                for i in range(len(player.cards)):
                    card = player.cards[i]
                    if card.card_type == current_card_type:
                        num_drawn += 1

                        if num_drawn != 0:
                            card_location = [ALL_CARDS_MARGIN[0] + (ALL_CARDS_SIZE[0] + ALL_CARDS_SPACING) * (num_drawn % self.num_per_row), ALL_CARDS_MARGIN[1] + ALL_CARDS_SPACING + (ALL_CARDS_SIZE[1] + ALL_CARDS_SPACING) * (int((num_drawn / self.num_per_row)) + 1)]
                            # print("i: ", i, "num per row: ", self.num_per_row, "%: ", i % self.num_per_row)
                        else:
                            card_location = [ALL_CARDS_MARGIN[0], ALL_CARDS_MARGIN[1] + ALL_CARDS_SPACING * 2 + ALL_CARDS_SIZE[1]]

                        if card.card_type == C.WONDER_C or card.card_type == C.WONDER_START:
                            wonders_drawn += 1
                            num_drawn -= 1

                            card_location[1] -= ALL_CARDS_SIZE[1] + ALL_CARDS_SPACING
                            card_location[0] += (ALL_CARDS_SIZE[0] + ALL_CARDS_SPACING) * wonders_drawn
                            
                        self.draw_card(card, card_location)
                        
            self.draw_war_tokens()
            self.draw_button()

    def draw_wonder_cards(self, player):
        for i, card in enumerate(player.wonder.layers_list):
            # print("drawing", card)
            if i != 0:
                card_location = (ALL_CARDS_MARGIN[0] + (ALL_CARDS_SIZE[0] + ALL_CARDS_SPACING) * (i % self.num_per_row), ALL_CARDS_MARGIN[1] + ALL_CARDS_SPACING + (ALL_CARDS_SIZE[1] + ALL_CARDS_SPACING) * (int((i / self.num_per_row))))
            else:
                card_location = (ALL_CARDS_MARGIN[0], ALL_CARDS_MARGIN[1] + ALL_CARDS_SPACING)

            # print("card location:", card_location)

            self.draw_card(card, card_location)

            greyout = pg.Surface((HAND_CARD_SIZE[0] + ROUND_DISTANCE * 2, HAND_CARD_SIZE[1] + ROUND_DISTANCE * 2))
            greyout.set_alpha(190)
            greyout.fill(BACKRGOUND_COLOR)
            screen.blit(greyout, (card_location[0] - ROUND_DISTANCE, card_location[1] - ROUND_DISTANCE))

    def draw_card(self, card, card_location):
        CardView.draw_hand_card_background(self, card, card_location)
        CardView.draw_hand_card_name(self, card.name, card_location)
        CardView.draw_coupons(self, card.provides_coupons, card_location)
        CardView.draw_hand_card_provides(self, card, card_location)
        CardView.draw_hand_card_cost(self, card, card_location)

    def draw_war_tokens(self):
        minus_token = pg.image.load("Images/minus_token.png")
        one_token = pg.image.load("Images/one_token.png")
        three_token = pg.image.load("Images/three_token.png")
        five_token = pg.image.load("Images/five_token.png")

        minus_token = pg.transform.smoothscale(minus_token, MINUS_TOKEN_SIZE)
        one_token = pg.transform.smoothscale(one_token, ONE_TOKEN_SIZE)
        three_token = pg.transform.smoothscale(three_token, THREE_TOKEN_SIZE)
        five_token = pg.transform.smoothscale(five_token, FIVE_TOKEN_SIZE)

        player = self.game.players[self.player_index]

        minus_total = 0
        one_total = 0
        three_total = 0
        five_total = 0

        total_distance = minus_total * MINUS_TOKEN_SIZE[0] + one_total * ONE_TOKEN_SIZE[0] + three_total * THREE_TOKEN_SIZE[0] + five_total * FIVE_TOKEN_SIZE[0]

        start_location = [self.bottom_right[0] - WAR_TOKENS_OFFSET[0] - total_distance, self.bottom_right[1] - WAR_TOKENS_OFFSET[1]]

        for token in player.war_tokens:
            if token == -1:
                minus_total += 1
            elif token == 1:
                one_total += 1
            elif token == 3:
                three_total += 1
            elif token == 5:
                five_total += 1

        for i in range(minus_total):
            screen.blit(minus_token, (start_location[0] - (i + 1) * MINUS_TOKEN_SIZE[0] - TOKEN_SPACING * (i+1), start_location[1] - MINUS_TOKEN_SIZE[1]))
        for i in range(one_total):
            screen.blit(one_token, (start_location[0] - minus_total * MINUS_TOKEN_SIZE[0] - (i + 1) * ONE_TOKEN_SIZE[0] - TOKEN_SPACING * (minus_total + i + 1), start_location[1] - ONE_TOKEN_SIZE[1]))
        for i in range(three_total):
            screen.blit(three_token, (start_location[0] - minus_total * MINUS_TOKEN_SIZE[0] - one_total * ONE_TOKEN_SIZE[0] - (i + 1) * THREE_TOKEN_SIZE[0] - TOKEN_SPACING * (minus_total + one_total + i + 1), start_location[1] - THREE_TOKEN_SIZE[1]))
        for i in range(five_total):
            screen.blit(five_token, (start_location[0] - minus_total * MINUS_TOKEN_SIZE[0] - one_total * ONE_TOKEN_SIZE[0] - three_total * THREE_TOKEN_SIZE[0] - (i + 1) * FIVE_TOKEN_SIZE[0] - TOKEN_SPACING * (minus_total + one_total + three_total + i + 1), start_location[1] - FIVE_TOKEN_SIZE[1])) 

    def draw_button(self):
        arrow_image = pg.image.load('Images/back_arrow.png')
        arrow_image = pg.transform.smoothscale(arrow_image, BACK_ARROW_SIZE)
        arrow_image_pos = (self.back_button_location)
        screen.blit(arrow_image, arrow_image_pos)

    def is_event_inside_back_button(self):
        return \
            pg.mouse.get_pos()[0] > self.back_button_location[0] and \
            pg.mouse.get_pos()[0] < self.back_button_location[0] + BACK_ARROW_SIZE[0] and \
            pg.mouse.get_pos()[1] > self.back_button_location[1] and \
            pg.mouse.get_pos()[1] < self.back_button_location[1] + BACK_ARROW_SIZE[1]

    def handle_event(self, event):
        if self.board.all_cards:
            if event.type == pg.MOUSEBUTTONUP:
                if self.is_event_inside_back_button():
                    self.controller.on_back_button_pressed()
                    return True
            return False

    def load_resource_image(self, resource):
        return pg.image.load(RESOURCE_IMAGE_FILE_NAMES[resource])
