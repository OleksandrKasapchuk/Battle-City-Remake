from constants import *
from abc import ABC, abstractmethod
from pygame import *
from map import *


class Sprite(sprite.Sprite):
    @abstractmethod
    def reset(self):
        pass
    def update(self):
        pass

class Player(Sprite): 
    def __init__(self, player_image, size_x, size_y, player_x, player_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.size_x, self.size_y = size_x, size_y 
        self.jumped = False
        self.vel_y = 0
        self.direction = 0
    def reset(self): 
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        dx = 0
        keys = key.get_pressed() 
        if keys[K_d] or keys[K_RIGHT]: 
            print('go right')
            self.rect.x += self.speed

        elif keys[K_a] or keys[K_LEFT]:
            print('go left')
            self.rect.x -= self.speed
    
        if keys[K_SPACE] and self.jumped == False:
            self.vel_y = -12
            self.jumped=True
        self.rect.y += self.vel_y

class Scene(ABC):
    @abstractmethod
    def update(self):
        pass

class GameScene(Scene):
    def __init__(self):
        #Логіка створень класів персонажів
        #print(gl.HP)
        self.main_character = Player("assets/images/test.jpg", 100, 100, 500, 500, 10)
        self.map = map1
        self.world = World(map1)

    def update(self):
        WINDOW.fill(BLUE_COLOR)
        self.main_character.reset()
        self.main_character.update()
        self.world.draw()
