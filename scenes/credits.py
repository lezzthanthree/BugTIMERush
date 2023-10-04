import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text
from scenes import gameover

class Credits():
    def __init__(self, main):
        self.main = main

        self.delay = 60 / 127 / 0.125
        self.beat = 0
        self.offset = 0

        self.rolling = True

        pg.mixer.music.load(CREDITS)
        self.start()

    def start(self):
        pg.mixer.music.play(loops=-1)
        self.rolling = True
        while self.rolling:
            self.check_beat()
            self.draw()
            self.events()
        self.main.scene.set_scene('gameover')

        
    def events(self):
        self.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.rolling:
                    self.beat = 13
                    self.draw_credits()
                    self.rolling = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.main.quit()
                    return
                if event.key == pg.K_SPACE:
                    if self.rolling:
                        self.beat = 13
                        self.draw_credits()
                        self.rolling = False

    def check_beat(self):
        next_beat = (pg.mixer.music.get_pos()/1000) > ((self.beat) * self.delay)
        if next_beat and self.beat < 13:
            self.beat += 1
            self.draw_credits()

    def draw_credits(self):
        if self.beat == 1:
            self.main.screen.fill(BLACK)
            title = TITLE_LOGO[0]
            title_rect = title.get_rect()
            title_rect.center = ((WIDTH/2), (HEIGHT/2))
            self.main.screen.blit(title, title_rect)
        if self.beat == 2:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "by", UNDERTALE_FONT, 20, WIDTH/2, HEIGHT/2 - 50, align="center")
            draw_text(self.main, "Sleepy Developers", UNDERTALE_FONT, 40, WIDTH/2, HEIGHT/2, align="center")
        if self.beat == 3:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "in partial fulfillment of the", UNDERTALE_FONT, 20, WIDTH/2, HEIGHT/2 - 75, align="center")
            draw_text(self.main, "course requirement in", UNDERTALE_FONT, 20, WIDTH/2, HEIGHT/2 - 50, align="center")
            draw_text(self.main, "Discrete Structures 2", UNDERTALE_FONT, 50, WIDTH/2, HEIGHT/2, align="center")
        if self.beat == 4:
            self.main.screen.fill(BLACK)
            dog_rect = DOG.get_rect()
            dog_rect.center = ((WIDTH/2), (HEIGHT/2))
            self.main.screen.blit(DOG, dog_rect)
        if self.beat == 5:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Sprite Design", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 40, align="w", color=YELLOW)
            draw_text(self.main, "Nykky Gatulayao", UNDERTALE_FONT, 30, 130, HEIGHT/2, align="w")
            draw_text(self.main, "Adrian Abelligos", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 40, align="w")
        if self.beat == 6:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Level Design", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 20, align="w", color=YELLOW)
            draw_text(self.main, "Carlo Agas", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 20, align="w")
        if self.beat == 7:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Programmers", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 20, align="w", color=YELLOW)
            draw_text(self.main, "Smilie Pop", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 20, align="w")
        if self.beat == 8:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Technicals and Papers", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 40, align="w", color=YELLOW)
            draw_text(self.main, "Mark Vincent Caspe", UNDERTALE_FONT, 30, 130, HEIGHT/2, align="w")
            draw_text(self.main, "Randolph Larano", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 40, align="w")
        if self.beat == 9:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Music (from UNDERTALE)", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 120, align="w", color=YELLOW)
            draw_text(self.main, "Once Upon A Time", UNDERTALE_FONT, 30, 130, HEIGHT/2 - 80, align="w")
            draw_text(self.main, "Start Menu", UNDERTALE_FONT, 30, 130, HEIGHT/2 - 40, align="w")
            draw_text(self.main, "CORE", UNDERTALE_FONT, 30, 130, HEIGHT/2, align="w")
            draw_text(self.main, "Can You Really Call This A Hotel", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 40, align="w")
            draw_text(self.main, "I Didn't Receive A Mint On", UNDERTALE_FONT, 30, 160, HEIGHT/2 + 80, align="w")
            draw_text(self.main, "My Pillow Or Anything", UNDERTALE_FONT, 30, 160, HEIGHT/2 + 120, align="w")
        if self.beat == 10:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Sounds", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 60, align="w", color=YELLOW)
            draw_text(self.main, "UNDERTALE", UNDERTALE_FONT, 30, 130, HEIGHT/2 - 20, align="w")
            draw_text(self.main, "Needy Streamer Overload", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 20, align="w")
            draw_text(self.main, "Touhou", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 60, align="w")
        if self.beat == 11:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Art Credits", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 80, align="w", color=YELLOW)
            draw_text(self.main, "Ansimuz", UNDERTALE_FONT, 30, 130, HEIGHT/2 - 40, align="w")
            draw_text(self.main, "Buch", UNDERTALE_FONT, 30, 130, HEIGHT/2, align="w")
            draw_text(self.main, "Emcee Flesher", UNDERTALE_FONT, 30, 130, HEIGHT/2 +  40, align="w")
            draw_text(self.main, "Pupkin", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 80, align="w")
        if self.beat == 12:
            self.main.screen.fill(BLACK)
            draw_text(self.main, "Game Inspirations", UNDERTALE_FONT, 30, 80, HEIGHT/2 - 60, align="w", color=YELLOW)
            draw_text(self.main, "UNDERTALE", UNDERTALE_FONT, 30, 130, HEIGHT/2 - 20, align="w")
            draw_text(self.main, "Portal", UNDERTALE_FONT, 30, 130, HEIGHT/2 + 20, align="w")
            draw_text(self.main, "Needy Streamer Overload", UNDERTALE_FONT, 30, 130, HEIGHT/2 +  60, align="w")
        if self.beat > 12:
            self.rolling = False
            TADA.play()

            self.main.screen.fill(BLACK)
            bg_rect = CONGRATS_BG.get_rect()
            bg_rect.topleft = (0, 0)
            self.main.screen.blit(CONGRATS_BG, bg_rect)

            draw_text(self.main, "From the developers: ", UNDERTALE_FONT, 20, 265, 180, align="nw", color=GREY)
            draw_text(self.main, "Hey, congrats!", UNDERTALE_FONT, 34, 263, 200, align="nw", color=GREY)

            draw_text(self.main, "Math is one of the hardest game", UNDERTALE_FONT, 15, 265, 250, align="nw", color=GREY)
            draw_text(self.main, "concepts when it comes to", UNDERTALE_FONT, 15, 265, 265, align="nw", color=GREY)
            draw_text(self.main, "puzzles.", UNDERTALE_FONT, 15, 265, 280, align="nw", color=GREY)
            draw_text(self.main, "If you have reached this", UNDERTALE_FONT, 15, 265, 300, align="nw", color=GREY)
            draw_text(self.main, "message, we wanted to say,", UNDERTALE_FONT, 15, 265, 315, align="nw", color=GREY)
            draw_text(self.main, "we are so proud of you to play", UNDERTALE_FONT, 15, 265, 330, align="nw", color=GREY)
            draw_text(self.main, "this game until the very end.", UNDERTALE_FONT, 15, 265, 345, align="nw", color=GREY)
            draw_text(self.main, "Thanks for playing!", UNDERTALE_FONT, 15, 265, 375, align="nw", color=GREY)
            draw_text(self.main, "Press SPACE", UNDERTALE_FONT, 20, WIDTH/2, 430, align="center", color=GREY)

            pg.display.flip()
            self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.main.clock.tick(FRAMES)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False
                        return

    def draw(self):
        pg.display.flip() 