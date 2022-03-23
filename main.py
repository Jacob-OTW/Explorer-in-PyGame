import pygame
import sys
import random
import math
import time

debug = True

pygame.init()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


class Stage:  # This class is used for stuff that I need to easily adapt SNAP! code
    bg = pygame.image.load('Background.png')
    XScroll = 0
    YScroll = 0

    @classmethod
    def HandleKeys(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if debug:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Planet.PlanetList[0].orbit_speed *= 0.5
                    elif event.key == pygame.K_DOWN:
                        Planet.PlanetList[0].orbit_speed *= 2
                    elif event.key == pygame.K_LEFT:
                        Planet.PlanetList[0].mass *= 0.5
                    elif event.key == pygame.K_RIGHT:
                        Planet.PlanetList[0].mass *= 2


class Player:  # This class is used for the player

    def __init__(self):
        # Positions
        self.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.angle = 0

        # Forces
        self.XF = 0
        self.YF = 0

        # Images
        self.Idle = pygame.image.load('Ship.png').convert()
        self.Idle.set_colorkey((0, 0, 0))
        self.img = pygame.transform.rotate(self.Idle, self.angle)

        # Masks
        temp = pygame.image.load('Lander.png').convert_alpha()
        self.lander_img = pygame.transform.rotate(temp, self.angle)
        self.mask = pygame.mask.from_surface(self.lander_img, 300)

        # Planet caching
        self.Current_Planet = None

        # Centered Rotation
        self.cpos = (
            self.position[0] - int(self.img.get_width() / 2), self.position[1] - int(self.img.get_height() / 2))

    def HandleInput(self):
        keys = pygame.key.get_pressed()
        # Rotation
        if keys[pygame.K_a]:
            self.rotate(5)
        if keys[pygame.K_d]:
            self.rotate(-5)
        # Movement
        if keys[pygame.K_SPACE]:
            self.accelerate()

    def draw(self):
        # Images
        temp = pygame.image.load('Lander.png').convert_alpha()
        self.lander_img = pygame.transform.rotate(temp, self.angle)

        # Mask
        self.mask = pygame.mask.from_surface(self.lander_img)

        # Centred Rotation
        self.cpos = (
            self.position[0] - int(self.img.get_width() / 2), self.position[1] - int(self.img.get_height() / 2))

        # Draw Mask
        if debug:
            olist = self.mask.outline()
            image = pygame.Surface([640, 480], pygame.SRCALPHA, 32)
            image = image.convert_alpha()
            pygame.draw.lines(image, (200, 150, 150), True, olist)
            screen.blit(image, self.cpos)

        # Draw Image
        screen.blit(self.img, self.cpos)

    def move(self):
        if self.Current_Planet:
            # Update X Force and Y Force
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_SPACE]:
                self.XF = self.Current_Planet.XF
                self.YF = self.Current_Planet.YF

        # Add X Force and Y Force values to the overall Scroll
        Stage.XScroll += self.XF
        Stage.YScroll += self.YF

    def rotate(self, r):
        # change the rotation value and render a new img
        self.angle += r
        self.img = pygame.transform.rotate(self.Idle, self.angle)

    def accelerate(self):
        # Convert is needed because math.sin and math.cos work in radian instead of degrees
        convert = 360 / (2 * math.pi)
        self.XF += math.cos(self.angle / convert) * 0.1
        self.YF -= math.sin(self.angle / convert) * 0.1

    def Touch(self):
        # Setup for Mask collision test
        if self.Current_Planet:
            # Set var to None if no longer touching the planet
            offset_x = play.cpos[0] - self.Current_Planet.position[0]
            offset_y = play.cpos[1] - self.Current_Planet.position[1]
            if not self.Current_Planet.mask.overlap(play.mask, (offset_x, offset_y)):  # If colliding with Planet
                self.Current_Planet = None


class Stars:  # This class is used for the background tiles
    StarList = []  # Objects are added to this list
    test_img = pygame.image.load('BG/BG1.png').convert_alpha()  # This variable is used for get_width and get_height

    @classmethod
    def randomBG(cls):
        # Returns one of the random images for the Background
        return pygame.image.load(f'BG/BG{random.randint(1, 3)}.png').convert_alpha()

    @classmethod
    def draw(cls):
        # This will move all the backgrounds and draw them
        for star in cls.StarList:
            star.move()
            screen.blit(star.img, star.position)

    @classmethod
    def addstars(cls):
        # This will create and 4 objects with the correct starting points for a flawless background
        for i in [(SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2, SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (
                          SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                          SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (
                          SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2,
                          SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5),
                  (SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                   SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5)]:
            cls.StarList.append(Stars(i[0], i[1]))

    def __init__(self, x, y):
        self.position = (x, y)
        self.img = self.randomBG()

    def move(self):
        x = self.position[0] - play.XF
        y = self.position[1] - play.YF
        c = False  # c is a trigger to tell if a new image is needed
        if x < 0 - SCREEN_WIDTH:
            x = x + Stars.test_img.get_width() * 2
            c = True
        elif x > SCREEN_WIDTH:
            x = 0 - SCREEN_WIDTH
            c = True
        if y < 0 - SCREEN_HEIGHT:
            y = SCREEN_HEIGHT
            c = True
        elif y > SCREEN_HEIGHT:
            y = 0 - SCREEN_HEIGHT
            c = True
        if c:
            self.img = Stars.randomBG()

        self.position = (x, y)


class MouseTrail:  # This class is for debugging
    def __init__(self):
        self.positions = []
        self.img = pygame.image.load('Heart.png').convert_alpha()

    def Check(self):
        if pygame.mouse.get_pressed(3)[0]:
            temp = pygame.mouse.get_pos()
            self.add_at(temp[0] + Stage.XScroll, temp[1] + Stage.YScroll)
        elif pygame.mouse.get_pressed(3)[2]:
            self.positions = []

    def add_at(self, x, y):
        self.positions.append((x, y))

    def draw(self):
        for pos in self.positions:
            screen.blit(self.img, (pos[0] - Stage.XScroll, pos[1] - Stage.YScroll))


class Planet:  # This class is used for Planets of all kind
    PlanetList = []  # Like the stars, all objects are stored in this list to check each one of them

    @classmethod
    def draw(cls):
        for planet in cls.PlanetList:
            # Check for characteristics
            if 'Static' in planet.status:
                pass
            elif 'Moving' in planet.status:
                x, y = planet.startx, planet.starty

                planet.XF = math.cos(planet.orbit_value) * planet.orbit_speed
                planet.YF = math.sin(planet.orbit_value) * planet.orbit_speed

                x += planet.XF
                y += planet.YF

                planet.orbit_value += planet.mass * planet.orbit_speed
                MT.add_at(planet.startx, planet.starty)

                planet.startx, planet.starty = x, y

            # Update
            planet.position = (planet.startx - Stage.XScroll, planet.starty - Stage.YScroll)  # Update Pos

            # Hitbox
            if debug:
                olist = planet.mask.outline()
                image = pygame.Surface([640, 480], pygame.SRCALPHA, 32)  # Create Emtpy Surface
                image = image.convert_alpha()  # ^
                pygame.draw.lines(image, (200, 150, 150), True, olist)  # Draw the hitbox lines onto the surface
                screen.blit(image, planet.position)  # Draw the surface

            # Blit the Surfaces
            screen.blit(planet.img, planet.position)

    @classmethod
    def Touch(cls):
        for planet in cls.PlanetList:
            # Setup for Mask collision test
            offset_x = play.cpos[0] - planet.position[0]
            offset_y = play.cpos[1] - planet.position[1]
            if planet.mask.overlap(play.mask, (offset_x, offset_y)):  # If colliding with Planet
                if play.Current_Planet != planet:
                    play.Current_Planet = planet

    def __init__(self, x, y, xf=0, yf=0, status=None, size=100, orbit_speed=10, mass=0.01, loot=None):
        if status is None:
            status = ['Static']

        # Set values
        self.startx = x
        self.starty = y
        self.XF = xf
        self.YF = yf
        self.status = status
        self.size = size
        self.orbit_speed = orbit_speed
        self.mass = mass
        self.loot = loot

        # std values
        self.orbit_value = 0

        # init
        self.position = (x - Stage.XScroll, y - Stage.YScroll)
        self.img = pygame.image.load('Planets/Planet1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.img)


surface = pygame.Surface(screen.get_size())
bg_color = pygame.Color('black')

play = Player()  # Create player

MT = MouseTrail()  # Create Mouse trail object for debugging

Stars.addstars()  # Add the 4 background tiles

Planet.PlanetList.append(Planet(0, 0, xf=0, yf=0, mass=0.01, orbit_speed=-10, status=['Moving']))

myfont = pygame.font.SysFont("monospace", 16)  # setup font for text

last_time = time.time()

while True:
    # Timing
    frame_time = time.time() - last_time
    last_time = time.time()

    # Events
    Stage.HandleKeys()  # Check if game quit or Keys were pressed
    MT.Check()  # Check if mouse button is down
    play.HandleInput()  # Check for inputs for turing and thrust
    play.move()  # Move the Scroll values by current X and Y Forces
    play.Touch()  # This checks if the player is still touching a planet
    Planet.Touch()  # This checks if the player is touching any planet

    # Visual
    screen.fill(bg_color)  # Fill the 'screen' surface with a solid color
    Stars.draw()  # Draw the Stars and update their position
    Planet.draw()  # Draw the Player
    play.draw()  # Draw Player onto surface
    MT.draw()  # Draw all Saved positions

    # Text
    text = myfont.render(f"{play.Current_Planet}", True, (255, 255, 0))
    screen.blit(text, (5, 10))
    text2 = myfont.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 0))
    screen.blit(text2, (5, 25))

    # Update
    pygame.display.flip()
    clock.tick(60)
