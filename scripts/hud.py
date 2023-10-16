import pygame as pg
from assets import *
from ui import draw_text
from settings import *
from colors import *

class HUD():
    def __init__(self, game, main, level, sprites):
        self.game = game
        self.main = main
        self.level = level
        self.sprites = sprites
    
    def draw_time(self):
        hud_rect = CLOCK_HUD.get_rect()
        hud_rect.topleft = (620, 30)
        self.main.screen.blit(CLOCK_HUD, hud_rect)
        if int(self.level.clock.timer) <= 10:
            color = RED
        else:
            color = WHITE
        time = f"{(int(self.level.clock.timer/60))}:{int(self.level.clock.timer)%60:02d}"
        # draw_text(self.main, str("{:.1f}".format(self.level.clock.timer)), LCD_FONT, 25, 700, 55, color=color, align="center")
        draw_text(self.main, time, LCD_FONT, 25, 700, 55, color=color, align="center")

    def draw_lives(self):
        if self.sprites.player.lives == 3:
            hud = PLAYER_LIVES[3]
        if self.sprites.player.lives == 2:
            hud = PLAYER_LIVES[2]
        if self.sprites.player.lives == 1:
            hud = PLAYER_LIVES[1]
        if self.sprites.player.lives <= 0 or self.sprites.player.lives > 3:
            hud = PLAYER_LIVES[0]

        hud_rect = hud.get_rect()
        hud_rect.bottomright = (WIDTH - 20, HEIGHT - 20)
        self.main.screen.blit(hud, hud_rect)

    def draw_score(self):
        hud_rect = SCORE_HUD.get_rect()
        hud_rect.topright = (250, 30)
        self.main.screen.blit(SCORE_HUD, hud_rect)
        if int(self.sprites.player.total) == int(self.level.sum):
            color = GREEN
        else:
            color = WHITE
        draw_text(self.main, str(f"{self.sprites.player.total}"), LCD_FONT, 35, 175, 63, color=color, align="e")

    def draw_sign(self):
        sign = self.sprites.player.current_sign
        hud = SIGN_HUD[sign]
        hud_rect = hud.get_rect()
        hud_rect.topright = (250, 30)
        self.main.screen.blit(hud, hud_rect)

    def draw_objective(self):
        hud_rect = OBJECTIVE_HUD.get_rect()
        hud_rect.topleft = (20, 550)
        self.main.screen.blit(OBJECTIVE_HUD, hud_rect)
        if int(self.sprites.player.total) == int(self.level.sum):
            color = GREEN
        else:
            color = RED
        draw_text(self.main, "Objective", UNDERTALE_FONT, 12, 30, 560, align="w")
        draw_text(self.main, str(self.level.sum), LCD_FONT, 25, 155, 593, color=color, align="e")
    
    def draw_no_key(self):
        if self.sprites.player.on_finish:
            draw_text(self.game.main, "You don't have the key!", UNDERTALE_FONT, 50, WIDTH/2, HEIGHT/2, color=RED, align="center")

    def draw_tip(self):
        if self.game.sprites.has_tips:
            self.game.sprites.tip_text.show()

    def draw_hud(self):
        self.draw_no_key()
        self.draw_tip()
        self.draw_time()
        self.draw_lives()
        self.draw_score()
        self.draw_sign()
        self.draw_objective()