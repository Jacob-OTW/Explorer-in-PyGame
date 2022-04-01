import pygame
import random
from settings import stage
from player_obj import play


class Stars:  # This class is used for the background tiles
    StarList = []  # Objects are added to this list
    test_img = pygame.image.load('Assets/BG/BG1.png').convert_alpha()  # Stored value for weight and height

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
        for u in [(stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2,
                   stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                   stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2,
                   stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5),
                  (stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                   stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5)]:
            cls.StarList.append(Stars(u[0], u[1]))

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
