import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text
from os import path, remove

class TestScene():
    def __init__(self, main):
        pg.mixer.music.stop()
        self.main = main

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
                if event.key == pg.K_0:
                    self.confirm_scene('prologue')
                if event.key == pg.K_1:
                    self.confirm_scene('title')
                if event.key == pg.K_2:
                    self.confirm_scene('level')
                if event.key == pg.K_3:
                    self.confirm_scene('game')
                if event.key == pg.K_4:
                    self.confirm_scene('dead')
                if event.key == pg.K_5:
                    self.confirm_scene('epilogue')
                if event.key == pg.K_6:
                    self.confirm_scene('credits')
                if event.key == pg.K_7:
                    self.confirm_scene('gameover')
                if event.key == pg.K_DELETE:
                    if path.isfile("currentlvl"):
                        remove("currentlvl")
                if event.key == pg.K_q:
                    self.main.quit()
                if event.key == pg.K_PERIOD:
                    self.main.gamehandler.set_level(self.main.gamehandler.get_level() + 1)
                if event.key == pg.K_COMMA:
                    self.main.gamehandler.set_level(self.main.gamehandler.get_level() - 1)
                
    def confirm_scene(self, scene):
        self.main.scene.set_scene(scene)
        self.playing = False
    
    def update(self):
        pass

    def draw(self):
        self.main.screen.fill(BLACK)
        draw_text(self.main, "0 = prologue", UNDERTALE_FONT, 30, 0, 0)
        draw_text(self.main, "1 = title", UNDERTALE_FONT, 30, 0, 30)
        draw_text(self.main, "2 = level", UNDERTALE_FONT, 30, 0, 60)
        draw_text(self.main, f"3 = game {self.main.gamehandler.get_level()}", UNDERTALE_FONT, 30, 0, 90)
        draw_text(self.main, "4 = dead", UNDERTALE_FONT, 30, 0, 120)
        draw_text(self.main, "5 = epilogue", UNDERTALE_FONT, 30, 0, 150)
        draw_text(self.main, "6 = credits", UNDERTALE_FONT, 30, 0, 180)
        draw_text(self.main, "7 = gameover", UNDERTALE_FONT, 30, 0, 210)
        draw_text(self.main, "DEL = delete save", UNDERTALE_FONT, 30, 0, 240)
        draw_text(self.main, "esc = test_assets", UNDERTALE_FONT, 30, 0, 330)
        draw_text(self.main, "q = quit", UNDERTALE_FONT, 30, 0, 360)

        pg.display.flip()