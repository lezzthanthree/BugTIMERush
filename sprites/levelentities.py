import pygame as pg
from assets import *
from settings import PLAYER_SPEED

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
            # print(f"{sprite} hits wall #{hits[0].name}")

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y
            # print(f"{sprite} hits wall #{hits[0].name}")

class LevelPlayer(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        self.groups = game.sprites.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.load_images()

        # Walking/Standing
        self.walking = False
        self.facing = "south"
        self.speed = PLAYER_SPEED
        self.vel = vec(0, 0)
        self.pos = vec(x, y)

        # Animation
        self.image = self.stand_frame
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.last_update = 0

        self.on_block = False
        self.afk = False

    def load_images(self):
        self.stand_frame = PLAYER_STAND

        self.walk_north_frame = PLAYER_WALK_NORTH

        self.walk_south_frame = PLAYER_WALK_SOUTH

        self.walk_west_frame  = PLAYER_WALK_WEST

        self.walk_east_frame  = PLAYER_WALK_EAST

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = self.speed

    def animate(self):
        now = pg.time.get_ticks()
        self.walking = False
        if self.vel.x != 0 or self.vel.y != 0:
            self.walking = True

        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 4
                if self.vel.x > 0:
                    self.image = self.walk_east_frame [self.current_frame]
                    self.facing = "east"
                elif self.vel.x < 0:
                    self.image = self.walk_west_frame [self.current_frame]
                    self.facing = "west"
                elif self.vel.y > 0:
                    self.image = self.walk_south_frame[self.current_frame]
                    self.facing = "south"
                elif self.vel.y < 0:
                    self.image = self.walk_north_frame[self.current_frame]
                    self.facing = "north"

        if not self.walking:
            if self.facing == "east":
                self.image = self.walk_east_frame[0]
            elif self.facing == "west":
                self.image = self.walk_west_frame[0]
            elif self.facing == "south":
                self.image = self.walk_south_frame[0]
            elif self.facing == "north":
                self.image = self.walk_north_frame[0]

    def check_afk(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 4000:
            self.afk = True
        else:
            self.afk = False

    
    def collision_with_level(self):
        hits = pg.sprite.spritecollide(self, self.game.sprites.level_tiles, False)
        if hits:
            if hits[0].level == 'credits':
                self.game.choosing = False
                self.game.main.scene.set_scene('epilogue')
                return
            
            if int(self.game.main.gamehandler.savedata[0]) < hits[0].level and not self.on_block:
                self.on_block = True
                NOPE.play()

            elif not self.on_block:
                self.game.choosing = False
                self.game.main.gamehandler.set_level(hits[0].level)
                self.game.main.scene.set_scene('game')
                print(f"****level {hits[0].level}****")
                pg.mixer.music.load(GAME_BGM)
                pg.mixer.music.play(loops=-1) 
                self.vel *= 0
                return
                
        if self.on_block:
            collision_with_walls(self, self.game.sprites.level_tiles, 'x')
            collision_with_walls(self, self.game.sprites.level_tiles, 'y')

        if not hits:
            self.on_block = False

    def update(self):
        self.get_keys()
        self.animate()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.collision_with_level()
        self.check_afk()

class LevelTile(pg.sprite.Sprite):
    def __init__(self, game, x, y, level):
        self._layer = 1
        self.groups = game.sprites.all_sprites, game.sprites.level_tiles
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.level = level
        self.image = PORTS[level]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
