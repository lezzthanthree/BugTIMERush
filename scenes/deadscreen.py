import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text, quit_screen
from scenes import title

class DeadScreen():
    def __init__(self, main, reason, level):
        pg.mixer.music.stop()
        self.main = main
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.reason = reason
        self.level = level
        self.start()

    def start(self):
        BSOD.play()
        self.playing = True
        while self.playing:
            self.update()
            self.draw()
            self.events()

    def events(self):
        self.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_screen(self)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.main.scene.set_scene('title')
                    self.playing = False
                    return
                if event.key == pg.K_SPACE:
                    self.main.scene.set_scene('game')
                    pg.mixer.music.load(GAME_BGM)
                    pg.mixer.music.play(loops=-1) 
                    self.playing = False
                    return
                
                

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.main.screen.fill(WIN10BLUE)
        draw_text(self.main, f":", UNDERTALE_FONT, 200, 0, 135, align="w")    
        draw_text(self.main, f"(", UNDERTALE_FONT, 200, 50, 150, align="w")    
        draw_text(self.main, f"A fatal exception has occured at level {self.level}. The current", UNDERTALE_FONT, 20, 30, 300, align="w")
        draw_text(self.main, f"player will be terminated.", UNDERTALE_FONT, 20, 30, 325, align="w")    
        draw_text(self.main, f"Stop code: {self.reason}", UNDERTALE_FONT, 20, 30, 400, align="w")    
        draw_text(self.main, "Press SPACE to retry the level.", UNDERTALE_FONT, 20, WIDTH/2, 550, align="center")
        draw_text(self.main, "Press ESC to reboot.", UNDERTALE_FONT, 20, WIDTH/2, 575, align="center")  
        pg.display.flip()
 