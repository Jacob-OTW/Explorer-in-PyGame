import pygame
import sys
import random
import time
from settings import stage
from player_obj import player_group, play
from planet_obj import planet_group
from creature_obj import creature_group
from pop_up_obj import pop_up_group
from shop_UI_obj import shop_ui_group, shop_ui, return_main_menu
from map_UI_obj import map_ui_group, map_ui
from mimic_obj import mimic_group, Mimic


def HandleKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                shop_ui.selected -= 1
                if shop_ui.selected < 0:
                    shop_ui.selected = shop_ui.max_shop_length
            if event.key == pygame.K_DOWN:
                shop_ui.selected += 1
                if shop_ui.selected > shop_ui.max_shop_length:
                    shop_ui.selected = 0
            if event.key == pygame.K_RETURN:
                shop_ui.use()
            if event.key == pygame.K_e:
                shop_ui.shop = True
                shop_ui.shop_list = return_main_menu()
            if event.key == pygame.K_m:
                map_ui.map = False if map_ui.map else True


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

mimic_group.add(Mimic(play, is_player=True))
for i in planet_group.sprites():
    mimic_group.add(Mimic(i))

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
    creature_group.update()
    shop_ui_group.update()
    pop_up_group.update()
    mimic_group.update()

    # Visual
    stage.screen.fill(bg_color)  # Fill the 'screen' surface with a solid color
    Stars.draw()  # Draw the Stars and update their position
    planet_group.draw(stage.screen)  # Draw the planets
    creature_group.draw(stage.screen)
    player_group.draw(stage.screen)
    MT.draw()  # Draw all Saved positions
    # play.draw_mask_attach()
    if shop_ui.shop:
        shop_ui_group.draw(stage.screen)
    if map_ui.map:
        map_ui_group.draw(stage.screen)
        mimic_group.draw(stage.screen)
    pop_up_group.draw(stage.screen)

    # Text
    text = myfont.render(f"", True, (255, 255, 0))
    stage.screen.blit(text, (5, 10))
    text2 = myfont.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 0))
    stage.screen.blit(text2, (5, 25))

    # Update
    pygame.display.flip()
    stage.clock.tick(60)
