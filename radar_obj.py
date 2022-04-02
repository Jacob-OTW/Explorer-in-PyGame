import pygame
import math
from settings import stage
from planet_obj import planet_group
from player_obj import play


def round_dir(x):
    while x > 360 or x < 0:
        if x > 360:
            x -= 360
        if x < 0:
            x += 360
    return x


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


def semi_equal(value, match, accuracy):
    if match - accuracy + 1 < value < match + accuracy + 1:
        return True
    else:
        return False


def dis_to(mp, tp):
    x = tp[0] - mp[0]
    y = tp[1] - mp[1]
    return math.sqrt(x ** 2 + y ** 2)


class Radar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Images
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect(bottom=stage.SCREEN_HEIGHT, left=0)
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
        # Rotate
        self.radar_cursor = pygame.transform.rotate(pygame.image.load('Assets/Radar/radar_cursor.png').convert_alpha(),
                                                    self.cursor_angle)
        self.radar_cursor_rect = self.radar_cursor.get_rect(center=(100, 100))
        if not self.lock:
            self.cursor_angle += 1
        else:
            self.cursor_angle = dir_to(play.rect.center, self.lock.rect.center) - 90
        if self.cursor_angle > 360:
            self.cursor_angle = 0

        # Detect
        self.scan_timer += 1
        if self.scan_timer % 5 == 0:
            for planet in planet_group.sprites():
                angle = round(round_dir(dir_to(play.rect.center, planet.rect.center)))
                dis = dis_to(play.rect.center, planet.rect.center)
                if semi_equal(angle, round_dir(self.cursor_angle + 90), 5) and dis < 2500:
                    if len(radar_ping_group.sprites()) < 25:
                        radar_ping_group.add(Radar_Ping(angle, dis, planet))

        # Update Image
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        self.image.blit(self.radar_screen, self.radar_screen_rect)
        self.radar_cursor.set_alpha(150)
        self.image.blit(self.radar_cursor, self.radar_cursor_rect)


class Radar_Ping(pygame.sprite.Sprite):
    def __init__(self, angle, dis, target):
        super().__init__()
        self.image = pygame.image.load('Assets/Radar/radar_ping.png').convert_alpha()
        convert = 360 / (math.pi * 2)
        x = math.cos((angle - 90) / convert) * (dis * (100 / 2500))
        y = math.sin((angle - 90) / convert) * (dis * (100 / 2500))
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
