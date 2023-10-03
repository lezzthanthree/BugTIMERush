import pygame as pg
from assets import *
from settings import *
from scripts import levelhandler, camera
from ui import draw_text, quit_screen

class LevelScreen():
    def __init__(self, main):
        self.main = main
        if int(self.main.gamehandler.savedata[0]) >= 8:
            pg.mixer.music.load(TITLE_ALL_BGM)
        else:
            pg.mixer.music.load(TITLE_BGM)

        self.dt = self.main.clock.tick(FRAMES)/100

        self.last_update = 0
        self.current_frame = 0
        self.change_frame = 1

        self.start()

    def start(self):
        print("starting")
        pg.mixer.music.play(loops=-1)

        self.level = levelhandler.LevelLoader(self, 'level')
        self.level.start_map()

        self.sprites = levelhandler.LevelSprites(self, self.level.map)
        self.sprites.create_sprites()

        self.camera = camera.Camera(self.level.map.width, self.level.map.height )
        
        self.choosing = True
        while self.choosing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        self.dt = self.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_screen(self)

    def update(self):
        self.sprites.all_sprites.update()

    def draw(self): 
        self.main.screen.blit(self.level.map_img, self.camera.apply_rect(self.level.map_rect))
        for sprite in self.sprites.all_sprites:
            self.main.screen.blit(sprite.image, self.camera.apply(sprite))
        self.sprites.all_sprites.draw(self.main.screen)
        if self.sprites.player.on_block:
            draw_text(self.main, "Locked!", UNDERTALE_FONT, 30, WIDTH/2, HEIGHT - 150, align="center")
        if self.sprites.player.afk:
            draw_text(self.main, "Press the arrow keys or WASD to move!", UNDERTALE_FONT, 20, WIDTH/2, HEIGHT - 150, align="center")
        self.draw_level_text()
        pg.display.flip()

    def draw_level_text(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + self.change_frame)
            if self.current_frame == 7 or self.current_frame == 0:
                self.change_frame *= -1
        img = LEVEL_TEXT[self.current_frame]
        img_rect = img.get_rect()
        img_rect.center = ((WIDTH/2), 175)
        self.main.screen.blit(img, img_rect)