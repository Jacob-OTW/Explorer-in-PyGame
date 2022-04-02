import pygame
import math
from settings import stage
from player_obj import play
from planet_obj import planet_group
from radar_obj import radar


def add_missile():
    missile_group.add(
        Missile((stage.XScroll + play.rect.centerx, stage.YScroll + play.rect.centery), (play.XF, play.YF)))


def dis_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    return math.sqrt(x ** 2 + y ** 2)


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


class Missile(pygame.sprite.Sprite):
    def __init__(self, start, force):
        super().__init__()
        self.idle = pygame.transform.scale(pygame.image.load('Assets/Missile/idle.png').convert_alpha(), (80, 80))
        self.image = self.idle
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.start = start
        self.force = pygame.math.Vector2(force)
        self.angle = 0
        self.health = 900
        self.target = radar.lock

    def update(self):
        # Position
        self.start += self.force
        self.image = pygame.transform.rotate(self.idle, self.angle)
        self.rect = self.image.get_rect(center=(self.start[0] - stage.XScroll, self.start[1] - stage.YScroll))

        # Lifespan
        self.health -= 1
        if self.health < 0:
            self.kill()

        # Tracking
        if self.target:
            convert = 360 / (math.pi * 2)
            x = self.target.rect.centerx + ((dis_to(self.rect.center, self.target.rect.center) / abs(self.force[0]) + 2) * self.target.XF / 2)
            y = self.target.rect.centery + ((dis_to(self.rect.center, self.target.rect.center) / abs(self.force[1]) + 2) * self.target.YF / 2)
            predict = (x, y)
            self.angle = dir_to(self.rect.center, predict) - 90
            self.start = (
                self.start[0] + (math.cos(self.angle / convert) * 2), self.start[1] - math.sin(self.angle / convert) * 2)

        # Collision
        for planet in planet_group.sprites():
            offset = (planet.rect.x - self.rect.x, planet.rect.y - self.rect.y)
            if self.mask.overlap(planet.mask, offset):
                if 'Asteroid' in planet.status:
                    planet.kill()
                self.kill()


missile_group = pygame.sprite.Group()
