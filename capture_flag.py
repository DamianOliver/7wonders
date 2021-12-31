import pygame as pg
import random as rand

SCREEN_DIMENSION = (1440, 1000)
SCREEN_SIZE = SCREEN_DIMENSION
BACKRGOUND_COLOR = (100, 100, 100)

SAFE_ZONE_COLOR = (170, 170, 170)
SAFE_ZONE_WIDTH = 75

LINE_COLOR = (40, 40, 40)
LINE_THICKNESS = 10

PLAYER_SIZE = 10
PLAYER_SPEED = 10
PLAYER_2_START_POS = [100 + SAFE_ZONE_WIDTH, 500]
PLAYER_1_START_POS = [1340 - SAFE_ZONE_WIDTH, 500]
PLAYER_2_RETURN_POS = [100 + SAFE_ZONE_WIDTH, 500]
PLAYER_1_RETURN_POS = [1340 - SAFE_ZONE_WIDTH, 500]
PLAYER_2_COLOR = (50, 50, 230)
PLAYER_1_COLOR = (230, 50, 50)

FLAG_SIZE = [22, 40]
FLAG_1_START_POS = [50 + SAFE_ZONE_WIDTH, 500 - (0.5 * FLAG_SIZE[1])]
FLAG_2_START_POS = [1390 - SAFE_ZONE_WIDTH - FLAG_SIZE[0], 500 - (0.5 * FLAG_SIZE[1])]
FLAG_1_RETURN_POS = [50 + SAFE_ZONE_WIDTH, 500 - (0.5 * FLAG_SIZE[1])]
FLAG_2_RETURN_POS = [1390 - FLAG_SIZE[0] - SAFE_ZONE_WIDTH, 500 - (0.5 * FLAG_SIZE[1])]

FRAME_TIME = 30

TAGGED_TIME = 4000

AI = True

block_1 = False

pg.init()

game_over = False

clock = pg.time.Clock()

screen = pg.display.set_mode((SCREEN_DIMENSION), pg.RESIZABLE)

class Player:
    def __init__(self, size, color, speed, pos, start_pos, number, tagged, augmented):
        self.size = size
        self.color = color
        self.speed = speed
        self.pos = pos
        self.number = number
        self.start_pos = start_pos
        self.tagged = tagged
        self.augmented = augmented

    def move(self, direction):
        if self.number == 1:
            opponent = player_2
        elif self.number == 2:
            opponent = player_1
        if not self.tagged > 0:
            if direction == "up":
                self.pos[1] -= self.speed

            elif direction == "down":
                self.pos[1] += self.speed

            elif direction == "right":
                self.pos[0] += self.speed

            elif direction == "left":
                self.pos[0] -= self.speed

            if self.pos[0] + self.size > SCREEN_DIMENSION[0]:
                self.pos[0] = SCREEN_DIMENSION[0] - self.size

            if self.pos[0] - self.size < 0:
                self.pos[0] = 0 + self.size

            if self.pos[1] + self.size > SCREEN_DIMENSION[1]:
                self.pos[1] = SCREEN_DIMENSION[1] - self.size

            if self.pos[1] - self.size < 1:
                self.pos[1] = 0 + self.size

    def draw_player(self):
        pg.draw.circle(screen, self.color, self.pos, PLAYER_SIZE)

    def check_for_tag(self):
        if self.number == 1:
            opponent = player_2
            if not opponent.pos[0] >= SCREEN_SIZE[0] * 0.5 - LINE_THICKNESS * 0.5:
                return
        elif self.number == 2:
            opponent = player_1
            if not opponent.pos[0] <= SCREEN_SIZE[0] * 0.5 + LINE_THICKNESS * 0.5:
                return
        if self.pos[0] + self.size >= opponent.pos[0] - self.size and self.pos[0] - self.size <= opponent.pos[0] + opponent.size:
            if self.pos[1] + self.size >= opponent.pos[1] - self.size and self.pos[1] - self.size <= opponent.pos[1] + opponent.size:
        # if abs(self.pos[0] - opponent.pos[0] <= (self.size + opponent.size) * 0.5):
        #     if abs(self.pos[1] - opponent.pos[1] <= (self.size + opponent.size) * 0.5):
                if not opponent.pos[0] < SAFE_ZONE_WIDTH and not opponent.pos[0] > SCREEN_SIZE[0] - SAFE_ZONE_WIDTH:
                    return True

        return False

    def update_tagged(self):
        if self.tagged > 0:
            self.tagged -= FRAME_TIME
            if self.tagged <= 0:
                self.tagged = 0


class Flag:
    def __init__(self, start_pos, pos, number, size, grabbed):
        self.start_pos = start_pos
        self.pos = pos
        self.number = number
        self.size = size
        self.flag_1 = pg.image.load("Capture_The_Flag_Images/flag_1.png")
        self.flag_2 = pg.image.load("Capture_The_Flag_Images/flag_2.png")
        self.grabbed = grabbed

    def draw_flag(self):
        if self.number == 1:
            flag_image = self.flag_1
        elif self.number == 2:
            flag_image = self.flag_2
        flag_image = pg.transform.scale(flag_image, FLAG_SIZE)
        screen.blit(flag_image, self.pos)

    def check_player(self):
        if not self.grabbed:
            if self.number == 1:
                player = player_1
            elif self.number == 2:
                player = player_2
            # print("distance", self.number, ":", abs(self.pos[0] - player.pos[0]), player.pos[0])
            if player.pos[0] - player.size <= self.pos[0] + self.size[0] and player.pos[0] + player.size >= self.pos[0]:
                if player.pos[1] - player.size <= self.pos[1] + self.size[1] and player.pos[1] + player.size >= self.pos[1]:
                    # print(player.number, "grabbed")
                    self.grabbed = True

    def move(self):
        if self.grabbed:
            # print("return distance: ", abs(SCREEN_SIZE[0] * 0.5 - self.pos[0]), "pos:", self.pos[0], self.number)
            if self.number == 1:
                player = player_1
            elif self.number == 2:
                player = player_2
            self.pos = [player.pos[0], player.pos[1] - 30]
        else:
            self.pos = self.start_pos.copy()

class Game:
    def check_for_win():
        global game_over
        if player_1.pos[0]  + player_1.size > SCREEN_SIZE[0] * 0.5 + LINE_THICKNESS * 0.5 and flag_1.grabbed:
            print("RED WINS!")
            game_over = True
        if player_2.pos[0] - player_1.size < SCREEN_SIZE[0] * 0.5 - LINE_THICKNESS * 0.5 and flag_2.grabbed:
            print("BLUE WINS!")
            game_over = True

    def update():
        player_2_tagged = player_1.check_for_tag()
        player_1_tagged = player_2.check_for_tag()
        if player_1_tagged:
            Game.on_tag(player_1)
        if player_2_tagged:
            Game.on_tag(player_2)
        flag_1.check_player()
        flag_2.check_player()
        flag_1.move()
        flag_2.move()
        player_1.draw_player()
        player_2.draw_player()
        flag_1.draw_flag()
        flag_2.draw_flag()
        player_1.update_tagged()
        player_2.update_tagged()

    

    def take_input():
        global block_1
        key_pressed = pg.key.get_pressed()
        input_1 = "placeholder"
        input_2 = "placeholder"
        if key_pressed[pg.K_UP]:
            input_2 = "up"

        if key_pressed[pg.K_DOWN]:
            input_2 = "down"

        if key_pressed[pg.K_LEFT]:
            input_1 = "left"

        if key_pressed[pg.K_RIGHT]:
            input_1 = "right"

        if key_pressed[pg.K_BACKSPACE]:
            Game.restart()

        player_1.move(input_1)
        player_1.move(input_2)

        if not AI:
            if key_pressed[pg.K_w]:
                player_2.move("up")

            if key_pressed[pg.K_s]:
                player_2.move("down")

            if key_pressed[pg.K_a]:
                player_2.move("left")

            if key_pressed[pg.K_d]:
                player_2.move("right")

            if key_pressed[pg.K_TAB]:
                if not block_1:
                    block_1 = True
                else:
                    block_1 = False

    def take_ai_input(input_1, input_2, player):
        if input_1 == "up" or input_2 == "up":
            player.move("up")

        if input_1 == "down" or input_2 == "down":
            player.move("down")

        if input_1 == "left" or input_2 == "left":
            player.move("left")

        if input_1 == "right" or input_2 == "right":
            player.move("right")

    def on_tag(tagged):
        tagged.pos = tagged.start_pos.copy()
        tagged.tagged += TAGGED_TIME
        if tagged.number == 1:
            flag_1.grabbed = False
        elif tagged.number == 2:
            flag_2.grabbed = False

    def restart():
        print("reset")
        global game_over
        player_1.pos = player_1.start_pos.copy()
        player_2.pos = player_2.start_pos.copy()
        player_1.tagged = 0
        player_2.tagged = 0
        flag_1.grabbed = False
        flag_2.grabbed = False
        flag_1.pos = flag_1.start_pos.copy()
        flag_2.pos = flag_2.start_pos.copy()
        player_1.tagged = 0
        player_2.tagged = 0
        game_over = False

class Bot:
    def __init__(self, current_action, strat, player, flag, opponent, own_flag, last_input):
        self.curent_action = current_action
        self.strat = strat
        self.player = player
        self.flag = flag
        self.opponent = opponent
        self.own_flag = own_flag
        self.last_input = last_input

    def run(self, direction):
        input_2 = "placeholder"
        input_1 = "placeholder"
        if direction == "right":
            direction_x = self.player.speed
        elif direction == "left":
            direction_x = -1 * self.player.speed

        if self.player.start_pos[0] > SCREEN_SIZE[0]:
            argument = self.player.pos[0] - 0.5 * self.player.size  - 0.5 * self.opponent.size > SCREEN_SIZE[0] / 2 - LINE_THICKNESS
        else:
            argument = self.player.pos[0] + 0.5 * self.player.size + 0.5 * self.opponent.size < SCREEN_SIZE[0] / 2 - LINE_THICKNESS
        if argument:
            input_1 = direction
            retreat = False
        elif not self.check_for_tag(self.player.pos[0] + direction_x, self.player.pos[1], self.opponent.pos[0], self.opponent.pos[1]):
            retreat = False
            input_1 = direction
        elif not self.check_for_tag(self.player.pos[0], self.player.pos[1], self.opponent.pos[0], self.opponent.pos[1]):
            retreat = True
            input_1 = "placeholder"
            direction_x = 0
        else:
            retreat = True
            if self.player.pos[0] > self.opponent.pos[0]:
                input_1 = "right"
                direction_x = self.player.speed
            else:
                input_1 = "left"
                direction_x = -1 * self.player.speed

        if not self.flag.grabbed:
            if abs(self.player.pos[0] - self.flag.pos[0]) <= abs(self.player.pos[1] - self.flag.pos[1]) or retreat:
                if self.player.pos[1] > self.flag.pos[1]:
                    direction_y = -1 * self.player.speed
                else:
                    direction_y = self.player.speed
                if not self.check_for_tag(self.player.pos[0] + direction_x, self.player.pos[1] + direction_y, self.opponent.pos[0], self.opponent.pos[1]) or argument:
                    if self.player.pos[1] > self.flag.pos[1]:
                        input_2 = "up"
                    else:
                        input_2 = "down"
                    if self.check_for_block():
                        input_2 = "placeholder"
                elif not self.check_for_tag(self.player.pos[0] + direction_x, self.player.pos[1], self.opponent.pos[0], self.opponent.pos[1]):
                    input_2 = "placeholder"
                else:
                    if self.player.pos[1] > self.opponent.pos[1]:
                        input_2 = "down"
                    else:
                        input_2 = "up"

            else:
                if self.player.pos[1] > self.opponent.pos[1]:
                    direction_y = self.player.speed
                    input_2 = "down"
                else:
                    direction_y = -1 * self.player.speed
                    input_2 = "up"
                if not self.check_for_tag(self.player.pos[0] + direction_x, self.player.pos[1] + direction_y, self.opponent.pos[0], self.opponent.pos[1]):
                    placeholder = 0
                elif not self.check_for_tag(self.player.pos[0] + direction_x, self.player.pos[1], self.opponent.pos[0], self.opponent.pos[1]):
                    input_2 = "placeholder"
                else:
                    if self.player.pos[1] > self.opponent.pos[1]:
                        input_2 = "down"
                    else:
                        input_2 = "up"

        else:
            if rand.randrange(0, 8) == 3:
                print("switch")
                if self.last_input[1] == "down":
                    input_2 = "up"
                    direction_y = -1 * self.player.speed
                else:
                    input_2 = "down"
                    direction_y = self.player.speed
            else:
                if self.last_input[1] == "down":
                    direction_y = self.player.speed
                    input_2 = "down"
                else:
                    direction_y = -1 * self.player.speed
                    input_2 = "up"

            if self.check_for_tag(self.player.pos[0], self.player.pos[1], self.opponent.pos[0], self.opponent.pos[1]):
                if self.player.pos[1] > self.opponent.pos[1]:
                    input_2 = "down"
                    direction_y = self.player.speed
                else:
                    input_2 = "up"
                    direction_y = -1 * self.player.speed

                if self.check_for_tag(self.player.pos[0], self.player.pos[1] + direction_y, self.opponent.pos[0], self.opponent.pos[1]):
                    if self.player.pos[0] > self.opponent.pos[0]:
                        input_2 = "right"
                    else:
                        input_2 = "left"
            else:
                if self.check_for_tag(self.player.pos[0], self.player.pos[1] + direction_y, self.opponent.pos[0], self.opponent.pos[1]):
                    input_2 = "placeholder"
                    direction_y = 0

                if self.check_for_tag(self.player.pos[0] + direction_x, self.player.pos[1] + direction_y, self.opponent.pos[0], self.opponent.pos[1]):
                    input_1 = "placeholder"





            # if self.check_for_block():
            #     input_2 = "placeholder"
            #     if self.player.pos[0] > self.own_flag.pos[0]:
            #         if not self.check_for_tag(self.player.pos[0] + self.player.speed, self.player.pos[1], self.opponent.pos[0], self.player.pos[1]):
            #             input_1 = "right"
            #     else:
            #         if not self.check_for_tag(self.player.pos[0] - self.player.speed, self.player.pos[1], self.opponent.pos[0], self.player.pos[1]):
            #             input_1 = "left"

            # if self.check_for_tag(self.player.pos[0] + self.direction_x, self.player.pos[1] + self.direction_y, self.opponent.pos[0], self.opponent.pos[1]):
            #     input_2 = "placeholder"
            # elif self.check_for_tag(self.player.pos[0] + self.direction_x, self.player.pos[1], self.opponent.pos[0], self.opponent.pos[1]):
            #     if self.player.pos[1] > self.opponent.pos[1]:

        if input_1 == "placeholder" and input_2 == "placeholder":
            if self.player.pos[0] > self.opponent.pos[0]:
                input_1 = "right"
            else:
                input_1 = "left"
            # if self.player.pos[1] > self.opponent.pos[1]:
            #     input_1 = "down"
            # else:
            #     input_1 = "up"
        print(input_1, input_2)
        return input_1, input_2

    def check_for_tag(self, pos_1_x, pos_1_y, pos_2_x, pos_2_y):
        # print("distance of x: ", abs(pos_1_x - pos_2_x), self.opponent.speed + (self.player.size * 0.5) + (self.opponent.size * 0.5))
        # print("distance of y: ", abs(pos_1_y - pos_2_y), self.opponent.speed + (self.player.size * 0.5) + (self.opponent.size * 0.5))
        if abs(pos_1_x - pos_2_x) <= self.opponent.speed + (self.player.size * 0.5) + (self.opponent.size * 0.5):
            if abs(pos_1_y - pos_2_y) <= self.opponent.speed + (self.player.size * 0.5) + (self.opponent.size * 0.5):
                if self.player.start_pos[0] > SCREEN_SIZE[0] / 2:
                    if pos_1_x - self.player.size > SCREEN_SIZE[0] / 2:
                        return False
                else:
                    if pos_1_x + self.player.size < SCREEN_SIZE[0] / 2:
                        return False
                if self.own_flag.grabbed:
                    return False
                print("oh no")
                return True
        return False

    def check_for_block(self,):
        if self.player.pos[0] - self.flag.pos[0] != 0 and self.player.pos[0] - self.opponent.pos[0] != 0:
            self_flag_angle = (self.player.pos[1] - self.flag.pos[1]) / (self.player.pos[0] - self.flag.pos[0])
            self_opponent_angle = (self.player.pos[1] - self.opponent.pos[1]) / (self.player.pos[0] - self.opponent.pos[0])
            # print(self_flag_angle, self_opponent_angle, abs(self_flag_angle - self_opponent_angle))
            if abs(self_flag_angle - self_opponent_angle) < .2:
                print("block")
                return True
        return False

    def attack(self):
        if self.player.tagged > 0:
            print("come on")
        input_1 = "placeholder"
        input_2 = "placeholder"
        if not self.flag.grabbed:
            if self.flag.pos[0] > self.player.pos[0]:
                input_1, input_2 = self.run("right")
            else:
                input_1, input_2 = self.run("left")
        else:
            input_1, input_2 = self.run("left")

        self.last_input = [input_1, input_2]
        return input_1, input_2


player_1 = Player(PLAYER_SIZE, PLAYER_1_COLOR, PLAYER_SPEED, PLAYER_1_START_POS, PLAYER_1_RETURN_POS, 1, 0, False)
player_2 = Player(PLAYER_SIZE, PLAYER_2_COLOR, PLAYER_SPEED, PLAYER_2_START_POS, PLAYER_2_RETURN_POS, 2, 0, False)
flag_1 = Flag(FLAG_1_RETURN_POS, FLAG_1_START_POS, 1, FLAG_SIZE, False)
flag_2 = Flag(FLAG_2_RETURN_POS, FLAG_2_START_POS, 2, FLAG_SIZE, False)

bot = Bot("choose", "choose", player_2, flag_2, player_1, flag_1, ["placeholder", "placeholder"])
aug_bot = Bot("choose", "choose", player_1, flag_1, player_2, flag_2, ["placeholder", "placeholder"])

def draw_background():
    pg.draw.rect(screen, (BACKRGOUND_COLOR), ((0, 0), SCREEN_SIZE))
    pg.draw.rect(screen, LINE_COLOR, ((720 - 0.5*LINE_THICKNESS, 0), (LINE_THICKNESS, SCREEN_SIZE[1])))
    pg.draw.rect(screen, SAFE_ZONE_COLOR, ((0, 0), (SAFE_ZONE_WIDTH, SCREEN_SIZE[1])))
    pg.draw.rect(screen, SAFE_ZONE_COLOR, ((SCREEN_SIZE[0] - SAFE_ZONE_WIDTH, 0), (SAFE_ZONE_WIDTH, SCREEN_SIZE[1])))

draw_background()

while True:
    clock.tick(FRAME_TIME)
    draw_background()

    Game.take_input()

    if AI:
        input_1, input_2 = bot.attack()
        Game.take_ai_input(input_1, input_2, player_2)

    Game.update()

    Game.check_for_win()

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            
    if game_over:
        for i in range(3):
            print(3-i)
            pg.time.wait(1000)
        Game.restart()
