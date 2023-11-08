    from pygame import *
from constants import *

tile_size = 64

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        brick_img = image.load("assets/images/brick.jpg")
        beton_img = image.load("assets/images/beton.jpg")
        ice_img = image.load("assets/images/ice.jpg")
        bush_img = image.load("assets/images/bush.jpg")
        water_img = image.load("assets/images/water.jpg")
        
        row_count = 0
        
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = transform.scale(brick_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                    
                elif tile == 2:
                    img = transform.scale(beton_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                elif tile == 3:
                    img = transform.scale(bush_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                elif tile == 4:
                    img = transform.scale(ice_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

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

map1 = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 4, 3, 3, 3, 3, 0, 0, 0, 1, 0],
        [0, 0, 4, 5, 5, 3, 1, 1, 0, 4, 4, 2, 0],
        [1, 0, 0, 5, 5, 3, 3, 1, 0, 5, 5, 2, 0],
        [1, 0, 1, 2, 1, 3, 3, 0, 4, 5, 5, 3, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 4, 3, 3, 3, 0],
        [2, 0, 0, 1, 1, 0, 2, 0, 3, 3, 3, 0, 0],
        [0, 0, 2, 2, 1, 0, 0, 0, 3, 2, 1, 0, 0],
        [0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 6, 1, 0, 0, 0, 1, 1]]

def draw_grid():
    for line in range(0, 13):
        draw.line(WINDOW, (255, 255, 255), (0, line * tile_size), (WIN_WIDTH, line * tile_size))
    for line in range(0, 13):
        draw.line(WINDOW, (255, 255, 255), (line * tile_size, 0), (line * tile_size, WIN_HEIGHT))
