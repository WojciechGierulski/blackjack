import counting


class DealerTurn:
    cooldown = 60
    @staticmethod
    def turn(game):
        if DealerTurn.cooldown <= 0:
            DealerTurn.cooldown = 60
            if game.dealer.hidden_card_is_visible:
                next_action = game.dealer.check_what(game)
                if next_action == "Dealer_stay":
                    DealerTurn.resolve_game(game)
                elif next_action == "Dealer_hit":
                    game.dealer.additional_cards.append(game.all_cards.draw_card(game))
                    game.dealer.additional_cards[-1].final_cords = game.dealer_cards_space[game.functions.dealer_card_nr]
                    game.functions.dealer_card_nr += 1
                elif next_action == "Dealer_bust":
                    DealerTurn.resolve_game(game)
            else:
                game.dealer.hidden_card_is_visible = True
        else:
            DealerTurn.cooldown -= 1

    @staticmethod
    def resolve_game(game):
        player_score = counting.determine_score([game.player.card1, game.player.card2] + game.player.additional_cards)
        dealer_score = counting.determine_score(
            [game.dealer.hidden_card, game.dealer.visible_card] + game.dealer.additional_cards)
        if player_score == dealer_score:
            game.wait_for_button("Draw!")
            game.player.cash += game.bet
            game.dealer_turn = False
            game.reset()
        elif player_score > dealer_score or dealer_score > 21:
            game.wait_for_button("You win!")
            game.player.cash += 2 * game.bet
            game.dealer_turn = False
            game.reset()
        else:
            game.wait_for_button("You lose!")
            game.dealer_turn = False
            game.reset()
