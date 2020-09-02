import pygame
import sys
from actionfunctions import ActionFunctions
from card import CardsDatabase
from game_params import GameParams, cursor_in_rect
from menu import Button, GameButton, BetButton
import random
from dealerturn import DealerTurn
from counting import determine_score


class Stack:
    """
    :param player
    :type player - Player object
    """

    def __init__(self, player, stack_cords):
        self.player = player
        self.object = player.card_back
        self.stack_cords = stack_cords
        self.backs_cords = []
        self.update_stack_image = True
        self.update_object()
        self.left = 10

    def update_object(self):
        self.object = self.player.card_back

    def draw_first_time(self, cards_left):
        self.backs_cords = []
        for a in range(round(cards_left / self.left)):
            x = random.randint(-25, 25) + self.stack_cords[0]
            y = random.randint(-25, 25) + self.stack_cords[1]
            self.backs_cords.append((x, y))

    def draw(self, cards_left):
        for a in range(len(self.backs_cords) - int(cards_left / self.left)):
            self.backs_cords.pop()
        self.update_object()
        if self.left > cards_left > 0:
            self.backs_cords.append((self.stack_cords[0], self.stack_cords[1]))
        for cord in self.backs_cords:
            GameParams.screen.blit(self.object, cord)


class ChipStack(Stack):
    """

    """

    def __init__(self, player, stack_cords):
        super().__init__(player, stack_cords)
        self.object = player.chip.image
        self.left = 10

    def update_object(self):
        self.object = self.player.chip.image


class Game:
    """
    :param player
    :type player - Player object
    :param dealer
    :type dealer - Dealer object
    :param cards
    :type cards - AllCards object
    :param stack
    :type stack - Stack object
    """
    back_button_cords = (10, 10)
    cash_cords = (15, 80)
    bet_cords = (15, 110)
    cards_stack_cords = (
        GameParams.size[0] - 1.4 * CardsDatabase.size[0], GameParams.size[1] / 2 - 0.5 * CardsDatabase.size[1] - 20)
    chip_stack_cords = (0 + 30, GameParams.size[1] / 2 - 50)

    font = pygame.font.SysFont("comicsans", 33)

    resume_time = 0

    def __init__(self, player, dealer, all_cards):
        self.functions = ActionFunctions()
        self.resume_buttons = True
        self.dealer_turn = False
        self.moving_chips = []
        self.bet = 0
        self.player = player
        self.cards_stack = Stack(self.player, self.cards_stack_cords)
        self.chip_stack = ChipStack(self.player, self.chip_stack_cords)
        self.dealer = dealer
        self.all_cards = all_cards
        self.run = True

        self.buttons = []
        self.buttons.append(Button(self.back_button_cords, "Menu"))
        self.buttons.append(GameButton((10, 410), "Hit"))
        self.buttons.append(GameButton((120, 410), "Stay"))
        self.buttons.append(GameButton((120, 220), "Deal"))
        self.buttons.append(BetButton((10, 280), "Bet 10"))
        self.buttons.append(BetButton((120, 280), "Bet 50"))
        self.buttons.append(BetButton((10, 345), "Bet 100"))
        self.buttons.append(BetButton((120, 345), "All in"))

        self.player_cards_space = []
        self.dealer_cards_space = []
        self.load_card_spaces()

    def load_card_spaces(self):
        cords_dealer = [230, 10]
        cords_player = [230, 310]
        for a in range(8):
            self.player_cards_space.append(cords_player[:])
            self.dealer_cards_space.append(cords_dealer[:])
            cords_dealer[0] += 0.8 * CardsDatabase.size[0]
            cords_player[0] += 0.8 * CardsDatabase.size[0]

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
                        if button.text == "Menu":
                            self.run = False
                        else:
                            if isinstance(button, BetButton):
                                self.functions.actions["Bet"](self, pressed)
                            else:
                                self.functions.actions[pressed](self)
                    button.clicking = False
        return pressed

    def draw_player_cards(self):
        if self.player.card1 != 0 and self.player.card2 != 0:
            self.player.card1.draw()
            self.player.card2.draw()
            for card in self.player.additional_cards:
                card.draw()

    def draw_dealer_cards(self):
        if self.dealer.visible_card != 0:
            self.dealer.visible_card.draw()
            if self.dealer.hidden_card_is_visible:
                self.dealer.hidden_card.draw()
            else:
                self.dealer.hidden_card.draw(self.player.card_back)
            for card in self.dealer.additional_cards:
                card.draw()

    def draw_score(self):
        try:
            if self.dealer.hidden_card_is_visible:
                dealer_score = determine_score(
                    [self.dealer.visible_card, self.dealer.hidden_card] + self.dealer.additional_cards)
            else:
                dealer_score = determine_score([self.dealer.visible_card])
            player_score = determine_score([self.player.card1, self.player.card2] + self.player.additional_cards)
        except:
            dealer_score = 0
            player_score = 0
        dealer_score = self.font.render(f"Dealer score: {dealer_score}", 1, (0, 0, 0))
        player_score = self.font.render(f"Player score: {player_score}", 1, (0, 0, 0))
        GameParams.screen.blit(dealer_score, (540, 20))
        GameParams.screen.blit(player_score, (550, 440))

    def draw(self):
        GameParams.screen.blit(GameParams.game_background, (0, 0))  # Background

        cash = self.font.render(f"Cash: {self.player.cash}$", 1, (0, 0, 0))  # Bet and cash text
        bet = self.font.render(f"Bet: {self.bet}$", 1, (0, 0, 0))
        GameParams.screen.blit(cash, self.cash_cords)
        GameParams.screen.blit(bet, self.bet_cords)

        for button in self.buttons:  # Buttons
            button.draw(GameParams.screen)

        self.cards_stack.draw(self.all_cards.cards_counter)  # Stack image
        self.chip_stack.draw(self.player.cash)

        for chip in self.moving_chips:
            chip.draw()

        self.draw_player_cards()
        self.draw_dealer_cards()
        self.draw_score()

    def reset(self):
        self.bet = 0
        self.player.reset()
        self.dealer.reset()
        self.functions.reset()
        self.moving_chips = []

    def run_game(self):
        self.all_cards.reset()
        button_text = None
        self.reset()
        self.run = True
        self.cards_stack.draw_first_time(self.all_cards.cards_counter)
        self.chip_stack.draw_first_time(self.player.cash)
        while self.run:
            GameParams.clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.dealer_turn:
                DealerTurn.turn(self)
            if self.resume_buttons:
                button_text = self.check_pressed(events)
            self.draw()
            pygame.display.update()
        return button_text
