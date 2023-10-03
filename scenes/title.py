import pygame as pg
from settings import *
from ui import draw_text
from assets import *
from colors import *

class TitleScreen():
    def __init__(self, main):
        pg.mixer.stop()
        pg.mixer.music.stop()
        self.main = main
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.start()

    def start(self):
        self.load_assets()
        START.play()
        self.playing = True
        while self.playing:
            self.update()
            self.draw()
            self.events()
        self.main.scene.set_scene('level')
        self.all_sprites.empty()
    
    def load_assets(self):
        self.title_bg = TITLE_BG
        self.title_bg_rect = self.title_bg.get_rect()
        self.title_bg_rect.center = ((WIDTH/2), (HEIGHT/2))
        self.title_logo = TitleLogo(self)

    def events(self):
        self.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.playing = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.main.screen.blit(self.title_bg, self.title_bg_rect)
        draw_text(self.main, "Press SPACE to continue", UNDERTALE_FONT, 25, WIDTH/2, 477, color=WHITE, align="center")    
        self.all_sprites.draw(self.main.screen)
        pg.display.flip()

class TitleLogo(pg.sprite.Sprite):
    def __init__(self, screen):
        self._layer = 2
        self.groups = screen.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.screen = screen
        
        self.current_frame = 0
        self.now = pg.time.get_ticks()
        self.last_update = self.now
        self.change_frame = 1

        self.load_images()
        self.image = self.title_frame[0]
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH/2), 150)

    def load_images(self):
        self.title_frame = TITLE_LOGO

    def animate(self):
        self.now = pg.time.get_ticks()
        if self.now - self.last_update > 200:
            self.last_update = self.now
            self.current_frame = (self.current_frame + self.change_frame)
            if self.current_frame == 7 or self.current_frame == 0:
                self.change_frame *= -1
            self.image = self.title_frame[self.current_frame]

    def update(self):
        self.animate()
    