import pygame
from settings import stage


class Map_UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/map_ui.png')
        self.rect = self.image.get_rect(center=(stage.SCREEN_WIDTH / 2, stage.SCREEN_HEIGHT / 2))
        self.map = False


map_ui_group = pygame.sprite.Group()
map_ui = Map_UI()
map_ui_group.add(map_ui)
