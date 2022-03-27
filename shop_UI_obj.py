import pygame
from settings import stage
from player_obj import play


class Shop_UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((200, 300))
        self.image.fill('Green')
        self.selector = pygame.Surface((200, 75))
        self.selector.fill('White')
        self.selector_rect = self.selector.get_rect()
        self.selected = 0
        self.rect = self.image.get_rect(right=stage.SCREEN_WIDTH, top=0)
        self.shop_list = ['Buy', 'Sell', 'Refuel', 'Exit']
        self.font = pygame.font.SysFont("monospace", 32)  # setup font for text
        self.directory = []
        self.shop = False

    def update(self):
        self.image = pygame.Surface((200, 300))
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
                    self.shop_list = ['Item1', 'Item2', 'Item3', 'Return']
                elif self.shop_list[self.selected] == 'Sell':  # Sell was selected
                    self.directory.append('Sell')
                    for i in range(3):
                        if i < len(play.inventory):
                            self.shop_list[i] = play.inventory[i]
                        else:
                            self.shop_list[i] = 'X'
                    self.shop_list[3] = 'Return'
                elif self.shop_list[self.selected] == 'Refuel':
                    print('You have been refueled!')
                elif self.shop_list[self.selected] == 'Exit':
                    self.shop = False
            elif self.directory[0] == 'Buy':  # Buy Menu
                if self.shop_list[self.selected] != 'Return':
                    print(f'You bought {self.shop_list[self.selected]}')
                else:
                    self.directory.pop()
                    self.shop_list = ['Buy', 'Sell', 'Refuel', 'Exit']
            elif self.directory[0] == 'Sell':  # Sell Menu
                if not self.shop_list[self.selected] == 'Return':
                    pass
                else:
                    self.directory.pop()
                    self.shop_list = ['Buy', 'Sell', 'Refuel', 'Exit']


shop_ui_group = pygame.sprite.GroupSingle()
shop_ui = Shop_UI()
shop_ui_group.add(shop_ui)
