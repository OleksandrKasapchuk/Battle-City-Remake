from constants import *
from abc import ABC, abstractmethod
from pygame import *
from map import *


class Player(sprite.Sprite): 
    def __init__(self, size_x, size_y, player_x, player_y, player_speed): 
        super().__init__() 
        
        self.up1 = transform.scale(image.load("tanks/player1.png"), (size_x, size_y)) 
        self.up2 = transform.scale(image.load("tanks/player2.png"), (size_x, size_y))
        self.image = self.up1
        self.ups = [self.up1, self.up2]
        self.downs = [transform.flip(self.up1, False, True), transform.flip(self.up2, False, True)]
        self.rights = [transform.rotate(self.up1, 270), transform.rotate(self.up2, 270)]
        self.lefts = [transform.flip(transform.rotate(self.up1, 270), True, False), transform.flip(transform.rotate(self.up2, 270), True, False)]

        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.size_x, self.size_y = size_x, size_y

        self.index = 0
        self.counter = 0
        self.direction = 0

    def reset(self): 
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 1
        keys = key.get_pressed() 
        if keys[K_d] or keys[K_RIGHT] and self.rect.x < 780: 
            dx = self.speed
            self.counter += 1
            self.direction = 1
        elif keys[K_a] or keys[K_LEFT] and self.rect.x > 0:
            dx = -self.speed
            self.counter += 1
            self.direction = -1
        elif keys[K_w] or keys[K_UP] and self.rect.y > 0:
            dy = -self.speed
            self.counter += 1
            self.direction = 2
        elif keys[K_s] or keys[K_DOWN] and self.rect.y < 780:
            dy = self.speed
            self.counter += 1
            self.direction = -2

        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size_x, self.size_y):
                dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size_x, self.size_y):
                dy = 0
            
            
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
            if self.index >= len(self.rights):
                self.index = 0
            if self.direction == 1:
                self.image = self.rights[self.index]
            if self.direction == -1:
                self.image = self.lefts[self.index]
            
            if self.direction == 2:
                self.image = self.ups[self.index]
            if self.direction == -2:
                self.image = self.downs[self.index]
    
        self.rect.x += dx
        self.rect.y += dy

class Scene(ABC):
    @abstractmethod
    def update(self):
        pass

class GameScene(Scene):
    def __init__(self):
        self.main_character = Player(60, 60, 400, 450, 5)
        self.map = map1
        self.world = World(map1)

    def update(self):
        WINDOW.fill(BLACK_COLOR)
        self.main_character.reset()
        self.main_character.update()
        self.world.draw()

game = GameScene()
