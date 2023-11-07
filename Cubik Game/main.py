import pygame
from constants import *
from scenes import *
#from logger import *

pygame.init()  

clock = pygame.time.Clock()

APP = True
SCENE_GAME = True
play = True

game = GameScene()

while APP:
    event = pygame.event.get()
    for e in event:
        if e.type == pygame.QUIT:
            APP = False
    
    if play:
        pygame.display.update()
        game.update()
        draw_grid()
    clock.tick(FPS)
