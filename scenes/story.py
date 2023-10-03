from settings import *
from os import path
from assets import *
from ui import draw_text
import pygame as pg
import time
from colors import *


dialogue = {
    'prologue': [["One night, a young", "programmer was coding", "his latest creation."],
              ["Debugging all night, he", "was becoming frustrated", "with errors he's seeing."],
              ["Desperate, he wished he", "could enter his computer", "and fix them from the inside."],
              ["Suddenly...", "", ""],
              ["A bright light appeared", "on his computer screen.", ""],
              ["To find his way back to", "the real world, he must solve", "some tricky math problems..."],],

    'epilogue': [["As the young programmer", "dodged all the mobs while", "solving complex arithmetics..."],
             ["...he managed to escape", "the digital world!", ""],
             ["When he woke up, he finds", "himself in his own room.", ""],
             ["Checking his source code,", "the errors on his creation", "have finally vanished!"]]
}

class Story():
    def __init__(self, main, story):
        self.main = main
        self.current_frame = 0
        self.story_line = dialogue[story]
        self.story_photos = STORY[story]
        pg.mixer.music.load(STORY_BGM[story])
        
        self.start(story)

    def start(self, story):
        pg.mixer.music.play()
        self.draw_story()
        if story == 'prologue':
            self.main.scene.set_scene('title')
        if story == 'epilogue':
            self.main.scene.set_scene('credits')

    def draw_story(self):
        current_photo = 0

        for dialogue in self.story_line:
            self.main.screen.fill(BLACK)
            pic_rect = self.story_photos[current_photo].get_rect()
            pic_rect.center = ((WIDTH/2), 250)
            current_line_number = 0
            skipped = False
            self.main.screen.blit(self.story_photos[current_photo], pic_rect)
            for line in dialogue:
                skipped = self.type_line(line, current_line_number, dialogue)
                if skipped:
                    break
                current_line_number += 1
            current_photo += 1
            if skipped:
                continue
            self.wait_for_next()

        draw_text(self.main, "Press SPACE to continue", UNDERTALE_FONT, 15, WIDTH/2, HEIGHT - 75, align="center")

        self.wait_for_key()

    def type_line(self, line, line_number, dialogue):
        string = ""
        black_rect = BLACK_DIALOGUE.get_rect()
        black_rect.center = ((WIDTH/2), (HEIGHT/2))
        for char in line:
            self.main.clock.tick(FRAMES)/1000
            TYPE.stop()
            self.main.screen.blit(BLACK_DIALOGUE, black_rect)
            string = string + char
            if line_number == 0:
                draw_text(self.main, string, UNDERTALE_FONT, 30, 175, 425, align="w") 
            if line_number == 1:
                draw_text(self.main, dialogue[0], UNDERTALE_FONT, 30, 175, 425, align="w") 
                draw_text(self.main, string, UNDERTALE_FONT, 30, 175, 465, align="w") 
            if line_number == 2:
                draw_text(self.main, dialogue[0], UNDERTALE_FONT, 30, 175, 425, align="w") 
                draw_text(self.main, dialogue[1], UNDERTALE_FONT, 30, 175, 465, align="w") 
                draw_text(self.main, string, UNDERTALE_FONT, 30, 175, 505, align="w")
            TYPE.play()
            time.sleep(0.05)

            pg.display.flip()
            skipped = self.skip()
            if skipped:
                self.main.screen.blit(BLACK_DIALOGUE, black_rect)
                draw_text(self.main, dialogue[0], UNDERTALE_FONT, 30, 175, 425, align="w") 
                draw_text(self.main, dialogue[1], UNDERTALE_FONT, 30, 175, 465, align="w") 
                draw_text(self.main, dialogue[2], UNDERTALE_FONT, 30, 175, 505, align="w")
                return True

    def wait_for_next(self):
        pg.display.flip()
        last_update = pg.time.get_ticks()
        waiting = True
        while waiting:
            now = pg.time.get_ticks()
            if now - last_update > 3000:
                waiting = False
                return
            self.main.clock.tick(FRAMES)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.main.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return

    def wait_for_key(self):
        pg.display.flip()
        waiting = True
        while waiting:
            self.main.clock.tick(FRAMES)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.main.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return

    def skip(self):
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return True
        return False