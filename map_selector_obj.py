import pygame
from mimic_obj import mimic_group


class Map_Selector(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill('Blue')
        self.rect = self.image.get_rect()
        self.target = None
        self.target_index = 1  # Starts with 1 because 0 is the ship
        self.possible = []
        for i in mimic_group.sprites():
            if i.target.seen:
                self.possible.append(i)

    def update(self):
        if self.target and not self.target.target.seen:
            Map_Selector.next_target()
        if self.possible and self.target:
            self.rect.center = self.target.rect.center

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


map_selector_group = pygame.sprite.GroupSingle()
map_selector = Map_Selector()
map_selector_group.add(map_selector)
