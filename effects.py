from settings import *


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.stored = pygame.image.load('Assets/explosion.png').convert_alpha()
        self.size = 0.1
        self.start = pos
        self.image = pygame.transform.scale(self.stored,
                                            (self.stored.get_width() * self.size, self.stored.get_height() * self.size))
        self.rect = self.image.get_rect(center=(self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll))
        self.opacity = 255

    def update(self):
        self.image = pygame.transform.scale(self.stored,
                                            (self.stored.get_width() * self.size, self.stored.get_height() * self.size))
        self.rect = self.image.get_rect(center=(self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll))
        if self.size <= 1:
            self.size += 0.1
        else:
            self.opacity -= 4.5
            self.image.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.kill()


effect_group = pygame.sprite.Group()
