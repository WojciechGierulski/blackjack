import pygame
class GameParams:
    size = (720, 480)
    name = "BlackJack"
    icon_path = "./backgrounds/icon.png"
    screen = pygame.display.set_mode(size)
    icon = pygame.image.load(icon_path)
    pygame.display.set_caption(name)
    pygame.display.set_icon(icon)

    game_bg_path = "./backgrounds/game_background.jpg"
    menu_bg_path = "./backgrounds/menu_background.jpg"
    black_jack_path = "./backgrounds/black_jack.jpg"

    game_background = pygame.image.load(game_bg_path)
    game_background = pygame.transform.scale(game_background, size)

    blackjack_caption = pygame.image.load(black_jack_path)
    blackjack_caption = pygame.transform.scale(blackjack_caption, (300, 130))

    menu_background = pygame.image.load(menu_bg_path)
    menu_background = pygame.transform.scale(menu_background, size)

    clock = pygame.time.Clock()


def cursor_in_rect(self_cords, mouse_cords, self_size):
    if mouse_cords[0] > self_cords[0] and (mouse_cords[0] < self_cords[0] + self_size[0]):
        if mouse_cords[1] > self_cords[1] and (mouse_cords[1] < self_cords[1] + self_size[1]):
            return True
        else:
            return False
    else:
        return False
