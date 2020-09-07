import pygame
import os
import random
from game_params import GameParams
import copy
import math


class CardsDatabase:
    """

    """
    cards = {}
    path = "cards"
    size = (80, 160)
    for filename in os.listdir(path):
        cards[filename[:-4]] = pygame.image.load(f"./{path}/{filename}")
        cards[filename[:-4]].convert_alpha()
        cards[filename[:-4]] = pygame.transform.scale(cards[filename[:-4]], size)

    backs = {}
    for filename in os.listdir("backs"):
        backs[filename[:-4]] = pygame.image.load(f"./backs/{filename}")
        backs[filename[:-4]] = pygame.transform.scale(backs[filename[:-4]], size)


class Card:
    """
    :param name
    :param img
    :param value
    """
    figures = ["A", "K", "Q", "J"]
    base_vel = 11

    def __init__(self, name):
        self.ready = False
        self.vel_determined = False
        self.vel = [0, 0]
        self.cords = [0, 0]
        self.final_cords = [0, 0]
        self.name = name
        self.image = CardsDatabase.cards[name]
        if self.name[0] in Card.figures:
            if self.name[0] == "A":
                self.value = 11
            else:
                self.value = 10
        else:
            self.value = int(self.name[:-1])

    def draw(self, image=0):
        if image == 0:
            image = self.image
        if not self.vel_determined:
            self.determine_vel()
        if self.cords[0] + self.vel[0] <= self.final_cords[0]:
            self.cords = self.final_cords
        else:
            self.cords[0] += self.vel[0]
            self.cords[1] += self.vel[1]
        GameParams.screen.blit(image, tuple(self.cords))

    def determine_vel(self):
        alfa = math.atan((self.final_cords[1] - self.cords[1]) / (self.final_cords[0] - self.cords[0]))
        self.vel[0] = -1 * self.base_vel * math.cos(alfa)
        self.vel[1] = -1 * self.base_vel * math.sin(alfa)
        self.vel_determined = True

class AllCards:
    """
    :param cards - actual cards in deck
    :type cards - dict {name : [CardObject, quantity]}
    """

    def __init__(self, decks_nr=4):
        self.decks_nr = decks_nr
        self.cards = {}
        self.cards_counter = None
        self.load_cards()

    def remove_card(self, name):
        if self.cards[name][1] >= 1:
            self.cards[name][1] -= 1
            self.cards_counter -= 1

    def load_cards(self):
        self.cards_counter = self.decks_nr * 52
        for name in CardsDatabase.cards:
            self.cards[name] = [Card(name), self.decks_nr]

    def reshuffle(self, game):
        game.functions.draw_caption(game, "Reshuffle", 2)
        cards = []
        cards.append(game.player.card1)
        cards.append(game.player.card2)
        cards.append(game.dealer.visible_card)
        cards.append(game.dealer.hidden_card)
        cards = cards + game.player.additional_cards + game.dealer.additional_cards
        self.reset()
        self.cards_counter -= len(cards)
        for card in cards:
            if card != 0:
                self.remove_card(card.name)
        game.cards_stack.draw_first_time(self.cards_counter)

    def draw_card(self, game):
        if self.cards_counter == 1:
            self.reshuffle(game)
        choose = True
        while choose:
            name, value = random.choice(list(self.cards.items()))
            if value[1] >= 1:
                self.remove_card(name)
                choose = False
                value[0].cords = list(game.cards_stack_cords)
                return copy.copy(value[0])

    def reset(self):
        self.cards_counter = self.decks_nr * 52
        for card in self.cards.values():
            card[1] = self.decks_nr
