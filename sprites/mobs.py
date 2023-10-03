import pygame as pg
from assets import *
from settings import *
from random import randint
from math import sqrt

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

class Zombie(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        self.groups = game.sprites.all_sprites, game.sprites.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.current_frame = 0
        self.last_update = 0
        self.image = ZOMBIE_STAND

        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_movement_update = 0
        self.moving = False

        self.radius = ZOMBIE_RADIUS
        self.offset = randint(-15, 15)
        self.rotation = 0
        self.distance = [0, 0]
        self.displacement = 0
        self.rect.topleft  = self.pos

    def animate(self):
        self.now = pg.time.get_ticks()

        if self.moving:
            if self.now - self.last_update > 200:
                self.last_update = self.now
                self.current_frame = (self.current_frame + 1) % 7
                self.image = ZOMBIE_WALK[self.current_frame]
        if not self.moving:
            self.image = ZOMBIE_STAND

    def movement(self):
        self.now = pg.time.get_ticks()
        self.distance = (self.game.sprites.player.pos - self.pos)
        self.displacement = sqrt((self.distance[0] ** 2) + (self.distance[1] ** 2))

        if self.displacement < self.radius:
            if not self.moving:
                DETECT.play()
            self.moving = True

        if self.now - self.last_movement_update > 500:
            self.last_movement_update = self.now
            self.rotation = -self.distance.angle_to(vec(1, 0)) + self.offset

            if self.moving:
                self.vel = vec(ZOMBIE_SPEED, 0).rotate(self.rotation)

        if self.displacement > self.radius:
            self.moving = False
            self.vel = vec(0, 0)

    def collision_with_player(self):
        player = self.game.sprites.player

        now = pg.time.get_ticks()   
        hits = pg.sprite.collide_rect(self, player)
        if hits and player.vulnerable:
            HURT.play()
            player.vulnerable = False
            player.last_invulnerable_update = now
            player.lives -= 1
            print("invulnerable for 2 seconds.")
            if player.lives == 0:
                self.game.main.gamehandler.set_reason("PLAYER_BUGGED_OUT")
                self.game.main.scene.set_scene('dead')

    def update(self):
        self.movement()
        self.animate()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        collision_with_walls(self, self.game.sprites.walls, 'x')
        collision_with_box(self, self.game.sprites.boxes, 'x', self.vel.x)
        self.rect.y = self.pos.y
        collision_with_walls(self, self.game.sprites.walls, 'y')
        collision_with_box(self, self.game.sprites.boxes, 'y', self.vel.y)

        self.collision_with_player()

class LinearZombie(pg.sprite.Sprite):
    def __init__(self, game, x, y, dir):
        self._layer = 2
        self.groups = game.sprites.all_sprites, game.sprites.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.current_frame = 0
        self.last_update = 0
        self.image = ZOMBIE_STAND

        self.direction = dir
        self.speed = ZOMBIE_SPEED

        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.last_movement_update = 0
        self.moving = False

        self.rect.center  = self.pos

    def animate(self):
        self.now = pg.time.get_ticks()

        if self.now - self.last_update > 200:
            self.last_update = self.now
            self.current_frame = (self.current_frame + 1) % 7
            self.image = ZOMBIE_WALK[self.current_frame]

    def movement(self):
        if self.direction == 'x':
            self.vel.x = self.speed
        if self.direction == 'y':
            self.vel.y = self.speed

    def collision_with_walls(self):
        hits = pg.sprite.spritecollide(self, self.game.sprites.walls, False) or pg.sprite.spritecollide(self, self.game.sprites.boxes, False)
        if hits:
            if self.direction == 'x':
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
            if self.direction == 'y':
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
            self.vel = vec(0, 0)
            self.speed *= -1

    def collision_with_player(self):
        player = self.game.sprites.player

        now = pg.time.get_ticks()   
        hits = pg.sprite.collide_rect(self, player)
        if hits and player.vulnerable:
            HURT.play()
            player.vulnerable = False
            player.last_invulnerable_update = now
            player.lives -= 1
            print("invulnerable for 2 seconds.")
            if player.lives == 0:
                self.game.main.gamehandler.set_reason("PLAYER_BUGGED_OUT")
                self.game.main.scene.set_scene('dead')
    
    def update(self):
        self.animate()
        self.movement()
        self.collision_with_walls()

        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        self.collision_with_player()

class Turret(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 1
        self.groups = game.sprites.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.now = pg.time.get_ticks()

        self.current_frame = 0
        self.last_firing_update = 0
        self.last_fired = 0

        self.image = TURRET
        self.rect = self.image.get_rect()

        self.pos = vec(x, y)
        self.target = vec(0, 0)
        self.firing = False
        self.shots_fired = 0

        self.radius = TURRET_RADIUS
        self.rotation = 0
        self.distance = [0, 0]
        self.displacement = 0
        self.rect.center = self.pos

    def fire(self):
        self.now = pg.time.get_ticks()
        self.distance = (self.game.sprites.player.pos - self.pos)
        self.displacement = sqrt((self.distance[0] ** 2) + (self.distance[1] ** 2))

        if self.displacement < self.radius:
            if not self.firing:
                self.shots_fired = 2
                DETECT.play()
            self.firing = True

        if self.now - self.last_firing_update > TURRET_COOLDOWN:
            self.last_firing_update = self.now
            self.shots_fired = 0
                
        if self.firing and (self.shots_fired < BULLETS_PER_TICK):
            if self.now - self.last_fired > SHOOT_EVERY:
                self.last_fired = self.now
                self.rotation = -self.distance.angle_to(vec(1, 0))
                self.target = vec(1, 0).rotate(self.rotation)

                Bullet(self.game, self.pos, self.target)
                SHOOT.play()
                self.shots_fired += 1

        if self.displacement > self.radius:
            self.firing = False

    def update(self):
        self.fire()

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.sprites.all_sprites, game.sprites.bullets, game.sprites.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos

        self.vel = dir * BULLET_SPEED

        self.spawn_time = pg.time.get_ticks()

    def collision_with_player(self):
        player = self.game.sprites.player

        now = pg.time.get_ticks()   
        hits = pg.sprite.collide_rect(self, player)
        if hits and player.vulnerable:
            HURT.play()
            player.vulnerable = False
            player.last_invulnerable_update = now
            player.lives -= 1
            print("invulnerable for 2 seconds.")
            if player.lives == 0:
                self.game.main.gamehandler.set_reason("PLAYER_GOT_SHOT")
                self.game.main.scene.set_scene('dead')
            self.kill()

    def update(self):
        now = pg.time.get_ticks()

        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if now - self.spawn_time > BULLET_SPAN:
            self.kill()
        hits = pg.sprite.spritecollide(self, self.game.sprites.walls, False) or pg.sprite.spritecollide(self, self.game.sprites.boxes, False)
        if hits:
            self.kill()
        self.collision_with_player()
