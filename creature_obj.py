import pygame
from settings import stage


class Creature(pygame.sprite.Sprite):
    def __init__(self, pos=(800, 800)):
        super().__init__()
        self.animation_index = 0
        self.animation_flow = True
        self.image = pygame.image.load(f'Assets/Creature/{self.animation_index}.png')
        self.rect = self.image.get_rect()
        self.startx, self.starty = pos
        self.angle = 90
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > 5:
            self.cycle_animation()
        self.image = pygame.image.load(f'Assets/Creature/{self.animation_index}.png')
        self.rect.x, self.rect.y = (self.startx - stage.XScroll, self.starty - stage.YScroll)

    def cycle_animation(self):
        if self.animation_flow:
            self.animation_index += 1
            if self.animation_index > 13:
                self.animation_index = 13
                self.animation_flow = False
        else:
            self.animation_index -= 1
            if self.animation_index < 0:
                self.animation_index = 0
                self.animation_flow = True

creature_group = pygame.sprite.Group()
creature_group.add(Creature())
