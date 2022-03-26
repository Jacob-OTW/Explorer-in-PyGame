import pygame
import math
from settings import stage


class Player(pygame.sprite.Sprite):  # This class is used for the player
    def __init__(self):
        super().__init__()
        # Set angle
        self.angle = 0

        # Store Image
        self.Idle = pygame.image.load('Ship.png').convert()
        self.Idle.set_colorkey((0, 0, 0))

        # Call Stored Image
        self.image = pygame.transform.rotate(self.Idle, self.angle)
        self.rect = self.image.get_rect()

        # Positions
        self.rect.center = (stage.SCREEN_WIDTH / 2, stage.SCREEN_HEIGHT / 2)

        # Forces
        self.XF = 0
        self.YF = 0

        # Masks
        self.lander_img = pygame.image.load('Lander.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.lander_img)

        # Planet caching
        self.Current_Planet = None

    def update(self):
        # Key Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(5)
        if keys[pygame.K_d]:
            self.rotate(-5)
        if keys[pygame.K_SPACE]:
            self.accelerate()

        # Release from Planet
        if self.Current_Planet:
            self.XF, self.YF = self.Current_Planet.XF, self.Current_Planet.YF
            # Set var to None if no longer touching the planet
            offset_x = play.rect.center[0] - self.Current_Planet.position[0]
            offset_y = play.rect.center[1] - self.Current_Planet.position[1]
            if not self.Current_Planet.mask.overlap(play.mask, (offset_x, offset_y)):  # If colliding with Planet
                self.Current_Planet = None

        # Move game world
        stage.change_scroll((self.XF, self.YF))

    def draw_mask(self):
        olist = self.mask.outline()
        img = pygame.Surface([640, 480], pygame.SRCALPHA, 32)
        img = img.convert_alpha()
        pygame.draw.lines(img, (200, 150, 150), True, olist)
        stage.screen.blit(img, (self.rect.x, self.rect.y))
        # screen.blit(self.lander_img, self.rect.center)

    def rotate(self, r):
        # change the rotation value and render a new img
        self.angle += r
        self.image = pygame.transform.rotate(self.Idle, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (stage.SCREEN_WIDTH / 2, stage.SCREEN_HEIGHT / 2)
        temp = pygame.image.load('Lander.png').convert_alpha()
        self.lander_img = pygame.transform.rotate(temp, self.angle)
        self.mask = pygame.mask.from_surface(self.lander_img)

    def accelerate(self):
        # Convert is needed because math.sin and math.cos work in radian instead of degrees
        convert = 360 / (2 * math.pi)
        self.XF += math.cos(self.angle / convert) * 0.1
        self.YF -= math.sin(self.angle / convert) * 0.1


play = Player()  # Create player
player_group = pygame.sprite.GroupSingle()
player_group.add(play)
