import pygame
import math
from settings import *
from player_obj import play
from planet_obj import planet_group
from radar_obj import radar
from nav_objs import Mimic, mimic_group
from effects import effect_group, Explosion


def add_missile():
    missile_group.add(
        Missile((Stage.XScroll + play.rect.centerx, Stage.YScroll + play.rect.centery)))
    mimic_group.add(Mimic(missile_group.sprites()[-1]))


class Missile(pygame.sprite.Sprite):
    def __init__(self, start):
        super().__init__()
        self.idle = pygame.transform.scale(pygame.image.load('Assets/Missile/idle.png').convert_alpha(), (80, 80))
        self.image = self.idle
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.start = start
        self.angle = 0
        self.health = 1200
        self.target = radar.lock
        self.seen = True
        self.speed = 15

    def update(self):
        # Position
        self.image = pygame.transform.rotate(self.idle, self.angle)
        self.rect = self.image.get_rect(center=(self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll))

        # Lifespan
        self.health -= 1
        if self.health < 0:
            self.kill()

        # Tracking
        convert = 360 / (math.pi * 2)
        if self.target:
            x = self.target.rect.centerx + ((dis_to(self.rect.center, self.target.rect.center) / self.speed) * self.target.XF)
            y = self.target.rect.centery + ((dis_to(self.rect.center, self.target.rect.center) / self.speed) * self.target.YF)
            predict = (x, y)
            self.angle = dir_to(self.rect.center, predict) - 90
        self.start = (
            self.start[0] + (math.cos(self.angle / convert) * self.speed), self.start[1] - math.sin(self.angle / convert) * self.speed)

        # Collision
        for planet in planet_group.sprites():
            offset = (planet.rect.x - self.rect.x, planet.rect.y - self.rect.y)
            if self.mask.overlap(planet.mask, offset):
                if 'Asteroid' in planet.status:
                    play.Current_Planet = None
                    planet.reconstruct()
                    planet.kill()
                effect_group.add(Explosion((Stage.XScroll + self.rect.centerx, Stage.YScroll + self.rect.centery)))
                self.kill()


missile_group = pygame.sprite.Group()