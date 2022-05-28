from settings import *
from player_obj import play


class Stars:  # This class is used for the background tiles
    StarList = []  # Objects are added to this list
    test_img = pygame.transform.scale(pygame.image.load(f'Assets/BG/BG{random.randint(1, 3)}.png').convert_alpha(), (Stage.SCREEN_WIDTH, Stage.SCREEN_HEIGHT))

    @classmethod
    def randomBG(cls):
        # Returns one of the random images for the Background
        return pygame.transform.scale(pygame.image.load(f'Assets/BG/BG{random.randint(1, 3)}.png').convert_alpha(), (Stage.SCREEN_WIDTH, Stage.SCREEN_HEIGHT))

    @classmethod
    def draw(cls):
        # This will move all the backgrounds and draw them
        for star in cls.StarList:
            star.move()
            Stage.screen.blit(star.img, star.position)

    @classmethod
    def addstars(cls):
        # This will create and 4 objects with the correct starting points for a flawless background
        for u in [(Stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2,
                   Stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (Stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                   Stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() / 2),
                  (Stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() / 2,
                   Stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5),
                  (Stage.SCREEN_WIDTH / 2 - cls.test_img.get_width() * 1.5,
                   Stage.SCREEN_HEIGHT / 2 - cls.test_img.get_height() * 1.5)]:
            cls.StarList.append(Stars(u[0], u[1]))

    def __init__(self, x, y):
        self.position = pygame.math.Vector2((x, y))
        self.img = self.randomBG()

    def move(self):
        x, y = self.position - play.force
        c = False  # c is a trigger to tell if a new image is needed
        if x < 0 - Stage.SCREEN_WIDTH:
            x = x + Stars.test_img.get_width() * 2
            c = True
        elif x > Stage.SCREEN_WIDTH:
            x = 0 - Stage.SCREEN_WIDTH
            c = True
        if y < 0 - Stage.SCREEN_HEIGHT:
            y = Stage.SCREEN_HEIGHT
            c = True
        elif y > Stage.SCREEN_HEIGHT:
            y = 0 - Stage.SCREEN_HEIGHT
            c = True
        if c:
            self.img = Stars.randomBG()

        self.position = (x, y)
