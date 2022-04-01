import math
import pygame

from settings import stage
from player_obj import play
from space_probe_obj import space_probe_group


def dis_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    return math.sqrt(x ** 2 + y ** 2)


class Planet(pygame.sprite.Sprite):  # This class is used for Planets of all kind
    def __init__(self, x, y, xf=0.0, yf=0.0, status=None, size=100, orbit_speed=10, mass=0.01, loot=None, costume_num='1',
                 buying=None, selling=None, chart=None):
        super().__init__()
        if status is None:
            status = ['Static']
        if buying is None:
            buying = {}
        if selling is None:
            selling = {}

        # init
        self.stored = pygame.image.load(f'Assets/Planets/{costume_num}.png').convert_alpha()
        self.image = self.stored
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(x - stage.XScroll, y - stage.YScroll))

        # Set values
        self.start = (x, y)
        self.XF = xf
        self.YF = yf
        self.status = status
        self.size = size
        self.orbit_speed = orbit_speed
        self.mass = mass
        self.loot = loot
        self.buying = buying
        self.selling = selling
        self.chart = chart
        self.seen_by_probe = False
        if self.chart:
            self.seen = False
        else:
            self.seen = True

        # std values
        self.orbit_value = 0

    def update(self):
        if 'Static' in self.status:  # Things to do if Static
            pass
        if 'Moving' in self.status:  # Things to do if Moving
            self.XF = math.cos(self.orbit_value) * self.orbit_speed
            self.YF = math.sin(self.orbit_value) * self.orbit_speed

            self.orbit_value += self.mass * self.orbit_speed

            self.start = (self.start[0] + self.XF, self.start[1] + self.YF)

            if play.Current_Planet == self:
                stage.change_scroll((self.XF, self.YF))
        elif 'Asteroid' in self.status:
            self.start = (self.start[0] + self.XF, self.start[1] + self.YF)
            if play.Current_Planet == self:
                stage.change_scroll((self.XF, self.YF))
        if 'Loot' in self.status:
            if play.Current_Planet == self:
                if self.loot not in play.inventory:
                    play.inventory.append(self.loot)
        stage.loop(self)

        self.image = pygame.transform.scale(self.stored, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = (
            self.start[0] - stage.XScroll, self.start[1] - stage.YScroll)
        if space_probe_group.sprites():
            if dis_to(self.rect.center, space_probe_group.sprites()[0].rect.center) < 2000:
                self.seen_by_probe = True

        if self.chart:
            if self.chart in play.inventory or self.seen_by_probe:
                self.seen = True
            else:
                self.seen = False
        else:
            self.seen = True

        # Setup for Mask collision test
        offset = (play.rect.x - self.rect.x, play.rect.y - self.rect.y)
        if self.mask.overlap(play.mask, offset):  # If colliding with Planet
            if play.Current_Planet != self:
                play.Current_Planet = self


planet_group = pygame.sprite.Group()
planet_group.add(Planet(0, 70, status=['Static']))
planet_group.add(
    Planet(0, -130, xf=8, yf=-3, mass=0.005, orbit_speed=2, size=50, costume_num='3', buying={'Wood': 5, 'Steel': 10},
           selling={'Wood': 3, 'Item': 10, 'Dead Skin': 15}, status=['Moving', 'Shop']))
planet_group.add(Planet(0, -260, xf=8, yf=-3, mass=0.003, orbit_speed=4, size=50, costume_num='4', loot='Item',
                        status=['Moving', 'Loot'], chart='Item'))
planet_group.add(Planet(100, 100, xf=3.2, yf=2.1, costume_num='asteroid', loot='Item_A', status=['Asteroid', 'Loot']))
