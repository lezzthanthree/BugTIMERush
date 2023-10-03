import pygame as pg
from assets import *

vec = pg.math.Vector2

def collision_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y

class Walls(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.sprites.walls 
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Flashlight(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = 4
        self.groups = game.sprites.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.now = pg.time.get_ticks()

        self.image = FLASHLIGHT
        self.rect = self.image.get_rect()

        self.rect.center = self.game.sprites.player.rect.center

    def update(self):
        self.rect.center = self.game.sprites.player.rect.center

class Box(pg.sprite.Sprite):
    def __init__(self, game, x, y, name):
        self._layer = 2
        self.groups = game.sprites.all_sprites, game.sprites.boxes
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = BOX
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.name = name

    def collision_with_box(self, dir, vel):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.sprites.boxes, False)
            if hits and not hits[0].name == self.name:
                hits[0].vel.x = vel
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width 
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x = 0

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.sprites.boxes, False)
            if hits and not hits[0].name == self.name:
                hits[0].vel.y = vel
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                self.vel.x = 0

    def update(self):
        self.pos += self.vel * self.game.dt
        self.vel *= 0.95
        self.rect.x = self.pos.x
        collision_with_walls(self, self.game.sprites.walls, 'x')
        self.collision_with_box('x', self.vel.x)
        self.rect.y = self.pos.y
        collision_with_walls(self, self.game.sprites.walls, 'y')
        self.collision_with_box('y', self.vel.y)