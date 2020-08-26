from menu import Button, Menu
from game_params import GameParams, cursor_in_rect
import pygame
import sys
from card import CardsDatabase


class ShopItem:
    """
    :param image
    :type image - pygame image
    :param bought
    :type bought - bool
    :param name
    :type name - string
    :param size
    :type size - [int, int]
    """
    size = (70, 120)
    font = pygame.font.SysFont("comicsans", 30)
    prices = {"gray_back": 0, "green_back": 500, "blue_back": 100, "purple_back": 2000, "red_back": 5000,
              "yellow_back": 1000}

    def __init__(self, cords, image, name, bought=False, chosen=False):
        self.cords = cords
        self.image = pygame.transform.scale(image, self.size)
        self.name = name
        self.bought = bought
        self.chosen = chosen
        self.price = self.prices[self.name]

    def draw(self, screen):
        screen.blit(self.image, self.cords)
        if not self.bought:
            text = f"{self.price}$"
        else:
            if not self.chosen:
                text = f"Owned"
            else:
                text = f"Chosen"
        caption = self.font.render(text, 1, (0, 0, 0))
        cords = (self.cords[0] + self.size[0] / 2 - caption.get_width() / 2,
                 self.cords[1] + self.size[1] + caption.get_height())
        screen.blit(caption, cords)

    def buy_or_choose(self, player, shop_items):
        if not self.bought:
            if player.cash - self.price >= 0:
                player.cash -= self.price
                self.bought = True
        if self.bought:
            for item in shop_items:
                if item.chosen:
                    item.chosen = False
            player.card_back = CardsDatabase.backs[self.name]
            self.chosen = True


class Shop:
    """

    """
    back_button_cords = (10, 10)
    font = pygame.font.SysFont("comicsans", 30, True)

    def __init__(self, player):
        self.player = player
        self.background = GameParams.menu_background
        self.run = True
        self.buttons = []
        self.buttons.append(Button(self.back_button_cords, "Menu"))
        self.shop_items = []

    def load_shop_items(self):
        start_cords = [30, 90]
        where_cords = start_cords[:]
        for name in CardsDatabase.backs:
            item = ShopItem(where_cords[:], CardsDatabase.backs[name], name)
            self.shop_items.append(item)
            where_cords[0] += 2 * ShopItem.size[0] + start_cords[0]
            if (where_cords[0] + list(ShopItem.size)[0] + start_cords[0]) >= GameParams.size[0]:
                where_cords[0] = start_cords[0]
                where_cords[1] = where_cords[1] + start_cords[1] + list(ShopItem.size)[1]
        for item in self.shop_items:
            if item.name == "gray_back":
                item.bought = True
                item.chosen = True
                break

    def draw(self, screen):
        screen.blit(GameParams.menu_background, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        for shop_item in self.shop_items:
            shop_item.draw(screen)

        text = self.font.render(f"Cash: {self.player.cash}$", 1, (0, 0, 0))
        screen.blit(text, (550, 430))

    def check_pressed(self, events):
        pressed = None
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if cursor_in_rect(button.cords, pygame.mouse.get_pos(), button.size):
                        button.clicking = True
            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    if cursor_in_rect(button.cords, pygame.mouse.get_pos(), button.size) and button.clicking == True:
                        pressed = button.text
                        self.run = False
                    button.clicking = False
                for shop_item in self.shop_items:
                    if cursor_in_rect(shop_item.cords, pygame.mouse.get_pos(), shop_item.size):
                        shop_item.buy_or_choose(self.player, self.shop_items)
        return pressed

    def run_shop(self):
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
