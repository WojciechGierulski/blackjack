import pygame
import sys
from game_params import GameParams, cursor_in_rect

class Button:
    font = pygame.font.SysFont("comicsans", 30, True)
    size = (100, 60)
    normal_image = pygame.image.load("./rest/button.png")
    normal_image = pygame.transform.scale(normal_image, size)
    pressed_image = pygame.image.load("./rest/pressed_button.png")
    pressed_image = pygame.transform.scale(pressed_image, size)
    """
    :param img
    :type img - pygame image
    :param text
    :type text - string
    :param cords
    :type cords - [int, int]
    """
    def __init__(self, cords, text=""):
        self.cords = cords
        self.text = text
        self.clicking = False

    def draw(self, screen):
        text = self.font.render(self.text, 1, (0,0,0))
        if self.clicking:
            screen.blit(self.pressed_image, tuple(self.cords))
        else:
            screen.blit(self.normal_image, tuple(self.cords))
        screen.blit(text, (self.cords[0] + 0.5 * self.normal_image.get_width() - text.get_width()/2, self.cords[1] + 22))

class GameButton(Button):
    """

    """
    def __init__(self, cords, text=""):
        super().__init__(cords, text)

class BetButton(GameButton):
    """

    """
    def __init__(self, cords, text=""):
        super().__init__(cords, text)

class Menu:
    """

    """
    def __init__(self):
        self.background = GameParams.menu_background
        self.run = True
        self.buttons = []
        self.buttons.append(Button((GameParams.size[0]/2 - Button.size[0]/2, 200), "Play"))
        self.buttons.append(Button((GameParams.size[0]/2 - Button.size[0]/2, 300), "Shop"))
        self.buttons.append(Button((GameParams.size[0]/2 - Button.size[0]/2, 400), "Quit"))

    def run_menu(self):
        self.run = True
        button_text = None
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            button_text = self.check_pressed(events)
            self.draw(GameParams.screen)
            pygame.display.update()
        return button_text


    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(GameParams.blackjack_caption, (223, 50))
        for button in self.buttons:
            button.draw(screen)

    def check_pressed(self, events):
        pressed = None
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if cursor_in_rect(button.cords, pygame.mouse.get_pos(), button.size):
                        button.clicking = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    if cursor_in_rect(button.cords, pygame.mouse.get_pos(), button.size) and button.clicking == True:
                        pressed = button.text
                        self.run = False
                    button.clicking = False
        return pressed


