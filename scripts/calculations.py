from assets import EXPLODE, KEYSPAWN
from sprites import goals

def calculate(game, number, player):
    sign = player.current_sign
    if sign == '+':
        player.total += number
    if sign == '-':
        player.total -= number
    if sign == 'X':
        player.total *= number
    if sign == 'D':
        if number == 0:
            EXPLODE.play()
            game.main.gamehandler.set_reason("BLACK_HOLE_DESTRUCTION")
            game.main.scene.set_scene('dead')
            game.playing = False
            return
        player.total = int(player.total/number)

def check_match(game, player):
    if int(game.level.sum) == int(player.total):
        for sprites in game.sprites.numbers:
            sprites.kill()
        for sprites in game.sprites.signs:
            sprites.kill()
        KEYSPAWN.play()
        goals.Key(game, game.sprites.chest.pos.x, game.sprites.chest.pos.y)
        game.sprites.chest.kill()
