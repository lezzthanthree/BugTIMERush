import pygame as pg
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        
        self.width = width
        self.height = height

    # Apply the camera to the player
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    # Move the camera when the player moves
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    # Update the position of the camera
    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        x = min(0, x)
        y = min(0, y)

        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
