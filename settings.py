import pygame


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

    @classmethod
    def loop(cls, self):
        if self.start[0] > stage.World_Size_X / 2:
            self.start = ((stage.World_Size_X / 2) * -1, self.start[1])
        elif self.start[0] < (stage.World_Size_X / 2 * -1):
            self.start = (stage.World_Size_X / 2, self.start[1])
        elif self.start[1] > stage.World_Size_Y / 2:
            self.start = (self.start[0], (stage.World_Size_Y / 2) * -1)
        elif self.start[1] < (stage.World_Size_Y / 2) * -1:
            self.start = (self.start[0], stage.World_Size_Y / 2)

    @classmethod
    def split(cls, a, n, r):  # Split a into n parts and return the r(th) value, used to spread workload over cycles
        k, m = divmod(len(a), n)
        store = (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
        return list(store)[r]