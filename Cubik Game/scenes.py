#імпортуємо файли
from constants import *
from abc import ABC, abstractmethod
from pygame import *
from map import *
from sprites import *
from logger import *

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (0,255,0))
lose = font1.render('YOU LOST!', True, (255,0,0))

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
        self.base = baza
        self.tanks_group = tanks_group
        self.heart_image_red = transform.scale(image.load("assets/images/heart_red.png"), (20, 20))
        self.heart_image_white = transform.scale(image.load("assets/images/heart_white.png"), (20, 20))
    #оновлення сцени гри
    def update(self):
        WINDOW.blit(play_background,(0,0))
        #промальовка персонажів
        for tank in self.tanks_group:
            tank.reset()
            tank.update()
        self.main_character.reset()
        self.main_character.update()
        self.world.draw()
        self.base.reset()

            

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

        # Перевірка, чи всі танки мертві
        all_tanks_dead = all(not tank.alive for tank in tanks_group)

        if all_tanks_dead:
            # Тут вводьте код для обробки перемоги
            WINDOW.fill(BLACK_COLOR)
            WINDOW.blit(win, (200,200))
            play = False
            finish = True

    def on_lose_game(self):
        WINDOW.fill(BLACK_COLOR)
        WINDOW.blit(lose, (200,200))
        play = False
        finish = True
        
        
game = GameScene()
