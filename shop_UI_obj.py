import pygame
from settings import stage
from player_obj import play


def return_main_menu():
    return ['Buy', 'Sell', 'Refuel', 'Inventory', 'Exit']


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
        self.shop = False

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
                    for i in range(self.max_shop_length):
                        self.shop_list[i] = f'Item {i}'
                    self.shop_list[self.max_shop_length] = 'Return'
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
                    for i in range(self.max_shop_length):
                        if i < len(play.inventory):
                            self.shop_list[i] = play.inventory[i]
                        else:
                            self.shop_list[i] = ''
                    self.shop_list[self.max_shop_length] = 'Return'
                elif self.shop_list[self.selected] == 'Exit':
                    self.shop = False
            # Extra Menus
            elif self.directory[0] == 'Buy':  # Buy Menu
                if self.shop_list[self.selected] != 'Return':
                    print(f'You bought {self.shop_list[self.selected]}')
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
                pass


shop_ui_group = pygame.sprite.GroupSingle()
shop_ui = Shop_UI()
shop_ui_group.add(shop_ui)
