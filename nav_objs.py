import pygame
import math
from settings import stage
from player_obj import play


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
            self.image = pygame.Surface((self.target.rect.width / self.div, self.target.rect.height / self.div),
                                        pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(center=((x * 0.018) + stage.SCREEN_WIDTH / 2,
                                                (y * 0.018) + stage.SCREEN_HEIGHT / 2))

        if not self.target.alive():
            self.kill()


mimic_group = pygame.sprite.Group()


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.image.load('Assets/arrow.png').convert_alpha()
        self.image = self.stored
        self.rect = self.image.get_rect()
        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        self.rect = self.image.get_rect(center=play.rect.center)
        if map_selector.target:
            pass
            self.angle = dir_to(self.rect.center, map_selector.target.target.rect.center)


arrow_group = pygame.sprite.GroupSingle()
arrow = Arrow()
arrow_group.add(arrow)


class Map_Selector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('Blue')
        self.rect = self.image.get_rect()
        self.target = None
        self.target_index = 1  # Starts with 1 because 0 is the ship
        self.possible = []
        for mimic in mimic_group.sprites():
            if mimic.target.seen:
                self.possible.append(mimic)

    def update(self):
        if self.target and not self.target.target.seen:
            Map_Selector.next_target()
        if self.possible and self.target:
            self.rect.center = self.target.rect.center
        if self.target and not self.target.alive():
            self.target = None

    @classmethod
    def next_target(cls):
        a = []
        for i in mimic_group.sprites():
            if i.target.seen:
                a.append(i)
        map_selector.possible = a
        if not map_selector.target:
            map_selector.target = a[0]
        else:
            map_selector.target_index += 1
            if map_selector.target_index > len(a) - 1:
                map_selector.target_index = 1
        map_selector.target = map_selector.possible[map_selector.target_index]

    @classmethod
    def set_target(cls, obj):
        a = obj.target
        for i in mimic_group.sprites():
            if i.target == a:
                map_selector.possible.append(i)
                map_selector.target = i


map_selector_group = pygame.sprite.GroupSingle()
map_selector = Map_Selector()
map_selector_group.add(map_selector)


class Map_UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/map_ui.png').convert_alpha()
        self.rect = self.image.get_rect(center=(stage.SCREEN_WIDTH / 2, stage.SCREEN_HEIGHT / 2))
        self.map = False


map_ui_group = pygame.sprite.Group()
map_ui = Map_UI()
map_ui_group.add(map_ui)
