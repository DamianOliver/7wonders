import random

NUM_PLAYERS = 1
NUM_CARDS_PER_PLAYER = 7
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

    def play(self):
        while self.turn < NUM_TURNS:

            print("turn {}".format(self.turn))

            for i in range(len(self.players)):
                player = self.players[i]
                hand = self.hands[(i + self.turn) % len(self.hands)]
                print("  Player {}".format(player.player_number))
                player.select_card(hand)

            self.turn += 1

        self.print_player_cards()

    def print_player_cards(self):
        for player in self.players:
            print("  Player {} Cards: ".format(player.player_number))
            player.print_cards()


    def create_deck(self):
        deck = [ \
            Card("Tavern", "Commercial", provides_resources = [("brick",)]), 
            Card("Tavern", "Commercial", provides_resources = [("coal",)]), 
            Card("Stone + Bricks 'r' Us", "Raw Resource Either/Or", provides_resources = [("stone", "brick")]), 
            Card("Temple", "Civic", points = 4, cost = ["coal"]), 
            Card("Scriptorium", "Science", provides_sciences = ["science_symbol"]), 
            Card("Scriptorium", "Science", provides_sciences = ["science_symbol"]), 
            Card("Quarry", "Raw Resource", provides_resources = [("stone",)]),
            Card("Quarry", "Raw Resource", provides_resources = [("stone",)]), 
            Card("Towel Factory", "Manufactored Resource", provides_resources = [("silk",)]), 
            Card("Towel Factory", "Manufactored Resource", provides_resources = [("silk",)]), 
            Card("Guard Tower", "Military", num_shields = 1, cost = ["stone"]), 
            Card("Guard Tower", "Military", num_shields = 1, cost = ["stone"]), 
            Card("University", "Science", provides_sciences = ["science_symbol", "science_symbol"], cost = ["brick", "silk"]), 
            Card("Palace", "Civic", points = 8, cost = ["stone", "stone"])]
        random.shuffle(deck)
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


    def select_card(self, hand_cards):
        while True:
            self.print_cards()
            selected_card_number = self.ask_for_card_selection(hand_cards)
            selected_card = hand_cards[selected_card_number]
            player_resources_available = self.available_resources(self.cards)
            
            if self.has_resources_for_card(player_resources_available, selected_card):
                self.cards.append(hand_cards[selected_card_number])
                del hand_cards[selected_card_number]
            else:
                print("You do not have the required resources for that card.")

    def available_resources(self, cards):
        resources = []
        either_or_resources = []
        for card in cards:
            for resource_tuple in card.provides_resources:
                 resources.append(resource_tuple[0])                
            #if card.card_type == "Raw Resource" or card.card_type == "Manufactored Resource" or card.card_type == "Commercial":

                #resources.extend(card.provides_resources)
            #elif card.card_type == "Raw Resource Either/Or" or self.cards[card].card_type == "Manufactored Resource Either/Or":
                #either_or.append(card.provides_resources)
        # I really don't know what I'm doing...
        # for card in either_or_resources:
        #     new_list = resources.copy
        #     for resource in card.provides_resources:
        #         new_list.append(resource)
        #         resources.append(new_list)
        return resources

    def has_resources_for_card(self, resources, card):
        card_resource_cost = card.cost.copy()

        i = 0
        a = 0
        while i < len(card_resource_cost):
            while a < len(resources):
                if resources[a] == card_resource_cost[i]:
                    del resources[a]
                    del card_resource_cost[i]
                    i -= 1
                    break 
                else: 
                    a += 1
            i += 1

        return len(card_resource_cost) == 0

    def ask_for_card_selection(self, hand_cards):
        for i in range(len(hand_cards)):
            print("Number: {} {}".format(i, hand_cards[i].__str__()))
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
