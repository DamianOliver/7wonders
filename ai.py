from game import *

import random as rand

# TO DO:

    # obviously also teach the ai what all the most important cards in the game do... or at least what they're worth




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

        self.resource_values_dict = {
            1 : 1,
            2 : 0.75,
            3 : 0.67,
            4 : 0.6,
        }

        self.order_list = [C.SCIENCE, C.SCIENCE, C.SCIENCE, C.MILITARY, C.MILITARY, C.MILITARY]
        rand.shuffle(self.order_list)

        self.set_bias_from_wonder()

        if self.player.player_number < 3:
            self.type = 1
        else:
            self.type = 2

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
                self.bias_dict[C.CIVIC] = 0
                self.bias_dict[C.MFG_R] = -2
            self.bias_dict[C.COMMERCIAL] = 2

        elif self.player.wonder.name == "Babylon":
            self.bias_dict[C.SCIENCE] = 4
            self.bias_dict[C.MFG_R] = 3

        elif self.player.wonder.name == "Ghiza":
            self.bias_dict[C.RAW_R] = 0.5
            self.bias_dict[C.MFG_R] = -1.5
            self.bias_dict[C.CIVIC] = 0
            self.bias_dict[C.MILITARY] = 1
            self.bias_dict[C.WONDER_C] = 4

        elif self.player.wonder.name == "Ephesos":
            self.bias_dict[C.RAW_R] = -1
            self.bias_dict[C.MFG_R] = -1

            if rand.randint(1, 2) == 2:
                self.bias_dict[C.SCIENCE] = 4
                self.bias_dict[C.RAW_R] = -2

        elif self.player.wonder.name == "Rhodos":
            self.bias_dict[C.MILITARY] = 2
            self.bias_dict[C.RAW_R] = 2
            self.bias_dict[C.SCIENCE] = -2
            self.bias_dict[C.MFG_R] = -2

        elif self.player.wonder == "Olympia":
            if rand.randint(1, 2) == 2:
                self.bias_dict[C.SCIENCE] = 4
            else:
                self.bias_dict[C.SCIENCE] = -2
                self.bias_dict[C.MFG_R] = -2

    def evaluate(self, hand, age):
        print("------------------------------------------")
        play_card_cost, play_eval = self.eval_play_cards(hand, age)
        best_play_card = play_card_cost[0]
        play_cost = play_card_cost[1]
        if best_play_card:
            print(best_play_card.name, "with eval of", play_eval)
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
            if cost[0] < 100 and cost[0] + cost[1] + card.money_cost <= self.player.money and not self.is_in_cards(card, self.player.cards):
                provides_eval = self.eval_play_card(card, age)
                provides_eval += self.eval_money(-(cost[0] + cost[1] + card.money_cost))
                print("v cost {} - {} evaluated at - {} v".format(cost, card.money_cost, -(cost[0] + cost[1] + card.money_cost)))
                print("{} scored at: {}".format(card.name, provides_eval))
                if provides_eval > best_eval:
                    best_eval = provides_eval
                    best_card = (card, cost)

        return best_card, best_eval

    def is_in_cards(self, card, cards):
        for player_card in cards:
            if card.name == player_card.name:
                return True

    def eval_play_card(self, card, age):
        eval = card.points
        if len(card.provides_resources) > 0:
            eval += self.eval_resources(card)
        if card.num_shields > 0:
            eval += self.eval_shields(card, age)
            eval += self.bias_dict[C.MILITARY]
        if len(card.provides_sciences) > 0:
            eval += self.eval_science(card, age)
            eval += self.bias_dict[C.SCIENCE]
        if card.provides_money > 0:
            eval += self.eval_money(card.provides_money)
        if card.icon:
            eval += self.eval_icon(card.icon)

        return eval

    def eval_resources(self, card):
        # FIGURE OUT WHY EITHER OR RESOURCE CARDS SCORE LOWER - PROBABLY MAKE A TEST DECK OR SOMETHING
        current_resource_tuples = self.player.available_resources_tuples(self.player.cards)
        resource_totals = self.sum_resources(current_resource_tuples)
        added_value = 0
        for resource_tuple in card.provides_resources:
            for resource in resource_tuple:
                if resource.is_raw():
                    if resource not in resource_totals:
                        added_value += self.resource_values_dict[len(resource_tuple)] * 2
                    else:
                        added_value += max(self.resource_values_dict[len(resource_tuple)] * 2 - resource_totals[resource], 0)

                else:
                    if resource not in resource_totals:
                        added_value += self.resource_values_dict[len(resource_tuple)]
                    else:
                        # -3 because duplicate manufactored resource cards is really dumb
                        pen = -3 if len(resource_tuple) == 1 else -3
                        added_value += max(self.resource_values_dict[len(resource_tuple)] - resource_totals[resource], 0) + pen
        if card.card_type == C.RAW_R:
            added_value += self.bias_dict[C.RAW_R]
            return added_value * 2
        else:
            added_value += self.bias_dict[C.MFG_R]
            return added_value * 3

    def sum_resources(self, resource_tuples):
        resource_totals = {}
        for resource_tuple in resource_tuples:
            for resource in resource_tuple:
                if resource not in resource_totals:
                    resource_totals[resource] = self.resource_values_dict[len(resource_tuple)]
                else:
                    resource_totals[resource] += self.resource_values_dict[len(resource_tuple)]
        return resource_totals

    def eval_shields(self, card, age):
        eval = 0
        left_player, right_player = self.left_right_players(self.player)
        eval += self.shield_compare(self.player, left_player, card, age)
        eval += self.shield_compare(self.player, right_player, card, age)
        eval /= 2
        return eval

    def shield_compare(self, player, compare_player, card, age):
        prior_difference = player.num_shields - compare_player.num_shields
        shield_difference = (player.num_shields + card.num_shields) - compare_player.num_shields
        if prior_difference <= 0:
            if shield_difference > 0:
                return 2 * age - 1
            elif shield_difference == 0:
                return 2 * age - 2
            elif shield_difference < age:
                return age
            return 0
        else:
            if prior_difference < age:
                return age + 1
            else:
                return age


    def eval_science(self, card, age):
        # WARNING - DOES NOT WORK FOR MULTIPLE SCIENCE TUPLES
        # add smarter analysis based on age - bias toward completion should be weighted more toward endgame, number of cards in existence
        eval = 3 - age
        totals_list = self.total_science()
        print(card.provides_sciences)
        science = card.provides_sciences[0][0]

        if science == S.COG:
            science_index = 0
        elif science == S.COMPASS:
            science_index = 1
        elif science == S.TABLET:
            science_index = 2

        if len(card.provides_sciences) > 1:
            science_index = totals_list.index(min(totals_list))

        bias_multiplier = 3

        min_bias = (totals_list[0] + totals_list[1] + totals_list[2]) / 3 - min(totals_list) * bias_multiplier

        eval += (3 - totals_list[science_index] - min(totals_list)) * min_bias
    
        return eval

    def eval_icon(self, icon):
        left_player, right_player = self.left_right_players(self.player)
        if isinstance(icon, DiscountIcon):
            # obviously should eventually take into account missing resources once that becomes a thing
            # also this value will likely need to be adjusted
            if icon.direction == "right":
                compare_players = [right_player]
            elif icon.direction == "left":
                compare_players = [left_player]
            else:
                compare_players = [left_player, right_player]
            total_cards = 0
            for player in compare_players:
                total_cards += self.sum_card_type(player, C.RAW_R)
            
            if icon.type == C.MFG_R:
                if self.sum_card_type(player, C.MFG_R) > 1:
                    return 1
            
            return 3.5

        elif isinstance(icon, StuffPerCard):
            # needs to updated to include future expectations though that isn't a huge deal
            compare_players = []
            if "right" in icon.directions:
                compare_players.append(right_player)
            if "left" in icon.directions:
                compare_players.append(left_player)
            if "down" in icon.directions:
                compare_players.append(self.player)

            total_cards = 0
            for player in compare_players:
                total_cards += self.sum_card_type(player, icon.card_type)

            card_eval = total_cards * icon.provides[1]
            card_eval += self.eval_money(total_cards * icon.provides[0])
            return card_eval

        elif isinstance(icon, StuffForWonderStage):
            total = icon.total(self.player, self.players)
            card_eval = total * icon.provides[1]
            card_eval += self.eval_money(total * icon.provides[0])
            return card_eval

        elif isinstance(icon, StuffForMilitaryTokens):
            total = icon.total(self.player, self.players)
            card_eval = total * icon.provides[1]
            return card_eval

        elif isinstance(icon, CopyGuild):
            return icon.score(self.player, self.players)

        return 0

    def eval_money(self, money_num):
        # add some fancy equation with bias when money low
        if self.player.money < 3:
            return money_num / 1.5
        else:
            return money_num * 2 / 5


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
            money_cost = self.eval_money(-(cost[0] + cost[1]))
            provides_eval += money_cost
            print()
            print("v eval decreased by", money_cost, "with cost of", cost)
            print("Wonder stage", self.player.wonder_level + 1, "evaluated at", provides_eval)
            
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
        if self.player.can_play_card(card):
            return (0, 0)
        left_player, right_player = self.left_right_players(self.player)
        left_resources = self.availble_buy_resources(left_player.cards)
        right_resources = right_player.available_resources_tuples(right_player.cards)
        either_or_resources = []
        needed_resources = card.cost.copy()
        for resource_tuple in self.player.available_resources_tuples(self.player.cards):
            if len(resource_tuple) == 1:
                if resource_tuple[0] in needed_resources:
                    needed_resources.remove(resource_tuple[0])
            else:
                either_or_resources.append(resource_tuple)

        best_cost = self.recursive_calc(either_or_resources, left_resources, right_resources, needed_resources, [0, 0])
        return best_cost

    def availble_buy_resources(self, cards):
        resource_tuples = []
        for card in cards:
            # maybe can just use in and a list? less efficient but cleaner
            if card.card_type == C.RAW_R or card.card_type == C.MFG_R or card.card_type == C.WONDER_START:
                for resource_tuple in card.provides_resources:
                    resource_tuples.append(resource_tuple)
        return resource_tuples


    def recursive_calc(self, either_or_resources, left_resources, right_resources, needed_resources, cost):
        cost_list = []
        # print("needed resources, cost:", needed_resources, cost)
        if len(needed_resources) == 0:
            return cost
        for resource_tuple in either_or_resources:
            for resource in resource_tuple:
                if resource in needed_resources:
                    new_either_or_resources = either_or_resources.copy()
                    new_either_or_resources.remove(resource_tuple)
                    new_needed_resources = needed_resources.copy()
                    new_needed_resources.remove(resource)
                    cost_list.append(self.recursive_calc(new_either_or_resources, left_resources, right_resources, new_needed_resources, cost))
        for resource_tuple in left_resources:
            for resource in resource_tuple:
                if resource in needed_resources:
                    new_left_resources = left_resources.copy()
                    new_left_resources.remove(resource_tuple)
                    new_needed_resources = needed_resources.copy()
                    new_needed_resources.remove(resource)
                    added_cost = self.calc_resources_cost("left", resource)
                    new_cost = (cost[0] + added_cost, cost[1])
                    cost_list.append(self.recursive_calc(either_or_resources, new_left_resources, right_resources, new_needed_resources, new_cost))
        for resource_tuple in right_resources:
            for resource in resource_tuple:
                if resource in needed_resources:
                    new_right_resources = right_resources.copy()
                    new_right_resources.remove(resource_tuple)
                    new_needed_resources = needed_resources.copy()
                    new_needed_resources.remove(resource)
                    added_cost = self.calc_resources_cost("right", resource)
                    new_cost = (cost[0], cost[1] + added_cost)
                    cost_list.append(self.recursive_calc(either_or_resources, left_resources, new_right_resources, new_needed_resources, new_cost))
        
        best_cost = [999, 999]
        # print("cost list:", cost_list)
        for cost_val in cost_list:
            if (cost_val[0] + cost_val[1]) < best_cost[0] + best_cost[1]:
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

    def sum_card_type(self, player, card_type):
        total = 0
        for card in player.cards:
            if card.card_type == card_type:
                total += 1
        return total

    def eval_discard(self, player):
        # really just a placeholder for now
        return 1

        
