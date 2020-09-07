def check_for_aces(cards):
        value = 0
        for card in cards:
            if card.name[0] == "A":
                value += 1
        return value


def count_score(cards):
        score = 0
        for card in cards:
                score += card.value
        return score


def determine_score(cards):
    if 0 not in cards:
        score = count_score(cards)
        if score <= 21:
            return score
        else:
            aces = check_for_aces(cards)
            if aces == 0:
                return score
            else:
                while score > 21 and aces > 0:
                    aces -= 1
                    score -= 10
            return score
    else:
        return 0


def count_scores(game):
    if game.functions.dealed:
        player_score = determine_score(game.player.additional_cards + [game.player.card2, game.player.card1])
        if not game.dealer.hidden_card_is_visible:
            dealer_score = determine_score([game.dealer.visible_card])
        else:
            dealer_score = determine_score(
                [game.dealer.visible_card, game.dealer.hidden_card] + game.dealer.additional_cards)
    else:
        player_score = 0
        dealer_score = 0
    return player_score, dealer_score
