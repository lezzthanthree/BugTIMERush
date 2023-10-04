import pygame as pg
import pytmx
from sprites import player, goals, collectibles, obstacles, tip, mobs, levelentities
from settings import *
from os import path
from scripts import gameclock

game_folder = ""

POSSIBLE_SYMBOLS = ['+', '-', 'X', 'D']

class TiledMap():
    # Initilizes the dimensions of the map
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True) 
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    # Render the map per tile
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tileheight, 
                                            y * self.tmxdata.tilewidth))

    # Return the whole map and display to the screen
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface     

class LevelLoader():
    def __init__(self, game, level):
        self.game = game
        self.level_file = f"lvl\\{level}.tmx"
        self.level_number = level

    def start_map(self):
        if self.level_number != 'level':
            self.get_level_data()
            self.clock = gameclock.GameClock(self.game, self.seconds)
        self.create_map()

    def get_level_data(self):
        self.game_details = []
        with open(path.join(game_folder, 'lvl\\level_details'), 'rt') as f:
            for line in f:
                split = line.split(',')
                self.game_details.append(split)   
        f.close()

        self.sum = self.game_details[self.level_number][0]
        self.seconds = int(self.game_details[self.level_number][1])

    def create_map(self):
        self.map = TiledMap(self.level_file)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
class GameSprites():
    def __init__(self, game, map_data: TiledMap):
        self.game = game
        self.map = map_data

        self.has_tips = False

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.signs = pg.sprite.Group()
        self.numbers = pg.sprite.Group()
        self.finish = pg.sprite.Group()
        self.boxes = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.tips = pg.sprite.Group()   

    def create_sprites(self):
        box_id = 0
        tip_id = 0
        for tile_object in self.map.tmxdata.objects:
            name = tile_object.name
            x = tile_object.x
            y = tile_object.y

            if name == 'player':
                self.player = player.Player(self.game, x, y)
            if name == 'chest':
                self.chest = goals.Chest(self.game, x, y)
            if name == 'finish':
                self.finish = goals.Finish(self.game, x, y)
            if name == 'wall':
                obstacles.Walls(self.game, x, y, tile_object.width, tile_object.height)
            if name == 'zombie':
                mobs.Zombie(self.game, x, y)
            if name == 'zombiex':
                mobs.LinearZombie(self.game, x, y, 'x')
            if name == 'zombiey':
                mobs.LinearZombie(self.game, x, y, 'y')
            if name == 'turret':
                mobs.Turret(self.game, x, y)
            if str(name).isnumeric():
                collectibles.Numbers(self.game, x, y, int(name))
            if name in POSSIBLE_SYMBOLS:
                collectibles.Signs(self.game, x, y, name)
            if name == 'block':
                obstacles.Box(self.game, x, y, box_id)
                box_id += 1
            if name == 'flashlight':
                self.flashlight = obstacles.Flashlight(self.game)
            if name == 'tutorial':
                tip.Tip(self.game, x, y, tip_id)
                tip_id += 1
                self.has_tips = True

        if self.has_tips:
            self.tip_text = tip.TipText(self.game)

class LevelSprites():
    def __init__(self, game, map_data: TiledMap):
        self.game = game
        self.map = map_data

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.level_tiles = pg.sprite.Group()

    def create_sprites(self):
        level = 0
        for tile_object in self.map.tmxdata.objects:
            name = tile_object.name
            x = tile_object.x
            y = tile_object.y

            if name == 'player':
                self.player = levelentities.LevelPlayer(self.game, x, y)
            if name == 'level':
                levelentities.LevelTile(self.game, x, y, level)
                level += 1

        if int(self.game.main.gamehandler.savedata[0]) == 8:
            levelentities.LevelTile(self.game, 656, 50, 'credits')
