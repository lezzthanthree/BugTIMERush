import pygame as pg
from assets import *
from settings import *
from scripts import calculations

vec = pg.math.Vector2

class Signs(pg.sprite.Sprite):
    def __init__(self, game, x, y, sign):
        self._layer = 1
        self.groups = game.sprites.all_sprites, game.sprites.signs
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = SIGNS[sign]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.sign = sign

    def collected(self):
        hits = pg.sprite.collide_rect(self, self.game.sprites.player)
        if hits:
            self.game.sprites.player.current_sign = self.sign
            SIGN.play()
            self.kill()

    def update(self):
        self.collected()

class Numbers(pg.sprite.Sprite):
    def __init__(self, game, x, y, number):
        self._layer = 1
        self.groups = game.sprites.all_sprites, game.sprites.numbers
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = NUMBERS[number]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.number = number

    def collected(self):
        hits = pg.sprite.collide_rect(self, self.game.sprites.player)
        if hits:
            calculations.calculate(self.game, self.number, self.game.sprites.player)
            PICK.play()
            self.game.level.clock.timer += 3
            calculations.check_match(self.game, self.game.sprites.player)
            self.kill()

    def update(self):
        self.collected()