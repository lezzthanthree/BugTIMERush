import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text
from os import path, listdir

game_folder = ""
img_folder = path.join(game_folder, "img")

class TestSprite():
    def __init__(self, main):
        pg.mixer.music.stop()
        self.main = main
        self.current_image = 0
        self.last_update = 0
        self.x = 0
        self.y = 0
        self.start()

    def start(self):
        self.playing = True
        self.images = self.load_images()
        self.len = len(self.images)
        
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
                if event.key == pg.K_LEFT:
                    self.x -= 1
                if event.key == pg.K_RIGHT:
                    self.x += 1
                if event.key == pg.K_UP:
                    self.y -= 1
                if event.key == pg.K_DOWN:
                    self.y += 1
                    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.current_image = (self.current_image + 1) % self.len
            self.last_update = now

    def draw(self):
        self.main.screen.fill(WIN10BLUE)
        rect = self.images[self.current_image].get_rect()
        rect.topleft = (self.x, self.y)
        self.main.screen.blit(self.images[self.current_image], rect)
        pg.display.flip()
    
    def load_images(self):
        files = listdir(img_folder)
        png_images = []

        for file in files:
            if file.endswith('.png'):
                self.main.screen.fill(WIN10BLUE)
                draw_text(self.main, f"load {file}", UNDERTALE_FONT, 30, 0, 0)
                pg.display.flip()

                load = pg.image.load(path.join(img_folder, file))
                png_images.append(load)

        return png_images