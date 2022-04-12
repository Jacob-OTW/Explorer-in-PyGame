import math
import pygame
import random
from settings import stage
from player_obj import play
from space_probe_obj import space_probe_group
from effects import effect_group, Explosion
from nav_objs import map_selector, Mimic, mimic_group


def dis_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    return math.sqrt(x ** 2 + y ** 2)


class Planet(pygame.sprite.Sprite):  # This class is used for Planets of all kind
    def __init__(self, x, y, force=(0.0, 0.0), status=None, size=100, orbit_speed=10, mass=0.01, loot=None,
                 costume_num='1',
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
        self.XF = force[0]
        self.YF = force[1]
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
        self.kill_in = 300
        self.should_kill = False

        # std values
        self.orbit_value = 0

        # Mimic
        mimic_group.add(Mimic(self))

    def reconstruct(self):
        x1 = random.randint(-18000, 18000)
        y1 = random.randint(-8000, 8000)
        v = random.uniform(-5, 5), random.uniform(-5, 5)
        planet_group.add(Planet(x1, y1, force=v, costume_num='asteroid', status=['Asteroid', 'Loot'], loot=self.loot))

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

        if self.chart:
            for probe in space_probe_group.sprites():
                if dis_to(self.rect.center, probe.rect.center) < 2000:
                    self.seen_by_probe = True
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

        if self.should_kill:
            self.kill_in -= 1
            if self.kill_in <= 0:
                effect_group.add(Explosion((stage.XScroll + self.rect.centerx, stage.YScroll + self.rect.centery)))
                play.Current_Planet = None
                map_selector.target = None
                if 'Asteroid' in self.status:
                    self.reconstruct()
                self.kill()


def create_planet_system(num, pos):
    systems = {
        0: [
            Planet(pos[0], pos[1] + 70, status=['Static']),
            Planet(pos[0], pos[1] + -130, mass=0.005, orbit_speed=2, size=50, costume_num='3',
                   buying={'Map-C1': 10, 'Tracker': 10, 'Fuel Upgrade': 5},
                   selling={'Nemon Rock': 5, 'Japur Rock': 15, 'Japur Dust': 10, 'Dead Skin': 10, 'Wierd Rock': 10,
                            'Crude Oil': 75, 'Old DNA': 15},
                   status=['Moving', 'Shop']),
            Planet(pos[0], pos[1] + -260, mass=0.003, orbit_speed=4, size=50, costume_num='4', loot='Nemon Rock',
                   status=['Moving', 'Loot'])
        ],
        1: [
            Planet(pos[0], pos[1] + 70, status=['Static'], chart='Map-C1'),
            Planet(pos[0], pos[1] - 25, mass=0.005, orbit_speed=2, size=50, costume_num='3',
                   buying={'Map-C2': 25, 'Probe': 15, 'Radar': 20, 'Gas Can': 10, 'Crude Oil': 50, 'Missile': 30},
                   selling={'Nemon Rock': 15, 'Japur Rock': 5, 'Japur Dust': 5, 'Dead Skin': 15, 'Ice': 5, 'Flag': 20},
                   status=['Moving', 'Shop'], chart='Map-C1'),
            Planet(pos[0], pos[1] + -260, mass=0.0025, orbit_speed=4, size=50, costume_num='4', loot='Japur Rock',
                   status=['Moving', 'Loot'], chart='Map-C1'),
            Planet(pos[0], pos[1] + -350, mass=0.002, orbit_speed=-4, size=50, costume_num='4', loot='Japur Dust',
                   status=['Moving', 'Loot'], chart='Map-C1')
        ],
        2: [
            Planet(pos[0], pos[1] + 70, status=['Static'], chart='Map-C2'),
            Planet(pos[0], pos[1] - 70, mass=0.005, orbit_speed=5, size=50, costume_num='2', status=['Moving'], chart='Map-C2'),
            Planet(pos[0], pos[1] - 200, mass=0.0018, orbit_speed=2, size=50, costume_num='2', status=['Moving'], chart='Map-C2'),
        ]
                }
    for planet in systems[num]:
        planet_group.add(planet)


planet_group = pygame.sprite.Group()
create_planet_system(0, (random.randint(-18000, 18000), random.uniform(-8000, 8000)))
create_planet_system(1, (random.randint(-18000, 18000), random.uniform(-8000, 8000)))
create_planet_system(2, (random.randint(-18000, 18000), random.uniform(-8000, 8000)))
planet_group.add(Planet(100, 100, force=(2.4, 2.4), costume_num='asteroid', loot='Item_A', status=['Asteroid', 'Loot']))
