import numpy 
import random

class Matrice_lab:

    def __init__(self,largeur):
        self.largeur = largeur
        self.matrice = numpy.ones((2*largeur+1,2*largeur+1))
        self.culs_de_sacs = []

    def génération(self):
        self.petite_matrice = numpy.ones((self.largeur,self.largeur))
        j = self.largeur*self.largeur-2   #pour incrémentation de la boucle
        k = 0
        r = random.randint(0,self.largeur-1)     #génère une coordonnée sur l'axe y
        self.petite_matrice[r][0] = 0                  #creuse l'entrée, elle se trouve toujours à gauche
        self.matrice[2*r+1][2*0+1] = 0          #fait la même dans les murs
        self.matrice[2*r+1][2*0] = 0
        self.coordonnées = [r,0]            #"""c'est une liste d'un couple de coordonnées"""
        culs_de_sac = [self.coordonnées]
        self.possibilités = self.chercher_possibilités()  #"""c'est une liste de couples de coordonnées"""
        chemin = []                 #garde une trace des cases explorées
        while(k != j):
            k+=1                    #incrémentation de la boucle
            chemin.append(self.coordonnées)
            self.coordonnées = self.choisir()
            self.creuser()
            self.possibilités = self.chercher_possibilités()
            if (self.possibilités == []):
                i = 0
                culs_de_sac.append(self.coordonnées)
                while (self.possibilités == []):    #tant qu'on a aucune possibilités d'avancer on recule
                    i+=1
                    self.coordonnées = self.remonter(chemin,i)
                    self.possibilités = self.chercher_possibilités()
        """fin de la boucle principale de génération"""            
        self.culs_de_sac = culs_de_sac
        #correction des erreurs de type "caillots de 1:"; cf rapport
        for i in range(1,self.largeur*2-1):
            for j in range(1,self.largeur*2-1):
                if self.matrice[i][j] == 1:
                    if self.matrice[i][j+1] == 1:
                        if self.matrice[i][j-1] == 1:
                            if self.matrice[i+1][j] == 1:
                                if self.matrice[i-1][j] == 1:
                                    self.matrice[i][j] = 0
                                    self.matrice[i][j+1] = 0
                                    self.matrice[i][j-1] = 0
                                    self.matrice[i+1][j] = 0
                                    self.matrice[i-1][j] = 0

    def chercher_possibilités(self):
        liste = []
        x = self.coordonnées[0]
        y = self.coordonnées[1]
        if (x!= 0):
            if (self.petite_matrice[x-1][y] != 0):
                liste.append([x-1,y,"haut"])
        if (x!= self.largeur-1):
            if (self.petite_matrice[x+1][y] != 0):
                liste.append([x+1,y,"bas"])
        if (y != 0):
            if (self.petite_matrice[x][y-1] != 0):
                liste.append([x,y-1,"gauche"])
        if (y != self.largeur-1):
            if (self.petite_matrice[x][y+1] != 0):
                liste.append([x,y+1,"droite"])
        return liste

    def choisir(self):
        r = random.randint(0,len(self.possibilités)-1)
        return self.possibilités[r]
                
    def creuser(self):
        self.petite_matrice[self.coordonnées[0]][self.coordonnées[1]] = 0           #met à 0 la nouvelle case visitée
        self.matrice[2*self.coordonnées[0]+1][2*self.coordonnées[1]+1] = 0    #met à 0 la case correspondante dans les murs
        if (self.coordonnées[2] == "haut"):
            self.matrice[2*self.coordonnées[0]+1+1][2*self.coordonnées[1]+1] = 0
        if (self.coordonnées[2] == "bas"):
            self.matrice[2*self.coordonnées[0]+1-1][2*self.coordonnées[1]+1] = 0
        if (self.coordonnées[2] == "gauche"):
            self.matrice[2*self.coordonnées[0]+1][2*self.coordonnées[1]+1+1] = 0
        if (self.coordonnées[2] == "droite"):
            self.matrice[2*self.coordonnées[0]+1][2*self.coordonnées[1]+1-1] = 0        

    def remonter(self,chemin,n):
        return chemin[(len(chemin)-n)]

    def tourner_droite(self):
        self.matrice = numpy.swapaxes(self.matrice,0,1)
        self.matrice = numpy.fliplr(self.matrice)