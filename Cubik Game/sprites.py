from pygame import *
from constants import *
from map import * 
from logger import *

class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_speed, player_x, player_y, size_x, size_y, direction):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x , size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = direction

    def reset(self):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))


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
        

class Enemy(GameSprite):
    def update(self):
        pass

class Bullet(GameSprite):
    def update(self):
        if self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == -1:
            self.rect.x -= self.speed
        elif self.direction == 2:
            self.rect.y -= self.speed
        elif self.direction == -2:
            self.rect.y += self.speed
        '''
        if self.rect.y > WIN_HEIGHT or self.rect.x > WIN_WIDTH or self.rect.y < 0 or self.rect.x < 0:
            self.kill()
            fired = False
        '''