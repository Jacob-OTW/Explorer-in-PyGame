import pygame
from settings import stage


class Mimic(pygame.sprite.Sprite):
    map_zoom = 2

    def __init__(self, target):
        super().__init__()
        self.target = target
        self.image = pygame.transform.scale(target.image, (10, 10))
        self.rect = self.image.get_rect()

    def update(self):
        self.image = pygame.transform.scale(self.target.image,
                                            (self.target.rect.width / 25, self.target.rect.height / 25))
        self.rect.center = ((self.target.startx * 0.018 / Mimic.map_zoom) + stage.SCREEN_WIDTH / 2,
                            (self.target.starty * 0.018 / Mimic.map_zoom) + stage.SCREEN_HEIGHT / 2)


mimic_group = pygame.sprite.Group()
