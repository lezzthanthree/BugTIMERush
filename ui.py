import pygame as pg
from settings import *
from assets import *

def draw_text(game, text, font_name, size, x, y, color=(255,255,255), align="nw"):
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
    game.screen.blit(text_surface, text_rect)

def loading_screen(game):
    dim_screen = pg.Surface(game.screen.get_size()).convert_alpha()
    dim_screen.fill((0,0,0,200))
    game.screen.blit(dim_screen, (0, 0))

    bug_rect = ZOMBIE_STAND.get_rect()
    bug_rect.center = ((WIDTH/2), (HEIGHT/2) - 50)
    game.screen.blit(ZOMBIE_STAND, bug_rect)
    # if debugger:
    #     draw_text("D E B U G  M O D E", undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 + 25, align="center")
    #     draw_text("CHECK TERMINAL FOR OPTIONS", undertale_font, 20, WHITE, WIDTH/2, HEIGHT/2 + 50, align="center")
    # else:
    draw_text(game, "L O A D I N G . . .", UNDERTALE_FONT, 20, WIDTH/2, HEIGHT/2 + 25, align="center") 
    draw_text(game, "Sleepy Developers (C) 2023", UNDERTALE_FONT, 15, WIDTH/2, HEIGHT - 75, align="center") 
    draw_text(game, "Discrete Structures II", UNDERTALE_FONT, 15, WIDTH/2, HEIGHT - 55, align="center") 
    pg.display.flip()

def quit_screen(game):
    dim_screen = pg.Surface(game.main.screen.get_size()).convert_alpha()
    dim_screen.fill((0,0,0,155))
    game.main.screen.blit(dim_screen, (0, 0))
    draw_text(game.main, "Quit?", UNDERTALE_FONT, 48, WIDTH/2, HEIGHT/2, align="center")    
    draw_text(game.main, "Press ESC again to quit.", UNDERTALE_FONT, 20, WIDTH/2, 450, align="center")  
    draw_text(game.main, "Press SPACE to cancel.", UNDERTALE_FONT, 20, WIDTH/2, 475, align="center")  
    pg.display.flip()
    wait_for_key_quit(game)

def pause_screen(game):
    PAUSE.play()
    dim_screen = pg.Surface(game.main.screen.get_size()).convert_alpha()
    dim_screen.fill((0,0,0,155))
    game.main.screen.blit(dim_screen, (0, 0))
    draw_text(game.main, "Paused", UNDERTALE_FONT, 48, WIDTH/2, HEIGHT/2, align="center")    
    draw_text(game.main, "Press SPACE to resume.", UNDERTALE_FONT, 20, WIDTH/2, 450, align="center")  
    draw_text(game.main, "Press F5 to retry the level.", UNDERTALE_FONT, 20, WIDTH/2, 475, align="center")  
    draw_text(game.main, "Press ESC to go to title screen.", UNDERTALE_FONT, 20, WIDTH/2, 500, align="center")  
    pg.display.flip()
    wait_for_key_pause(game)
    PAUSE.stop()

def wait_for_key_pause(game):
    waiting = True
    while waiting:
        game.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:   
                game.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    waiting = False
                    return
                if event.key == pg.K_F5:
                    waiting = False
                    game.playing = False
                if event.key == pg.K_ESCAPE:
                    game.playing = False
                    game.main.scene.set_scene('title')
                    return

def wait_for_key_quit(game):
    waiting = True
    while waiting:
        game.main.clock.tick(FRAMES)/1000
        for event in pg.event.get():
            if event.type == pg.QUIT:   
                game.main.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    waiting = False
                    return
                if event.key == pg.K_ESCAPE:
                    game.main.quit()
                    return
