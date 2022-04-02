import random
import pygame
import sys
import time
from settings import stage
from player_obj import player_group, play
from planet_obj import planet_group
from creature_obj import creature_group
from pop_up_obj import pop_up_group
from shop_UI_obj import shop_ui_group, shop_ui, return_main_menu
from nav_objs import mimic_group, Mimic, map_selector_group, map_selector, map_ui_group, map_ui, arrow_group
from star_obj import Stars
from space_probe_obj import space_probe_group
from radar_obj import radar_group, radar, radar_ping_group


def HandleKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Cycle through menu up
                shop_ui.selected -= 1
                if shop_ui.selected < 0:
                    shop_ui.selected = shop_ui.max_shop_length
            if event.key == pygame.K_DOWN:  # Cycle through menu down
                shop_ui.selected += 1
                if shop_ui.selected > shop_ui.max_shop_length:
                    shop_ui.selected = 0
            if event.key == pygame.K_RETURN:  # Confirm Action in Shop UI
                shop_ui.use()
            if event.key == pygame.K_e:  # Open Shop_UI
                shop_ui.shop = True
                shop_ui.directory = []
                shop_ui.shop_list = return_main_menu()
            if event.key == pygame.K_m:  # Open and close map
                map_ui.map = False if map_ui.map else True
            if event.key == pygame.K_g:  # Cycle target for arrow and map
                map_selector.next_target()
            if event.key == pygame.K_i:
                if 'Radar' in play.inventory and radar_ping_group.sprites():
                    r = random.choice(radar_ping_group.sprites())
                    radar.lock = r.target
                    map_selector.set_target(r)


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


MT = MouseTrail()  # Create Mouse trail object for debugging

Stars.addstars()  # Add the 4 background tiles

mimic_group.add(Mimic(play, is_player=True))  # Add mimics for all objects
for i in creature_group.sprites():
    mimic_group.add(Mimic(i))
for i in planet_group.sprites():
    mimic_group.add(Mimic(i))

myfont = pygame.font.SysFont("monospace", 16)  # setup font for text

last_time = time.time()
play.inventory.append('Probe')
while True:
    # Timing
    frame_time = time.time() - last_time
    last_time = time.time()

    # Events
    HandleKeys()  # Check if game quit or Keys were pressed
    MT.Check()  # Check if mouse button is down
    player_group.update()
    arrow_group.update()
    planet_group.update()
    creature_group.update()
    space_probe_group.update()
    shop_ui_group.update()
    pop_up_group.update()
    mimic_group.update()
    map_selector_group.update()
    radar_group.update()
    radar_ping_group.update()

    # Visual
    stage.screen.fill('black')  # Fill the 'screen' surface with a solid color
    Stars.draw()  # Draw the Stars and update their position
    space_probe_group.draw(stage.screen)
    planet_group.draw(stage.screen)  # Draw the planets
    creature_group.draw(stage.screen)
    player_group.draw(stage.screen)
    if map_selector.target:
        arrow_group.draw(stage.screen)
    MT.draw()  # Draw all Saved positions
    # play.draw_mask_attach()
    if shop_ui.shop:
        shop_ui_group.draw(stage.screen)
    if map_ui.map:
        map_ui_group.draw(stage.screen)
        if map_selector.target:
            map_selector_group.draw(stage.screen)
        mimic_group.draw(stage.screen)
    if 'Radar' in play.inventory:
        radar_group.draw(stage.screen)
        radar_ping_group.draw(stage.screen)
    pop_up_group.draw(stage.screen)

    # Text
    text = myfont.render(f"{map_selector.target}", True, (255, 255, 0))
    stage.screen.blit(text, (5, 10))
    text2 = myfont.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 0))
    stage.screen.blit(text2, (5, 25))

    # Update
    pygame.display.flip()
    stage.clock.tick(60)
