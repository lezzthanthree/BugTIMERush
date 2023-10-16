import pygame as pg
import sys
from settings import *
from assets import *
from scripts import scenehandler, gamehandler
from ui import loading_screen

class Game:
    def __init__(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.display.set_icon(ICON)

        self.gamehandler = gamehandler.Game()
        self.scene = scenehandler.Scene(self)
        
    def start(self):
        loading_screen(self)
        while True:
            self.scene.load_scene()
        
    def quit(self):
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        g = Game()
        g.start()
    except Exception as e:
        import ctypes
        import traceback
        ctypes.windll.user32.MessageBoxW(0, f"An exception has occured. \n\n{str(e)}\n\nCheck the traceback.txt for more details.", "Error", 0x10)
        with open('traceback.txt', 'w+') as f:
            traceback.print_exc(file=f)

        traceback.print_exc()