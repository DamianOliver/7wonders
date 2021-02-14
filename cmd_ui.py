# Copyright 2020 Damian Piech

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from game import *

class CmdUi:
    def __init__(self):
        self.game = Game()

    def play(self):
        while self.game.turn < NUM_TURNS:
            print("turn {}".format(self.game.turn))

            for i in range(len(self.game.players)):
                
                 = self.game.players[i]
                hand = self.game.hands[(i + self.game.turn) % len(self.game.hands)] 
                print("  Player {}".format(player.player_number))
                player.print_cards()
                for i in range(len(hand)):
                    print("Number: {} {}".format(i, hand[i].__str__()))
                action = self.ask_for_action()
                if action == "d":
                    self.discard_card(player, hand)
                elif action == "p":
                    self.select_card(player, hand)
                # elif action == "b":
                #     player.buy_resource(player)
            self.game.turn += 1
        self.game.print_player_cards()

    def ask_for_action(self):
        while True:
            action_input = input("Select your action, d for discard, p for play card, or b to buy a resource: ")
            if action_input == "d" or action_input == "p" or action_input == "b":
                return action_input

    def ask_for_card_selection(self, hand_cards):
        while True:
            try:
                index = int(input("  Select a card: "))
                if index >= 0 and index < len(hand_cards):
                    return index
            except ValueError:
                pass
                
            print("Enter a number from 0 to {}".format(len(hand_cards) - 1))
            print("hand cards", len(hand_cards))
            print("hand: ", hand_cards)

    def select_card(self, player, hand_cards):
        while True:
            selected_card_number = self.ask_for_card_selection(hand_cards)
            selected_card = hand_cards[selected_card_number]

            if player.play_card(selected_card):
                del hand_cards[selected_card_number]
                break
            else:
                print("You do not have the required resources for that card.")

    def discard_card(self, player, hand_cards):
        selected_card_number = self.ask_for_card_selection(hand_cards)
        selected_card = hand_cards[selected_card_number]
        del hand_cards[selected_card_number]
        player.give_moneys_for_discard()
        print("MONEY: ", player.money)