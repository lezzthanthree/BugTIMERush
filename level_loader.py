from settings import *
import pygame as pg
from tilemap import *
import os
from os import path
vec = pg.math.Vector2

game_folder = ""
snd_folder = path.join(game_folder, 'snd')
img_folder = os.path.join(game_folder, "img")

# Checks for collisions for walls
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

class LevelLoader():
    def __init__(self, game):
        self.game = game
    
    # Loads the Level Stage
    def level_loader(self):
        pg.mixer.music.load(path.join(snd_folder, TITLEBGM))
        pg.mixer.music.play(loops=-1) 
        pg.mixer.music.set_volume(VOLUME) 

        print("picking level...")
        if self.game.debugger:
            print("F12 | unlock all level")
        for sprite in self.game.all_sprites:
            sprite.kill()
        self.game.all_sprites.empty()
        self.level_floor = TiledMap(path.join(game_folder, 'lvl\\level.tmx'))
        self.level_floor_img = self.level_floor.makemap()
        self.level_floor_rect = self.level_floor_img.get_rect()
        self.game.level_tiles = pg.sprite.Group()
        self.last_update = 0
        self.current_frame = 0
        self.game.all_sprites.empty()

        level = 0
        for tile_object in self.level_floor.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = LevelPlayer(self.game, tile_object.x, tile_object.y)
            if tile_object.name == 'level':
                Levels(self.game, tile_object.x, tile_object.y, level)
                level += 1
        sum = 0
        for total in self.game.savedata:
            sum += int(total)
        if sum == 16:
            Levels(self.game, 570, 50, 8)

        self.game.camera = Camera(self.level_floor.width, self.level_floor.height)
        self.level_load_update_loop()

    # Update Loop for the Level Stage
    def level_load_update_loop(self):
        self.picking = True
        while self.picking:
            self.draw_level_sprites()
            self.draw_level_text()
            self.draw_instructions()
            self.game.clock.tick(FPS)/1000
            pg.display.flip()
            self.game.all_sprites.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.game.quit()
                if event.type == pg.KEYDOWN:
                    if self.game.debugger and event.key == pg.K_F12:
                        self.game.highestlevel = 8
                        snd = pg.mixer.Sound(path.join(snd_folder, "unlockall.wav"))
                        snd.play()

    # Draws the sprites                                                        
    def draw_level_sprites(self):
        self.game.screen.blit(self.level_floor_img, self.game.camera.apply_rect(self.level_floor_rect))
        if self.player.on_block == True:
            self.game.draw_text(f"Locked!", self.game.undertale_font, 30, WHITE, WIDTH/2, HEIGHT - 150, align="center")
        for sprite in self.game.all_sprites:
            self.game.screen.blit(sprite.image, self.game.camera.apply(sprite))

    # Draws the Level Animation, text
    def draw_level_text(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 8
        img = self.game.level_frame[self.current_frame]
        img_rect = img.get_rect()
        img_rect.center = ((WIDTH/2), 175)
        self.game.screen.blit(img, img_rect)

    # Draws the WASD/Arrow Keys
    def draw_instructions(self):
        img = self.game.instructions
        img_rect = img.get_rect()
        img_rect.center = (710, 600)
        self.game.screen.blit(img, img_rect)
    

    
class LevelPlayer(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.walking = False
        self.facing = "south"
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.on_block = False

        self.image = self.stand_frame
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y)

    def load_images(self):
        self.stand_frame = self.game.player_stand_frame

        self.walk_north_frame = self.game.player_walk_north_frame

        self.walk_south_frame = self.game.player_walk_south_frame

        self.walk_west_frame  = self.game.player_walk_west_frame

        self.walk_east_frame  = self.game.player_walk_east_frame 

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -200
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = 200
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -200
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = 200

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

    def collision_with_level(self):
        hits = pg.sprite.spritecollide(self, self.game.level_tiles, False)
        if hits:
            if int(self.game.highestlevel) < hits[0].level and not self.on_block:
                self.on_block = True
                snd = pg.mixer.Sound(path.join(snd_folder, NOPE))
                snd.play()

            elif not self.on_block:
                self.game.levelloader.picking = False
                self.game.level = hits[0].level
                print(f"****level {hits[0].level}****")
                pg.mixer.music.load(path.join(snd_folder, BGM))
                pg.mixer.music.play(loops=-1) 
                self.vel *= 0
                self.game.new()
                return
                
        if self.on_block:
            collision_with_walls(self, self.game.level_tiles, 'x')
            collision_with_walls(self, self.game.level_tiles, 'y')

        if not hits:
            self.on_block = False

    def update(self):
        self.animate()
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.collision_with_level()

class Levels(pg.sprite.Sprite):
    def __init__(self, game, x, y, level):
        self._layer = 1
        self.groups = game.all_sprites, game.level_tiles
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.level = level
        self.image = game.ports[level]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

