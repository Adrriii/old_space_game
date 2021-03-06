import pygame
from model import *

class Controller:
    """Gère les interactions utilisateurs"""
    def __init__(self, event_manager):
        self.event_manager = event_manager
        pygame.key.set_repeat(1,400)    #Permet la répétition de touche, interval de 200 ms

    def tick(self):
        for event in pygame.event.get():
            cont = True
            if event.type == pygame.QUIT:
                cont = self.event_manager.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    cont = self.event_manager.shoot(event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_LEFT:
                    cont = self.event_manager.move_player("left", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_RIGHT:
                    cont = self.event_manager.move_player("right", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_UP:
                    cont = self.event_manager.move_player("up", event.type == pygame.KEYDOWN)

                elif event.key == pygame.K_DOWN:
                    cont = self.event_manager.move_player("down", event.type == pygame.KEYDOWN)

            if not cont: return False

        return True
