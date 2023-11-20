#імпортуємо модулі
from logger import *
import pygame
from constants import *
from scenes import *
from sprites import *


logging.info(f'Програма була запущена')

pygame.init()  

clock = pygame.time.Clock()

APP = True
SCENE_GAME = True
started = False
play = False
finish = False

#ігровий цикл
while APP:
        event = pygame.event.get()
        for e in event:
            if e.type == pygame.QUIT:
                APP = False
        if not finish:
            if not started:
                WINDOW.blit(start_background, (0,0))
                btn_play.draw()
                btn_exit.draw()
                WINDOW.blit(logo1,(100,-150))
                if btn_play.clicked:
                    start = True
                    play = True
                if btn_exit.clicked:
                    APP = False
            #гра 
            if play:
                game.update()
        pygame.display.update()
        clock.tick(FPS)
