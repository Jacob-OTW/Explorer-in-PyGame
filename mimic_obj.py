import pygame
from settings import stage


class Mimic(pygame.sprite.Sprite):
    def __init__(self, target, is_player=False):
        super().__init__()
        self.player = is_player
        self.target = target
        self.div = 5 if self.player else 10
        self.image = pygame.transform.scale(self.target.image,
                                            (self.target.rect.width / self.div, self.target.rect.height / self.div))
        self.rect = self.image.get_rect()

    def update(self):
        x = stage.XScroll + self.target.rect.centerx if self.player else self.target.start[0]
        y = stage.YScroll + self.target.rect.centery if self.player else self.target.start[1]
        if self.target.seen:
            self.image = pygame.transform.scale(self.target.image,
                                                (self.target.rect.width / self.div, self.target.rect.height / self.div))
        else:
            self.image = pygame.Surface((self.target.rect.width / self.div, self.target.rect.height / self.div), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(center=((x * 0.018) + stage.SCREEN_WIDTH / 2,
                                                (y * 0.018) + stage.SCREEN_HEIGHT / 2))


mimic_group = pygame.sprite.Group()
