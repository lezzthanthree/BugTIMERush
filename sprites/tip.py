import pygame as pg
from assets import *
from ui import draw_text
from settings import *

vec = pg.math.Vector2

text = {
    0: [["That is a number tile.", "Picking it will be calculated according to your current arithmetic."],
        ["That is an arithmetic tile.", "It will change your current addition to multiplication."],
        ["Now, try taking that number tile.", "It will multiply your score."],
        ["Your current score is now 45.", "However, we went over the objective. Let's subtract some numbers."],
        ["Taking that number will subtract your", "current score."],
        ["Be aware of the mobs on the level you are in!", "You only have three lives, so be cautious!"],
        ["Exacting your score to the objective will open the chest", "that will lead you to the next level."],
        ["What are you even doing here?", "There's nothing to see here."]],
    2: [["Subtraction, huh...", "I'll try using them if ever I miscalculate."]],
    3: [["Now, multiplication!?", "Darn, I can't even hold big numbers well..."]],
    4: [["Division...", "Will this be ever handy later?"]],
    5: [["Wow, I can't see...", "I still have time to roam around first."], 
        ["If only I can use the blocks", "as my shield..."]],
    6: [["I need 128 first...", ""],
        ["Next, I think, I need to get down by 88...", ""],
        ["Great, on the objective...", ""]]
}

class Tip(pg.sprite.Sprite):
    def __init__(self, game, x, y, id):
        self._layer = 1
        self.groups = game.sprites.all_sprites, game.sprites.tips
        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = TIP_HITBOX
        self.rect = self.image.get_rect()
        self.id = id
        self.on_block = False
        self.pos = vec(x, y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def collision_with_player(self):
        hits = pg.sprite.collide_rect(self, self.game.sprites.player)
        if hits:
            if not self.on_block:
                TIP.play()
            self.on_block = True
            self.game.sprites.tip_text.set_id(self.id)
            self.game.sprites.tip_text.set_bool(True)
        
        if not hits and self.on_block:
            self.on_block = False
            self.game.sprites.tip_text.set_bool(False)
            self.kill()

    def update(self):
        self.collision_with_player()

class TipText():
    def __init__(self, game):
        self.game = game
        self.id = 0
        self.show_text = False

    def show(self):
        text_to_show = ''
        level = self.game.main.gamehandler.get_level()
        if self.show_text:
            dialogue_rect = TUTORIAL_DIALOGUE.get_rect()
            dialogue_rect.topleft = (0, 0)
            self.game.main.screen.blit(TUTORIAL_DIALOGUE, dialogue_rect)
            draw_text(self.game.main, str(text[level][self.id][0]), UNDERTALE_FONT, 15, WIDTH/2, 435, align="center")
            draw_text(self.game.main, str(text[level][self.id][1]), UNDERTALE_FONT, 15, WIDTH/2, 460, align="center")

    def set_id(self, id):
        self.id = id

    def set_bool(self, condition):
        self.show_text = condition

    def update(self):
        self.show()