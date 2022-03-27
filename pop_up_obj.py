import pygame
from settings import stage


def add_pop_up(*args: str):
    if args:
        for i, arg in enumerate(args):
            pop_up_group.add(Pop_Up(arg, i))


class Pop_Up(pygame.sprite.Sprite):
    def __init__(self, t: str, pos_y=0):
        super().__init__()
        self.font = pygame.font.SysFont("monospace", 32)
        self.image = pygame.image.load('Assets/pop_up.png')
        self.rect = self.image.get_rect(centerx=stage.SCREEN_WIDTH - 100, top=375 + 50 * pos_y)
        self.text = self.font.render(t, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(100, 25))
        self.image.blit(self.text, self.text_rect)
        self.opacity = 255

    def update(self):
        self.rect.y += 1
        self.opacity -= 2.5
        if self.opacity <= 0:
            self.kill()
        self.image.set_alpha(self.opacity)


pop_up_group = pygame.sprite.Group()
