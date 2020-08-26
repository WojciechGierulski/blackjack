import pygame
import random
from game_params import GameParams
import counting
from player import Chip


class ActionFunctions:
    """

    """
    dealed = True
    able_to_hit = False
    able_to_stay = False
    able_to_bet = True

    font = pygame.font.SysFont("comicsans", 70, True)

    def reset(self):
        self.dealed = True
        self.able_to_hit = False
        self.able_to_stay = False
        self.able_to_bet = True

    def draw_caption(self, game, text, seconds=1.5, reset=False):
        game.resume_buttons = False
        text1 = self.font.render(text, 1, (0, 0, 255))
        game.captions.append([text1, (int(
            GameParams.size[0] / 2 - text1.get_width() / 2),
                                      int(GameParams.size[1] / 2) - text1.get_height() / 2),
                              (60 * seconds), reset])

    def bet(self, game, value):
        if self.able_to_bet:
            self.dealed = False
            game.chip_stack.update_stack_image = True
            if value == "All in":
                value = game.player.cash
            else:
                value = int(value[4:])
            if game.player.cash - value >= 0: # Able to bet amount of cash
                game.bet += value
                game.player.cash -= value
                # Add moving chip
                i = int(int(value)/10)
                for a in range(i):
                    x = random.randint(230, 510)
                    y = random.randint(180, 200)
                    game.moving_chips.append(Chip(list(game.chip_stack.backs_cords[-1]), [x, y]))
                    game.chip_stack.backs_cords.pop()

    def bust(self, game, seconds=1.5):
        self.draw_caption(game, "BUST!", seconds, True)

    def blackjack(self, game, seconds=1.5):
        self.draw_caption(game, "BLACKJACK!", seconds, True)
        game.player.cash += game.bet * 2.5

    def hit(self, game):
        print(game.all_cards.cards_counter)
        if self.able_to_hit:
            game.cards_stack.update_stack_image = True
            game.player.additional_cards.append(game.all_cards.draw_card(game))
            game.player.additional_cards[-1].final_cords = game.player_cards_space[self.player_card_nr]
            self.player_card_nr += 1
            score = counting.determine_score([game.player.card1, game.player.card2] + game.player.additional_cards)
            if score > 21:
                self.bust(game)
            elif score == 21:
                self.blackjack(game)

    def stay(self, game):
        if self.able_to_stay:
            self.able_to_hit = False
            self.able_to_stay = False
            game.dealer_turn = True

    def deal(self, game):
        if not self.dealed:
            game.player.additional_cards = []

            self.dealed = True
            self.able_to_hit = True
            self.able_to_stay = True
            self.able_to_bet = False

            self.player_card_nr = 0
            self.dealer_card_nr = 0

            game.cards_stack.update_stack_image = True
            # Player draw
            game.player.card1 = game.all_cards.draw_card(game)
            game.player.card2 = game.all_cards.draw_card(game)
            game.player.card1.final_cords = game.player_cards_space[self.player_card_nr]
            self.player_card_nr += 1
            game.player.card2.final_cords = game.player_cards_space[self.player_card_nr]
            self.player_card_nr += 1
            # Dealer draw
            game.dealer.draw_2_cards(game.all_cards, game)
            game.dealer.visible_card.final_cords = game.dealer_cards_space[self.dealer_card_nr]
            self.dealer_card_nr += 1
            game.dealer.hidden_card.final_cords = game.dealer_cards_space[self.dealer_card_nr]
            self.dealer_card_nr += 1

            if counting.determine_score([game.player.card1, game.player.card2]) == 21:
                self.blackjack(game, 3)

    def __init__(self):
        self.actions = {"Hit": self.hit, "Stay": self.stay, "Deal": self.deal, "Bet": self.bet}
        self.player_card_nr = 0
        self.dealer_card_nr = 0
