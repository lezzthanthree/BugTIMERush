import pygame as pg
import sys
import traceback
import keyboard
from os import path
from settings import *
from sprites import *
from tilemap import *
from gameclock import *
from level_loader import *
from story import *
from titlescreen import *

game_folder = ""
snd_folder = path.join(game_folder, 'snd')
img_folder = path.join(game_folder, "img")

class Game:
    # Initiate pygame program
    def __init__(self):
        print("initializing pygame...")
        pg.init()
        pg.mixer.init()
        pg.font.init()
        pg.mixer.music.set_volume(VOLUME)
        icon = pg.image.load(path.join(img_folder, "icon.png"))
        pg.display.set_icon(icon)
        self.undertale_font = path.join(img_folder, UNDERTALEFONT)
        self.lcd_font = path.join(img_folder, LCDFONT)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(FPS)/1000
        self.running = True

        self.debugger = True

        self.level = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.symbols = ['+', '-', 'X', 'D']
        try:
            self.load_images()
        except:
            self.throw_exception("FileNotFoundError: Some textures are reported missing.")
            
        self.loading_screen()
        self.levelloader = LevelLoader(self)
        self.story = Story(self)
        self.start_screen = TitleScreen(self)

        self.savedata = []
        if os.path.isfile(path.join(game_folder, "currentlvl")):
            with open(path.join(game_folder, 'currentlvl'), 'rt') as f:
                for line in f:
                    self.savedata.append(line.strip())
            f.close()
        else:
            f = open(path.join(game_folder, 'currentlvl'), "w+")
            for i in range(10):
                f.write('0\n')
                self.savedata.append(0)
            f.close()
        print(self.savedata)
        self.savedata
        self.highestlevel = self.savedata[0]

    # Load every single image in one go.
    def load_images(self):
        print("loading images")
        
        self.zombie_stand_frame = pg.image.load(path.join(img_folder, ZOMBIE_STAND))
        self.loading_screen()
        
        self.player_stand_frame = pg.image.load(path.join(img_folder, PLAYER_STAND))

        self.player_walk_north_frame = [pg.image.load(path.join(img_folder, PLAYER_WALK_N_0)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_N_1)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_N_2)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_N_3))]

        self.player_walk_south_frame = [pg.image.load(path.join(img_folder, PLAYER_WALK_S_0)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_S_1)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_S_2)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_S_3))]

        self.player_walk_west_frame =  [pg.image.load(path.join(img_folder, PLAYER_WALK_W_0)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_W_1)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_W_2)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_W_3))] 

        self.player_walk_east_frame =  [pg.image.load(path.join(img_folder, PLAYER_WALK_E_0)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_E_1)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_E_2)), 
                                        pg.image.load(path.join(img_folder, PLAYER_WALK_E_3))]

        self.player_lives_img        = [pg.image.load(path.join(img_folder, LIVES3)),
                                        pg.image.load(path.join(img_folder, LIVES2)),
                                        pg.image.load(path.join(img_folder, LIVES1)),
                                        pg.image.load(path.join(img_folder, MORELIVES))]


        self.zombie_moving_frame = [pg.image.load(path.join(img_folder, ZOMBIE_FRAME_0)),
                                    pg.image.load(path.join(img_folder, ZOMBIE_FRAME_1)),
                                    pg.image.load(path.join(img_folder, ZOMBIE_FRAME_2)),
                                    pg.image.load(path.join(img_folder, ZOMBIE_FRAME_3)),
                                    pg.image.load(path.join(img_folder, ZOMBIE_FRAME_4)),
                                    pg.image.load(path.join(img_folder, ZOMBIE_FRAME_5)),
                                    pg.image.load(path.join(img_folder, ZOMBIE_FRAME_6))]

        self.turret_stand_frame = pg.image.load(path.join(img_folder, TURRET_STAND))

        self.bullet_img         = pg.image.load(path.join(img_folder, BULLET_IMG))

        self.currentarithmetic       = [pg.image.load(path.join(img_folder, CUR_PLUS)), 
                                        pg.image.load(path.join(img_folder, CUR_MINUS)), 
                                        pg.image.load(path.join(img_folder, CUR_CROSS)), 
                                        pg.image.load(path.join(img_folder, CUR_OBELUS))]
        
        self.score_hud               =  pg.image.load(path.join(img_folder, SCORE_HUD))

        self.timer_hud               =  pg.image.load(path.join(img_folder, TIMER_HUD))

        self.objective_hud           =  pg.image.load(path.join(img_folder, OBJECTIVE_HUD))

        self.arithmetictiles        =  [pg.image.load(path.join(img_folder, PLUS)), 
                                        pg.image.load(path.join(img_folder, MINUS)), 
                                        pg.image.load(path.join(img_folder, CROSS)), 
                                        pg.image.load(path.join(img_folder, OBELUS))]
        
        self.numbertiles            =  [pg.image.load(path.join(img_folder, ZERO)), 
                                        pg.image.load(path.join(img_folder, ONE)), 
                                        pg.image.load(path.join(img_folder, TWO)), 
                                        pg.image.load(path.join(img_folder, THREE)), 
                                        pg.image.load(path.join(img_folder, FOUR)), 
                                        pg.image.load(path.join(img_folder, FIVE)), 
                                        pg.image.load(path.join(img_folder, SIX)), 
                                        pg.image.load(path.join(img_folder, SEVEN)), 
                                        pg.image.load(path.join(img_folder, EIGHT)), 
                                        pg.image.load(path.join(img_folder, NINE)), 
                                        pg.image.load(path.join(img_folder, TEN)),]

        self.block_img = pg.image.load(path.join(img_folder, BLOCK))

        self.chest_img = pg.image.load(path.join(img_folder, CHEST))

        self.key_frame_img   = [pg.image.load(path.join(img_folder, KEY_FRAME_0)),
                                pg.image.load(path.join(img_folder, KEY_FRAME_1)),
                                pg.image.load(path.join(img_folder, KEY_FRAME_2)),
                                pg.image.load(path.join(img_folder, KEY_FRAME_3))]

        self.finish_locked_img = pg.image.load(path.join(img_folder, FINISH_LOCKED))

        self.finish_opened_img = pg.image.load(path.join(img_folder, FINISH_OPENED))

        self.flashlight_img = pg.image.load(path.join(img_folder, FLASHLIGHT))

        self.radio_off = pg.image.load(path.join(img_folder, RADIO_OFF))
        self.radio_on = pg.image.load(path.join(img_folder, RADIO_ON))
        self.radio_none = pg.image.load(path.join(img_folder, RADIO_NONE))

        self.title_frame = [pg.image.load(path.join(img_folder, TITLE_0)),
                            pg.image.load(path.join(img_folder, TITLE_1)),
                            pg.image.load(path.join(img_folder, TITLE_2)),
                            pg.image.load(path.join(img_folder, TITLE_3)),
                            pg.image.load(path.join(img_folder, TITLE_4)),
                            pg.image.load(path.join(img_folder, TITLE_5)),
                            pg.image.load(path.join(img_folder, TITLE_6)),
                            pg.image.load(path.join(img_folder, TITLE_7))]
        
        self.title_bg = pg.image.load(path.join(img_folder, TITLE_BG))

        self.level_frame = [pg.image.load(path.join(img_folder, LEVEL_0)),
                            pg.image.load(path.join(img_folder, LEVEL_1)),
                            pg.image.load(path.join(img_folder, LEVEL_2)),
                            pg.image.load(path.join(img_folder, LEVEL_3)),
                            pg.image.load(path.join(img_folder, LEVEL_4)),
                            pg.image.load(path.join(img_folder, LEVEL_5)),
                            pg.image.load(path.join(img_folder, LEVEL_6)),
                            pg.image.load(path.join(img_folder, LEVEL_7))]
        
        self.ports       = [pg.image.load(path.join(img_folder, PORT_0)),
                            pg.image.load(path.join(img_folder, PORT_1)),
                            pg.image.load(path.join(img_folder, PORT_2)),
                            pg.image.load(path.join(img_folder, PORT_3)),
                            pg.image.load(path.join(img_folder, PORT_4)),
                            pg.image.load(path.join(img_folder, PORT_5)),
                            pg.image.load(path.join(img_folder, PORT_6)),
                            pg.image.load(path.join(img_folder, PORT_7)),
                            pg.image.load(path.join(img_folder, PORT_SECRET)),]

        self.tutorial_hitbox = pg.image.load(path.join(img_folder, TUTORIAL))

        self.instructions = pg.image.load(path.join(img_folder, INSTRUCTIONS))

    # Loads the level's data
    def load_data(self, level):
        print("loading data...")
        try:
            print("loading map")
            self.map = TiledMap(path.join(game_folder, level))
        except ValueError:
            self.throw_exception(f"ValueError: Remove the offset for {self.level}.tmx")
        except:
            self.throw_exception(f"TileMapException: Check if a tilemap or a .tmx file is provided for level {self.level}.")

        self.game_details = []
        with open(path.join(game_folder, 'lvl\\level_details'), 'rt') as f:
            for line in f:
                split = line.split(',')
                self.game_details.append(split)   
        f.close()

        try:
            print(f"game details: {self.game_details[self.level]}")
            self.sum = self.game_details[self.level][0]
            self.seconds = self.game_details[self.level][1]
        except:
            self.throw_exception(f"IndexError: Some level details was not provided for level {self.level}.")

        if not self.sum.isnumeric():
            self.throw_exception(f"ValueError: {self.sum} is not an integer.")
        if int(self.sum) == 0:
            self.throw_exception("ZeroException: Sum cannot be 0.")
        
        self.map_img = self.map.makemap()
        self.map_rect = self.map_img.get_rect()


        self.radio_unlocked = self.savedata[self.level + 1]

        print(f"total needed: {self.sum}")
        print(f"clock: {self.seconds}") 
        print(f"radio unlocked: {self.radio_unlocked}") 
        
    # This creates new level
    def new(self):
        self.loading_screen()
        pg.mixer.stop()
        print("creating new level...")
        self.all_sprites.empty()
        
        self.load_data("lvl\\" + str(self.level) + ".tmx")
        self.mobs = pg.sprite.Group()
        self.turrets = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.boxes = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.numbers = pg.sprite.Group()
        self.sign = pg.sprite.Group()
        self.finish = pg.sprite.Group()
        self.tutorial = pg.sprite.Group()

        wall_id = 0
        box_id = 0
        tutorial_id = 0
        has_player = False
        has_chest = False
        has_finish = False
        self.tutorial_level = False
        self.has_radio = False

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
                if self.player.lives > 3 or self.player.lives <= 0:
                    self.anti_cheat()
                    return
                has_player = True
            if tile_object.name == 'zombie':
                Zombie(self, tile_object.x, tile_object.y)
            if tile_object.name == 'zombiex':
                LinearZombie(self, tile_object.x, tile_object.y, 'x')
            if tile_object.name == 'zombiey':
                LinearZombie(self, tile_object.x, tile_object.y, 'y')
            if tile_object.name == 'turret':
                Turret(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, wall_id)
                wall_id += 1
            if tile_object.name == 'block':
                Box(self, tile_object.x, tile_object.y, box_id)
                box_id += 1
            if tile_object.name == 'chest':
                self.chest = Chest(self, tile_object.x, tile_object.y)
                has_chest = True
            if tile_object.name == 'finish':
                self.finish = Finish(self, tile_object.x, tile_object.y)
                has_finish = True
            if tile_object.name == 'radio':
                self.radio = Radio(self, tile_object.x, tile_object.y)
                self.has_radio = True
            if tile_object.name == 'radiofinal':
                self.radiofinal = RadioFinal(self, tile_object.x, tile_object.y)
                self.has_radio = True
            if tile_object.name == 'tutorial':
                Tutorial(self, tile_object.x, tile_object.y, tutorial_id)
                tutorial_id += 1
                self.tutorial_level = True
            if tile_object.name == 'flashlight':
                self.flashlight = Flashlight(self, tile_object.x, tile_object.y)
            if tile_object.name in self.symbols:
                Sign(self, tile_object.x, tile_object.y, tile_object.name)
            if str(tile_object.name).isnumeric():
                Numbers(self, tile_object.x, tile_object.y, int(tile_object.name))

        if not has_player:
            self.throw_exception(f"PlayerObjectException: No player object has been provided on {self.level}.tmx.")
        if not has_chest:
            self.throw_exception(f"ChestObjectException: No chest object has been provided on {self.level}.tmx.")
        if not has_finish:
            self.throw_exception(f"FinishObjectException: No finish object has been provided on {self.level}.tmx.")
        if self.tutorial_level:
            self.tutorial_text = TutorialText(self)

        self.gameclock = GameClock(self, int(self.seconds.strip()))
        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    # This will run the level
    def run(self):
        print("running...")
        self.playing = True
        if self.debugger:
            print("F12 | skip puzzle")
        while self.playing:
            # Tick clock according to how many frames per seconds
            self.dt = self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw_sprites()
        print("unrunning...")

    # This will update which sprite's data changed
    def update(self):
        self.gameclock.update()
        self.all_sprites.update()
        self.camera.update(self.player)
        if self.has_radio and self.radio.sound:
            pg.mixer.music.set_volume(0.01)
        else:
            pg.mixer.music.set_volume(VOLUME)
            
    # Then draw them after it updates
    def draw_sprites(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_hud() 
        pg.display.flip()

    # Draws the HUD of the game
    def draw_hud(self):
        self.player.draw_player_health()
        self.player.draw_current_score()
        self.player.draw_current_sign()
        self.draw_objective()
        self.gameclock.draw_clock()
        if self.tutorial_level:
            self.tutorial_text.show()
        if self.player.on_finish == True:
            self.draw_text("You don't have the key!", self.undertale_font, 50, RED, WIDTH/2, HEIGHT/2, align="center")

    # Draws the GUI for the objective
    def draw_objective(self):
        img = self.objective_hud
        img_rect = img.get_rect()
        img_rect.topleft = (20, 550)
        self.screen.blit(img, img_rect)
        if int(self.player.collected_numbers) == int(self.sum):
            color = GREEN
        else:
            color = RED
        self.draw_text("Objective", self.undertale_font, 12, WHITE, 30, 560, align="w")
        self.draw_text(str(f"{self.sum}"), self.lcd_font, 25, color, 155, 593, align="e")

    # This creates and draws texts
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)    
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Catch events here
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_ESCAPE:
                    self.pause_screen()
                if event.key == pg.K_END:
                    self.ded_screen("GOD_IS_MERCILESS")
                if self.debugger and event.key == pg.K_F12:
                    self.player.collected_numbers = self.sum
                    self.player.check_match()

    # Displays the loading screen
    def loading_screen(self):
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,200))
        self.screen.blit(self.dim_screen, (0, 0))

        bug = self.zombie_stand_frame
        bug_rect = bug.get_rect()
        bug_rect.center = ((WIDTH/2), (HEIGHT/2) - 50)
        self.screen.blit(bug, bug_rect)
        if self.debugger:
            self.draw_text("D E B U G  M O D E", self.undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 + 25, align="center")
            self.draw_text("CHECK TERMINAL FOR OPTIONS", self.undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 + 50, align="center")
        else:
            self.draw_text("L O A D I N G . . .", self.undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 + 25, align="center") 
        self.draw_text("Sleepy Developers (C) 2023", self.undertale_font, 15, WHITE, WIDTH/2, HEIGHT - 75, align="center") 
        self.draw_text("Discrete Structures II", self.undertale_font, 15, WHITE, WIDTH/2, HEIGHT - 55, align="center") 
        pg.display.flip()

    # Display the Ded Screen (Windows 10 BSOD)
    def ded_screen(self, reason):
        self.playing = False
        pg.mixer.music.stop()
        if self.has_radio:
            self.radio.radiomusic.stop()

        snd = pg.mixer.Sound(path.join(snd_folder, BSOD))
        snd.play()
        print("ded screen showed")

        self.screen.fill(WIN10BLUE)
        self.draw_text(f":", self.undertale_font, 200, WHITE, 0, 135, align="w")    
        self.draw_text(f"(", self.undertale_font, 200, WHITE, 50, 150, align="w")    
        self.draw_text(f"A fatal exception has occured at level {self.level}. The current", self.undertale_font, 20, WHITE, 30, 300, align="w")
        self.draw_text(f"player will be terminated.", self.undertale_font, 20, WHITE, 30, 325, align="w")    
        self.draw_text(f"Stop code: {reason}", self.undertale_font, 20, WHITE, 30, 400, align="w")    
        self.draw_text("Press SPACE to retry the level.", self.undertale_font, 20, WHITE, WIDTH/2, 550, align="center")
        self.draw_text("Press ESC to reboot.", self.undertale_font, 20, WHITE, WIDTH/2, 575, align="center")  
        pg.display.flip()
        self.wait_for_key_bsod()

        snd.stop()

    # Displays the Pause Screen
    def pause_screen(self):
        snd = pg.mixer.Sound(path.join(snd_folder, PAUSE))
        snd.play()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,155))
        self.screen.blit(self.dim_screen, (0, 0))
        self.draw_text("Paused", self.undertale_font, 48, WHITE, WIDTH/2, HEIGHT/2, align="center")    
        self.draw_text("Press SPACE to resume.", self.undertale_font, 20, WHITE, WIDTH/2, 450, align="center")  
        self.draw_text("Press F5 to retry the level.", self.undertale_font, 20, WHITE, WIDTH/2, 475, align="center")  
        self.draw_text("Press ESC to go to title screen.", self.undertale_font, 20, WHITE, WIDTH/2, 500, align="center")  
        pg.display.flip()
        self.wait_for_key()
        snd.stop()

    # Throw exceptions
    def throw_exception(self, exception):
        # this is too much effort for a throw_exception() screen. thank you toby fox.
        pg.mixer.music.load("snd\\throw.ogg")
        pg.mixer.music.play(loops=-1)

        self.screen.fill(BLACK)
        self.draw_text(exception, self.undertale_font, 15, RED, WIDTH/2, HEIGHT - 100, align="center")
        self.draw_text("Press SPACE to crash the game and save the traceback.txt file.", self.undertale_font, 15, RED, WIDTH/2, HEIGHT - 50, align="center")
        self.draw_text("Press ESC to return to title screen.", self.undertale_font, 15, RED, WIDTH/2, HEIGHT - 25, align="center")
        dog = pg.image.load(path.join(game_folder, "img\\annoyingdog.png"))
        dog_rect = dog.get_rect()
        dog_rect.center = ((WIDTH/2), (HEIGHT/2))
        self.screen.blit(dog, dog_rect)
        pg.display.flip()
        self.wait_for_key()

        with open('traceback.txt', 'w+') as f:
            traceback.print_exc(file=f)

        raise Exception(exception)

    # Waits for the user keypress
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False
                        return
                    if event.key == pg.K_F5:
                        waiting = False
                        self.load_data("lvl\\" + str(self.level) + ".tmx")
                        self.new()
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        pg.mixer.stop()
                        self.start_screen.title_loader()
                        return

    # Waits for the user keypress
    def wait_for_key_bsod(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)/1000
            for event in pg.event.get():
                if event.type == pg.QUIT:   
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False
                        self.playing = False
                        pg.mixer.music.load(path.join(snd_folder, BGM))
                        pg.mixer.music.play(loops=-1) 
                        self.new()
                        return
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.playing = False
                        pg.mixer.stop()
                        self.start_screen.title_loader()
                        return
                
    # Call function if the user wants to quit the game
    def quit(self):
        pg.quit()
        sys.exit()

    # Function to save the data on file
    def save(self):
        f = open(path.join(game_folder, 'currentlvl'), "w+")
        for data in self.savedata:
            f.write(f"{data}\n")
        f.close()
    
    # Detects if the player's lives are below 0, above 3, or if the clock is below -1
    def anti_cheat(self):
        import ctypes
        pg.mixer.music.stop()
        mscare = pg.image.load(path.join(game_folder, "img\\mscare.png"))
        mscare_rect = mscare.get_rect()
        mscare_rect.center = ((WIDTH/2), (HEIGHT/2))
        snd = pg.mixer.Sound(path.join(snd_folder, "mscare.wav"))
        snd.play()
        self.screen.blit(mscare, mscare_rect)   
        pg.display.flip()
        ctypes.windll.user32.MessageBoxW(0, f"Are you trying to cheat, {os.getlogin()}?", "", 0)
        time.sleep(5)
        pg.mixer.stop()
        self.ded_screen("MONIKA_INTERCEPTION")


# Starts the game
g = Game()

if g.debugger:
    print("0 | start game")
    print("1 | title screen")
    print("2 | level selection")
    print("3 | player test")
    print("4 | show exception screen")
    print("5 | show prologue screen")
    print("6 | show anti cheat screen")
    print("7 | show ded screen")
    print("8 | show credits screen")
    print("9 | show epilogue screen")

    time_menu = time.time()
    while time.time() - 2 < time_menu:
        if keyboard.is_pressed("0"):
            g.story.story_loader('prologue')
            g.start_screen.title_loader()
            break
        elif keyboard.is_pressed("1"):
            g.start_screen.title_loader()
            break
        elif keyboard.is_pressed("2"):
            g.levelloader.level_loader()
            break
        elif keyboard.is_pressed("3"):
            g.level = -1
            g.load_data("lvl\\debug.tmx")
            g.mobs = pg.sprite.Group()
            g.turrets = pg.sprite.Group()
            g.walls = pg.sprite.Group()
            g.boxes = pg.sprite.Group()
            g.sign = pg.sprite.Group()
            g.numbers = pg.sprite.Group()
            g.has_radio = False
            g.tutorial_level = False
            g.finish = pg.sprite.Group()
            g.chest = Chest(g, 500, 500)
            g.finish = Finish(g, 200, 200)
            g.player = Player(g, 75, 75)
            g.gameclock = GameClock(g, 99999)
            g.camera = Camera(WIDTH, HEIGHT)
            g.run()
        elif keyboard.is_pressed("4"):
            g.throw_exception("Exception: User asked for it.")
            g.quit()
        elif keyboard.is_pressed("5"):
            g.story.story_loader('prologue')
            g.quit()
        elif keyboard.is_pressed("6"):
            g.level = -1
            g.has_radio = False
            g.anti_cheat()
            break
        elif keyboard.is_pressed("7"):
            g.level = -1
            g.has_radio = False
            g.ded_screen("MANUALLY_INITIATED_CRASH")
            break
        elif keyboard.is_pressed("8"):
            g.story.draw_congrats()
            g.quit()    
            break
        elif keyboard.is_pressed("9"):
            g.story.story_loader('epilogue')
            g.story.draw_congrats()
            g.story.ded_screen("NO_PLAYER_IN_SIMULATION")
            break

g.story.story_loader('prologue')
g.start_screen.title_loader()