import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text
from scenes import title
from random import randint

characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{};:,.? "

class GameOver():
    def __init__(self, main, reason):
        pg.mixer.stop()
        pg.mixer.music.stop()

        self.main = main
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.reason = reason
        self.string = ""
        self.start()

    def start(self):
        BSOD.play(loops=-1)
        self.playing = True
        while self.playing:
            self.update()
            self.draw()
            self.events()
            self.randomize_title()

    def randomize_title(self):
        self.string = ""
        for i in range(10):
            self.string += characters[randint(0, len(characters)-1)]
        pg.display.set_caption(self.string)

    def events(self):
        self.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    raise Exception(self.reason)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.main.screen.fill(WIN10BLUE)
        draw_text(self.main, f":", UNDERTALE_FONT, 200, 0, 135, align="w")    
        draw_text(self.main, f"(", UNDERTALE_FONT, 200, 50, 150, align="w")    
        draw_text(self.main, f"A fatal exception has occured at \"{self.string}.exe\".", UNDERTALE_FONT, 20, 30, 300, align="w")
        draw_text(self.main, f"The current application will be terminated.", UNDERTALE_FONT, 20, 30, 325, align="w")    
        draw_text(self.main, f"Stop code: {self.reason}", UNDERTALE_FONT, 20, 30, 400, align="w")    
        draw_text(self.main, "Press SPACE to terminate the application.", UNDERTALE_FONT, 20, WIDTH/2, 550, align="center")
        pg.display.flip()
 