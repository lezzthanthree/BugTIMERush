import pygame as pg
from settings import *
from assets import *
from colors import *
from ui import draw_text
from os import path, listdir

game_folder = ""
snd_folder = path.join(game_folder, "snd")

class TestSound():
    def __init__(self, main):
        pg.mixer.music.stop()
        self.main = main

        self.current_sound = 0
        self.sound_names = []
        self.pos = 0
        self.start()

    def start(self):
        self.playing = True
        self.sounds = self.load_sounds()
        self.len = len(self.sounds)
        
        self.play(self.sounds[self.sound_names[self.current_sound]])
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
                    self.current_sound = (self.current_sound + 1) % self.len
                    self.play(self.sounds[self.sound_names[self.current_sound]])
                if event.key == pg.K_COMMA:
                    self.current_sound = (self.current_sound - 1) % self.len
                    self.play(self.sounds[self.sound_names[self.current_sound]])
                if event.key == pg.K_SPACE:
                    pg.mixer.music.pause()
                if event.key == pg.K_p:
                    pg.mixer.music.unpause()

    def play(self, sound):
        pg.mixer.music.load(sound)
        pg.mixer.music.play(loops=-1)
                    
    def update(self):
        self.pos = (pg.mixer.music.get_pos())/1000
        pass

    def draw(self):
        self.main.screen.fill(BLACK)
        draw_text(self.main, self.sound_names[self.current_sound], UNDERTALE_FONT, 30, 0, 0)
        draw_text(self.main, f"{self.current_sound}/{self.len - 1}", UNDERTALE_FONT, 30, 0, 40)
        draw_text(self.main, f"{self.pos}", UNDERTALE_FONT, 30, 0, 80)
        pg.display.flip()
    
    def load_sounds(self):
        files = listdir(snd_folder)
        sounds = {}

        for file in files:
            if file.endswith('.wav') or file.endswith('.ogg'):
                self.main.screen.fill(WIN10BLUE)
                self.sound_names.append(file)
                draw_text(self.main, file, UNDERTALE_FONT, 30, 0, 0)
                pg.display.flip()

                load = path.join(snd_folder, file)
                sounds[file] = load

        return sounds