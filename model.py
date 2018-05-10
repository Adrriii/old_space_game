## TODO:
#   * Faire varier la vitesse angulaire maximum en fonction de la vitesse actuelle du joueur
import sys
from math import *

DEFAULT_MAP = "maps/map_0.map"
V_MAX = 5
ANGLE_MAX = 20

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
        sys.stderr.write("Shoot function not implemented yet !\n")
        return True

class Map:
    """Class modélisant la map du jeu"""
    def __init__(self, model):
        self.array = []     #Liste contenant tous les objets du jeu
        self.width = 0
        self.height = 0
        self.model = model
        self.array.append(Object(0.2, 163, (100, 100), "asteroid", 30, 30))

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

class Object():
    def __init__(self, speed = 0, angle = 0, pos = (0, 0), type = "", width = 0, height = 0):
        self.speed = speed
        self.angle = angle

        self.pos = pos

        self.width = width
        self.height = height

        self.type = type

    def calculate_new_coord(self):
        delta_x = self.speed * cos((self.angle - 90)%360 * 3.14/180)
        delta_y = self.speed * sin((self.angle - 90)%360 * 3.14/180)

        return (self.pos[0] + delta_x, self.pos[1] + delta_y)

    def play(self):
        self.pos = self.calculate_new_coord()

class Player():
    """Class modélisant le joueur"""
    def __init__(self):
        self.V_Max = V_MAX          #Vitesse maximum que peut atteindre le joueur
        self.V = 0                  #Vitesse actuelle du joueur
        self.V_unit = 0.1           #Valeur de l'accélération qui peur être apportée au joueur

        self.angle_max = ANGLE_MAX  #Vitesse angulaire maximum
        self.V_angle = 0            #Vitesse angulaire actuelle du joueur
        self.angle_unit = 0.2      #Valeur de "l'accélération angulaire" du joueur
        self.angle = 90             #Angle atuelle du joueur

        self.pos = (0, 0)           #Position (x, y) du joueur dans le jeu

        self.go_up = False          #Est-ce que le joueur avance ?
        self.go_left = False        #                     va à gauche ?
        self.go_right = False       #                        à droite ?
        self.go_down = False        #Frein

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

    def move(self):
        """Fonction gérant le mouvement du joueur"""
        if self.go_up:
            if self.V + self.V_unit < self.V_Max:
                self.V += self.V_unit

        elif self.go_down:
            if self.V > 0:
                if self.V - self.V_unit > 0:
                    self.V -= self.V_unit
                else:
                    self.V = 0
        else:
            if self.V > 0:
                if self.V - self.V_unit > 0:
                    self.V -= self.V_unit/4
                else:
                    self.V = 0

        delta_x = self.V * cos((self.angle - 90)%360 * 3.14/180)
        delta_y = self.V * sin((self.angle - 90)%360 * 3.14/180)

        #print("angle ", self.angle, " delta x ",delta_x, " delta_y ", delta_y)

        self.pos = (self.pos[0] + delta_x, self.pos[1] + delta_y)

        angle_limit = 1 - (self.V / self.V_Max)/3
        if angle_limit < 0.3:
            angle_limit = 0.3

        if self.go_left:
            if  self.V_angle - self.angle_unit > -self.angle_max:
                self.V_angle -= self.angle_unit * angle_limit


        elif self.go_right:
            if self.V_angle + self.angle_unit < self.angle_max:
                self.V_angle += self.angle_unit * angle_limit
        else:
            if abs(self.V_angle) < 0.1:
                self.V_angle = 0

            elif self.V_angle < 0:
                self.V_angle += self.angle_unit * angle_limit

            elif self.V_angle > 0:
                self.V_angle -= self.angle_unit * angle_limit

        self.angle = (self.V_angle + self.angle)%360

class Model:
    """Model du jeu"""
    def __init__(self):
        self.player = Player()
        self.map = Map(self)
        self.map_path = DEFAULT_MAP


    def load_map(self, map_name):
        self.map_path = map_name
        self.map.load(map_name)

    def tick(self):
        self.player.move()
        for element in self.map.array:
            element.play()
