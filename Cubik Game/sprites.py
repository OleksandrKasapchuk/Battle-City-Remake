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
        
        self.up1 = transform.scale(image.load("tanks_textures/player1.png"), (size_x, size_y)) 
        self.up2 = transform.scale(image.load("tanks_textures/player2.png"), (size_x, size_y))
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
        self.bullets = sprite.Group()
        self.last_shot_time = -5000  # Змінна для відстеження часу останнього вистрілу
        self.shoot_cooldown = 5000  # Затримка між вистрілами у мілісекундах

    def reset(self): 
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))
        self.bullets.update()
        self.bullets.draw(WINDOW)

    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 1
        current_time = time.get_ticks()
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
        elif keys[K_SPACE]:# and current_time - self.last_shot_time > self.shoot_cooldown:
            self.fire()
            self.last_shot_time = current_time

        for bullet in self.bullets:
            bullet.update()

        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size_x, self.size_y) and tile not in bushes:
                dx = 0
                
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size_x, self.size_y) and tile not in bushes:
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
        

    def fire(self):
        bullet = Bullet("assets/images/bullet.png", 10, self.rect.centerx, self.rect.top, 45, 45, self.direction)
        self.bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        pass

class Bullet(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y, direction):
        super().__init__(player_image, player_speed, player_x, player_y, size_x, size_y, direction)

        if direction in [1, -1]:
            self.rotation = 270 if direction == 1 else 90
            self.image = transform.flip(self.image, True, False)
        elif direction in [2, -2]:
            self.rotation = 0 if direction == 2 else 180

        self.image = transform.rotate(self.image, self.rotation)

    def update(self):
        if self.direction == 1:
            self.rect.x += self.speed
        elif self.direction == -1:
            self.rect.x -= self.speed
        elif self.direction == 2:
            self.rect.y -= self.speed
        elif self.direction == -2:
            self.rect.y += self.speed

