import pygame
import math
from player_obj import play
from map_selector_obj import map_selector


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


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.image.load('Assets/arrow.png')
        self.image = self.stored
        self.rect = self.image.get_rect()
        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        self.rect = self.image.get_rect(center=play.rect.center)
        if map_selector.target:
            pass
            self.angle = dir_to(self.rect.center, map_selector.target.target.rect.center)


arrow_group = pygame.sprite.GroupSingle()
arrow = Arrow()
arrow_group.add(arrow)
