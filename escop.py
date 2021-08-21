import pygame
#import math
#import random as rand
from collections import deque

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
MOVE_SPEED = 8
LOOK_DOWN_DELAY = 100
LOOK_DOWN_DURATION = 120

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
    def render(self, screen, cam):
        pass
    def update(self):
        pass

class Rect(Entity):
    def __init__(self, x, y, w, h, image = None, color = None):
        Entity.__init__(self, x, y, w, h)
        self.color = color
        self.image = image
        if image is None and color is None:
            self.color = DEFAULT_COLOR
            self.useColor = True
            self.useImage = False
        elif image is None:
            self.color = color
            self.useColor = True
            self.useImage = False
        else:
            self.image = pygame.transform.scale(image, (w, h))
            self.useColor = False
            self.useImage = True
    def render(self, screen, cam):
        if self.useColor:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - cam.pos.x, self.pos.y - cam.pos.y, self.w, self.h))
        elif self.useImage:
            screen.blit(self.image, (self.pos.x - cam.pos.x, self.pos.y - cam.pos.y))

    def getCollision(self, rect):
        xColliding = rect.pos.x < self.pos.x + self.w and rect.pos.x + rect.w > self.pos.x
        yColliding = rect.pos.y < self.pos.y + self.h and rect.pos.y + rect.h > self.pos.y

        collision = (0, 0)
        if xColliding and yColliding:
            if rect.pos.x < self.pos.x:
                collision = (rect.pos.x + rect.w - self.pos.x, collision[1])
            elif rect.pos.x + rect.w > self.pos.x + self.w:
                collision = (self.pos.x + self.w - rect.pos.x, collision[1])
            else:
                smaller = rect
                if self.w < rect.w:
                    smaller = self
                collision = (smaller.w, collision[1])
            if rect.pos.y < self.pos.y:
                collision = (collision[0], rect.pos.y + rect.h - self.pos.y)
            elif rect.pos.y + rect.h > self.pos.y + self.h:
                collision = (collision[0], self.pos.y + self.h - rect.pos.y)
            else:
                smaller = rect
                if self.h < rect.h:
                    smaller = self
                collision = (collision[0], smaller.h)
        return collision
    def isColliding(self, rect):
        xColliding = rect.pos.x < self.pos.x + self.w and rect.pos.x + rect.w > self.pos.x
        yColliding = rect.pos.y < self.pos.y + self.h and rect.pos.y + rect.h > self.pos.y

        return xColliding and yColliding
    def handleCollision(self, rect):
        collision = self.getCollision(rect)
        if collision[0] > collision[1]:

            #if self.pos.y <= rect.pos.y:
            if self.vel.y > 0:
                self.vel.y = 0
                self.pos.y = rect.pos.y - self.h
                return True
            else:
                self.vel.y = 0
                self.pos.y = rect.pos.y + rect.h

        else:
            if self.vel.x > 0:
                self.pos.x = rect.pos.x - self.w
            else:
                self.pos.x = rect.pos.x + rect.w


            self.vel.x = 0
        return False



class Physical_Rect(Rect):
    def __init__(self, x, y, w, h, x_vel = 0, y_vel = 0, image = None, color = None, hasGravity = True):
        Rect.__init__(self, x, y, w, h, image = image, color = color)
        self.vel = Vector2(x_vel, y_vel)
        self.is_jumping = False
        self.hasGravity = hasGravity
        self.going = False


    def update(self):
        self.pos = self.pos + self.vel
        if (self.hasGravity):
            self.vel.y += GRAVITY
        if self.going:
            gotoStep()

    def goto(self, position, duration):
        self.going = True
        self.goHere = position
        self.goTime = duration
    def gotoStep(self):
        pass

class Camera(Rect):
    def __init__(self, x, y, w, h, player):
        Rect.__init__(self, x, y, w, h)
        self.player = player
        self.lookDownOffset = SCREEN_HEIGHT / 4
        self.lookDownStep = self.lookDownOffset / LOOK_DOWN_DURATION
        self.lookDownCount = 0

        self.playerPrev = deque()
        for i in range(5):
            self.playerPrev.append(self.player.pos)

    def update(self):


        playerPos = self.playerPrev.popleft()
        self.pos.x = playerPos.x + (self.player.w / 2) - self.w / 2
        self.pos.y = playerPos.y - 4 * self.h / 7

        if self.lookDownCount >= LOOK_DOWN_DELAY:
            self.playerPrev.append(Vector2(self.player.pos.x, self.player.pos.y + self.lookDownStep))
            if not (self.lookDownCount - LOOK_DOWN_DELAY > LOOK_DOWN_DURATION):
                self.lookDownStep += self.lookDownOffset / LOOK_DOWN_DURATION
        else:
            self.playerPrev.append(self.player.pos)
            self.lookDownStep = self.lookDownOffset / LOOK_DOWN_DURATION

        if keys_down['s']:
            self.lookDownCount += 1
        else:
            self.lookDownCount = 0


    def render(self, screen, cam):
        pass



class Cop(Physical_Rect):
    def __init__(self, x, y, w, h, image):
        Physical_Rect.__init__(self, x, y, w, h, image = image)
    def update(self):
        Physical_Rect.update(self)

class Coon(Physical_Rect):
    def __init__(self, x, y, w, h, image = None, color = None):
        Physical_Rect.__init__(self, x, y, w, h, image = image, color = color)
        self.lookRight = True;

    def update(self):
        self.is_jumping = True
        if (self.image is not None):
            if self.vel.x < 0 and self.lookRight:
                self.lookRight = False
                self.image = pygame.transform.flip(self.image, True, False)
            elif self.vel.x > 0 and (not self.lookRight):
                self.lookRight = True
                self.image = pygame.transform.flip(self.image, True, False)
        Physical_Rect.update(self)
        for other in collideable:
            if (self.isColliding(other)):
                self.handleCollision(other)


    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel.y -= 30
    def handleCollision(self, rect):
        if Rect.handleCollision(self, rect):
            self.is_jumping = False



def handle_input():
    common_objs['player'].vel.x = 0
    if keys_down['a']:
        common_objs['player'].vel.x += -MOVE_SPEED
    if keys_down['d']:
        common_objs['player'].vel.x += MOVE_SPEED
    if keys_down['space']:
        common_objs['player'].jump()


def update():
    handle_input()
    for obj in gameobjects:
        obj.update()


def render():
    screen.fill(BLACK)

    for obj in gameobjects:
        if obj is not common_objs['cam'] and obj.isColliding(common_objs['cam']):
            obj.render(screen, common_objs['cam'])

    pygame.display.flip()

def main():
    global screen, stop, clock, keys_down, gameobjects, common_objs, collideable

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

    #coon = Coon(SCREEN_WIDTH / 2 - 140 / 2, 4 * SCREEN_HEIGHT / 5, 140, 140, pygame.image.load('Images/racoon.png'))
    coon = Coon(SCREEN_WIDTH / 2 - 140 / 2, 4 * SCREEN_HEIGHT / 5, 20, 20, color = WHITE)
    cop = Cop(300, 0, 130, 180, pygame.image.load('Images/cop.png'))
    cam = Camera(coon.pos.x + (coon.w / 2) - SCREEN_WIDTH / 2, coon.pos.y + coon.h - SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, coon)
    block = Rect(0, SCREEN_HEIGHT - 200, 50, 200, color = BLUE)
    ground = Rect(-200, SCREEN_HEIGHT - 50, 800, 50, color = YELLOW)

    common_objs = {}
    gameobjects = []
    collideable = []
    gameobjects.append(coon)
    gameobjects.append(cop)
    gameobjects.append(cam)
    gameobjects.append(block)
    gameobjects.append(ground)

    collideable.append(block)
    collideable.append(ground)

    common_objs['player'] = coon
    common_objs['test_cop'] = cop
    common_objs['cam'] = cam


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
