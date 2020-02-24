## TODO:
#


from model import *
import pygame

DEFAULT_WIDTH = 700
DEFAULT_HEIGHT = 1000

SPRITE_PLAYER = ["assets/player/ship_00.png"]
SPRITE_ASTEROID = ["assets/asteroid/asteroid_00.png"]
SPRITE_SHOOT = ["assets/shoot/Shoot_00.png"]


class View:
    """Class définissant la vue"""
    def __init__(self, model):
        self.model = model
        self.width = model.map.width
        self.height = model.map.height

        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)     #Faudra bien penser à gérer la taille :/

        self.sprite = {
            "player": [pygame.image.load(sprite) for sprite in SPRITE_PLAYER],
            "asteroid": [pygame.image.load(sprite) for sprite in SPRITE_ASTEROID],
            "shoot": [pygame.image.load(sprite) for sprite in SPRITE_SHOOT]
        }

    def render_map(self):
        """Fonction permettant de dessiner le jeu à l'écran"""
        map = self.model.map

        #Vaut mieux une fonction qui tourne une image celon un certain angle, a faire
        player_surface = self.resize(self.sprite["player"][0], self.model.player.h, self.model.player.w)
        rotate_player_surface = self.rotate(player_surface, self.model.player.angle)

        self.win.blit(rotate_player_surface[0], rotate_player_surface[1].move(self.model.player.pos))


        for element in map.array:
            if not element.sprite in self.sprite.keys():
                sys.stderr.write("Can't find texture for : " + element.sprite)
                continue
            #Gérer les animations plus tard
            surface = self.resize(self.sprite[element.sprite][0], element.width, element.height)
            
            new_surface_info = self.rotate(surface, (element.angle + element.rotation)%360)

            self.win.blit(new_surface_info[0], new_surface_info[1].move(element.pos))

    def rotate(self, surface, angle):
        old_rect = pygame.Surface.get_rect(surface)
        old_center = old_rect.center

        new_surface = pygame.transform.rotate(surface, - angle)
        new_rect = pygame.Surface.get_rect(new_surface)
        new_rect.center = old_center

        return (new_surface, new_rect)


    def resize(self, surface, width, height):
        return pygame.transform.scale(surface, (width, height))

    def tick(self):
        self.width = self.win.get_width()
        self.height = self.win.get_height()
        self.win.fill([0, 0, 0])

        self.render_map()
        pygame.display.flip()
