from settings import *
from key_binds import keybinds


class Player(pygame.sprite.Sprite):  # This class is used for the player
    def __init__(self):
        super().__init__()
        # Set angle
        self.angle = 0

        # Store Image
        self.Surface = pygame.Surface((90, 52), pygame.SRCALPHA, 32)
        self.Idle = pygame.image.load('Assets/Ship.png').convert()
        self.Idle.set_colorkey((0, 0, 0))
        self.burner = {0: pygame.image.load('Assets/burner0.png').convert_alpha(),
                       1: pygame.image.load('Assets/burner1.png').convert_alpha()}
        self.burner_index = 0
        self.burner_timer = 0

        # Call Stored Image
        self.image = self.Surface
        self.rect = self.image.get_rect(center=(Stage.SCREEN_WIDTH / 2, Stage.SCREEN_HEIGHT / 2))

        # Forces
        self.force = pygame.math.Vector2((0, 0))

        # Masks
        self.lander_img = pygame.image.load('Assets/Lander.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.lander_img)

        # Planet caching
        self.Current_Planet = None
        self.offset = None

        # Mimic
        self.seen = True

        # Inventory
        self.inventory = []
        self.money = 10

    def update(self, planet_group: list):
        self.Surface = pygame.Surface((90, 52), pygame.SRCALPHA, 32)
        self.Surface.blit(self.Idle, (0, 0))
        # Key Input
        keys = pygame.key.get_pressed()
        if keys[keybinds['Thrust']]:
            self.Surface.blit(self.burner[self.burner_index], (0, 0))
            self.burner_timer += 1
            if self.burner_timer >= 5:
                self.burner_index = 0 if self.burner_index == 1 else 1
                self.burner_timer = 0
            self.accelerate()
        if keys[keybinds['Turn_Left']]:
            self.rotate(-5)
        if keys[keybinds['Turn_Right']]:
            self.rotate(5)

        # Release from Planet
        if self.Current_Planet:
            keyboard = pygame.key.get_pressed()
            if not keyboard[pygame.K_SPACE]:
                self.force = pygame.math.Vector2(self.Current_Planet.force)

            # Set var to None if no longer touching the planet
            offset = (play.rect.x - self.Current_Planet.rect.x, play.rect.y - self.Current_Planet.rect.y)
            if not self.Current_Planet.mask.overlap(play.mask, offset):  # If colliding with Planet
                self.Current_Planet = None

        # Move game world if floating
        if not self.Current_Planet:
            Stage.change_scroll(self.force)
            if Stage.XScroll > 25000:
                Stage.XScroll = -25000
            elif Stage.XScroll < -25000:
                Stage.XScroll = 25000
            elif Stage.YScroll > 10000:
                Stage.YScroll = -10000
            elif Stage.YScroll < -10000:
                Stage.YScroll = 10000

        # Align all images and masks
        self.image = pygame.transform.rotate(self.Surface, self.angle)
        self.rect = self.image.get_rect(center=(Stage.SCREEN_WIDTH / 2, Stage.SCREEN_HEIGHT / 2))
        self.lander_img = pygame.transform.rotate(pygame.image.load('Assets/Lander.png').convert_alpha(), self.angle)
        self.mask = pygame.mask.from_surface(self.lander_img)

        for obj in self.overlaps_with(planet_group):
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_SPACE]:
                self.Current_Planet = obj

    def draw_mask_attach(self):  # Draws the hit_box at the bottom of player for debugging
        olist = self.mask.outline()
        img = pygame.Surface([640, 480], pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.lines(img, (200, 150, 150), True, olist)
        Stage.screen.blit(img, (self.rect.x, self.rect.y))

    def rotate(self, r):  # change the rotation value and render a new img
        self.angle += r

    def overlaps_with(self, group: pygame.sprite.AbstractGroup):
        col = pygame.sprite.spritecollide(self, group, False)
        overlapping = []
        for obj in col:
            if self.mask.overlap(obj.mask, (obj.rect.x - self.rect.x, obj.rect.y - self.rect.y)):
                overlapping.append(obj)
        return overlapping

    def accelerate(self):  # Convert is needed because math.sin and math.cos work in radian instead of degrees
        x = math.cos(math.radians(self.angle)) * 0.1
        y = math.sin(math.radians(self.angle)) * -0.1
        self.force += pygame.math.Vector2((x, y))
        self.Current_Planet = None


play = Player()  # Create player
player_group = pygame.sprite.GroupSingle(play)
