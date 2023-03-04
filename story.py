from settings import *
import pygame as pg
from os import path
import time

game_folder = ""
snd_folder = path.join(game_folder, 'snd')
img_folder = path.join(game_folder, "img")

prologue =   [["One night, a young", "programmer was coding", "his latest creation."],
              ["Debugging all night, he", "was becoming frustrated", "with errors he's seeing."],
              ["Desperate, he wished he", "could enter his computer", "and fix them from the inside."],
              ["Suddenly...", "", ""],
              ["A bright light appeared", "on his computer screen.", ""],
              ["To find his way back to", "the real world, he must solve", "some tricky math problems..."],]

epilogue =  [["As the young programmer", "dodged all the mobs while", "solving complex arithmetics..."],
             ["...he managed to escape", "the digital world!", ""],
             ["When he woke up, he finds", "himself in his own room.", ""],
             ["Checking his source code,", "the errors on his creation", "have finally vanished!"]]

class Story():
    def __init__(self, game):
        self.game = game
        self.current_frame = 0
        self.story_line = []
        self.file_name = ""

    # Load the story
    def story_loader(self, story):
        if story == "prologue":
            self.story_line = prologue
            self.file_name = "prologue"
        if story == "epilogue":
            self.story_line = epilogue
            self.file_name = "epilogue"

        pg.mixer.stop()
        pg.mixer.music.load(path.join(snd_folder, f'{self.file_name}.ogg'))
        pg.mixer.music.set_volume(VOLUME)
        pg.mixer.music.play()

        self.draw_story()
        self.story_update_loop()

    # Update loop
    def story_update_loop(self):
        self.reading = True
        while self.reading:
            self.game.clock.tick(FPS)/1000
            pg.display.flip()
            self.game.all_sprites.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.current_frame += 1
                        self.draw_story()

    # Draws the story
    def draw_story(self):
        if self.current_frame >= len(self.story_line):
            self.reading = False
            self.game.draw_text("Press SPACE to continue", self.game.undertale_font, 15, WHITE, WIDTH/2, HEIGHT - 75, align="center") 
            return
        self.game.screen.fill(BLACK)
        test = pg.image.load(path.join(img_folder, f"{self.file_name}_{self.current_frame}.png"))
        test_rect = test.get_rect()
        test_rect.center = ((WIDTH/2), 250)
        self.game.screen.blit(test, test_rect)

        string = ""
        i = 0
        snd = pg.mixer.Sound(path.join(snd_folder, 'txt.wav'))
        for lines in self.story_line[self.current_frame]:
            self.game.clock.tick(FPS)/1000
            time.sleep(0.1)
            for char in self.story_line[self.current_frame][i]:
                self.game.screen.fill(BLACK)
                self.game.screen.blit(test, test_rect)
                snd.stop()
                self.game.clock.tick(FPS)/1000
                string = string + char
                if i == 0:
                    self.game.draw_text(string, self.game.undertale_font, 30, WHITE, 175, 425, align="w") 
                if i == 1:
                    self.game.draw_text(self.story_line[self.current_frame][0], self.game.undertale_font, 30, WHITE, 175, 425, align="w") 
                    self.game.draw_text(string, self.game.undertale_font, 30, WHITE, 175, 465, align="w") 
                if i == 2:
                    self.game.draw_text(self.story_line[self.current_frame][0], self.game.undertale_font, 30, WHITE, 175, 425, align="w") 
                    self.game.draw_text(self.story_line[self.current_frame][1], self.game.undertale_font, 30, WHITE, 175, 465, align="w") 
                    self.game.draw_text(string, self.game.undertale_font, 30, WHITE, 175, 505, align="w")
                snd.play()
                time.sleep(0.05)
                pg.display.flip()
                for event in pg.event.get():
                    if event.type == pg.QUIT:   
                        self.game.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            self.draw_skip()
                            self.current_frame += 1
                            self.draw_story()
                            return
                        if event.key == pg.K_END:
                            waiting = False
                            self.story_loader('epilogue')
                            self.draw_congrats()
                            self.ded_screen("NO_PLAYER_IN_SIMULATION")
                            return
            i += 1
            string = ""
        waiting = True
        last_update = pg.time.get_ticks()
        while waiting:
            now = pg.time.get_ticks()
            if now - last_update > 3000:
                self.current_frame += 1
                waiting = False
                self.draw_story()
                return
            self.game.clock.tick(FPS)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.draw_skip()
                        self.current_frame += 1
                        self.draw_story()
                        return

        self.draw_skip()

    # Draws the dialogue when the user skipped
    def draw_skip(self):
        self.game.draw_text(self.story_line[self.current_frame][0], self.game.undertale_font, 30, WHITE, 175, 425, align="w") 
        self.game.draw_text(self.story_line[self.current_frame][1], self.game.undertale_font, 30, WHITE, 175, 465, align="w") 
        self.game.draw_text(self.story_line[self.current_frame][2], self.game.undertale_font, 30, WHITE, 175, 505, align="w") 

    # Draw the congrats section
    def draw_congrats(self):
        # seconds / bpm / scale
        self.delay = 60 / 127 / 0.125
        self.beat = 0
        self.offset = 0
        pg.mixer.music.load(path.join(snd_folder, 'congrats.ogg'))
        pg.mixer.music.play(loops=-1)
        self.wait_for_key_credits()

    # Update loop for the credits
    def wait_for_key_credits(self):
        self.rolling = True
        while self.rolling:
            next_beat = (pg.mixer.music.get_pos()/1000) > ((self.beat) * self.delay)
            if next_beat:
                self.beat += 1
                self.draw_credits()
            pg.display.flip()
            self.game.clock.tick(FPS)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.rolling = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.beat = 13
                        self.rolling = False
                        self.draw_credits()
                        return

    # Draws the sections        
    def draw_credits(self):
        if self.beat == 1:
            self.game.screen.fill(BLACK)
            title = self.game.title_frame[0]
            title_rect = title.get_rect()
            title_rect.center = ((WIDTH/2), (HEIGHT/2))
            self.game.screen.blit(title, title_rect)
        if self.beat == 2:
            self.game.screen.fill(BLACK)
            self.game.draw_text("by", self.game.undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 - 50, align="center")
            self.game.draw_text("Sleepy Developers", self.game.undertale_font, 40, WHITE, WIDTH/2, HEIGHT/2, align="center")
        if self.beat == 3:
            self.game.screen.fill(BLACK)
            self.game.draw_text("in partial fulfillment of the", self.game.undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 - 75, align="center")
            self.game.draw_text("course requirement in", self.game.undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 - 50, align="center")
            self.game.draw_text("Discrete Structures 2", self.game.undertale_font, 50, WHITE, WIDTH/2, HEIGHT/2, align="center")
        if self.beat == 4:
            self.game.screen.fill(BLACK)
            bg = pg.image.load(path.join(game_folder, "img\\annoyingdog.png"))
            bg_rect = bg.get_rect()
            bg_rect.center = ((WIDTH/2), (HEIGHT/2))
            self.game.screen.blit(bg, bg_rect)
        if self.beat == 5:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Sprite Design", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 40, align="w")
            self.game.draw_text("Nykky Gatulayao", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2, align="w")
            self.game.draw_text("Adrian Abelligos", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 40, align="w")
        if self.beat == 6:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Level Design", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 20, align="w")
            self.game.draw_text("Carlo Agas", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 20, align="w")
        if self.beat == 7:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Programmers", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 20, align="w")
            self.game.draw_text("Genesis Lovino", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 20, align="w")
        if self.beat == 8:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Technicals and Papers", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 40, align="w")
            self.game.draw_text("Mark Vincent Caspe", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2, align="w")
            self.game.draw_text("Randolph Larano", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 40, align="w")
        if self.beat == 9:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Music (from UNDERTALE)", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 80, align="w")
            self.game.draw_text("Once Upon A Time", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 - 40, align="w")
            self.game.draw_text("Start Menu", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2, align="w")
            self.game.draw_text("CORE", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 40, align="w")
            self.game.draw_text("Can You Really Call This A Hotel", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 80, align="w")
        if self.beat == 10:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Sounds", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 60, align="w")
            self.game.draw_text("UNDERTALE", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 - 20, align="w")
            self.game.draw_text("Needy Streamer Overload", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 20, align="w")
            self.game.draw_text("Touhou", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 60, align="w")
        if self.beat == 11:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Art Inspirations", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 80, align="w")
            self.game.draw_text("Ansimuz", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 - 40, align="w")
            self.game.draw_text("Buch", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2, align="w")
            self.game.draw_text("Emcee Flesher", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 +  40, align="w")
            self.game.draw_text("Pupkin", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 80, align="w")
        if self.beat == 12:
            self.game.screen.fill(BLACK)
            self.game.draw_text("Game Inspirations", self.game.undertale_font, 30, YELLOW, 80, HEIGHT/2 - 60, align="w")
            self.game.draw_text("UNDERTALE", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 - 20, align="w")
            self.game.draw_text("Portal", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 + 20, align="w")
            self.game.draw_text("Needy Streamer Overload", self.game.undertale_font, 30, WHITE, 130, HEIGHT/2 +  60, align="w")
        if self.beat > 12:
            snd = pg.mixer.Sound(path.join(snd_folder, 'unlockall.wav'))
            snd.play()

            self.game.screen.fill(BLACK)
            bg = pg.image.load(path.join(game_folder, "img\\congrats_bg.png"))
            bg_rect = bg.get_rect()
            bg_rect.topleft = (0, 0)
            self.game.screen.blit(bg, bg_rect)
            self.rolling = False

            self.game.draw_text("From the developers: ", self.game.undertale_font, 20, GREY, 265, 180, align="nw")
            self.game.draw_text("Hey, congrats!", self.game.undertale_font, 34, GREY, 263, 200, align="nw")

            self.game.draw_text("Math is one of the hardest game", self.game.undertale_font, 15, GREY, 265, 250, align="nw")
            self.game.draw_text("concepts when it comes to", self.game.undertale_font, 15, GREY, 265, 265, align="nw")
            self.game.draw_text("puzzles.", self.game.undertale_font, 15, GREY, 265, 280, align="nw")
            self.game.draw_text("If you have reached this", self.game.undertale_font, 15, GREY, 265, 300, align="nw")
            self.game.draw_text("message, we wanted to say,", self.game.undertale_font, 15, GREY, 265, 315, align="nw")
            self.game.draw_text("we are so proud of you to play", self.game.undertale_font, 15, GREY, 265, 330, align="nw")
            self.game.draw_text("this game until the very end.", self.game.undertale_font, 15, GREY, 265, 345, align="nw")
            self.game.draw_text("Thanks for playing!", self.game.undertale_font, 15, GREY, 265, 375, align="nw")
            self.game.draw_text("Press SPACE", self.game.undertale_font, 20, GREY, WIDTH/2, 430, align="center")

            pg.display.flip()
            self.wait_for_key_bsod()

    # Draws the ending BSoD
    def ded_screen(self, reason):
        self.game.playing = False
        pg.mixer.music.stop()

        snd = pg.mixer.Sound(path.join(snd_folder, BSOD))
        snd.play(loops=-1)
        print("ded screen showed")

        self.game.screen.fill(WIN10BLUE)
        self.game.draw_text(f":", self.game.undertale_font, 200, WHITE, 0, 135, align="w")    
        self.game.draw_text(f"(", self.game.undertale_font, 200, WHITE, 50, 150, align="w")    
        self.game.draw_text(f"A fatal exception has occured at \"Bug TIME Rush.exe\". The ", self.game.undertale_font, 20, WHITE, 30, 300, align="w")
        self.game.draw_text(f"current application will be terminated.", self.game.undertale_font, 20, WHITE, 30, 325, align="w")    
        self.game.draw_text(f"Stop code: {reason}", self.game.undertale_font, 20, WHITE, 30, 400, align="w")    
        self.game.draw_text("Press SPACE to terminate the application.", self.game.undertale_font, 20, WHITE, WIDTH/2, 550, align="center") 
        pg.display.flip()
        self.wait_for_key_bsod()

        raise Exception("PlayerNotFound: The player has escaped the simulation.")

    # Update loop for BSoD   
    def wait_for_key_bsod(self):
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False
                        return
                