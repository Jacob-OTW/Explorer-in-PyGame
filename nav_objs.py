from settings import *
from player_obj import play, Player


class Mimic(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.player = True if type(target) == Player else False
        self.target = target
        self.div = 5 if self.player else 10  # If the player was drawn at that size, it would be too small
        self.image = pygame.transform.scale(self.target.image,
                                            (self.target.rect.width / self.div, self.target.rect.height / self.div))
        self.rect = self.image.get_rect()

    def update(self):
        x = Stage.XScroll + self.target.rect.centerx if self.player else self.target.start[0]
        y = Stage.YScroll + self.target.rect.centery if self.player else self.target.start[1]
        if self.target.seen:
            self.image = pygame.transform.scale(self.target.image,
                                                (self.target.rect.width / self.div, self.target.rect.height / self.div))
        else:
            self.image = pygame.Surface((self.target.rect.width / self.div, self.target.rect.height / self.div),
                                        pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(center=((x * 0.018) + Stage.SCREEN_WIDTH / 2,
                                                (y * 0.018) + Stage.SCREEN_HEIGHT / 2))

        if not self.target.alive():
            self.kill()


mimic_group = pygame.sprite.Group()


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.stored = pygame.image.load('Assets/arrow.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.stored, 0, 1.0)
        self.rect = self.image.get_rect()
        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(self.stored, self.angle - 90)
        self.rect = self.image.get_rect(center=play.rect.center)
        if map_selector.target:
            pass
            self.angle = dir_to(self.rect.center, map_selector.target.target.rect.center)


arrow = Arrow()
arrow_group = pygame.sprite.GroupSingle(arrow)


class MapSelector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('Green')
        self.rect = self.image.get_rect()
        self.target = None
        self.target_index = 1  # Starts with 1 because 0 is the player
        self.possible = []
        for mimic in mimic_group.sprites():
            if Mimic(mimic).target.seen:
                self.possible.append(mimic)

    def update(self):
        if self.target and not self.target.target.seen:
            self.next_target()
        if self.possible and self.target is not None:  # There are possible options, and the local option is not None
            self.rect.center = self.target.rect.center
        if self.target and not self.target.alive():
            self.target = None

    def next_target(self):
        # Set possible to all mimic that are on the map
        possible = []
        for mimic in mimic_group.sprites():
            if Mimic(mimic).target.seen and not Mimic(mimic).player:
                possible.append(mimic)
        self.possible = possible

        # Set a target if not target is set.
        if self.target:
            self.target_index += 1
            if self.target_index > len(possible) - 1:
                self.target_index = 0
        if len(self.possible) <= self.target_index:
            self.target_index = len(self.possible) - 1
        self.target = self.possible[self.target_index]

    def set_target(self, obj):
        a = obj.target
        for mimic in mimic_group.sprites():
            if Mimic(mimic).target == a:
                self.possible.append(mimic)
                self.target = mimic


map_selector = MapSelector()
map_selector_group = pygame.sprite.GroupSingle(map_selector)


class MapUI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/map_ui.png').convert_alpha()
        self.rect = self.image.get_rect(center=(Stage.SCREEN_WIDTH / 2, Stage.SCREEN_HEIGHT / 2))
        self.map = False


map_ui = MapUI()
map_ui_group = pygame.sprite.Group(map_ui)
