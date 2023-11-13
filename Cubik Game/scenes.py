from constants import *
from abc import ABC, abstractmethod
from pygame import *
from map import *
from sprites import *
from logger import *

class Scene(ABC):
    @abstractmethod
    def update(self):
        pass

class GameScene(Scene):
    def __init__(self):
        self.main_character = Player(58, 58, 400, 450, 5)
        self.map = map1
        self.world = world

    def update(self):
        WINDOW.fill(BLACK_COLOR)
        self.main_character.reset()
        self.main_character.update()
        self.world.draw()

        if fired:
            self.main_character.bullet.reset()
            self.main_character.bullet.update()

game = GameScene()
