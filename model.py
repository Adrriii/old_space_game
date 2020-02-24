## TODO:
#   * Faire varier la vitesse angulaire maximum en fonction de la vitesse actuelle du joueur
import sys
from math import *
from random import randrange

DEFAULT_MAP = "maps/map_0.map"
V_MAX = 5
ANGLE_MAX = 20

def check_collision(x1, y1, h1, w1, x2, y2, h2, w2):
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2

class Event_Manager:
    """Class gérant tous les événements du jeu"""
    def __init__(self, model):
        self.model = model

    def quit(self):
        return False

    def move_player(self, dir, state):
        self.model.player.update_move(dir, state)
        return True

    def shoot(self, state):
        self.model.player.active_shoot(state)
        return True

class Map:
    """Class modélisant la map du jeu"""
    def __init__(self, model):
        self.array = []     #Liste contenant tous les objets du jeu
        self.width = 0
        self.height = 0
        self.model = model

    def load(self, filename):
        """Lecture du fichier passé en argument"""
        player_pos = (0, 0)
        try:
            file = open(filename, "r")

            for row in file.readlines():
                row = row.strip('\n')
                _row = row.split(' ')

                if _row[0] == "width":
                    self.width = int(_row[1])

                elif _row[0] == "height":
                    self.height = int(_row[1])

                elif _row[0] == "player":
                    self.model.player.pos = (int(_row[1]), int(_row[2]))
        except:
            sys.stderr.write("Error in load map, can't open file.\n")
        return player_pos

    def add_random_asteroid(self):
        """self, speed, angle, rotation_angle, rotation_speed, pos, type, width, height"""
        asteroid = Asteroid()
        asteroid.speed = randrange(1, 10)
        asteroid.angle = randrange(0, 360)
        asteroid.rotation_angle = randrange(0, 360)
        asteroid.rotation_speed = randrange(0, 6)
        asteroid.pos = (randrange(0, 700), randrange(0, 1000))
        asteroid.width = asteroid.height = randrange(10, 50)
        self.add_obj(asteroid)

    def add_obj(self, obj):
        self.array.append(obj)

class Object():
    def __init__(self):
        self.speed = 0 
        self.angle = 0
        self.rotation = 0
        self.rotation_speed = 0

        self.pos = (0,0)

        self.width = 0
        self.height = 0

        self.sprite = "default"

    def calculate_new_coord(self):
        self.move()

    def tick(self):
        if self.go_up:
            if self.V + self.V_unit < self.V_Max:
                self.V += self.V_unit
        else:
            if self.V > 0:
                if self.V - self.V_unit > 0:
                    self.V -= self.V_unit/4
                else:
                    self.V = 0

        if self.go_left:
            if  self.V_angle - self.angle_unit > -self.angle_max:
                self.V_angle -= self.angle_unit

        if self.go_right:
            if self.V_angle + self.angle_unit < self.angle_max:
                self.V_angle += self.angle_unit

    def move(self):
        """Fonction gérant le mouvement d'un objet"""

        delta_x = self.V * cos((self.angle - 90)%360 * 3.14/180)
        delta_y = self.V * sin((self.angle - 90)%360 * 3.14/180)

        #print("angle ", self.angle, " delta x ",delta_x, " delta_y ", delta_y)

        self.pos = (self.pos[0] + delta_x, self.pos[1] + delta_y)

        self.angle = (self.V_angle + self.angle) % 360

    def play(self):
        self.pos = self.calculate_new_coord()
        self.rotation += self.rotation_speed

class Asteroid(Object):
    
    def __init__(self):
        super().__init__()
        self.sprite = "asteroid"

class Projectile(Object):
    def __init__(self, player):
        super().__init__()

        self.speed = 10
        self.angle = player.angle
        self.rotation = 0
        self.rotation_speed = 0
        self.pos = player.pos
        self.width = 20
        self.height = 40

        self.sprite = "shoot"

class Player(Object):
    """Class modélisant le joueur"""
    def __init__(self):
        super().__init__()
        self.V_Max = V_MAX          #Vitesse maximum que peut atteindre le joueur
        self.V = 0                  #Vitesse actuelle du joueur
        self.V_unit = 0.1           #Valeur de l'accélération qui peur être apportée au joueur

        self.angle_max = ANGLE_MAX  #Vitesse angulaire maximum
        self.V_angle = 0            #Vitesse angulaire actuelle du joueur
        self.angle_unit = 0.2      #Valeur de "l'accélération angulaire" du joueur
        self.angle = 90             #Angle atuelle du joueur

        self.pos = (0, 0)           #Position (x, y) du joueur dans le jeu
        self.h = 40
        self.w = 40

        self.go_up = False          #Est-ce que le joueur avance ?
        self.go_left = False        #                     va à gauche ?
        self.go_right = False       #                        à droite ?
        self.go_down = False        #Frein
        self.shoot = False

    def update_move(self, dir, state):
        """Change l'état du joueur en fonction de la diréction donnée"""
        if dir == "up":     #Grosse duplication de code bien moche à changer
            self.go_up = state
            if state:
                self.go_down = False

        elif dir == "left":
            self.go_left = state
            if state:
                self.go_right = False

        elif dir == "right":
            self.go_right = state
            if state:
                self.go_left = False

        elif dir == "down":
            self.go_down = state
            if state:
                self.go_up = False

    def active_shoot(self, state):
        self.shoot = state




class Model:
    """Model du jeu"""
    def __init__(self):
        self.player = Player()
        self.map = Map(self)
        self.map_path = DEFAULT_MAP

    def load_map(self, map_name):
        self.map_path = map_name
        self.map.load(map_name)

    def check_player_collision(self):
        for element in self.map.array:
            if check_collision(
                self.player.pos[0], self.player.pos[1], self.player.w, self.player.h,
                element.pos[0], element.pos[1], element.width, element.height):
                break

    def print_statue(self):
        print("\033[2J")
        print("Go_up    = " + str(self.player.go_up))
        print("Go_down  = " + str(self.player.go_down))
        print("Go_left  = " + str(self.player.go_left))
        print("Go_right = " + str(self.player.go_right))
        print("Shoot    = " + str(self.player.shoot))
        print("Pos      = " + str(self.player.pos))
        print("Angle    = " + str(self.player.angle))


    def tick(self):
        self.print_statue()
        self.player.move()
        for element in self.map.array:
            element.play()
        self.check_player_collision()
        if randrange(0, 100)%26 == 0:
            self.map.add_random_asteroid()

        if self.player.shoot:
            projectile = Projectile(self.player)
            self.map.add_obj(projectile)
