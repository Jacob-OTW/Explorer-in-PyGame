import pygame.transform

from settings import *
from player_obj import play
from space_probe_obj import space_probe_group
from effects import effect_group, Explosion
from nav_objs import map_selector, Mimic, mimic_group


class Planet(pygame.sprite.Sprite):  # This class is used for Planets of all kind
    __slots__ = ('stored', 'image', 'mask', 'rect', 'start', 'force', 'size', 'orbit_speed', 'mass', 'loot', 'buying',
                 'selling', 'chart', 'seen_by_probe', 'seen', 'kill_in', 'should_kill', 'static', 'moving', 'asteroid',
                 'shop', 'orbit_value')

    def __init__(self, x, y, force=(0.0, 0.0), static=False, moving=False, shop=False, asteroid=False, size=100,
                 orbit_speed=10, mass=0.01, loot=None, costume_num='1', buying=None, selling=None, chart=None):
        super().__init__()
        if buying is None:
            buying = {}
        if selling is None:
            selling = {}

        # init
        self.stored = pygame.image.load(f'Assets/Planets/{costume_num}.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.stored, 0, 1.0)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(x - Stage.XScroll, y - Stage.YScroll))

        # Set values
        self.start = pygame.math.Vector2((x, y))
        self.force = pygame.math.Vector2(force)
        self.size = size
        self.orbit_speed = orbit_speed
        self.mass = mass
        self.loot = loot
        self.buying = buying
        self.selling = selling
        self.chart = chart
        self.seen_by_probe = False
        self.seen = False if self.chart else True
        self.kill_in = 300
        self.should_kill = False

        # Status values, a collection of booleans to influence behavior.
        self.static = static
        self.moving = moving
        self.asteroid = asteroid
        self.shop = shop

        # std values
        self.orbit_value = 0

        # Mimic
        mimic_group.add(Mimic(self))

    def reconstruct(self):
        x1 = random.randint(-18000, 18000)
        y1 = random.randint(-8000, 8000)
        v = random.uniform(-5, 5), random.uniform(-5, 5)
        planet_group.add(Planet(x1, y1, force=v, costume_num='asteroid', asteroid=True, loot=self.loot))
        if play.Current_Planet == self:
            play.Current_Planet = None
        self.kill()

    def update(self):
        if self.static:  # Things to do if Static
            pass
        if self.moving:  # Things to do if Moving
            self.force = pygame.math.Vector2(math.cos(self.orbit_value) * self.orbit_speed,
                                             math.sin(self.orbit_value) * self.orbit_speed)
            self.orbit_value += self.mass * self.orbit_speed
            self.start += self.force

            if play.Current_Planet == self:
                Stage.change_scroll(self.force)
        elif self.asteroid:
            self.start += self.force
            if play.Current_Planet == self:
                Stage.change_scroll(self.force)
        if self.loot:
            if play.Current_Planet == self:
                if self.loot not in play.inventory:
                    play.inventory.append(self.loot)
        loop(self)

        self.image = pygame.transform.scale(self.stored, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = (
            self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll)

        if self.chart:
            self.seen = bool(list(filter(
                lambda probe: dis_to(self.rect.center, probe.rect.center) < 2000, space_probe_group.sprites()
            )))
            """
            it will only keep the probe object if the lambda function which checks if 
            each element is closer than 2000. If the list it adds to not empty, the creature was seen
            """

            if self.chart in play.inventory or self.seen_by_probe:
                self.seen = True
            else:
                self.seen = False
        else:
            self.seen = True

        if self.should_kill:
            self.kill_in -= 1
            if self.kill_in <= 0:
                effect_group.add(Explosion((Stage.XScroll + self.rect.centerx, Stage.YScroll + self.rect.centery)))
                play.Current_Planet = None
                map_selector.target = None
                if self.asteroid:
                    self.reconstruct()
                self.kill()


def create_planet_system(num, pos):
    systems = {
        0: [
            Planet(pos[0], pos[1] + 70, static=True),
            Planet(pos[0], pos[1] + -130, mass=0.005, orbit_speed=2, size=50, costume_num='3',
                   buying={'Map-C1': 10, 'Tracker': 10, 'Fuel Upgrade': 5},
                   selling={'Nemon Rock': 5, 'Japur Rock': 15, 'Japur Dust': 10, 'Dead Skin': 10, 'Wierd Rock': 10,
                            'Crude Oil': 75, 'Old DNA': 15},
                   shop=True, moving=True),
            Planet(pos[0], pos[1] + -260, mass=0.003, orbit_speed=4, size=50, costume_num='4', loot='Nemon Rock',
                   moving=True)
        ],
        1: [
            Planet(pos[0], pos[1] + 70, static=True, chart='Map-C1'),
            Planet(pos[0], pos[1] - 25, mass=0.005, orbit_speed=2, size=50, costume_num='3',
                   buying={'Map-C2': 25, 'Probe': 15, 'Radar': 20, 'Gas Can': 10, 'Crude Oil': 50, 'Missile': 30},
                   selling={'Nemon Rock': 15, 'Japur Rock': 5, 'Japur Dust': 5, 'Dead Skin': 15, 'Ice': 5, 'Flag': 20},
                   shop=True, moving=True, chart='Map-C1'),
            Planet(pos[0], pos[1] + -260, mass=0.0025, orbit_speed=4, size=50, costume_num='4', loot='Japur Rock',
                   moving=True, chart='Map-C1'),
            Planet(pos[0], pos[1] + -350, mass=0.002, orbit_speed=-4, size=50, costume_num='4', loot='Japur Dust',
                   moving=True, chart='Map-C1')
        ],
        2: [
            Planet(pos[0], pos[1] + 70, static=True, chart='Map-C2'),
            Planet(pos[0], pos[1] - 70, mass=0.005, orbit_speed=5, size=50, costume_num='2', moving=True,
                   chart='Map-C2'),
            Planet(pos[0], pos[1] - 200, mass=0.0018, orbit_speed=2, size=50, costume_num='2', moving=True,
                   chart='Map-C2'),
        ]
    }
    for planet in systems[num]:
        planet_group.add(planet)


planet_group = pygame.sprite.Group()
create_planet_system(0, (random.randint(-18000, 18000), random.uniform(-8000, 8000)))
create_planet_system(1, (random.randint(-18000, 18000), random.uniform(-8000, 8000)))
create_planet_system(2, (random.randint(-18000, 18000), random.uniform(-8000, 8000)))
planet_group.add(Planet(100, 100, force=(2.4, 2.4), costume_num='asteroid', loot='Item_A', asteroid=True))
