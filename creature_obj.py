from settings import *
from player_obj import play
from space_probe_obj import space_probe_group
from nav_objs import Mimic, mimic_group


class Creature(pygame.sprite.Sprite):
    __slots__ = ('animation_index', 'animation_flow', 'image',
                 'rect', 'start', 'force', 'angle', 'timer', 'loot', 'seen')

    def __init__(self, pos=(800, 800)):
        super().__init__()
        self.animation_index = 0
        self.animation_flow = True
        self.image = pygame.image.load(f'Assets/Creature/{self.animation_index}.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.start = pygame.math.Vector2(pos)
        self.force = pygame.math.Vector2(0, 0)
        self.angle = 90
        self.timer = 0
        self.loot = 'Dead Skin'
        self.seen = False
        mimic_group.add(Mimic(self))

    def update(self):
        self.cycle_animation()
        self.start += self.force
        loop(self)
        self.force *= 98 / 100
        self.image = pygame.transform.rotate(pygame.image.load(f'Assets/Creature/{round(self.animation_index)}.png'),
                                             self.angle - 90)
        self.rect = self.image.get_rect(center=(self.start[0] - Stage.XScroll, self.start[1] - Stage.YScroll))
        if math.sqrt((self.rect.x - play.rect.x) ** 2 + (
                self.rect.y - play.rect.y) ** 2) < 200 and self.loot not in play.inventory:
            play.inventory.append(self.loot)

        self.seen = bool(list(filter(
            lambda probe: dis_to(self.rect.center, probe.rect.center) < 2000, space_probe_group.sprites()
        )))
        """
        1. Go through all the elements.
        2. Only keep the elements where the rect is within 2000px.
        3. if the list is emtpy, seen is False, else its True.
        """

    def cycle_animation(self):
        speed = 0.3
        if self.animation_flow:
            self.animation_index += speed
            if round(self.animation_index) > 13:
                self.animation_index = 13
                self.animation_flow = False
                self.accelerate()
        else:
            self.animation_index -= speed
            if round(self.animation_index) < 0:
                self.animation_index = 0
                self.animation_flow = True
                self.angle += random.uniform(-20, 20)

    def accelerate(self):
        x = math.sin(math.radians(self.angle)) * 3
        y = math.cos(math.radians(self.angle)) * 3
        self.force = pygame.math.Vector2(x, y)


creature_group = pygame.sprite.Group()
creature_group.add(Creature(pos=(400, 400)))
