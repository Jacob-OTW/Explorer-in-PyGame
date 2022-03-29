import pygame
import math
import random
from settings import stage


class Creature(pygame.sprite.Sprite):
    def __init__(self, pos=(800, 800)):
        super().__init__()
        self.animation_index = 0
        self.animation_flow = True
        self.image = pygame.image.load(f'Assets/Creature/{self.animation_index}.png')
        self.rect = self.image.get_rect()
        self.start = pos
        self.force = pygame.math.Vector2(0, 0)
        self.angle = 90
        self.timer = 0

    def update(self):
        self.cycle_animation()
        self.start += self.force
        self.force *= 98 / 100
        self.image = pygame.transform.rotate(pygame.image.load(f'Assets/Creature/{round(self.animation_index)}.png'), self.angle - 90)
        self.rect = self.image.get_rect(center=(self.start[0] - stage.XScroll, self.start[1] - stage.YScroll))

    def cycle_animation(self):
        speed = 0.3
        if self.animation_flow:
            self.animation_index += speed
            if round(self.animation_index) > 13:
                self.animation_index = 13
                self.animation_flow = False
                self.accelerate()
        else:
            self.animation_index -= speed
            if round(self.animation_index) < 0:
                self.animation_index = 0
                self.animation_flow = True
                self.angle += random.uniform(-20, 20)

    def accelerate(self):
        convert = math.pi * 2 / 360
        x = math.sin(self.angle * convert) * 3
        y = math.cos(self.angle * convert) * 3
        self.force = pygame.math.Vector2(x, y)


creature_group = pygame.sprite.Group()
creature_group.add(Creature(pos=(400, 400)))
