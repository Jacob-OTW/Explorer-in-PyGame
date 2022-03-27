import math
import pygame

from settings import stage
from player_obj import play


class Planet(pygame.sprite.Sprite):  # This class is used for Planets of all kind
    def __init__(self, x, y, xf=0, yf=0, status=None, size=100, orbit_speed=10, mass=0.01, loot=None, costume_num=1, buying=None, selling=None):  # buying is a dict of items that can be bought, and selling can be sold by the player
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
        self.startx = x
        self.starty = y
        self.XF = xf
        self.YF = yf
        self.status = status
        self.size = size
        self.orbit_speed = orbit_speed
        self.mass = mass
        self.loot = loot
        self.buying = buying
        self.selling = selling

        # std values
        self.orbit_value = 0

    def update(self):
        if 'Static' in self.status:  # Things to do if Static
            pass
        if 'Moving' in self.status:  # Things to do if Moving
            self.XF = math.cos(self.orbit_value) * self.orbit_speed
            self.YF = math.sin(self.orbit_value) * self.orbit_speed

            self.orbit_value += self.mass * self.orbit_speed

            self.startx += self.XF
            self.starty += self.YF
            if play.Current_Planet == self:
                stage.change_scroll((self.XF, self.YF))
        if 'Loot' in self.status:
            if play.Current_Planet == self:
                if self.loot not in play.inventory:
                    play.inventory.append(self.loot)

        self.image = pygame.transform.scale(self.stored, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = (self.startx - stage.XScroll, self.starty - stage.YScroll)  # Update Pos  # Move rect to updated position

        # Setup for Mask collision test
        offset = (play.rect.x - self.rect.x, play.rect.y - self.rect.y)
        if self.mask.overlap(play.mask, offset):  # If colliding with Planet
            if play.Current_Planet != self:
                play.Current_Planet = self


planet_group = pygame.sprite.Group()
planet_group.add(Planet(0, 70, status=['Static']))
planet_group.add(Planet(0, -130, xf=8, yf=-3, mass=0.005, orbit_speed=2, size=50, costume_num=3, buying={'Wood': 5, 'Steel': 10},  status=['Moving', 'Shop']))
planet_group.add(Planet(0, -260, xf=8, yf=-3, mass=0.003, orbit_speed=4, size=50, costume_num=4, loot='Item', status=['Moving', 'Loot']))
