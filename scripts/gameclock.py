import pygame as pg
from settings import *
from assets import *

class GameClock:
    def __init__(self, game, timer):
        self.game = game
        self.now = pg.time.get_ticks()
        self.last_update = self.now
        self.timer = timer

    # Clock Ticks
    def tick(self):
        self.now = pg.time.get_ticks()

        if self.now - self.last_update > 100:
            self.last_update = self.now
            self.timer -= 0.1
        
        if self.timer < 0:
            HURT.play()
            print("ded")
            self.game.main.gamehandler.set_reason("CLOCK_PROCESS_TIMED_OUT")
            self.game.main.scene.set_scene('dead')
            self.game.playing = False

    def update(self):
        self.tick()