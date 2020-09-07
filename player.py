import card
import pygame
import math
from game_params import GameParams

class Chip:
    image = pygame.image.load("./rest/pokerchip.png")
    image.convert_alpha()
    vel = [0, 0]
    base_vel = 9

    def __init__(self, cords, final_cords):
        self.cords = cords
        self.final_cords = final_cords
        self.vel_determined = False

    def draw(self, image=0):
        if image == 0:
            image = self.image
        if not self.vel_determined:
            self.determine_vel()
        if self.cords[0] + self.vel[0] >= self.final_cords[0]:
            self.cords = self.final_cords
        else:
            self.cords[0] += self.vel[0]
            self.cords[1] += self.vel[1]
        GameParams.screen.blit(image, tuple(self.cords))

    def determine_vel(self):
        alfa = math.atan((self.final_cords[1] - self.cords[1]) / (self.final_cords[0] - self.cords[0]))
        self.vel[0] = self.base_vel * math.cos(alfa)
        self.vel[1] = self.base_vel * math.sin(alfa)
        self.vel_determined = True

class Player:
    """

    """

    def __init__(self, cash=500):
        self.card1 = 0
        self.card2 = 0
        self.cash = cash
        self.additional_cards = []
        self.card_back = card.CardsDatabase.backs["gray_back"]
        self.chip = Chip([-100, -100], [-100, -100])

    def reset(self):
        self.card1 = 0
        self.card2 = 0
        self.additional_cards = []
