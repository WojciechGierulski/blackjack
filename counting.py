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
