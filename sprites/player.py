import pygame as pg
from assets import *
from settings import *
from ui import draw_text
from colors import *
from scripts import gamedata

vec = pg.math.Vector2

# Checks for collisions of walls
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

def collision_with_box(sprite, group, dir, vel):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            hits[0].vel.x = vel
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width 
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.rect.x = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            hits[0].vel.y = vel
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.rect.y = sprite.pos.y

class Player(pg.sprite.Sprite):
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

        # Player Stats
        self.lives = 3
        self.total = 0
        self.current_sign = '+'
        self.holding_key = False
        self.on_finish = False
        self.vulnerable = True
        self.last_invulneralble_update = 0

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

    def check_lives(self):
        if self.lives == 0:
            self.game.main.scene.set_scene('dead')
            self.game.playing = False
        if self.lives > 3 or self.lives < 0:
            raise Exception("AntiCheatException: Player has more lives to spend")
        
    def collision_on_finish(self):
        hits = pg.sprite.collide_rect(self, self.game.sprites.finish)
        if hits and not self.on_finish:
            if self.holding_key:
                self.game.main.gamehandler.set_level(self.game.main.gamehandler.get_level() + 1)

                highest_level = int(self.game.main.gamehandler.savedata[0])
                if highest_level < self.game.main.gamehandler.get_level():
                    self.game.main.gamehandler.savedata[0] = self.game.main.gamehandler.get_level()
                    gamedata.save(self.game.main.gamehandler.savedata)
                if self.game.main.gamehandler.get_level() == 8:
                    self.game.main.scene.set_scene('epilogue')
                self.game.playing = False
            else:
                NOPE.play()
                self.on_finish = True
        if not hits and self.on_finish:
            self.on_finish = False

    def check_vulnerability(self):
        now = pg.time.get_ticks()
        if not self.vulnerable:
            if now - self.last_invulnerable_update > 2000:
                self.vulnerable = True
                print("now vulnerable")

    def update(self):
        self.check_lives()
        self.animate()
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collision_with_walls(self, self.game.sprites.walls, 'x')
        collision_with_box(self, self.game.sprites.boxes, 'x', self.vel.x)
        self.rect.y = self.pos.y
        collision_with_walls(self, self.game.sprites.walls, 'y')
        collision_with_box(self, self.game.sprites.boxes, 'y', self.vel.y)

        self.check_vulnerability()
        self.collision_on_finish()