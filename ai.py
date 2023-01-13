from game import C, R, S

import random as rand

class Ai:
    def __init__(self, player, players):
        self.player = player
        self.players = players

        self.bias_dict = {
            C.MILITARY: 0,
            C.SCIENCE: 0,
            C.CIVIC: 0,
            C.COMMERCIAL: 0,
            C.MFG_R: 0,
            C.RAW_R: 0,
            C.GUILD: 0,
            C.WONDER_C: 3,
        }

        self.set_bias_from_wonder()

    def set_bias_from_wonder(self):
        if self.player.wonder.name == "Alexandria":
            if rand.randint(1, 2) == 2:
                # science focus
                self.bias_dict[C.SCIENCE] = 4
                self.bias_dict[C.MFG_R] = 3
            else:
                # military/civic focus
                self.bias_dict[C.MILITARY] = 3
                self.bias_dict[C.RAW_R] = 3
                self.bias_dict[C.CIVIC] = 1
            self.bias_dict[C.COMMERCIAL] = 2

        elif self.player.wonder.name == "Babylon":
            self.bias_dict[C.SCIENCE] = 4
            self.bias_dict[C.MFG_R] = 3

        elif self.player.wonder.name == "Ghiza":
            self.bias_dict[C.RAW_R] = 3
            self.bias_dict[C.CIVIC] = 3
            self.bias_dict[C.MILITARY] = 2

        elif self.player.wonder.name == "Ephesos":
            # ephesos is kinda screwed until buying resources becomes a thing
            #   - granted they're all screwed until building wonders becomes a thing
            self.bias_dict[C.RAW_R] = -1
            self.bias_dict[C.MFG_R] = -1

            if rand.randint(1, 2) == 2:
                self.bias_dict[C.SCIENCE] = 4

        elif self.player.wonder.name == "Rhodos":
            self.bias_dict[C.MILITARY] = 5
            self.bias_dict[C.RAW_R] = 2
            self.bias_dict[C.SCIENCE] = -2

        elif self.player.wonder == "Olympia":
            if rand.randint(1, 2) == 2:
                self.bias_dict[C.SCIENCE] = 4
            else:
                self.bias_dict[C.SCIENCE] = -2

    def evaluate(self, hand, age):
        print("------------------------------------------")
        best_play_card, play_eval = self.eval_play_cards(hand, age)
        print(best_play_card.name)
        wonder_eval = self.eval_wonder(age)
        if wonder_eval:
            if wonder_eval > play_eval:
                return hand[0], "wonder"
        if best_play_card:
            return best_play_card, "play"
        
        print("discarding")
        return hand[0], "discard"

    def eval_play_cards(self, hand, age):
        best_card = None
        best_eval = -99
        for card in hand:
            if self.player.can_play_card(card) and not self.player.can_play_card(card):
                provides_eval = self.eval_play_card(card, age)
                provides_eval += self.bias_dict[card.card_type]
                print("{} scored at: {}".format(card.name, provides_eval))
                if provides_eval > best_eval:
                    best_eval = provides_eval
                    best_card = card
        if best_card:
            return best_card, best_eval

    def eval_play_card(self, card, age):
        eval = card.points
        if len(card.provides_resources) > 0:
            eval += self.eval_resources(card)
        if card.num_shields > 0:
            eval += self.eval_shields(card, age)
        if len(card.provides_sciences) > 0:
            eval += self.eval_science(card, age)

        return eval

    def eval_resources(self, card):
        # basic start - add individual resource preferences especially for different biases as well as for wonder, ect.
        eval = -1
        for resource_tuple in card.provides_resources:
            eval += len(resource_tuple) / 2 + 1/2

        current_resources = self.player.available_resources_tuples(self.player.cards)
        print("cp", current_resources, "-", card.provides_resources[0])
        if card.provides_resources not in current_resources:
            eval += 3

        return eval

    def eval_shields(self, card, age):
        # add smarter calculations based on age, total number of military cards, direction of passing, etc.
        eval = 0
        left_player, right_player = self.left_right_players(self.player)
        left_difference = (self.player.num_shields - left_player.num_shields - 1) / card.num_shields
        right_difference = (self.player.num_shields - right_player.num_shields - 1) / card.num_shields
        eval += 2 - abs(left_difference) * (2 * age - 1)
        eval += 2 - abs(right_difference) * (2 * age - 1)

        return eval

    def eval_science(self, card, age):
        # WARNING - DOES NOT WORK FOR MULTIPLE SCIENCE TUPLES
        # add smarter analysis based on age - bias toward completion should be weighted more toward endgame, number of cards in existence
        eval = 3 - age
        totals_list = self.total_science()
        print(card.provides_sciences)
        if len(card.provides_sciences) > 1:
            print("big science boy")
        else:
            science = card.provides_sciences[0][0]

        if science == S.COG:
            science_index = 0
        elif science == S.COMPASS:
            science_index = 1
        elif science == S.TABLET:
            science_index = 2

        bias_multiplier = 3

        min_bias = (totals_list[0] + totals_list[1] + totals_list[2]) / 3 - min(totals_list) * bias_multiplier

        eval += (3 - totals_list[science_index] - min(totals_list)) * min_bias
    
        return eval



    def total_science(self):
        totals_list = [0, 0, 0, 0]
        available_sciences = []

        for played_card in self.player.cards:
            if len(played_card.provides_sciences) > 1:
                totals_list[3] += 1
            elif len(played_card.provides_sciences) > 0:
                available_sciences.append(played_card.provides_sciences)

        for science in available_sciences:
            if science[0] == S.COG:
                totals_list[0] += 1
            elif science[0] == S.COMPASS:
                totals_list[1] += 1
            elif science[0] == S.TABLET:
                totals_list[2] += 1

        for i in range(totals_list[3]):
            min_index = 0
            lowest = 99
            for i in range(len(totals_list) - 1):
                if totals_list[i] < lowest:
                    min_index = i
                    lowest = totals_list[i]

            totals_list[min_index] += 1

        return totals_list[:-1]


    def eval_wonder(self, age):
        wonder_card = self.player.wonder.layers_list[self.player.wonder_level + 1]
        if self.player.can_play_card(wonder_card):
            provides_eval = self.eval_play_card(wonder_card, age)
            provides_eval += self.bias_dict[C.WONDER_C]
            return provides_eval
        return None


    def left_right_players(self, player):
        player_index = player.player_number

        if player_index == 0:
            left_player = self.players[len(self.players) - 1]
        else:
            left_player = self.players[player_index - 1]

        if player_index == len(self.players) - 1:
            right_player = self.players[0]
        else:
            right_player = self.players[player_index + 1]

        return left_player, right_player

    def eval_discard(self, player):
        # really just a placeholder for now
        return 1

        
