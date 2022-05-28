import pygame
import math
import random
import sys
import time


# This file exists so there isn't a circular import
class stage:
    pygame.init()
    SCREEN_WIDTH = 1600  # 960
    SCREEN_HEIGHT = 800  # 720
    World_Size_X = 50000
    World_Size_Y = 20000

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    bg = pygame.image.load('Assets/Background.png').convert_alpha()
    XScroll = 0
    YScroll = 0

    debug = True

    @classmethod
    def change_scroll(cls, tup):
        cls.XScroll += tup[0]
        cls.YScroll += tup[1]


def loop(self):
    if self.start[0] > stage.World_Size_X / 2:
        self.start = ((stage.World_Size_X / 2) * -1, self.start[1])
    elif self.start[0] < (stage.World_Size_X / 2 * -1):
        self.start = (stage.World_Size_X / 2, self.start[1])
    elif self.start[1] > stage.World_Size_Y / 2:
        self.start = (self.start[0], (stage.World_Size_Y / 2) * -1)
    elif self.start[1] < (stage.World_Size_Y / 2) * -1:
        self.start = (self.start[0], stage.World_Size_Y / 2)


def split(a, n, r):  # Split a into n parts and return the r(th) value, used to spread workload over cycles
    k, m = divmod(len(a), n)
    store = (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
    return list(store)[r]


def round_dir(x):
    while x > 360 or x < 0:
        if x > 360:
            x -= 360
        if x < 0:
            x += 360
    return x


def dir_to(mp, tp):
    convert = 57.29577951
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    if y == 0:
        return 90 if x > 0 else 270
    if y > 0:
        return (math.atan(x / y)) * convert
    else:
        return math.atan(x / y) * convert + 180


def semi_equal(value, match, accuracy):
    if match - accuracy + 1 < value < match + accuracy + 1:
        return True
    else:
        return False


def dis_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    return math.sqrt(x ** 2 + y ** 2)
