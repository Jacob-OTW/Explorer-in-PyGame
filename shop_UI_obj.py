import pygame
from settings import stage
from player_obj import play
from pop_up_obj import add_pop_up
from nav_objs import map_selector
from space_probe_obj import add_probe


def return_main_menu():  # Returns main menu options
    a = []
    if play.Current_Planet and 'Shop' in play.Current_Planet.status:
        a.append('Buy')
        a.append('Sell')
        a.append('Refuel')
    else:
        a.append('')
        a.append('')
        a.append('')
    a.append('Inventory')
    a.append('Settings')
    a.append('Exit')
    return a


def return_inventory():  # Returns the inventory as shop list option
    while len(shop_ui.shop_list) - 1 < shop_ui.max_shop_length:
        shop_ui.shop_list.append('')
    for i in range(shop_ui.max_shop_length - 2):
        if i + shop_ui.page < len(play.inventory):
            shop_ui.shop_list[i] = play.inventory[i + shop_ui.page]
        else:
            shop_ui.shop_list[i] = ''
    shop_ui.shop_list[shop_ui.max_shop_length - 2] = 'Next Page'
    shop_ui.shop_list[shop_ui.max_shop_length - 1] = 'Last Page'
    shop_ui.shop_list[shop_ui.max_shop_length] = 'Return'


def return_buy():
    a = []
    while len(a) - 1 < shop_ui.max_shop_length:
        a.append('')
    for i, item in enumerate(play.Current_Planet.buying):
        if i < shop_ui.max_shop_length - 1:
            a[i] = item
    a[shop_ui.max_shop_length] = 'Return'
    return a


def return_sell():
    a = []
    while len(a) - 1 < shop_ui.max_shop_length:
        a.append('')
    clean = []
    for item in play.inventory:
        if item in play.Current_Planet.selling:
            clean.append(item)
    for i, item in enumerate(clean):
        if item not in play.Current_Planet.selling:
            continue
        else:
            if i < shop_ui.max_shop_length - 1:
                a[i] = item
    a[shop_ui.max_shop_length] = 'Return'
    return a


def return_settings():
    a = []
    while len(a) - 1 < shop_ui.max_shop_length:
        a.append('')
    shop_ui.shop_list = a
    shop_ui.shop_list[0] = 'Clear Target'
    shop_ui.shop_list[shop_ui.max_shop_length] = 'Return'


class Shop_UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_shop_length = 7  # Max amount of fields (n+1)
        self.image = pygame.image.load('Assets/shop_ui.png').convert_alpha()
        self.rect = self.image.get_rect(right=stage.SCREEN_WIDTH, top=0)  # Align Surface at top-right corner
        self.shop_list = return_main_menu()  # Set the menu to main options
        self.font = pygame.font.SysFont("bahnschrift", 34)  # setup font for text
        self.test_text = self.font.render('test text', True, (255, 255, 255))  # Used for text sizes
        self.selector = pygame.image.load(
            'Assets/selector.png').convert_alpha()  # This Surface goes to the selected surface to select things in the UI
        self.selector_rect = self.selector.get_rect()  # Create rect for selector to move it.
        self.selected = 0  # Start value for selector
        self.directory = []  # The directory is used to figure out what the user did before the function was called
        self.cached_item = None  # used to delete items and such
        self.shop = False  # Is shop shown
        self.page = 0  # Page is used for the inventory and later prob. for selling and buying
        self.usable_items = ['Item', 'Dead Skin', 'Probe']

    def update(self):
        self.image = pygame.image.load('Assets/shop_ui.png').convert_alpha()
        self.selector_rect.midtop = (
            100, self.selected * 50 + self.test_text.get_height() / 2 + 4)  # Set selector position
        self.image.blit(self.selector, self.selector_rect)  # Draw selector to Surface
        for i, item in enumerate(self.shop_list):  # Draw the Text from the shop_list
            text = self.font.render(f'{item}', True, (0, 0, 0))
            text_rect = text.get_rect(center=(100, i * 50 + text.get_height()))
            self.image.blit(text, text_rect)

    def use(self):  # Used whenever the user presses 'Return'
        if self.shop:
            choice = self.shop_list[self.selected]  # Choice is the item that was just confirmed by the user
            if not self.directory:  # Main Menu
                match choice:
                    case 'Buy':  # Buy was selected
                        self.directory.append('Buy')
                        self.shop_list = return_buy()
                    case 'Sell':  # Sell was selected
                        self.directory.append('Sell')
                        self.shop_list = return_sell()
                    case 'Refuel':
                        print('You have been refueled!')
                    case 'Inventory':
                        self.directory.append('Inventory')
                        return_inventory()
                    case 'Settings':
                        self.directory.append('Settings')
                        return_settings()
                    case 'Exit':
                        self.shop = False
            elif self.directory[0] == 'Inventory':  # Inventory menu
                if len(self.directory) > 1 and self.directory[1] == 'Item':
                    if self.cached_item == '' or choice == 'Return':
                        self.directory.pop()
                        return_inventory()
                    elif choice == 'Del':
                        if self.cached_item in play.inventory:
                            add_pop_up(f'-{self.cached_item}')
                            play.inventory.remove(self.cached_item)
                            self.directory.pop()
                            return_inventory()
                    elif choice == 'Use':
                        match self.cached_item:
                            case 'Item':
                                print('Yes')
                            case 'Dead Skin':
                                print('No')
                            case 'Probe':
                                add_probe()
                                play.inventory.remove('Probe')
                                self.directory.pop()
                                return_inventory()

                    else:
                        self.directory.pop()
                        return_inventory()
                else:
                    match choice:
                        case 'Next Page':
                            self.page += self.max_shop_length - 2
                            return_inventory()
                        case 'Last Page':
                            self.page -= self.max_shop_length - 2
                            if self.page < 0:
                                self.page = 0
                            return_inventory()
                        case 'Return':
                            self.directory.pop()
                            self.shop_list = return_main_menu()
                        case _:
                            self.cached_item = self.shop_list[self.selected]
                            if self.cached_item != '':
                                if self.cached_item in self.usable_items:
                                    self.shop_list = ['Use', 'Del', 'Return']
                                else:
                                    self.shop_list = ['Del', 'Return']
                                self.directory.append('Item')
            elif self.directory[0] == 'Settings':
                match choice:
                    case 'Return':
                        self.directory.pop()
                        self.shop_list = return_main_menu()
                    case 'Clear Target':
                        map_selector.target = None
            elif not play.Current_Planet or 'Shop' not in play.Current_Planet.status:
                self.shop = False
                self.shop_list = return_main_menu()
                self.directory = []
            # Extra Menus
            elif self.directory[0] == 'Buy':  # Buy Menu
                if choice != 'Return':
                    item = choice
                    if item in play.Current_Planet.buying:
                        price = play.Current_Planet.buying[item]
                        if play.money >= price:
                            play.money -= price
                            play.inventory.append(item)
                            add_pop_up(f'+{item}', f'-{price}')
                else:
                    self.directory.pop()
                    self.shop_list = return_main_menu()
            elif self.directory[0] == 'Sell':  # Sell Menu
                if not choice == 'Return':
                    if choice in play.Current_Planet.selling:
                        play.inventory.remove(choice)
                        play.money += play.Current_Planet.selling[choice]
                        add_pop_up(f'-{choice}', f'+{play.Current_Planet.selling[choice]}')
                        self.shop_list = return_sell()
                else:
                    self.directory.pop()
                    self.shop_list = return_main_menu()


shop_ui_group = pygame.sprite.GroupSingle()
shop_ui = Shop_UI()
shop_ui_group.add(shop_ui)
