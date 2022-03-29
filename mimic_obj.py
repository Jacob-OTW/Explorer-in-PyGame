import pygame
from settings import stage


class Mimic(pygame.sprite.Sprite):
    map_zoom = 1

    def __init__(self, target, is_player=False):
        super().__init__()
        self.player = is_player
        self.target = target
        self.div = 10 if self.player else 10
        self.image = pygame.transform.scale(self.target.image,
                                            (self.target.rect.width / self.div, self.target.rect.height / self.div))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.transform.scale(self.target.image,
                                            (self.target.rect.width / self.div, self.target.rect.height / self.div))
        x = stage.XScroll + self.target.rect.centerx if self.player else self.target.startx
        y = stage.YScroll + self.target.rect.centery if self.player else self.target.starty
        self.rect.center = ((x * 0.018 / Mimic.map_zoom) + stage.SCREEN_WIDTH / 2,
                            (y * 0.018 / Mimic.map_zoom) + stage.SCREEN_HEIGHT / 2)


mimic_group = pygame.sprite.Group()
