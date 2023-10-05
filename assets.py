import pygame as pg
from os import path

game_folder = ""
snd_folder = path.join(game_folder, 'snd')
img_folder = path.join(game_folder, "img")

pg.mixer.init()

# FONT
UNDERTALE_FONT = path.join(img_folder, "Determination.otf")
LCD_FONT = path.join(img_folder, "LCD.ttf")

# SPRITES
ICON = pg.image.load(path.join(img_folder, "icon.png"))
TITLE_BG = pg.image.load(path.join(img_folder, "title_bg.png"))
TITLE_LOGO = [pg.image.load(path.join(img_folder, "title_1.png")),
              pg.image.load(path.join(img_folder, "title_2.png")),
              pg.image.load(path.join(img_folder, "title_3.png")),
              pg.image.load(path.join(img_folder, "title_4.png")),
              pg.image.load(path.join(img_folder, "title_5.png")),
              pg.image.load(path.join(img_folder, "title_6.png")),
              pg.image.load(path.join(img_folder, "title_7.png")),
              pg.image.load(path.join(img_folder, "title_0.png"))]

PLAYER_STAND = pg.image.load(path.join(img_folder, "frisk.png"))
PLAYER_MOVE = {
    'north':   [pg.image.load(path.join(img_folder, "frisk_0u.png")), 
                pg.image.load(path.join(img_folder, "frisk_1u.png")), 
                pg.image.load(path.join(img_folder, "frisk_2u.png")), 
                pg.image.load(path.join(img_folder, "frisk_3u.png"))],
    'south':   [pg.image.load(path.join(img_folder, "frisk_0d.png")), 
                pg.image.load(path.join(img_folder, "frisk_1d.png")), 
                pg.image.load(path.join(img_folder, "frisk_2d.png")), 
                pg.image.load(path.join(img_folder, "frisk_3d.png"))],
    'west':    [pg.image.load(path.join(img_folder, "frisk_0l.png")), 
                pg.image.load(path.join(img_folder, "frisk_1l.png")), 
                pg.image.load(path.join(img_folder, "frisk_2l.png")), 
                pg.image.load(path.join(img_folder, "frisk_3l.png"))],
    'east':    [pg.image.load(path.join(img_folder, "frisk_0r.png")), 
                pg.image.load(path.join(img_folder, "frisk_1r.png")), 
                pg.image.load(path.join(img_folder, "frisk_2r.png")), 
                pg.image.load(path.join(img_folder, "frisk_3r.png"))]
}

PLAYER_LIVES = [pg.image.load(path.join(img_folder, "morelives.png")),
                pg.image.load(path.join(img_folder, "1lives.png")),
                pg.image.load(path.join(img_folder, "2lives.png")),
                pg.image.load(path.join(img_folder, "3lives.png")),]

ZOMBIE_STAND = pg.image.load(path.join(img_folder, "zombie_0.png"))

ZOMBIE_WALK = [pg.image.load(path.join(img_folder, "zombie_0.png")),
               pg.image.load(path.join(img_folder, "zombie_1.png")),
               pg.image.load(path.join(img_folder, "zombie_2.png")),
               pg.image.load(path.join(img_folder, "zombie_3.png")),
               pg.image.load(path.join(img_folder, "zombie_4.png")),
               pg.image.load(path.join(img_folder, "zombie_5.png")),
               pg.image.load(path.join(img_folder, "zombie_6.png")),]

TURRET = pg.image.load(path.join(img_folder, "turret.png"))
BULLET = pg.image.load(path.join(img_folder, "bullet.png"))

BOX = pg.image.load(path.join(img_folder, "block.png"))

NUMBERS = {
    0: pg.image.load(path.join(img_folder, "0.png")),
    1: pg.image.load(path.join(img_folder, "1.png")),
    2: pg.image.load(path.join(img_folder, "2.png")),
    3: pg.image.load(path.join(img_folder, "3.png")),
    4: pg.image.load(path.join(img_folder, "4.png")),
    5: pg.image.load(path.join(img_folder, "5.png")),
    6: pg.image.load(path.join(img_folder, "6.png")),
    7: pg.image.load(path.join(img_folder, "7.png")),
    8: pg.image.load(path.join(img_folder, "8.png")),
    9: pg.image.load(path.join(img_folder, "9.png")),
    10: pg.image.load(path.join(img_folder, "10.png")),
}

SIGNS = {
    '+': pg.image.load(path.join(img_folder, "+.png")),
    '-': pg.image.load(path.join(img_folder, "-.png")),
    'X': pg.image.load(path.join(img_folder, "X.png")),
    'D': pg.image.load(path.join(img_folder, "D.png"))
}

CHEST = pg.image.load(path.join(img_folder, "chest.png"))
KEY = [pg.image.load(path.join(img_folder, "key_0.png")),
       pg.image.load(path.join(img_folder, "key_1.png")),
       pg.image.load(path.join(img_folder, "key_2.png")),
       pg.image.load(path.join(img_folder, "key_3.png"))]
FINISH = {
    'locked': pg.image.load(path.join(img_folder, "finish_l.png")),
    'unlocked': pg.image.load(path.join(img_folder, "finish_o.png"))
}

FLASHLIGHT = pg.image.load(path.join(img_folder, "flashlight.png"))

TIP_HITBOX = pg.image.load(path.join(img_folder, "tutorial_hitbox.png"))

CONGRATS_BG = pg.image.load(path.join(img_folder, "congrats_bg.png"))

CLOCK_HUD = pg.image.load(path.join(img_folder, "cur_timer.png"))
SCORE_HUD = pg.image.load(path.join(img_folder, "cur_score.png"))
SIGN_HUD = {
    '+': pg.image.load(path.join(img_folder, "cur_+.png")),
    '-': pg.image.load(path.join(img_folder, "cur_-.png")),
    'X': pg.image.load(path.join(img_folder, "cur_X.png")),
    'D': pg.image.load(path.join(img_folder, "cur_D.png"))
}
OBJECTIVE_HUD = pg.image.load(path.join(img_folder, "cur_objective.png"))

DOG = pg.image.load(path.join(img_folder, "annoyingdog.png"))

STORY = {
    'prologue': [pg.image.load(path.join(img_folder, "prologue_0.png")),
                 pg.image.load(path.join(img_folder, "prologue_1.png")),
                 pg.image.load(path.join(img_folder, "prologue_2.png")),
                 pg.image.load(path.join(img_folder, "prologue_3.png")),
                 pg.image.load(path.join(img_folder, "prologue_4.png")),
                 pg.image.load(path.join(img_folder, "prologue_5.png"))],
    
    'epilogue': [pg.image.load(path.join(img_folder, "epilogue_0.png")),
                 pg.image.load(path.join(img_folder, "epilogue_1.png")),
                 pg.image.load(path.join(img_folder, "epilogue_2.png")),
                 pg.image.load(path.join(img_folder, "epilogue_3.png"))]
                 
}

BLACK_DIALOGUE = pg.image.load(path.join(img_folder, "dialogue.png"))
TUTORIAL_DIALOGUE = pg.image.load(path.join(img_folder, "tutorial_dialogue.png"))

LEVEL_TEXT = {
    0: pg.image.load(path.join(img_folder, "lvltext_0.png")),
    1: pg.image.load(path.join(img_folder, "lvltext_1.png")),
    2: pg.image.load(path.join(img_folder, "lvltext_2.png")),
    3: pg.image.load(path.join(img_folder, "lvltext_3.png")),
    4: pg.image.load(path.join(img_folder, "lvltext_4.png")),
    5: pg.image.load(path.join(img_folder, "lvltext_5.png")),
    6: pg.image.load(path.join(img_folder, "lvltext_6.png")),
    7: pg.image.load(path.join(img_folder, "lvltext_7.png")),
}

PORTS = {
    0: pg.image.load(path.join(img_folder, "port_0.png")),
    1: pg.image.load(path.join(img_folder, "port_1.png")),
    2: pg.image.load(path.join(img_folder, "port_2.png")),
    3: pg.image.load(path.join(img_folder, "port_3.png")),
    4: pg.image.load(path.join(img_folder, "port_4.png")),
    5: pg.image.load(path.join(img_folder, "port_5.png")),
    6: pg.image.load(path.join(img_folder, "port_6.png")),
    7: pg.image.load(path.join(img_folder, "port_7.png")),
    'credits': pg.image.load(path.join(img_folder, "port_credits.png")),
}

# SOUND
START = pg.mixer.Sound(path.join(snd_folder, "start.wav"))
HURT = pg.mixer.Sound(path.join(snd_folder, 'hurt.wav'))
BSOD = pg.mixer.Sound(path.join(snd_folder, "bluescreen.wav"))
TYPE = pg.mixer.Sound(path.join(snd_folder, "txt.wav"))
PAUSE = pg.mixer.Sound(path.join(snd_folder, "pause.wav"))
TADA = pg.mixer.Sound(path.join(snd_folder, "unlockall.wav"))
PICK = pg.mixer.Sound(path.join(snd_folder, "pick.wav"))
SIGN = pg.mixer.Sound(path.join(snd_folder, "sign.wav"))
EXPLODE = pg.mixer.Sound(path.join(snd_folder, "explode.wav"))
KEYSPAWN = pg.mixer.Sound(path.join(snd_folder, "bell.wav"))
KEYGET = pg.mixer.Sound(path.join(snd_folder, "grab.wav"))
NOPE = pg.mixer.Sound(path.join(snd_folder, "nope.wav"))
TIP = pg.mixer.Sound(path.join(snd_folder, "tip.wav"))
DETECT = pg.mixer.Sound(path.join(snd_folder, "!.wav"))
NEXT = pg.mixer.Sound(path.join(snd_folder, "next.wav"))
SHOOT = pg.mixer.Sound(path.join(snd_folder, "arrow.wav"))

# BGM
TITLE_BGM = path.join(snd_folder, "title.ogg")
TITLE_ALL_BGM = path.join(snd_folder, "title_all.ogg")
GAME_BGM = path.join(snd_folder, 'mus_core.ogg')
CREDITS = path.join(snd_folder, 'congrats.ogg')
STORY_BGM = {
    'prologue': path.join(snd_folder, 'prologue.ogg'),
    'epilogue': path.join(snd_folder, 'epilogue.ogg')
}