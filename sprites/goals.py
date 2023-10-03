import pygame as pg
from assets import *

vec = pg.math.Vector2

class Finish(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 1
        self.groups = game.sprites.all_sprites, game.sprites.finish
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.state = 'locked'
        self.image = FINISH['locked']
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        self.groups = game.sprites.all_sprites, game.sprites.walls
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = CHEST
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Key(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 1
        self.groups = game.sprites.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.last_update = 0

        self.load_images()
        self.image = self.key_frames[0]
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def load_images(self):
        self.key_frames = KEY

    def animate(self):
        now = pg.time.get_ticks()

        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 4
            self.image = self.key_frames[self.current_frame]

    def collision_with_player(self):
        hits = pg.sprite.collide_rect(self, self.game.sprites.player)
        if hits:
            print("got key!")
            self.game.sprites.player.holding_key = True
            self.kill()
            self.game.sprites.finish.image = FINISH['unlocked']
            KEYGET.play()
    
    def update(self):
        self.animate()
        self.collision_with_player()