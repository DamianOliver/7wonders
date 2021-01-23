from game import Game
import pygame as pg

# Controller reacts to events and modifies model (Board)

# Model holds information and logic on how states change

class Board:
    def __init__(self):
        self.needs_redraw = False
        self.discard = False
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
        self.game.current_player().give_moneys_for_discard()
        print("MONEY: ", self.game.current_player().money)
        self.game.current_player_finished()
        self.board.request_redraw()

    def on_discard_button_pressed(self):
        if not self.board.discard:
            self.board.discard = True
            self.board.request_redraw()
        else:
            self.board.discard = False
            self.board.request_redraw()

    def select_card(self, selected_card_number):
        hand = self.game.current_player_hand()
        print("selecting a card!!!")
        selected_card = hand[selected_card_number]

        if self.game.current_player().play_card(selected_card):
            del hand[selected_card_number]

        self.game.current_player_finished()
        self.board.request_redraw()
