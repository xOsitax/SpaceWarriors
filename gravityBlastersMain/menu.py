import pygame
import sys


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.screen_width / 2, self.game.screen_width / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 75

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.screen.blit(self.game.screen, (0, 0))
        pygame.display.flip()
        #self.game.reset_keys()


'''class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Singleplayer"
        self.singleplayerx, self.singleplayery = self.mid_w, self.mid_h + 30
        self.multiplayerx, self.multiplayery = self.mid_w, self.mid_h + 55
        self.leaderboardx, self.leaderboardy = self.mid_w, self.mid_h + 80
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 105
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 130

        self.cursor_rect.midtop = (self.singleplayerx + self.offset, self.singleplayery)

    def display_menu(self):
        self.game.screen.fill((0, 0, 0))
        self.game.draw_text('Space Warriors', 50, self.game.screen_width / 2, self.game.screen_height / 2 - 40)
        self.game.draw_text("Singleplayer", 20, self.singleplayerx, self.singleplayery)
        self.game.draw_text("Multiplayer", 20, self.multiplayerx, self.multiplayery)
        self.game.draw_text("Leaderboards", 20, self.leaderboardx, self.leaderboardy)
        self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
        self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)

        self.draw_cursor()
        self.blit_screen()

    def update(self):
        for self.game.event in pygame.event.get():
            if self.game.event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game.event.type == pygame.KEYDOWN:
                if self.game.event.key == pygame.K_SPACE:
                    if self.state == 'Singleplayer':
                        self.game.state = 'singlePlayer'
                    elif self.state == 'Multiplayer':
                        self.game.state = 'multiPlayer'
                    elif self.state == 'Leaderboards':
                        self.game.state = 'leaderboard'
                    elif self.state == 'Options':
                        self.game.state = 'options'
                    elif self.state == 'Credits':
                        self.game.state = 'credits'
            elif self.game.event.key == pygame.K_DOWN:
                if self.state == 'Singleplayer':
                    self.cursor_rect.midtop = (self.multiplayerx + self.offset, self.multiplayery)
                    self.state = 'Multiplayer'
                elif self.state == 'Multiplayer':
                    self.cursor_rect.midtop = (self.leaderboardx + self.offset, self.leaderboardy)
                    self.state = 'Leaderboards'
                elif self.state == 'Leaderboards':
                    self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                    self.state = 'Options'
                elif self.state == 'Options':
                    self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                    self.state = 'Credits'
                elif self.state == 'Credits':
                    self.cursor_rect.midtop = (self.singleplayerx + self.offset, self.singleplayery)
                    self.state = 'Singleplayer'
            elif self.game.event.key == pygame.K_UP:
                if self.state == 'Singleplayer':
                    self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                    self.state = 'Credits'
                elif self.state == 'Multiplayer':
                    self.cursor_rect.midtop = (self.singleplayerx + self.offset, self.singleplayery)
                    self.state = 'Singleplayer'
                elif self.state == 'Leaderboards':
                    self.cursor_rect.midtop = (self.multiplayerx + self.offset, self.multiplayery)
                    self.state = 'Multiplayer'
                elif self.state == 'Options':
                    self.cursor_rect.midtop = (self.leaderboardx + self.offset, self.leaderboardy)
                    self.state = 'Leaderboards'
                elif self.state == 'Credits':
                    self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                    self.state = 'Options'
'''

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.screen_width / 2, self.game.screen_height / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.state = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class Multiplayer(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Player Selection'
        self.p1x, self.p1y = self.mid_w - 200, self.mid_h + 20
        self.p2x, self.p2y = self.mid_w + 200, self.mid_h + 20
        self.cursor_rect.midtop = (self.p1x + self.offset, self.p1y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Ready?', 20, self.game.screen_width / 2, self.game.screen_height / 2 - 30)
            self.game.draw_text("Player 1", 15, self.p1x, self.p1y)
            self.game.draw_text("Player 2", 15, self.p2x, self.p2y)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.state = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Player 1':
                self.state = 'Unready'
                self.cursor_rect.midtop = (self.p1x + self.offset, self.p1y)
            elif self.state == 'Player 2':
                self.state = 'Unready'
                self.cursor_rect.midtop = (self.p2x + self.offset, self.p2y)
        elif self.game.START_KEY:
            self.state = 'Ready'
            # Start the multiplayer game
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.state = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.screen_width / 2, self.game.screen_height / 2 - 20)
            self.game.draw_text('Made by Phil,  Luis,  Rutva,  and Yessenia', 15, self.game.screen_width / 2,
                                self.game.screen_height / 2 + 10)
            self.blit_screen()


class Leaderboard(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.state = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Leaderboard', 20, self.game.screen_width / 2, self.game.screen_height / 2 - 20)
            self.game.draw_text('Top Scores:', 15, self.game.screen_width / 2, self.game.screen_height / 2 + 10)
            self.game.draw_text(str(self.game.initial) + "........." + str(self.game.hs), 22, self.game.screen_width / 2,
                                self.game.screen_height / 2 + 45)
            self.blit_screen()
