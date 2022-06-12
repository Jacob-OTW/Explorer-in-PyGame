from settings import *
from player_obj import player_group, play
from planet_obj import planet_group
from creature_obj import creature_group
from pop_up_obj import pop_up_group
from shop_UI_obj import shop_ui_group, shop_ui, return_main_menu
from nav_objs import mimic_group, Mimic, map_selector_group, map_selector, map_ui_group, map_ui, arrow_group
from star_obj import Stars
from space_probe_obj import space_probe_group
from radar_obj import radar_group, radar, radar_ping_group
from missile_obj import missile_group, Missile
from effects import effect_group
from key_binds import keybinds


def handle_keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == keybinds['Menu_Up']:  # Cycle through menu up
                shop_ui.selected -= 1
                if shop_ui.selected < 0:
                    shop_ui.selected = shop_ui.max_shop_length
            if event.key == keybinds['Menu_Down']:  # Cycle through menu down
                shop_ui.selected += 1
                if shop_ui.selected > shop_ui.max_shop_length:
                    shop_ui.selected = 0
            if event.key == keybinds['Menu_Confirm']:  # Confirm Action in Shop UI
                shop_ui.use()
            if event.key == keybinds['Open_Menu']:  # Open Shop_UI
                shop_ui.shop = True
                shop_ui.directory = []
                shop_ui.shop_list = return_main_menu()
            if event.key == keybinds['Open_Map']:  # Open and close map
                map_ui.map = False if map_ui.map else True
            if event.key == keybinds['Cycle_Map']:  # Cycle target for arrow and map
                map_selector.next_target()
            if event.key == keybinds['Lock_Radar']:  # Lock radar
                if 'Radar' in play.inventory and radar_ping_group.sprites():
                    r = random.choice(radar_ping_group.sprites())
                    r.target.seen_by_probe = True
                    radar.lock = r.target
                    map_selector.set_target(r)
            if event.key == pygame.K_q:
                Missile.add_missile()


class MouseTrail:  # This class is for debugging
    def __init__(self):
        self.positions = []
        self.img = pygame.image.load('Assets/Heart.png').convert_alpha()

    def check(self):
        if pygame.mouse.get_pressed(3)[0]:
            temp = pygame.mouse.get_pos()
            self.add_at(temp[0] + Stage.XScroll, temp[1] + Stage.YScroll)
        elif pygame.mouse.get_pressed(3)[2]:
            self.positions = []

    def add_at(self, x, y):
        self.positions.append((x, y))

    def draw(self):
        for pos in self.positions:
            Stage.screen.blit(self.img, (pos[0] - Stage.XScroll, pos[1] - Stage.YScroll))


MT = MouseTrail()  # Create Mouse trail object for debugging

Stars.addstars()  # Add the 4 background tiles

my_font = pygame.font.SysFont("monospace", 16)  # setup font for text

mimic_group.add(Mimic(play))

play.inventory.append('Radar')

last_time = time.time()
while True:
    # Timing
    frame_time = time.time() - last_time
    last_time = time.time()

    # Events
    handle_keys()  # Check if game quit or Keys were pressed
    MT.check()  # Check if mouse button is down and draw hearts
    player_group.update(planet_group)  # planet_group is passed as an argument because it can't import it (circle)
    arrow_group.update()
    planet_group.update()
    creature_group.update()
    space_probe_group.update()
    shop_ui_group.update()
    pop_up_group.update()
    mimic_group.update()
    map_selector_group.update()
    if 'Radar' in play.inventory:
        radar_group.update()
        radar_ping_group.update()
    missile_group.update()
    effect_group.update()

    # Visual
    Stage.screen.fill('black')  # Fill the 'screen' surface with a solid color
    Stars.draw()  # Draw the Stars and update their position
    space_probe_group.draw(Stage.screen)
    planet_group.draw(Stage.screen)  # Draw the planets
    creature_group.draw(Stage.screen)
    missile_group.draw(Stage.screen)
    player_group.draw(Stage.screen)
    effect_group.draw(Stage.screen)
    if map_selector.target:
        arrow_group.draw(Stage.screen)
    MT.draw()  # Draw all Saved positions
    # play.draw_mask_attach()
    if shop_ui.shop:
        shop_ui_group.draw(Stage.screen)
    if map_ui.map:
        map_ui_group.draw(Stage.screen)
        if map_selector.target:
            map_selector_group.draw(Stage.screen)
        mimic_group.draw(Stage.screen)
    if 'Radar' in play.inventory:
        radar_group.draw(Stage.screen)
        radar_ping_group.draw(Stage.screen)
    pop_up_group.draw(Stage.screen)

    # Text
    text = my_font.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 0))
    Stage.screen.blit(text, (5, 10))

    # Update
    pygame.display.flip()
    Stage.clock.tick(60)
