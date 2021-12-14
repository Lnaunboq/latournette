import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from module_géné_matrice import *
from random import randint

class Murs_lab:

    def __init__(self,matrice,espace,largeur_écran):
        self.matrice = matrice
        self.largeur = matrice.largeur*2+1
        self.espace = espace
        self.largeur_écran = largeur_écran
        self.body_labyrinthe = self.génération_body()
        self.génération_murs()


    def génération_joint(self):
        joint_centre_body = pymunk.Body(body_type = pymunk.Body.STATIC)
        joint_centre_body.position = (self.largeur_écran,self.largeur_écran-1)
        joint_centre_body2 = pymunk.Body(body_type = pymunk.Body.STATIC)
        joint_centre_body2.position = (self.largeur_écran,self.largeur_écran+1)
        rotation_joint = pymunk.PinJoint(self.body_labyrinthe, joint_centre_body, (0,0), (0,0))
        rotation_joint2 = pymunk.PinJoint(self.body_labyrinthe, joint_centre_body2, (0,0), (0,0))
        espace.add(joint_centre_body,joint_centre_body2)

    def génération_body(self):
        body_labyrinthe = pymunk.Body(10000,100000000)    #la deuxième valeur est l'inertie de l'objet
        body_labyrinthe.position = (self.largeur_écran/2,self.largeur_écran/2) #positionne au milieu de l'écran
        return body_labyrinthe
        
    def génération_murs(self):
        print(self.matrice.matrice)
        murs_horizontaux,murs_verticaux = [],[]
        l_mur = 500/self.largeur
        for i in range(0,self.largeur):
            debut_nouv_mur,fin_nouv_mur = 0,0
            for j in range(0,self.largeur-1):
                if self.matrice.matrice[i][j+1] != 0 and self.matrice.matrice[i][j] != 0:
                    fin_nouv_mur = j+1
                if self.matrice.matrice[i][j] == 0 and self.matrice.matrice[i][j+1] != 0 and self.matrice.matrice[i][j-1] != 0:
                    if debut_nouv_mur < fin_nouv_mur:
                        murs_horizontaux.append([i,debut_nouv_mur,fin_nouv_mur])
                    debut_nouv_mur = j+1
                if fin_nouv_mur == self.largeur:
                   murs_horizontaux.append([i,debut_nouv_mur,fin_nouv_mur])                
        murs_horizontaux.append([0,0,self.largeur-1])
        murs_horizontaux.append([self.largeur-1,0,self.largeur-1])

        self.matrice.tourner_droite()
        for i in range(0,self.largeur):
            debut_nouv_mur,fin_nouv_mur = 0,0
            for j in range(0,self.largeur-1):
                    if self.matrice.matrice[i][j+1] != 0 and self.matrice.matrice[i][j] != 0:
                        fin_nouv_mur = j+1
                    if self.matrice.matrice[i][j] == 0 and self.matrice.matrice[i][j+1] != 0 and self.matrice.matrice[i][j-1] != 0:
                        if debut_nouv_mur < fin_nouv_mur:
                            murs_verticaux.append([i,debut_nouv_mur,fin_nouv_mur])
                        debut_nouv_mur = j+1
                    if fin_nouv_mur == self.largeur:
                       murs_verticaux.append([i,debut_nouv_mur,fin_nouv_mur])
        murs_verticaux.append([self.largeur-1,0,self.largeur-1])
        j,w = 0,0
        while self.matrice.matrice[0][j] != 0:
            j+=1
        murs_verticaux.append([0,0,j-1])   
        murs_verticaux.append([0,j+1,self.largeur-1])
                    
        décalage = 250#(self.largeur_écran-200)/2 pour quand l'écran est de 700 pour test
        for mur in murs_horizontaux:
            seg_mur = pymunk.Segment(self.body_labyrinthe, (mur[1]*l_mur-décalage,-mur[0]*l_mur+décalage), (mur[2]*l_mur-décalage,-mur[0]*l_mur+décalage), 5)
            seg_mur.color = pygame.color.THECOLORS["midnightblue"]
            self.espace.add(seg_mur)

        for mur in murs_verticaux:
            seg_mur = pymunk.Segment(self.body_labyrinthe, (mur[0]*l_mur-décalage,(mur[1]+1)*l_mur-décalage), (mur[0]*l_mur-décalage,(mur[2]+1)*l_mur-décalage), 5)
            seg_mur.color = pygame.color.THECOLORS["midnightblue"]
            self.espace.add(seg_mur)

class Téléporteur:

    def __init__(self,matrice,espace):
        self.matrice = matrice
        self.largeur = self.matrice.largeur*2+1
        self.espace = espace
        self.génération_téléporteur()
        
            
    def génération_téléporteur(self):
        l_mur = 500/self.largeur
        i = random.randint(1,len(self.matrice.culs_de_sac)-1)
        """on devrait pas mettre le premier para à 0 pour éviter de prendre la sortie comme point de TP
        et culs de sac"""
        self.coords_TP = self.matrice.culs_de_sac[i]

        self.x = ((self.coords_TP[1] - int(self.matrice.largeur/2)-1)*2+1)*l_mur
        self.y_pymunk = ((-self.coords_TP[0] + int(self.matrice.largeur/2))*2+1)*l_mur
        self.y_pygame = ((self.coords_TP[0] - int(self.matrice.largeur/2))*2+1)*l_mur
        #self.body = pymunk.Body(10000,100000000)    #la deuxième valeur est l'inertie de l'objet
        #self.body.position = (self.x,self.y) #positionne le body
        """
        shape_téléporteur = pymunk.Poly(self.body, [(self.x+250,self.y+(l_mur/3)+250), (self.x-(l_mur/3)+250,self.y-(l_mur/4)+250),(self.x+(l_mur/3)+250,self.y-(l_mur/4)+250)])        
        shape_téléporteur.color = pygame.color.THECOLORS["darkorchid"]
        self.espace.add(shape_téléporteur)"""
        
        
class Cercle:

    def __init__(self, position_x, position_y, rayon,espace):
        self.position_x = position_x
        self.position_y = position_y
        self.rayon = rayon
        moment = pymunk.moment_for_circle(1, 0, self.rayon) #génère la physique de la balle adaptée aux caractéristiques de cette dernière
        body_cercle = pymunk.Body(0.03, moment) #poids de la balle, momentum
        body_cercle.position = position_x, position_y
        shape_cercle = pymunk.Circle(body_cercle, self.rayon)
        shape_cercle.color = pygame.color.THECOLORS["gold"]

        self.body = body_cercle
        espace.add(body_cercle, shape_cercle)