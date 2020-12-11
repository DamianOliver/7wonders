import random

NUM_PLAYERS = 1
NUM_CARDS_PER_PLAYER = 4
NUM_TURNS = NUM_CARDS_PER_PLAYER - 1

class Game:
    def __init__(self):
        self.turn = 0
        self.players = [Player(i) for i in range(NUM_PLAYERS)]
        self.hands = []
        self.deck = self.create_deck()
        self.hands = self.create_hands(self.deck)

    def next_turn(self):
        self.turn += 1

    def ask_for_action(self):
        while True:
            action_input = input("Select your action, d for discard, p for play card, or b to buy a resource: ")
            if action_input == "d" or action_input == "p" or action_input == "b":
                return action_input

    def player_right_left(self, player_index):
        if player_index == 0:
            player_right = self.players[player_index + 1]
            player_left = self.players[len(self.players)]
        elif player_index == len(self.players):
            player_right = self.players[0]
            player_left = self.players[player_index - 1]
        else:
            player_right = self.players[player_index + 1]
            player_left = self.player_indexplayers[ - 1]
        return player_right, player_left

    def play(self):
        while self.turn < NUM_TURNS:
            print("turn {}".format(self.turn))

            for i in range(len(self.players)):
                player = self.players[i]
                hand = self.hands[(i + self.turn) % len(self.hands)]
                print("  Player {}".format(player.player_number))
                player.print_cards()
                for i in range(len(hand)):
                    print("Number: {} {}".format(i, hand[i].__str__()))
                action = self.ask_for_action()
                if action == "d":
                    player.discard_card(hand)
                elif action == "p":
                    player.select_card(hand)
                # elif action == "b":
                #     player.buy_resource(player)


            self.turn += 1

        self.print_player_cards()

    def print_player_cards(self):
        for player in self.players:
            print("  Player {} Cards: ".format(player.player_number))
            player.print_cards()


    def create_deck(self):
        deck = [ \
            Card("University", "Science", provides_sciences = ["science_symbol", "science_symbol"], cost = ["brick", "silk"]), 
            Card("Towel Factory", "Manufactored Resource", provides_resources = [("silk",),("silk",)]), 
            Card("Stones + Bricks 'r' Us", "Raw Resource", provides_resources = [("stone", "brick")]), 
            Card("Tavern", "Commercial", provides_resources = [("brick",)]), 
            Card("Tavern", "Commercial", provides_resources = [("coal",)]), 
            Card("Temple", "Civic", points = 4, cost = ["coal"]), 
            Card("Scriptorium", "Science", provides_sciences = ["science_symbol"]), 
            Card("Scriptorium", "Science", provides_sciences = ["science_symbol"]), 
            Card("Quarry", "Raw Resource", provides_resources = [("stone",)]),
            Card("Quarry", "Raw Resource", provides_resources = [("stone",)]), 
            Card("Towel Factory", "Manufactored Resource", provides_resources = [("silk",)]), 
            Card("Guard Tower", "Military", num_shields = 1, cost = ["stone"]), 
            Card("Guard Tower", "Military", num_shields = 1, cost = ["stone"]), 
            Card("Palace", "Civic", points = 8, cost = ["stone", "stone"])]
        # random.shuffle(deck)
        return deck

    def create_hands(self, deck):
        hands = []
        for i in range(NUM_PLAYERS):
            deck_len = len(deck)
            start = i * NUM_CARDS_PER_PLAYER
            end = (i + 1) * NUM_CARDS_PER_PLAYER
            hands.append(self.deck[start:end])
        return hands

class Player:
    def __init__(self, player_number):
        self.player_number = player_number
        self.cards = []
        self.money = 3

    def discard_card(self, hand_cards):
        selected_card_number = self.ask_for_card_selection(hand_cards)
        selected_card = hand_cards[selected_card_number]
        del hand_cards[selected_card_number]
        self.money += 3
        print("MONEY: ", self.money)

    def select_card(self, hand_cards):
        while True:
            selected_card_number = self.ask_for_card_selection(hand_cards)
            selected_card = hand_cards[selected_card_number]
            # player_resources_available = self.available_resources(self.cards)
            
            # if self.has_resources_for_card(player_resources_available, selected_card):

            resource_tuples = self.available_resources_tuples()

            if self.has_resources(selected_card.cost, resource_tuples):
                self.cards.append(hand_cards[selected_card_number])
                del hand_cards[selected_card_number]
            else:
                print("You do not have the required resources for that card.")

    def available_resources_tuples(self):
        resource_tuples = []        
        for card in self.cards:
            for resource_tuple in card.provides_resources:
                resource_tuples.append(resource_tuple)
        return resource_tuples

    def has_resources(self, cost, resource_tuples):
        if len(cost) == 0:
            return True
        elif len(resource_tuples) == 0:
            return False
        elif len(resource_tuples[0]) == 0:
            return self.has_resources(cost, resource_tuples[1:])
        else:
            for resource_option in resource_tuples[0]:
                cost_copy = cost.copy()
                try: 
                    cost_copy.remove(resource_option)
                except:
                    pass
                if self.has_resources(cost_copy, resource_tuples[1:]):
                    return True


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

    def print_cards(self):
        self.total_science_symbols = 0
        self.total_score = 0
        for card in self.cards:
            if card.card_type == "Science":
                for i in range(0, len(card.provides_resources)):
                    self.total_science_symbols += 1
        print("total science symbols: ", self.total_science_symbols)
        for card in self.cards:
            if card.card_type == "Science":
                card.points = 0
                for i in range(len(card.provides_resources)):
                    card.points += self.total_science_symbols
            if card.points > 0 and len(card.provides_resources) > 0:
                print("    {} - Provides {} Points - {} Cost - {}".format(card.name, card.provides_resources, card.points, card.cost))
            elif card.points > 0:
                print("    {} - {} points Cost - {}".format(card.name, card.points, card.cost))
            else:
                print("    {} - Provides {} Cost - {}".format(card.name, card.provides_resources, card.cost))
            self.total_score += card.points
        print("Total Score: ", self.total_score)

    # def buy_resource(self, player_index):
    #     player_right_available_resources = []
    #     player_left_available_resources = []
    #     player_right_index, player_left_index = Game.player_right_left(player_index)
    #     right_player = Game.players[player_right_index]
    #     left_player = Game.players[player_left_index]
    #     for card in right_player.cards:
    #         if card.type == "Manufactored Resource" or card.type == "Raw Resource":
    #             player_right_available_resources.append(card)
    #             print(card.provides_resources)



class Card:
    def __init__( self, name, card_type, points = 0, provides_resources = [], cost = [], provides_sciences = [], num_shields = 0):
        self.cost = cost
        self.points = points
        self.card_type = card_type
        self.name = name
        self.provides_resources = provides_resources
        self.provides_sciences = provides_sciences
        self.num_sheilds = num_shields

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}: Card Type: {}  Points = {}, Resources = {}, Science = {}, Shields = {}, Cost {}".format(self.name, self.card_type, self.points, self.provides_resources, self.provides_sciences, self.num_sheilds, self.cost)



Game().play()
