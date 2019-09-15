import pygame
from pygame import *
from layout.layout import Layout


def pg_print_message(
        layout: Layout,
        message,
        x,
        y,
        sys_font="TO DEFINE A FONT",
        bold=True,
        size=32,
        color_fg=(237, 210, 36),
        color_bg=(0, 0, 0),
        alias=8,
        offset=4
):
    size = int(round((layout.w / 1280) * (size / 32) * 32))

    my_font = pygame.font.SysFont(sys_font, size)
    my_font.set_bold(bold)
    text = my_font.render(message, alias, color_bg)
    layout.screen_game.blit(text, (x + offset, y + offset))
    layout.screen_game.blit(text, (x - offset, y - offset))
    layout.screen_game.blit(text, (x + offset, y - offset))
    layout.screen_game.blit(text, (x - offset, y + offset))
    text = my_font.render(message, alias, color_fg)
    layout.screen_game.blit(text, (x, y))
