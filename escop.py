import pygame
#import math
#import random as rand

#colors
BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
GREEN=pygame.color.THECOLORS["green"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
ORANGE=pygame.color.THECOLORS["orange"]
VIOLET=pygame.color.THECOLORS["violet"]
LIGHT_CYAN=pygame.color.THECOLORS["lightcyan"]
LIGHT_GREEN=pygame.color.THECOLORS["lightgreen"]
LIGHT_BLUE=pygame.color.THECOLORS["lightblue"]
LIGHT_YELLOW=pygame.color.THECOLORS["lightyellow"]
DEFAULT_COLOR = RED

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
GRAVITY = 1

class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)
    def __EQ__(self, other):
        return self.x == other.x and self.y == other.y
    def __NE__(self, other):
        return (not (self == other))
    def __len__(self):
        return (self.x * self.x + self.y * self.y) ** (1/2)
    def clear(self):
        self.x = 0
        self.y = 0


class Entity():
    def __init__(self, x, y, w, h):
        self.pos = Vector2(x, y)
        self.w = w
        self.h = h
    def render(self, screen):
        pass
    def update(self):
        pass

class Rect():
    def __init__(self, x, y, w, h, image = None, color = None):
        Entity.__init__(self, x, y, w, h)
        if image is None and color is None:
            self.color = DEFAULT_COLOR
            self.useColor = True
        elif image is None:
            self.color = color
            self.useColor = True
        else:
            self.image = pygame.transform.scale(image, (w, h))
            self.useColor = False
    def render(self, screen):
        if self.useColor:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.w, self.h))
        else:
            screen.blit(self.image, (self.pos.x, self.pos.y))


class Physical_Rect(Rect):
    def __init__(self, x, y, w, h, x_vel = 0, y_vel = 0, image = None, color = None):
        Rect.__init__(self, x, y, w, h, image = image, color = color)
        self.vel = Vector2(x_vel, y_vel)
        self.is_jumping = False

    def update(self):
        self.pos = self.pos + self.vel

        self.vel.y += GRAVITY

        if self.pos.y + self.h > SCREEN_HEIGHT: #check if too high
            self.pos.y = SCREEN_HEIGHT - self.h
            self.vel.y = 0
            self.is_jumping = False
        if self.pos.x + self.w + 10 > SCREEN_WIDTH: #check if too far to right
            self.pos.x = SCREEN_WIDTH - self.w
            self.vel.x = 0
        if self.pos.x - 10 < 0: #check if too far to left
            self.pos.x = 0
            self.vel.x = 0


class Cop(Physical_Rect):
    def __init__(self, x, y, w, h, image):
        Physical_Rect.__init__(self, x, y, w, h, image=image)
    def update(self):
        Physical_Rect.update(self)

class Racoon(Physical_Rect):
    def __init__(self, x, y, w, h, image):
        Physical_Rect.__init__(self, x, y, w, h, image=image)

    def update(self):
        Physical_Rect.update(self)
    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel.y -= 30


def handle_input():
    common_objs['player'].vel.x = 0
    if keys_down['a']:
        common_objs['player'].vel.x += -10
    if keys_down['d']:
        common_objs['player'].vel.x += 10
    if keys_down['space']:
        common_objs['player'].jump()


def update():
    handle_input()
    for obj in gameobjects:
        obj.update()


def render():
    screen.fill(BLACK)

    for obj in gameobjects:
        obj.render(screen)

    pygame.display.flip()

def main():
    global screen, stop, clock, keys_down, gameobjects, common_objs

    pygame.init()
    stop = False
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    keys_down = {
        'a' : False,
        'd' : False,
        's' : False,
        'w' : False,
        'space' : False
    }

    racoon = Racoon(0, 0, 140, 140, pygame.image.load('Images/racoon.png'))
    cop = Cop(300, 0, 130, 160, pygame.image.load('Images/cop.png'))

    common_objs = {}
    gameobjects = []
    gameobjects.append(racoon)
    gameobjects.append(cop)
    common_objs['player'] = racoon
    common_objs['test_cop'] = cop

    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    keys_down['a'] = True
                elif event.key == pygame.K_d:
                    keys_down['d'] = True
                elif event.key == pygame.K_s:
                    keys_down['s'] = True
                elif event.key == pygame.K_w:
                    keys_down['w'] = True
                elif event.key == pygame.K_SPACE:
                    keys_down['space'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    keys_down['a'] = False
                elif event.key == pygame.K_d:
                    keys_down['d'] = False
                elif event.key == pygame.K_s:
                    keys_down['s'] = False
                elif event.key == pygame.K_w:
                    keys_down['w'] = False
                elif event.key == pygame.K_SPACE:
                    keys_down['space'] = False

        update()
        render()

        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
