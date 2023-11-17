#імпортуємо модулі
from pygame import *
from constants import *
from logger import *

tile_size = 64
#списки блоків
bushes = []
bricks = []
touchabels = []
#клас
class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        brick_img = image.load("assets/images/brick.png")
        beton_img = image.load("assets/images/beton.png")
        ice_img = image.load("assets/images/ice.png")
        bush_img = image.load("assets/images/bush.png")
        water_img = image.load("assets/images/water.png")
        
        row_count = 0
        
        for row in data:
            col_count = 0
            for tile in row:
                #блок цегли
                if tile == 1:
                    img = transform.scale(brick_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    bricks.append(tile)
                    touchabels.append(tile)
                #блок бетону
                elif tile == 2:
                    img = transform.scale(beton_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    touchabels.append(tile)
                #блок куща
                elif tile == 3:
                    img = transform.scale(bush_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    bushes.append(tile)
                #блок води
                elif tile == 5:
                    img = transform.scale(water_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
    

                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            WINDOW.blit(tile[0], tile[1])
#мапа
map1 = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0],
        [1, 2, 0, 0, 3, 3, 3, 3, 0, 0, 0, 1, 0],
        [0, 0, 0, 5, 5, 3, 1, 1, 0, 3, 3, 2, 0],
        [1, 0, 0, 5, 5, 3, 3, 1, 0, 5, 5, 2, 0],
        [1, 0, 1, 2, 1, 3, 3, 0, 0, 5, 5, 3, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0],
        [2, 0, 0, 1, 1, 0, 2, 0, 3, 3, 3, 0, 0],
        [0, 0, 2, 2, 1, 0, 0, 0, 2, 2, 1, 0, 0],
        [0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 6, 1, 0, 0, 0, 1, 1]]
#екземпляр світу
world = World(map1)
