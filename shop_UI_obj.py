import pygame
from settings import stage
from player_obj import play


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


class Shop_UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.max_shop_length = 4
        self.image = pygame.Surface((200, (self.max_shop_length + 1) * 75))
        self.image.fill('Green')
        self.rect = self.image.get_rect(right=stage.SCREEN_WIDTH, top=0)
        self.selector = pygame.Surface((200, 75))
        self.selector.fill('White')
        self.selector_rect = self.selector.get_rect()
        self.selected = 0
        self.shop_list = return_main_menu()
        self.font = pygame.font.SysFont("monospace", 32)  # setup font for text
        self.directory = []
        self.cached_item = None
        self.shop = False
        self.page = 0

    def update(self):
        self.image = pygame.Surface((200, (self.max_shop_length + 1) * 75))
        self.image.fill('Green')
        self.selector_rect.center = (100, self.selected * 75 + 37)
        self.image.blit(self.selector, self.selector_rect)
        for i, item in enumerate(self.shop_list):
            text = self.font.render(f'{item}', True, (0, 0, 0))
            text_rect = text.get_rect(center=(100, i * 75 + text.get_height()))
            self.image.blit(text, text_rect)

    def use(self):
        if self.shop:
            if not self.directory:  # Main Menu
                if self.shop_list[self.selected] == 'Buy':  # Buy was selected
                    self.directory.append('Buy')
                    self.shop_list = return_buy()
                elif self.shop_list[self.selected] == 'Sell':  # Sell was selected
                    self.directory.append('Sell')
                    for i in range(self.max_shop_length):
                        if i < len(play.inventory):
                            self.shop_list[i] = play.inventory[i]
                        else:
                            self.shop_list[i] = 'X'
                    self.shop_list[self.max_shop_length] = 'Return'
                elif self.shop_list[self.selected] == 'Refuel':
                    print('You have been refueled!')
                elif self.shop_list[self.selected] == 'Inventory':
                    self.directory.append('Inventory')
                    return_inventory()
                elif self.shop_list[self.selected] == 'Exit':
                    self.shop = False
            # Extra Menus
            elif self.directory[0] == 'Buy':  # Buy Menu
                if self.shop_list[self.selected] != 'Return':
                    item = self.shop_list[self.selected]
                    price = play.Current_Planet.buying[item]
                    if play.money >= price:
                        play.money -= price
                        play.inventory.append(item)
                else:
                    self.directory.pop()
                    self.shop_list = return_main_menu()
            elif self.directory[0] == 'Sell':  # Sell Menu
                if not self.shop_list[self.selected] == 'Return':
                    pass
                else:
                    self.directory.pop()
                    self.shop_list = return_main_menu()
            elif self.directory[0] == 'Inventory':
                if len(self.directory) > 1 and self.directory[1] == 'Item':
                    if self.cached_item == '' or self.shop_list[self.selected] == 'Return':
                        self.directory.pop()
                        return_inventory()
                    elif self.shop_list[self.selected] == 'Del':
                        play.inventory.remove(self.cached_item)
                        self.directory.pop()
                        return_inventory()
                    else:
                        self.directory.pop()
                        return_inventory()
                else:
                    if self.shop_list[self.selected] == 'Next Page':
                        self.page += 1
                        return_inventory()
                    elif self.shop_list[self.selected] == 'Last Page':
                        self.page -= 1
                        if self.page < 0:
                            self.page = 0
                        return_inventory()
                    elif self.shop_list[self.selected] == 'Return':
                        self.directory.pop()
                        self.shop_list = return_main_menu()
                    else:
                        self.cached_item = self.shop_list[self.selected]
                        if self.cached_item != '':
                            self.shop_list = ['Del', 'Return']
                            self.directory.append('Item')
                            print(self.cached_item)


shop_ui_group = pygame.sprite.GroupSingle()
shop_ui = Shop_UI()
shop_ui_group.add(shop_ui)
