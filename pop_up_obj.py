import pygame
from settings import stage


def add_pop_up(*args: str):  # Creates pop-ups
    if args:
        for i, arg in enumerate(args):
            pop_up_group.add(Pop_Up(arg, i))


class Pop_Up(pygame.sprite.Sprite):
    def __init__(self, t: str, pos_y=0):
        super().__init__()
        self.font = pygame.font.SysFont("bahnschrift", 32)
        self.image = pygame.image.load('Assets/pop_up.png').convert_alpha()  # Create Surface
        self.rect = self.image.get_rect(centerx=stage.SCREEN_WIDTH - 100, top=416 + 52 * pos_y)
        self.text = self.font.render(t, True, (255, 255, 255))  # Create assigned text
        self.text_rect = self.text.get_rect(center=(100, 25))  # Text_rect is used to place the text in the center
        self.image.blit(self.text, self.text_rect)  # Draw the text onto the Surface at the center
        self.opacity = 255  # The pop-up sprite will overtime turn transparent

    def update(self):
        self.rect.y += 1  # Go down by 1
        self.opacity -= 2.5  # Turn more transparent
        if self.opacity <= 0:  # Destroy if fully transparent
            self.kill()
        self.image.set_alpha(self.opacity)  # Change alpha value of Surface


pop_up_group = pygame.sprite.Group()
