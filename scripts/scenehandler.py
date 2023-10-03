import pygame as pg
from scenes import game, story, title, level, deadscreen, credits, gameover

class Scene():
    def __init__(self, main, scene = None):
        self.__scene = scene
        self.main = main
    
    def set_scene(self, scene):
        self.__scene = scene

    def load_scene(self):
        match self.__scene:
            case None | 'prologue':
                story.Story(self.main, 'prologue')
                return
            case 'title':
                title.TitleScreen(self.main)
                return
            case 'level':
                level.LevelScreen(self.main)
            case 'game':
                game.GameScreen(self.main, self.main.gamehandler.get_level())
                return
            case 'dead':
                deadscreen.DeadScreen(self.main, self.main.gamehandler.get_reason(), self.main.gamehandler.get_level())
            case 'epilogue':
                story.Story(self.main, 'epilogue')
                return
            case 'credits':
                credits.Credits(self.main)
                return
            case 'gameover':
                gameover.GameOver(self.main, "NO_PLAYER_IN_SIMULATION")
                return
            case _:
                raise Exception(f"SceneException: '{self.__scene}' does not exist.")