from pygame import *
from constants import *
from map import * 
from logger import *
from scenes import *
from random import choice,random

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
    def __init__(self, size_x, size_y, player_x, player_y, player_speed,max_health): 
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
        self.last_shot_time = -3000  
        self.shoot_cooldown = 3000
        # 
        self.shooting = False
        self.max_health = max_health
        self.health = max_health
        #
          

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

        if keys[K_SPACE] and current_time - self.last_shot_time > self.shoot_cooldown:
            self.fire()
            self.last_shot_time = current_time
            self.shooting = True

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
        bullet = Bullet("assets/images/bullet.png", 10, self.rect.centerx, self.rect.top, 45, 45, self.direction, False)
        self.bullets.add(bullet)

player = Player(58, 58, 400, 450, 5, max_health)


class Tank(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y, direction, health):
        super().__init__(player_image, player_speed, player_x, player_y, size_x, size_y, direction)
        self.original_image = self.image
        self.wall_collision = False
        self.health = health  # Додаємо параметр здоров'я

    def update(self):
        dx, dy = 0, 0
        
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) and tile not in bushes:
                self.wall_collision = True
                dx = 0

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) and tile not in bushes:
                self.wall_collision = True
                dy = 0





        if self.wall_collision:
            random_number = random()
            if random_number < 0.4:  # 40% probability
                player_directions = [player.direction, -player.direction]
                possible_directions = list(set([1, -1, 2, -2, *player_directions]))
                possible_directions.remove(-self.direction) 
                self.direction = choice(possible_directions)
            else:
                rotate_probability = random()
                if rotate_probability < 0.5: 
                    rotate_amount = choice([90, 180]) 
                    self.direction = self.rotate_direction(self.direction, rotate_amount)

            self.wall_collision = False

            self.rect.x = round(self.rect.x / tile_size) * tile_size
            self.rect.y = round(self.rect.y / tile_size) * tile_size

        # 1 право, -1 ліво,2 вверх,-2 вниз
        if self.direction == 1:
            dx += self.speed
            self.image = transform.rotate(self.original_image, -90)  # Rotate 90 degrees for right direction
        elif self.direction == -1:
            dx -= self.speed
            self.image = transform.rotate(self.original_image, 90)  # Rotate -90 degrees for left direction
        elif self.direction == 2:
            dy -= self.speed
            self.image = transform.rotate(self.original_image, 0)  # Rotate 180 degrees for up direction
        elif self.direction == -2:
            dy += self.speed
            self.image = transform.rotate(self.original_image, 180)  # Rotate 180 degrees for up direction

        self.rect.x += dx
        self.rect.y += dy

        self.wall_collision = False  # Reset wall collision to avoid constant direction changes

    @staticmethod
    def rotate_direction(direction, angle):
        # Rotate the direction by the specified angle
        if direction == 1:
            return -1 if angle == 90 else 2
        elif direction == -1:
            return 1 if angle == 90 else -2
        elif direction == 2:
            return 1 if angle == 90 else -1
        elif direction == -2:
            return -1 if angle == 90 else 1
        return direction  # Return the same direction if not 90 or 180 degrees


    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()


class FastTank(Tank):
    def __init__(self, player_x, player_y):
        super().__init__("tanks_textures/speed1.png", 3, player_x, player_y, 50, 50, 1, 1)

class ArmoredTank(Tank):
    def __init__(self, player_x, player_y):
        super().__init__("tanks_textures/fat1.png", 2, player_x, player_y, 50, 50, 1, 3)




class Bullet(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y, direction, exploded):
        super().__init__(player_image, player_speed, player_x, player_y, size_x, size_y, direction)

        self.explosion_images = [transform.scale(image.load("assets/images/exp1.png"), (50, 50)),
                                 transform.scale(image.load("assets/images/exp2.png"), (50, 50)),
                                 transform.scale(image.load("assets/images/exp3.png"), (50, 50))]
        
        self.explosion_index = 0
        self.explosion_counter = 0
        self.explosion_duration = 10
        self.exploded = exploded
        self.size_x = size_x 
        self.size_y = size_y 

        if direction in [1, -1]: 
            self.rotation = 270 if direction == 1 else 90 
            self.image = transform.flip(self.image, True, False) 
        elif direction in [2, -2]: 
            self.rotation = 0 if direction == 2 else 180 
 
        self.image = transform.rotate(self.image, self.rotation) 
 
        if direction == 1: 
            self.rotation = 180 
            self.image = transform.flip(self.image, True, False) 
            self.side_offset = 3 
            self.up_down_offset = 5 
 
        elif direction == -1: 
            self.rotation = 0 
            self.side_offset = -43 
            self.up_down_offset = 6 
 
        elif direction == 2: 
            self.rotation = 0 
            self.side_offset = -22 
            self.up_down_offset = -25 
 
        elif direction == -2: 
            self.rotation = 0 
            self.side_offset = -21.5 
            self.up_down_offset = 30 
 
        #self.image = transform.rotate(self.image, self.rotation) 
        self.rect.x += self.side_offset 
        self.rect.y += self.up_down_offset

    def update(self):
        if not self.exploded:
            dx, dy = 0, 0
            if self.direction == 1:
                dx += self.speed
            elif self.direction == -1:
                dx -= self.speed
            elif self.direction == 2:
                dy -= self.speed
            elif self.direction == -2:
                dy += self.speed
        
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x, self.rect.y, self.size_x, self.size_y) and tile in touchabels:
                    self.explode()
                    self.show_explosion()
                    if tile in bricks:
                        world.tile_list.remove(tile)

            self.rect.x += dx
            self.rect.y += dy
            
    def explode(self):
        self.kill()
        self.exploded = True

    def show_explosion(self):
        if self.explosion_counter < self.explosion_duration:
            WINDOW.blit(self.explosion_images[self.explosion_index], (self.rect.x, self.rect.y))
            self.explosion_counter += 1

            if player.rect.colliderect(self.rect.x, self.rect.y, self.size_x, self.size_y):
                player.health -= 1
        else:
            self.explosion_counter = 0
            self.explosion_index += 1
            if self.explosion_index >= len(self.explosion_images):
                self.exploded = False
                self.explosion_index = 0
