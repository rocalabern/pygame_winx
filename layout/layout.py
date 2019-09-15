import warnings

import pygame


class Layout:
    def __init__(
            self,
            screen_desktop: pygame.Surface,
            game_w: int = 4*1280,
            game_h: int = 4*720,
            debug: bool = True,
            allow_rescale: bool = True
    ):
        self.screen_desktop = screen_desktop
        # self.info_display = pygame.display.Info()
        # self.desktop_w = self.info_display.current_w
        # self.desktop_h = self.info_display.current_h
        self.screen_desktop_rect = self.screen_desktop.get_rect()
        self.desktop_w = self.screen_desktop_rect.width
        self.desktop_h = self.screen_desktop_rect.height

        self.game_aspect_ratio = game_w / game_h
        self.screen_game = pygame.Surface((game_w, game_h))
        self.screen_game_rect = self.screen_game.get_rect()
        self.game_w = game_w
        self.game_h = game_h

        if self.game_aspect_ratio < self.desktop_w / self.desktop_h:
            self.w = int(round(self.game_aspect_ratio * self.desktop_h))
            self.h = int(round(self.desktop_h))
            self.x_offset = int((self.desktop_w - self.w) / 2)
            self.y_offset = 0
            if debug:
                print("Max axis : height")
        else:
            self.w = int(round(self.desktop_w))
            self.h = int(round(self.desktop_w / self.game_aspect_ratio))
            self.x_offset = 0
            self.y_offset = int((self.desktop_h - self.h) / 2)
            if debug:
                print("Max axis : with")
        if not allow_rescale and self.w >= self.game_w and self.h >= self.game_h:
            self.allow_rescale = False
            self.w = self.game_w
            self.h = self.game_h
            self.x_offset = int((self.desktop_w - self.w) / 2)
            self.y_offset = int((self.desktop_h - self.h) / 2)
        else:
            self.allow_rescale = True
            warnings.warn('We must to rescale, resolution not enough')

        if debug:
            print("aspect_ratio : " + str(self.game_aspect_ratio))
            print("screen : " + str(self.w) + " x " + str(self.h))
            print("offset : " + str(self.x_offset) + " , " + str(self.y_offset))

    def position_desktop(self, x=0.5, y=0.5):
        factor_x = x * self.w
        factor_y = y * self.h
        pos_x = int(round(self.x_offset + factor_x))
        pos_y = int(round(self.y_offset + factor_y))
        return pos_x, pos_y

    def position_game(self, x=0.5, y=0.5):
        factor_x = x * self.game_w
        factor_y = y * self.game_h
        pos_x = int(round(0 + factor_x))
        pos_y = int(round(0 + factor_y))
        return pos_x, pos_y

    def update(self, rect:pygame.Rect = None, zoom: float = 1.0):
        if self.allow_rescale:
            if rect is not None:
                perc_x = (rect.left + rect.width / 2) / self.game_w
                perc_y = (rect.top + rect.height / 2) / self.game_h
                scaled_screen = pygame.transform.scale(self.screen_game, (int(round(zoom*(self.w+1))), int(round(zoom*(self.h+1)))))
                x_offset = int(round(self.x_offset + self.w/2 - perc_x * zoom * self.w))
                y_offset = int(round(self.x_offset + self.h/2 - perc_y * zoom * self.h))
                x_offset = max(min(x_offset, 0), - scaled_screen.get_width() + self.desktop_w)
                y_offset = max(min(y_offset, 0), - scaled_screen.get_height() + self.desktop_h)
                self.screen_desktop.blit(scaled_screen, (x_offset, y_offset))
                scaled_screen = pygame.transform.scale(self.screen_game, (320, 180))
                self.screen_desktop.blit(scaled_screen, (0, 0))
            else:
                scaled_screen = pygame.transform.scale(self.screen_game, (self.w+1, self.h+1))
                self.screen_desktop.blit(scaled_screen, (self.x_offset, self.y_offset))
        else:
            self.screen_desktop.blit(self.screen_game, (self.x_offset, self.y_offset))
        pygame.display.update()
