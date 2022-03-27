import pygame
import math
from settings import stage


class Player(pygame.sprite.Sprite):  # This class is used for the player
    def __init__(self):
        super().__init__()
        # Set angle
        self.angle = 0

        # Store Image
        self.Idle = pygame.image.load('Assets/Ship.png').convert()
        self.Idle.set_colorkey((0, 0, 0))

        # Call Stored Image
        self.image = pygame.transform.rotate(self.Idle, self.angle)
        self.rect = self.image.get_rect(center=(stage.SCREEN_WIDTH / 2, stage.SCREEN_HEIGHT / 2))

        # Forces
        self.XF = 0
        self.YF = 0

        # Masks
        self.lander_img = pygame.image.load('Assets/Lander.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.lander_img)

        # Planet caching
        self.Current_Planet = None
        self.offset = None

        # Inventory
        self.inventory = []
        self.money = 10

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
            keyboard = pygame.key.get_pressed()
            if not keyboard[pygame.K_SPACE]:
                self.XF, self.YF = self.Current_Planet.XF, self.Current_Planet.YF

            # Set var to None if no longer touching the planet
            offset = (play.rect.x - self.Current_Planet.rect.x, play.rect.y - self.Current_Planet.rect.y)
            if not self.Current_Planet.mask.overlap(play.mask, offset):  # If colliding with Planet
                self.Current_Planet = None

        # Move game world if floating
        if not self.Current_Planet:
            stage.change_scroll((self.XF, self.YF))

    def draw_mask_attach(self):
        olist = self.mask.outline()
        img = pygame.Surface([640, 480], pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.lines(img, (200, 150, 150), True, olist)
        stage.screen.blit(img, (self.rect.x, self.rect.y))

    def rotate(self, r):
        # change the rotation value and render a new img
        self.angle += r
        self.image = pygame.transform.rotate(self.Idle, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (stage.SCREEN_WIDTH / 2, stage.SCREEN_HEIGHT / 2)
        self.lander_img = pygame.transform.rotate(pygame.image.load('Assets/Lander.png').convert_alpha(), self.angle)
        self.mask = pygame.mask.from_surface(self.lander_img)

    def accelerate(self):
        # Convert is needed because math.sin and math.cos work in radian instead of degrees
        convert = 360 / (2 * math.pi)
        self.XF += math.cos(self.angle / convert) * 0.1
        self.YF -= math.sin(self.angle / convert) * 0.1
        self.Current_Planet = None


play = Player()  # Create player
player_group = pygame.sprite.GroupSingle()
player_group.add(play)
