import pygame
import sys
import random
import math
import time
from settings import stage
from player_obj import player_group, play
from planet_obj import planet_group


def HandleKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


class Stars:  # This class is used for the background tiles
    StarList = []  # Objects are added to this list
    test_img = pygame.image.load('Assets/BG/BG1.png').convert_alpha()  # This variable is used for get_width and get_height

    @classmethod
    def randomBG(cls):
        # Returns one of the random images for the Background
        return pygame.image.load(f'Assets/BG/BG{random.randint(1, 3)}.png').convert_alpha()

    @classmethod
    def draw(cls):
        # This will move all the backgrounds and draw them
        for star in cls.StarList:
            star.move()
            stage.screen.blit(star.img, star.position)

    @classmethod
    def addstars(cls):
        # This will create and 4 objects with the correct starting points for a flawless background
        for i in [(stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2, stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (
                          stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                          stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (
                          stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2,
                          stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5),
                  (stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                   stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5)]:
            cls.StarList.append(Stars(i[0], i[1]))

    def __init__(self, x, y):
        self.position = (x, y)
        self.img = self.randomBG()

    def move(self):
        x = self.position[0] - play.XF
        y = self.position[1] - play.YF
        c = False  # c is a trigger to tell if a new image is needed
        if x < 0 - stage.SCREEN_WIDTH:
            x = x + Stars.test_img.get_width() * 2
            c = True
        elif x > stage.SCREEN_WIDTH:
            x = 0 - stage.SCREEN_WIDTH
            c = True
        if y < 0 - stage.SCREEN_HEIGHT:
            y = stage.SCREEN_HEIGHT
            c = True
        elif y > stage.SCREEN_HEIGHT:
            y = 0 - stage.SCREEN_HEIGHT
            c = True
        if c:
            self.img = Stars.randomBG()

        self.position = (x, y)


class MouseTrail:  # This class is for debugging
    def __init__(self):
        self.positions = []
        self.img = pygame.image.load('Assets/Heart.png').convert_alpha()

    def Check(self):
        if pygame.mouse.get_pressed(3)[0]:
            temp = pygame.mouse.get_pos()
            self.add_at(temp[0] + stage.XScroll, temp[1] + stage.YScroll)
        elif pygame.mouse.get_pressed(3)[2]:
            self.positions = []

    def add_at(self, x, y):
        self.positions.append((x, y))

    def draw(self):
        for pos in self.positions:
            stage.screen.blit(self.img, (pos[0] - stage.XScroll, pos[1] - stage.YScroll))


surface = pygame.Surface(stage.screen.get_size())
bg_color = pygame.Color('black')

MT = MouseTrail()  # Create Mouse trail object for debugging

Stars.addstars()  # Add the 4 background tiles

myfont = pygame.font.SysFont("monospace", 16)  # setup font for text

last_time = time.time()
while True:
    # Timing
    frame_time = time.time() - last_time
    last_time = time.time()

    # Events
    HandleKeys()  # Check if game quit or Keys were pressed
    MT.Check()  # Check if mouse button is down
    player_group.update()
    planet_group.update()

    # Visual
    stage.screen.fill(bg_color)  # Fill the 'screen' surface with a solid color
    Stars.draw()  # Draw the Stars and update their position
    planet_group.draw(stage.screen)  # Draw the Player
    player_group.draw(stage.screen)
    MT.draw()  # Draw all Saved positions

    # Text
    text = myfont.render(f"{play.offset}", True, (255, 255, 0))
    stage.screen.blit(text, (5, 10))
    text2 = myfont.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 0))
    stage.screen.blit(text2, (5, 25))

    # Update
    pygame.display.flip()
    stage.clock.tick(60)
