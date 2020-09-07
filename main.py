import pygame
pygame.init()
from game_params import GameParams
from game import Game, ActionFunctions
from player import Player
from dealer import Dealer
from card import AllCards, Card, CardsDatabase
from menu import Menu
from shop import Shop

player1 = Player()
dealer1 = Dealer()
cards = AllCards(1)

menu1 = Menu()
shop1 = Shop(player1)
shop1.load_shop_items()

game1 = Game(player1, dealer1, cards)

what_next = menu1.run_menu()
run = True
while run:
    if what_next == "Quit":
        run = False
    if what_next == "Play":
        what_next = game1.run_game()
    if what_next == "Shop":
        what_next = shop1.run_shop()
    if what_next == "Menu":
        what_next = menu1.run_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
