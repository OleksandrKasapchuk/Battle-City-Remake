#імпортуємо файли
from constants import *
from abc import ABC, abstractmethod
from pygame import *
from map import *
from sprites import *
from logger import *

#асбтрактний клас сцени
class Scene(ABC):
    @abstractmethod
    def update(self):
        pass

#клас сцени гри
class GameScene(Scene):
    def __init__(self):
        self.main_character = player
        self.map = map1
        self.world = world
        self.base = GameSprite("assets/images/baza.png", 0, 385, 770, 64, 64, 0)
        self.fast_tank = FastTank(0, 120)
        self.armored_tank = ArmoredTank(450, 100)
        self.tanks_group = sprite.Group(self.fast_tank, self.armored_tank)
        self.heart_image_red = transform.scale(image.load("assets/images/heart_red.png"), (20, 20))
        self.heart_image_white = transform.scale(image.load("assets/images/heart_white.png"), (20, 20))
    #оновлення сцени гри
    def update(self):
        WINDOW.fill(BLACK_COLOR)
        #промальовка персонажів
        self.main_character.reset()
        self.main_character.update()
        self.world.draw()
        self.base.reset()

        for tank in self.tanks_group:
            tank.reset()
            tank.update()
            

        current_health = self.main_character.health
        max_health = self.main_character.max_health

        heart_width = 20
        #показ життів
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

#об'єкт сцени
game = GameScene()
