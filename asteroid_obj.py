import pygame
from settings import stage


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), force=(0, 0), loot='Item_A'):
        super().__init__()
        self.status = ['Asteroid']
        self.image = pygame.image.load('Assets/Planets/asteroid.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.startx, self.starty = pos
        self.XF, self.YF = force
        self.loot = loot

    def update(self):
        self.startx += self.XF
        self.starty += self.YF
        self.rect.x = self.startx - stage.XScroll
        self.rect.y = self.starty - stage.YScroll


asteroid_group = pygame.sprite.Group()
asteroid_group.add(Asteroid(pos=(100, 100), force=(1, 1)))
