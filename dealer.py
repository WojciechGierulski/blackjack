import pygame
from card import Card
import copy
from counting import determine_score

class Dealer:
    """
    :param hidden/visible card
    :type hidden/visible card - Card object
    :param additional_cards
    :type additional_cards - Card objects list []
    :param max_score - min score when not drawing next card
    :type max_score - int
    """
    def __init__(self, cash=10000, min=17):
        self.hidden_card_is_visible = False
        self.cash = cash
        self.min_score = min
        self.hidden_card = 0
        self.visible_card = 0
        self.additional_cards = []

    def draw_2_cards(self, cards, game):
        # cards is AllCard object
        self.hidden_card = copy.copy(cards.draw_card(game))
        self.visible_card = copy.copy(cards.draw_card(game))

    def check_what(self, game):
        # cards is AllCard object
        cards = [self.visible_card, self.hidden_card] + self.additional_cards
        score = determine_score(cards)
        if score <= 21:
            player_score = determine_score([game.player.card1, game.player.card2] + game.player.additional_cards)
            if score >= self.min_score:
                if score >= player_score:
                    return "Dealer_stay"
                elif score < player_score:
                    return "Dealer_hit"
            else:
                return "Dealer_hit"
        else:
            return "Dealer_bust"

    def reset(self):
        self.hidden_card = 0
        self.visible_card = 0
        self.additional_cards = []
        self.hidden_card_is_visible = False
