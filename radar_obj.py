from settings import *
from planet_obj import planet_group
from player_obj import play


class Radar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Images
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(bottom=Stage.SCREEN_HEIGHT, left=0)
        self.radar_screen = pygame.image.load('Assets/Radar/radar_screen.png').convert_alpha()
        self.radar_screen_rect = self.radar_screen.get_rect(center=(100, 100))
        self.radar_cursor = pygame.image.load('Assets/Radar/radar_cursor.png').convert_alpha()
        self.radar_cursor_rect = self.radar_cursor.get_rect(center=(100, 100))

        # Angles
        self.cursor_angle = 0

        # Lock
        self.lock = None

        self.scan_timer = 0

    def update(self):
        # Drop Lock
        if self.lock and not self.lock.alive():
            self.lock = None

        # Rotate image
        self.radar_cursor = pygame.transform.rotate(pygame.image.load('Assets/Radar/radar_cursor.png').convert_alpha(),
                                                    self.cursor_angle)
        self.radar_cursor_rect = self.radar_cursor.get_rect(center=(100, 100))

        if not self.lock:
            self.cursor_angle += 1
        else:
            self.cursor_angle = dir_to(play.rect.center, self.lock.rect.center) - 90

        if self.cursor_angle > 360:
            self.cursor_angle = 0

        # Detect planets and create radar ping. Will spread workload over x many cycles.
        self.scan_timer += 1
        cycle_amount = 15
        for planet in split(planet_group.sprites(), cycle_amount, self.scan_timer % cycle_amount):
            angle = round(round_dir(dir_to(play.rect.center, planet.rect.center)))
            dis = dis_to(play.rect.center, planet.rect.center)
            if semi_equal(angle, round_dir(self.cursor_angle + 90), cycle_amount) and dis < 2500:
                radar_ping_group.add(RadarPing(angle, dis, planet))
        # Update Image
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        self.image.blit(self.radar_screen, self.radar_screen_rect)
        self.radar_cursor.set_alpha(150)
        self.image.blit(self.radar_cursor, self.radar_cursor_rect)


class RadarPing(pygame.sprite.Sprite):
    def __init__(self, angle, dis, target):
        super().__init__()
        self.image = pygame.image.load('Assets/Radar/radar_ping.png').convert_alpha()
        x = math.sin(math.radians(angle)) * (dis * (100 / 2500))
        y = math.cos(math.radians(angle)) * (dis * (100 / 2500)) * -1
        self.rect = self.image.get_rect(center=(
            radar.rect.centerx + x,
            radar.rect.centery - y))
        self.target = target
        self.opacity = 255

    def update(self):
        self.opacity -= 2.5
        if self.opacity < 0:
            self.kill()
        self.image.set_alpha(self.opacity)


radar_group = pygame.sprite.GroupSingle()
radar = Radar()
radar_group.add(radar)
radar_ping_group = pygame.sprite.Group()
