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

        self.order_list = [C.SCIENCE, C.SCIENCE, C.SCIENCE, C.MILITARY, C.MILITARY, C.MILITARY]
        rand.shuffle(self.order_list)

        self.set_bias_from_wonder()

    def set_bias_from_wonder(self):
        # for testing
        # self.bias_dict[self.order_list[self.player.player_number]] = 6
        return


    # def set_bias_from_wonder(self):
    #     if self.player.wonder.name == "Alexandria":
    #         if rand.randint(1, 2) == 2:
    #             # science focus
    #             self.bias_dict[C.SCIENCE] = 4
    #             self.bias_dict[C.MFG_R] = 3
    #         else:
    #             # military/civic focus
    #             self.bias_dict[C.MILITARY] = 3
    #             self.bias_dict[C.RAW_R] = 3
    #             self.bias_dict[C.CIVIC] = 1
    #         self.bias_dict[C.COMMERCIAL] = 2

    #     elif self.player.wonder.name == "Babylon":
    #         self.bias_dict[C.SCIENCE] = 4
    #         self.bias_dict[C.MFG_R] = 3

    #     elif self.player.wonder.name == "Ghiza":
    #         self.bias_dict[C.RAW_R] = 3
    #         self.bias_dict[C.CIVIC] = 3
    #         self.bias_dict[C.MILITARY] = 2

    #     elif self.player.wonder.name == "Ephesos":
    #         # ephesos is kinda screwed until buying resources becomes a thing
    #         #   - granted they're all screwed until building wonders becomes a thing
    #         self.bias_dict[C.RAW_R] = -1
    #         self.bias_dict[C.MFG_R] = -1

    #         if rand.randint(1, 2) == 2:
    #             self.bias_dict[C.SCIENCE] = 4

    #     elif self.player.wonder.name == "Rhodos":
    #         self.bias_dict[C.MILITARY] = 5
    #         self.bias_dict[C.RAW_R] = 2
    #         self.bias_dict[C.SCIENCE] = -2

    #     elif self.player.wonder == "Olympia":
    #         if rand.randint(1, 2) == 2:
    #             self.bias_dict[C.SCIENCE] = 4
    #         else:
    #             self.bias_dict[C.SCIENCE] = -2

    def evaluate(self, hand, age):
        print("------------------------------------------")
        play_card_cost, play_eval = self.eval_play_cards(hand, age)
        best_play_card = play_card_cost[0]
        play_cost = play_card_cost[1]
        if best_play_card:
            print(best_play_card.name)
        wonder_eval, wonder_cost = self.eval_wonder(age)
        if wonder_eval:
            if wonder_eval > play_eval:
                return hand[0], "wonder", wonder_cost
        if best_play_card:
            return best_play_card, "play", play_cost
        
        print("discarding")
        return hand[0], "discard", [0, 0]

    def eval_play_cards(self, hand, age):
        best_card = (None, [999, 999])
        best_eval = -99
        for card in hand:
            cost = self.calc_purchase(card)
            if cost[0] < 100 and cost[0] + cost[1] <= self.player.money:
                provides_eval = self.eval_play_card(card, age)
                provides_eval += self.eval_money(-(cost[0] + cost[1]))
                print("cost eval:", -(cost[0] + cost[1]))
                provides_eval += self.bias_dict[card.card_type]
                print("{} scored at: {}".format(card.name, provides_eval))
                if provides_eval > best_eval:
                    best_eval = provides_eval
                    best_card = (card, cost)

        return best_card, best_eval

    def eval_play_card(self, card, age):
        eval = card.points
        if len(card.provides_resources) > 0:
            eval += self.eval_resources(card)
        if card.num_shields > 0:
            eval += self.eval_shields(card, age)
        if len(card.provides_sciences) > 0:
            eval += self.eval_science(card, age)
        if card.provides_money > 0:
            eval += self.eval_money(card.provides_money)

        return eval

    def eval_resources(self, card):
        # basic start - add individual resource preferences especially for different biases as well as for wonder, ect.
        eval = -1
        for resource_tuple in card.provides_resources:
            eval += len(resource_tuple) / 2 + 1/2

        current_resources = self.player.available_resources_tuples(self.player.cards)
        # print("cp", current_resources, "-", card.provides_resources[0])
        if card.provides_resources not in current_resources:
            eval += 3
        elif card.card_type == C.MFG_R:
            eval -= 6

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
            pass
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

    def eval_money(self, money_num):
        # add some fancy equation with bias when money low
        if self.player.money < 3:
            return money_num / 2
        else:
            return money_num * 2 / 5

# 6 - 2 -> 1
# c - diff
# 5 - (6- 2)

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
        if self.player.wonder_level == len(self.player.wonder.layers_list) - 1:
            return None, [0, 0]
        wonder_card = self.player.wonder.layers_list[self.player.wonder_level + 1]
        cost = self.calc_purchase(wonder_card)
        if cost[0] < 100 and cost[0] + cost[1] <= self.player.money:
            provides_eval = self.eval_play_card(wonder_card, age)
            provides_eval += self.bias_dict[C.WONDER_C]
            provides_eval += self.eval_money(cost[0] + cost[1])
            return provides_eval, cost
        return None, [0, 0]
    
    def calc_needed_resources(self, card):
        needed_resources = [(resource,) for resource in card.cost]
        player_resource_tuples = self.player.available_resource_tuples()

        for resource_tuple in player_resource_tuples:
            if resource_tuple in needed_resources:
                needed_resources.remove(resource_tuple)
            elif len(resource_tuple) > 1:
                new_cost = []
                for resource in resource_tuple:
                    if (resource,) in needed_resources:
                        needed_resources.remove((resource,))
                        needed_resources.append(resource)
            if len(new_cost) > 1:
                needed_resources.append(new_cost)

    def calc_purchase(self, card):
        left_player, right_player = self.left_right_players(self.player)
        left_resources = left_player.available_resources_tuples(self.player.cards)
        right_resources = right_player.available_resources_tuples(self.player.cards)
        needed_resources = card.cost
        # need to deal with needed resources
        # they need to exclude player resources
        # fun
        best_cost = self.recursive_calc(left_resources, right_resources, needed_resources, [0, 0])
        print("_____________________")
        print("left:", left_resources)
        print("right:", right_resources)
        print("needed resources:", needed_resources)
        print("best_cost:", best_cost)
        print("_____________________")
        return best_cost


    def recursive_calc(self, left_resources, right_resources, needed_resources, cost):
        cost_list = []
        print("needed resources, cost:", needed_resources, cost)
        if len(needed_resources) == 0:
            print("it actually got used")
            return cost
        for resource_tuple in left_resources:
            for resource in resource_tuple:
                if (resource,) in needed_resources:
                    new_left_resources = left_resources.copy()
                    new_left_resources.remove(resource_tuple)
                    new_needed_resources = needed_resources.copy()
                    new_needed_resources.remove((resource,))
                    added_cost = self.calc_resources_cost("left", resource)
                    new_cost = (cost[0] + added_cost, cost[1])
                    cost_list.append(self.recursive_calc(new_left_resources, right_resources, new_needed_resources, new_cost))
        for resource_tuple in right_resources:
            for resource in resource_tuple:
                if (resource,) in needed_resources:
                    new_right_resources = right_resources.copy()
                    new_right_resources.remove(resource_tuple)
                    new_needed_resources = needed_resources.copy()
                    new_needed_resources.remove((resource,))
                    added_cost = self.calc_resources_cost("right", resource)
                    new_cost = (cost[0], cost[1] + added_cost)
                    cost_list.append(self.recursive_calc(left_resources, new_right_resources, new_needed_resources, new_cost))
        
        # if len(left_resources) == 0 and len(right_resources) == 0:
        #     print("no more resources")
        #     return [999, 999]
        
        best_cost_val = 99999
        best_cost = [999, 999]
        print("cost list:", cost_list)
        for cost_val in cost_list:
            if (cost_val[0] + cost_val[1]) < best_cost_val:
                best_cost_val = cost_val[0] + cost_val[1]
                best_cost = cost_val
        return best_cost
        
    def calc_resources_cost(self, direction, resource):
        if resource.is_raw():
            if direction == "left":
                return self.player.left_cost_r
            return self.player.right_cost_r
        if direction == "left":
            return self.player.left_cost_m
        return self.player.right_cost_m

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

        
