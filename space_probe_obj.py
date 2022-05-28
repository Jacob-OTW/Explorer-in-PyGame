from settings import *
from player_obj import play
from nav_objs import mimic_group, Mimic


def add_probe():
    probe = Probe((Stage.XScroll + Stage.SCREEN_WIDTH / 2, Stage.YScroll + Stage.SCREEN_HEIGHT / 2), angle=play.angle,
                  force=(play.XF, play.YF))
    space_probe_group.add(probe)
    mimic_group.add(Mimic(probe))


class Probe(pygame.sprite.Sprite):
    def __init__(self, start=(0, 0), angle=0, force=(0, 0)):
        super().__init__()
        self.stored = pygame.transform.scale(pygame.image.load('Assets/probe.png').convert_alpha(), (56, 60))
        self.image = self.stored
        self.rect = self.image.get_rect()
        self.start = start
        self.angle = angle
        self.force = pygame.math.Vector2(force)
        self.seen = True

    def update(self):
        self.start += self.force
        self.image = pygame.transform.rotate(self.stored, self.angle)
        self.rect = self.image.get_rect(center=(self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll))
        Stage.loop(self)


space_probe_group = pygame.sprite.GroupSingle()
