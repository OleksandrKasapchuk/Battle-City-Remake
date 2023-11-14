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
        self.main_character = Player(58, 58, 400, 450, 5, max_health)
        self.map = map1
        self.world = world

        self.heart_image_red = transform.scale(image.load("assets/images/heart_red.png"), (20, 20))
        self.heart_image_white = transform.scale(image.load("assets/images/heart_white.png"), (20, 20))

    def update(self):
        WINDOW.fill(WHITE_COLOR)
        self.main_character.reset()
        self.main_character.update()
        self.world.draw()

        current_health = self.main_character.health
        max_health = self.main_character.max_health

        heart_width = 20

        for i in range(max_health):
            heart_x = WIN_WIDTH - 10 - (i + 1) * (heart_width + 20) 
            heart_y = 10  

            if i < current_health:
                WINDOW.blit(self.heart_image_red, (heart_x, heart_y))
            else:
                WINDOW.blit(self.heart_image_white, (heart_x, heart_y))

        if current_health == 0:
            self.on_lose_game()

        if fired:
            self.main_character.bullet.reset()
            self.main_character.bullet.update()

    def on_lose_game(self):
        print("Game Over. You lost!")

game = GameScene()
