import pygame as pg
import random as rand
import math

pg.init()

SCREEN_DIMENSION = [1440, 1000]
FRAME_TIME = 30

SIDE_BAR_SIZE = (200, SCREEN_DIMENSION[1])
HEALTH_BAR_SIZE = (75, SCREEN_DIMENSION[1] * 0.7)
HEALTH_BAR_BORDER = 3

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

        if self.pos[0] - self.size < 0 + SIDE_BAR_SIZE[0]:
            self.pos[0] = SIDE_BAR_SIZE[0] + self.size

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
        if degrees_angle < 0:
            degrees_angle += 360
        # print(degrees_angle)
        line = pg.image.load("Fight_Images/rocket_launcher.png")
        return degrees_angle

class Weapon:
    def __init__(self, fire_rate, cooldown_time, cooldown, projectile_type, size, image, player):
        self.fire_rate = fire_rate
        self.cooldown_time = cooldown_time
        self.cooldown = cooldown
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

    def shoot(self):
        if not self.cooldown_time > 0:
            game.projectile_list.append(self.projectile_type(self.player.pos.copy(), self.player.rotation))
            self.cooldown_time += self.cooldown

    def update_cooldown_time(self):
        if self.cooldown_time > 0:
            self.cooldown_time -= 1


class RocketLauncher(Weapon):
    def __init__(self, player):
        super().__init__(300, 0, 50, Rocket, [100, 50], pg.image.load("Fight_Images/rocket_launcher.png"), player)

class Projectile:
    def __init__(self, pos, rotation, speed, damage, image, size):
        self.pos = pos
        self.rotation = rotation
        self.speed = 0
        self.damage = damage
        self.image = image
        self.size = size

    def rocket_tip(self):
        return pg.math.Vector2(self.size[0] * .9, self.size[1] / 2)

    def update_pos(self):
        self.pos[0] -= self.speed * math.cos(math.radians(self.rotation))
        self.pos[1] -= self.speed * math.sin(math.radians(self.rotation))

    def draw(self):
        image, rect = self.rotate(self.image, self.rotation, (self.pos[0], self.pos[1]), pg.math.Vector2(0, 0))
        screen.blit(image, rect)

    def rotate(self, surface, angle, pivot, offset):
        rotated_image = pg.transform.rotozoom(surface, -angle, 1)
        rect = rotated_image.get_rect(center=pivot)
        return rotated_image, rect

    def check_for_collision(self, point, player_point, player_size):
        rotated_tip = self.rocket_tip().rotate(self.rotation)
        x = rotated_tip[0] + self.pos[0]
        y = rotated_tip[1] + self.pos[1]

        print(abs(point + x - player_point[0]), abs(y - player_point[1]), player_size)

        pg.draw.circle(screen, (0, 0, 0), (x, y), 10)

        if abs(point + x - player_point[0]) < player_size and abs(x - player_point[1]) < player_size:
            return True
        return False

class Rocket(Projectile):
    def __init__(self, pos, rotation):
        image = pg.image.load("Fight_Images/rocket.png")
        image = pg.transform.scale(image, (80, 40))
        image = pg.transform.rotate(image, 180)
        super().__init__(pos, rotation, 3, 80, image, (80, 40))

class Game:
    def __init__(self, player, bot_list, projectile_list):
        self.projectile_list = projectile_list
        self.player = player
        self.bot_list = bot_list

    def draw_background(self):
        background = pg.transform.scale(background_image, SCREEN_DIMENSION)
        screen.blit(background, (0, 0))

    def draw_side_bar(self):
        pg.draw.rect(screen, (100, 100, 100), ((0, 0), SIDE_BAR_SIZE))
        self.draw_health()

    def draw_health(self):
        pg.draw.rect(screen, (25, 25, 25), ((30, ((SCREEN_DIMENSION[1] - HEALTH_BAR_SIZE[1])) / 2), HEALTH_BAR_SIZE))
        pg.draw.rect(screen, (200, 10, 10), ((30 + HEALTH_BAR_BORDER, (((SCREEN_DIMENSION[1] - HEALTH_BAR_SIZE[1]) / 2) + (HEALTH_BAR_SIZE[1]) * (1 - self.player.health / 100)) + HEALTH_BAR_BORDER), (HEALTH_BAR_SIZE[0] - HEALTH_BAR_BORDER * 2, (HEALTH_BAR_SIZE[1] - HEALTH_BAR_BORDER * 2) * self.player.health / 100)))

    def update(self):
        self.draw_background()
        input_1, input_2 = game.take_input()
        self.player.move(input_1, input_2)
        self.player.rotation = self.player.rotate()
        self.player.draw()
        self.player.weapon.draw()
        self.player.weapon.update_cooldown_time()
        for projectile in self.projectile_list:
            if projectile.check_for_collision((projectile.pos[0] + projectile.size[0] * 0.5, projectile.pos[1]), self.player.pos, self.player.size):
                self.player.health -= projectile.damage
                self.projectile_list.remove(projectile)
            for player in self.bot_list:
                if projectile.check_for_collision((projectile.pos[0] + projectile.size[0] * 0.5, projectile.pos[1] + projectile.size[1] * 0.5), player.pos, player.size):
                    player.health -= projectile.damage
                    self.projectile_list.remove(projectile)
        for projectile in self.projectile_list:
            projectile.update_pos()
            self.check_out_of_bounds(projectile)
            projectile.draw()
        self.draw_side_bar()

    def take_input(self):
        key_pressed = pg.key.get_pressed()
        input_1 = "placeholder"
        input_2 = "placeholder"

        if key_pressed[pg.K_UP] or key_pressed[pg.K_w]:
            input_2 = "up"

        if key_pressed[pg.K_DOWN] or key_pressed[pg.K_s]:
            input_2 = "down"

        if key_pressed[pg.K_LEFT] or key_pressed[pg.K_a]:
            input_1 = "left"

        if key_pressed[pg.K_RIGHT] or key_pressed[pg.K_d]:
            input_1 = "right"

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        if pg.mouse.get_pressed()[0]:
            game.player.weapon.shoot()

        return input_1, input_2

    def check_out_of_bounds(self, projectile):
        if projectile.pos[0] - projectile.size[0] > SCREEN_DIMENSION[0]:
            self.projectile_list.remove(projectile)
        elif projectile.pos[0] + projectile.size[0] < 0 + SIDE_BAR_SIZE[0]:
            self.projectile_list.remove(projectile)
        elif projectile.pos[1] - projectile.size[1] > SCREEN_DIMENSION[1]:
            self.projectile_list.remove(projectile)
        elif projectile.pos[1] + projectile.size[1] < 0:
            self.projectile_list.remove(projectile)

game = Game(Player([100 + SIDE_BAR_SIZE[0], SCREEN_DIMENSION[1] / 2], 0, PLAYER_SPEED, 100, "placeholder", (230, 30, 30), 10), [], [])

game.player.weapon = RocketLauncher(game.player)

while True:
    clock.tick(FRAME_TIME)
    game.update()

    pg.display.update()