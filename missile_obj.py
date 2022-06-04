from settings import *
from player_obj import play
from planet_obj import planet_group
from radar_obj import radar
from nav_objs import Mimic, mimic_group
from effects import effect_group, Explosion


def add_missile():
    missile_group.add(
        Missile((Stage.XScroll + play.rect.centerx, Stage.YScroll + play.rect.centery)))
    mimic_group.add(Mimic(missile_group.sprites()[-1]))


class Missile(pygame.sprite.Sprite):
    def __init__(self, start):
        super().__init__()
        self.idle = pygame.transform.scale(pygame.image.load('Assets/Missile/idle.png').convert_alpha(), (80, 80))
        self.image = self.idle
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.start = start
        self.angle = play.angle
        self.health = 1200
        self.target = radar.lock
        self.seen = True
        self.speed = 15

    def predicted_los(self, target, r=0):
        if target:
            t = dis_to(self.rect.center, self.predicted_los(target, r=r + 1) if r <= 2 else target.rect.center) / self.speed
            return target.rect.centerx + (target.force[0] * int(t)), target.rect.centery + (
                    -target.force[1] * int(t))
        else:
            return 0

    def face_to(self, vector_pos):
        angle = dir_to(self.rect.center, vector_pos) - 90
        self.angle += math.sin(math.radians(angle - self.angle)) * 2.5

    def update(self):
        # Position
        self.image = pygame.transform.rotate(self.idle, self.angle)
        self.rect = self.image.get_rect(center=(self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll))

        # Lifespan
        self.health -= 1
        if self.health < 0:
            self.kill()

        # Tracking
        if self.target is not None:
            self.face_to(self.predicted_los(self.target))
        v = pygame.math.Vector2((self.speed, 0)).rotate(self.angle)
        self.start = pygame.math.Vector2((self.start[0] + v[0], self.start[1] - v[1]))

        # Collision
        for planet in overlaps_with(self, planet_group):
            if 'Asteroid' in planet.status:
                planet.reconstruct()
            effect_group.add(Explosion((Stage.XScroll + self.rect.centerx, Stage.YScroll + self.rect.centery)))
            self.kill()


missile_group = pygame.sprite.Group()
