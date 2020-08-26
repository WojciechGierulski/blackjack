import counting


class DealerTurn:
    @staticmethod
    def turn(game):
        if len(game.captions) == 0:
            if game.dealer.hidden_card_is_visible:
                next_action = game.dealer.check_what(game)
                if next_action == "Dealer_stay":
                    DealerTurn.resolve_game(game)
                elif next_action == "Dealer_hit":
                    game.functions.draw_caption(game, "Dealer hits", 2, False)
                    game.dealer.additional_cards.append(game.all_cards.draw_card(game))
                    game.dealer.additional_cards[-1].final_cords = game.dealer_cards_space[game.functions.dealer_card_nr]
                    game.functions.dealer_card_nr += 1
                elif next_action == "Dealer_bust":
                    game.functions.draw_caption(game, "Dealer busts", 2, False)
                    DealerTurn.resolve_game(game)
            else:
                game.functions.draw_caption(game, "", 1, False)
                game.dealer.hidden_card_is_visible = True


    @staticmethod
    def resolve_game(game):
        player_score = counting.determine_score([game.player.card1, game.player.card2] + game.player.additional_cards)
        dealer_score = counting.determine_score(
            [game.dealer.hidden_card, game.dealer.visible_card] + game.dealer.additional_cards)
        if player_score == dealer_score:
            game.player.cash +=  game.bet
            game.dealer_turn = False
            game.functions.draw_caption(game, "Draw", 2, True)
        elif player_score > dealer_score or dealer_score > 21:
            game.player.cash += 2 * game.bet
            game.dealer_turn = False
            game.functions.draw_caption(game, "You win", 2, True)
        else:
            game.functions.draw_caption(game, "Dealer wins", 2, True)
            game.dealer_turn = False
