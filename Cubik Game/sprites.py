#імпортуємо модулі
from pygame import *
from constants import *
from map import * 
from logger import *
from scenes import *
from random import choice,random

tanks_group = sprite.Group()

#клас спрайтів
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

#клас гравця
class Player(sprite.Sprite): 
    def __init__(self, size_x, size_y, player_x, player_y, player_speed,max_health): 
        super().__init__() 
        #зображення гравця
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
        self.last_shot_time = -2000  
        self.shoot_cooldown = 3000
        self.shooting = False
        self.max_health = max_health
        self.health = max_health
        
          
    #промальовка гравця
    def reset(self): 
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))
        self.bullets.update()
        self.bullets.draw(WINDOW)
    #оновлення гравця
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
            fire_sound.set_volume(0.04)
            fire_sound.play()
            self.fire()
            self.last_shot_time = current_time
            self.shooting = True

        for bullet in self.bullets:
            bullet.update()

        for tile in world.tile_list:
            #колізія по х
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size_x, self.size_y) and tile not in bushes:
                dx = 0
                
            #колізія по у
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size_x, self.size_y) and tile not in bushes:
                dy = 0
        #анімація
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
        #рух
        self.rect.x += dx
        self.rect.y += dy
        

    def fire(self):
        #створення кулі(постріл)
        bullet = Bullet("assets/images/bullet.png", 10, self.rect.centerx, self.rect.top, 45, 45, self.direction, False)
        self.bullets.add(bullet)

player = Player(58, 58, 400, 575, 5, max_health)

class Tank(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y, direction, health):
        super().__init__(player_image, player_speed, player_x, player_y, size_x, size_y, direction)

        self.original_image = self.image
        self.wall_collision = False
        self.health = health
        self.last_shot_time = -3000
        tanks_group.add(self)
        self.bullets = sprite.Group()
        self.alive = True

    def update(self):
        dx, dy = 0, 0
        walk_cooldown = 1

        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) and tile not in bushes:
                self.wall_collision = True
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) and tile not in bushes:
                self.wall_collision = True
                dy = 0

        if self.rect.x + dx < 0:
            dx = -self.rect.x
            self.direction = self.rotate_direction(self.direction,180)

        elif self.rect.x + dx + self.rect.width > WIN_WIDTH:
            dx = WIN_WIDTH - self.rect.x - self.rect.width
            self.direction = self.rotate_direction(self.direction,180)

        if self.rect.y + dy < 0:
            dy = -self.rect.y
            self.direction = self.rotate_direction(self.direction,180)
            
        elif self.rect.y + dy + self.rect.height > WIN_HEIGHT:
            dy = WIN_HEIGHT - self.rect.y - self.rect.height
            self.direction = self.rotate_direction(self.direction,180)





        if self.wall_collision:
            random_number = random()
            if random_number < 0.4:  # 40% шанс
                player_directions = [player.direction, -player.direction]
                possible_directions = list(set([1, -1, 2, -2, *player_directions]))
                possible_directions.remove(-self.direction)  # видаляє протилежний напрямок
                self.direction = choice(possible_directions)
            else:
                rotate_probability = random()
                if rotate_probability < 0.5:  # 50% шанс
                    rotate_amount = choice([90, 180])  # повертає на 90 або 180 градусів
                    self.direction = self.rotate_direction(self.direction, rotate_amount)
                else:
                    if self.direction == 1:
                        self.direction = -2
                    elif self.direction == -1:
                        self.direction = 2
                    elif self.direction == 2:
                        self.direction = 1
                    elif self.direction == -2:
                        self.direction = -1

            self.wall_collision = False

            self.rect.x = round(self.rect.x / tile_size) * tile_size
            self.rect.y = round(self.rect.y / tile_size) * tile_size

        if self.direction == 1:
            dx += self.speed
            self.image = transform.rotate(self.original_image, -90)  # 0 градусів для напрямку вправо
        elif self.direction == -1:
            dx -= self.speed
            self.image = transform.rotate(self.original_image, 90)  # 180 градусів для напрямку вліво
        elif self.direction == 2:
            dy -= self.speed
            self.image = transform.rotate(self.original_image, 0)  # 90 градусів для напрямку вгору
        elif self.direction == -2:
            dy += self.speed
            self.image = transform.rotate(self.original_image, 180)  # -90 градусів для напрямку вниз

        self.rect.x += dx
        self.rect.y += dy

        current_time = time.get_ticks()
        if current_time - self.last_shot_time >= 3500:
            self.last_shot_time = current_time
            self.fire()

    def reset(self): 
        WINDOW.blit(self.image, self.rect.topleft)
        self.bullets.update()
        self.bullets.draw(WINDOW)

    @staticmethod
    def rotate_direction(direction, angle):
        if direction == 1:
            return -1 if angle == 90 else 2
        elif direction == -1:
            return 1 if angle == 90 else -2
        elif direction == 2:
            return 1 if angle == 90 else -1
        elif direction == -2:
            return -1 if angle == 90 else 1
        return direction

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            self.kill()

            

#клас швидкого танка
class FastTank(Tank):
    def __init__(self, player_x, player_y):
        super().__init__("tanks_textures/speed1.png", 5, player_x, player_y, 50, 50, 1, 1)

    def fire(self):
        #створення кулі(постріл)
        bullet = Bullet("assets/images/bullet.png", 10, self.rect.centerx, self.rect.top, 45, 45, self.direction, False)
        fire_sound.set_volume(0.04)
        fire_sound.play()
        self.bullets.add(bullet)

#клас броньованого танка
class ArmoredTank(Tank):
    def __init__(self, player_x, player_y):
        super().__init__("tanks_textures/fat1.png", 2, player_x, player_y, 50, 50, 1, 3)

    def fire(self):
        #створення кулі(постріл)
        bullet = Bullet("assets/images/bullet.png", 10, self.rect.centerx, self.rect.top, 45, 45, self.direction, False)
        fire_sound.set_volume(0.04)
        fire_sound.play()
        self.bullets.add(bullet)

fast_tank1 = FastTank(21, 640)
fast_tank2 = FastTank(192, 119)
fast_tank3 = FastTank(518, 322)

armored_tank1 = ArmoredTank(633, 640)
armored_tank2 = ArmoredTank(640, 64)
armored_tank2 = ArmoredTank(510, 128)

baza = GameSprite("assets/images/baza.png", 0, 385, 770, 64, 64, 0)

#клас кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_speed, player_x, player_y, size_x, size_y, direction, exploded):
        super().__init__(player_image, player_speed, player_x, player_y, size_x, size_y, direction)

        self.explosion_images = [transform.scale(image.load("assets/images/exp1.png"), (50, 50)),
                                 transform.scale(image.load("assets/images/exp2.png"), (50, 50)),
                                 transform.scale(image.load("assets/images/exp3.png"), (50, 50))]
        self.side_offset = 0
        self.up_down_offset = 0
        self.rotation = 0
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

        self.rect.x += self.side_offset 
        self.rect.y += self.up_down_offset
    
    def update(self):
        dx, dy = 0, 0
        #пересування
        if self.direction == 1:
            dx += self.speed
        elif self.direction == -1:
            dx -= self.speed
        elif self.direction == 2:
            dy -= self.speed
        elif self.direction == -2:
            dy += self.speed
        if self.exploded:
            self.explode()
            self.show_explosion()


        #колізія
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y, self.size_x, self.size_y) and tile in touchabels:
                self.exploded = True
                if tile in bricks:
                    tile[2] -= 1
                    tile[0] = brick_b_img
                    if tile[2] < 0:
                        world.tile_list.remove(tile)
    
        for tank in tanks_group:
            if tank.rect.colliderect(self.rect.x, self.rect.y, self.size_x, self.size_y) and self in player.bullets:
                self.exploded = True
                tank.hit()

            if player.rect.colliderect(self.rect.x, self.rect.y, self.size_x, self.size_y) and self in tank.bullets:
                self.exploded = True
                player.health +- 1

        if baza.rect.colliderect(self.rect.x, self.rect.y, self.size_x, self.size_y):
            player.health = 0
        #рух
        self.rect.x += dx
        self.rect.y += dy

    #вибух кулі    
    def explode(self):
        self.kill()
        self.exploded = True
    #анімацію вибуху
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


class Button():
    def __init__(self, btn_image, x, y, size_x, size_y):
        self.image = transform.scale(btn_image,(size_x,size_y))
        self.rect = self.image.get_rect()
        self.size_x, self.size_y = size_x, size_y 
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.wait = 5
        self.clicked = False
        self.action = False
    def draw(self):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

        #get mouse position
        pos = mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.action = True
                self.clicked = True
                
        if mouse.get_pressed()[0] == 0:
            self.clicked = False

btn_play = Button(play_button, 300, 500, 200, 100)
btn_exit = Button(exit_button, 300, 650, 200, 100)
