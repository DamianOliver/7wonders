import pygame as pg
import random as rand
import math

pg.init()

SCREEN_DIMENSION = [1440, 1000]
FRAME_TIME = 30

PLAYER_SPEED = 10

background_image = pg.image.load("Fight_Images/background.png")

clock = pg.time.Clock()
screen = pg.display.set_mode((SCREEN_DIMENSION), pg.RESIZABLE)

class Player:
    def __init__(self, pos, rotation, speed, health, weapon, color, size):
        self.pos = pos
        self.rotation = rotation
        self.speed = speed
        self.health = health
        self.weapon = weapon
        self.color = color
        self.size = size

    def draw(self):
        pg.draw.circle(screen, self.color, self.pos, self.size)

    def move(self, input_1, input_2):
        if input_1 == "up" or input_2 == "up":
            self.pos[1] -= self.speed
        if input_1 == "down" or input_2 == "down":
            self.pos[1] += self.speed
        if input_1 == "right" or input_2 == "right":
            self.pos[0] += self.speed
        if input_1 == "left" or input_2 == "left":
            self.pos[0] -= self.speed

        if self.pos[0] + self.size > SCREEN_DIMENSION[0]:
            self.pos[0] = SCREEN_DIMENSION[0] - self.size

        if self.pos[0] - self.size < 0:
            self.pos[0] = 0 + self.size

        if self.pos[1] + self.size > SCREEN_DIMENSION[1]:
            self.pos[1] = SCREEN_DIMENSION[1] - self.size

        if self.pos[1] - self.size < 1:
            self.pos[1] = 0 + self.size

    def rotate(self):
        mouse_pos = pg.mouse.get_pos()
        dx = (self.pos[0] - mouse_pos[0])
        dy = (self.pos[1] - mouse_pos[1])
        angle = math.atan2(dy, dx)
        degrees_angle = angle * 180 / 3.14159
        print(degrees_angle)
        return degrees_angle

class Weapon:
    def __init__(self, fire_rate, cooldown_time, projectile_type, size, image, player):
        self.fire_rate = fire_rate
        self.cooldown_time = cooldown_time
        self.projectile_type = projectile_type
        self.size = size
        self.image = image
        self.player = player

    def draw(self):
        weapon_image = pg.transform.scale(self.image, self.size)
        weapon_image = pg.transform.rotate(weapon_image, 180)
        if self.player.rotation > -90 and self.player.rotation < 90:
            weapon_image = pg.transform.flip(weapon_image, False, True)
        blit_pos = [self.player.pos[0], self.player.pos[1] - self.size[1] * 0.5]
        weapon_image, weapon_rect = self.rotate(weapon_image, self.player.rotation, (self.player.pos[0], self.player.pos[1]), pg.math.Vector2(0, 0))
        screen.blit(weapon_image, weapon_rect)

    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pg.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot+rotated_offset)
        # print(player.pos, angle, offset, rotated_offset, rect)
        return rotated_image, rect  # Return the rotated image and shifted rect.


class RocketLauncher(Weapon):
    def __init__(self, player):
        super().__init__(300, 0, Rocket, [100, 50], pg.image.load("Fight_Images/rocket_launcher.png"), player)

class Projectile:
    def __init__(self, pos, rotation, speed, damage, size, image):
        self.pos = pos
        self.rotation = rotation
        self.speed = speed
        self.damage = damage
        self.size = size
        self.image = image

class Rocket(Projectile):
    def __init__(self, pos, rotation):
        super().__init__(pos, rotation, 15, 80, [10, 2], pg.image.load("Fight_Images/rocket.png"))

player_1 = Player([100, SCREEN_DIMENSION[1] / 2], 0, PLAYER_SPEED, 100, "placeholder", (230, 30, 30), 10)
player_1.weapon = RocketLauncher(player_1)

class Game:
    def draw_background():
        background = pg.transform.scale(background_image, SCREEN_DIMENSION)
        screen.blit(background, (0, 0))

    def update():
        Game.draw_background()
        input_1, input_2 = Game.take_input()
        player_1.move(input_1, input_2)
        player_1.rotation = player_1.rotate()
        player_1.draw()
        player_1.weapon.draw()

    def take_input():
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

        return input_1, input_2

while True:
    clock.tick(FRAME_TIME)
    Game.update()

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
