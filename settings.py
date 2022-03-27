import pygame


class stage:
    pygame.init()
    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 720

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
