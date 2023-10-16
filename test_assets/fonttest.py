import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text

class TestFont():
    def __init__(self, main):
        pg.mixer.music.stop()
        self.main = main
        self.size = 30
        self.start()

    def start(self):
        self.playing = True
        while self.playing:
            self.update()
            self.draw()
            self.events()

    def events(self):
        self.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                if event.key == pg.K_PERIOD:
                    self.size += 1
                if event.key == pg.K_COMMA:
                    self.size -= 1
                    
    def update(self):
        pass

    def draw(self):
        self.main.screen.fill(BLACK)
        draw_text(self.main, f"abcdefghijklmnopqrstuvwxyz0123456789", UNDERTALE_FONT, self.size, 0, 0, align="nw")
        draw_text(self.main, f"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", UNDERTALE_FONT, self.size, 0, 10+self.size, align="nw")
        draw_text(self.main, f"0123456789", LCD_FONT, self.size, 0, 400+self.size, align="nw")
        draw_text(self.main, str(self.size), LCD_FONT, self.size, 0, 450+self.size, align="nw")
        draw_text(self.main, f"The quick brown fox jumps over the lazy dog", UNDERTALE_FONT, self.size, 0, 100+self.size, align="nw")
        pg.display.flip()
 