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
    def render(self, screen, cam):
        pass
    def update(self):
        pass

class Rect(Entity):
    def __init__(self, x, y, w, h, image = None, color = None):
        Entity.__init__(self, x, y, w, h)
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
        xColliding = rect.pos.x <= self.pos.x + self.w and rect.pos.x + rect.w >= self.pos.x
        yColliding = rect.pos.y <= self.pos.y + self.h and rect.pos.y + rect.h >= self.pos.y

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
        xColliding = rect.pos.x <= self.pos.x + self.w and rect.pos.x + rect.w >= self.pos.x
        yColliding = rect.pos.y <= self.pos.y + self.h and rect.pos.y + rect.h >= self.pos.y

        return xColliding and yColliding





class Physical_Rect(Rect):
    def __init__(self, x, y, w, h, x_vel = 0, y_vel = 0, image = None, color = None, hasGravity = True):
        Rect.__init__(self, x, y, w, h, image = image, color = color)
        self.vel = Vector2(x_vel, y_vel)
        self.is_jumping = False
        self.hasGravity = hasGravity

    def update(self):
        self.pos = self.pos + self.vel

        if (self.hasGravity):
            self.vel.y += GRAVITY

        if self.pos.y + self.h > SCREEN_HEIGHT: #check if too high
            self.pos.y = SCREEN_HEIGHT - self.h
            self.vel.y = 0
            self.is_jumping = False
        '''
        if self.pos.x + self.w + 10 > SCREEN_WIDTH: #check if too far to right
            self.pos.x = SCREEN_WIDTH - self.w
            self.vel.x = 0
        if self.pos.x - 10 < 0: #check if too far to left
            self.pos.x = 0
            self.vel.x = 0
        '''

class Camera(Rect):
    def __init__(self, x, y, w, h, player):
        Rect.__init__(self, x, y, w, h)
        self.player = player
        self.yOffset = self.player.h

    def update(self):
        self.pos.x = self.player.pos.x + (self.player.w / 2) - self.w / 2
        #if self.player.pos.y + self.player.h < self.h / 2:
        #    self.pos.y -= (self.yOffset / 10)
        #else:
        #self.pos.y = self.player.pos.y + self.player.h - self.h + self.yOffset
        self.pos.y = 0 + self.yOffset
    def render(self, screen, cam):
        pass


class Cop(Physical_Rect):
    def __init__(self, x, y, w, h, image):
        Physical_Rect.__init__(self, x, y, w, h, image = image)
    def update(self):
        Physical_Rect.update(self)

class Coon(Physical_Rect):
    def __init__(self, x, y, w, h, image):
        Physical_Rect.__init__(self, x, y, w, h, image=image)
        self.lookRight = True;

    def update(self):
        if self.vel.x < 0 and self.lookRight:
            self.lookRight = False
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.vel.x > 0 and (not self.lookRight):
            self.lookRight = True
            self.image = pygame.transform.flip(self.image, True, False)

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
    print(common_objs['test_rec'].getCollision(common_objs['other_rec']))


def render():
    screen.fill(BLACK)

    #print("------------------")
    for obj in gameobjects:

        if obj is not common_objs['cam'] and obj.isColliding(common_objs['cam']):
            #print("RENDERING " + str(obj))
            obj.render(screen, common_objs['cam'])

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

    coon = Coon(SCREEN_WIDTH / 2 - 140 / 2, 4 * SCREEN_HEIGHT / 5, 140, 140, pygame.image.load('Images/coon.png'))
    cop = Cop(300, 0, 130, 180, pygame.image.load('Images/cop.png'))
    cam = Camera(coon.pos.x + (coon.w / 2) - SCREEN_WIDTH / 2, coon.pos.y + coon.h - SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, coon)

    testRec = Rect(300, 300, 100, 100, color = VIOLET)
    otherRec = Physical_Rect(350, 350, 10, 10, 0.1, -0.1, color = RED, hasGravity = False)

    common_objs = {}
    gameobjects = []
    gameobjects.append(coon)
    gameobjects.append(cop)
    gameobjects.append(cam)

    gameobjects.append(testRec)
    gameobjects.append(otherRec)

    common_objs['player'] = coon
    common_objs['test_cop'] = cop
    common_objs['cam'] = cam

    common_objs['test_rec'] = testRec
    common_objs['other_rec'] = otherRec

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
