import pygame as pg
from scripts import levelhandler, camera, hud
from settings import *
from assets import *
from ui import loading_screen, pause_screen, quit_screen

class GameScreen():
    def __init__(self, main, level):
        pg.mixer.stop()
        self.main = main
        self.level_number = level
        self.dt = self.main.clock.tick(FRAMES)/1000
        self.start()

    def start(self):
        NEXT.play()
        loading_screen(self.main)

        self.level = levelhandler.LevelLoader(self, self.level_number)
        self.level.start_map()

        self.sprites = levelhandler.GameSprites(self, self.level.map)
        self.sprites.create_sprites()

        self.camera = camera.Camera(self.level.map.width, self.level.map.height)
        self.hud = hud.HUD(self, self.main, self.level, self.sprites)

        self.playing = True
        while self.playing:
            self.dt = self.main.clock.tick(FRAMES)/1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_screen(self)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                    pause_screen(self)
                if event.key == pg.K_DELETE:
                    self.main.gamehandler.set_reason("GOD_IS_MERCILESS")
                    self.main.scene.set_scene('dead')
                    self.playing = False
                    return

    def update(self):
        self.level.clock.update()
        self.sprites.all_sprites.update()
        self.camera.update(self.sprites.player)

    def draw(self):
        self.main.screen.blit(self.level.map_img, self.camera.apply_rect(self.level.map_rect))
        for sprite in self.sprites.all_sprites:
            self.main.screen.blit(sprite.image, self.camera.apply(sprite))
        self.hud.draw_hud()
        pg.display.flip()
