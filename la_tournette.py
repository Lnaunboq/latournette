import pygame, sys
from pygame import *
from pygame.locals import *
from sys import *
from module_géné_matrice import *
from module_géné_labyrinthe2 import *
from test_save import *


class Bouton:
    def __init__(self,fenetre,fond,bouton,position_bouton,position_x,position_y):
        position_bouton = position_bouton.move(position_x,position_y)
        fenetre.blit(bouton,position_bouton)
        pygame.display.flip()



def musique():
    pygame.mixer.init()
    musique_menu = mixer.music.load("audio/loopin_in_the_sky01.mp3")
    mixer.music.play(-1)



def main_musique():
    musique()
    main()



def deplacer_curseur(fenetre,fond,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,bouton_x,bouton_y):
    if curseur_pos == 1 and play == 0:
        Bouton(fenetre,fond,img_bouton["jouer"],position_bouton["jouer"],coord_x["jouer"],coord_y["jouer"])
    if curseur_pos == 2 and play == 0:
        Bouton(fenetre,fond,img_bouton["scores"],position_bouton["scores"],coord_x["scores"],coord_y["scores"])
    if curseur_pos == 3 and play == 0:
        Bouton(fenetre,fond,img_bouton["credits"],position_bouton["credits"],coord_x["credits"],coord_y["credits"])
    if curseur_pos == 4 and play == 0:
        Bouton(fenetre,fond,img_bouton["commandes"],position_bouton["commandes"],coord_x["commandes"],coord_y["commandes"])
    if curseur_pos == 5 and play == 0:
        Bouton(fenetre,fond,img_bouton["quitter"],position_bouton["quitter"],coord_x["quitter"],coord_y["quitter"])
    if curseur_pos == 6 and play == 1:
        Bouton(fenetre,fond,img_bouton["normal"],position_bouton["normal"],coord_x["normal"],coord_y["normal"])
    if curseur_pos == 7 and play == 1:
        Bouton(fenetre,fond,img_bouton["difficile"],position_bouton["difficile"],coord_x["difficile"],coord_y["difficile"])
    if curseur_pos == 8 and play == 1:
        Bouton(fenetre,fond,img_bouton["extreme"],position_bouton["extreme"],coord_x["extreme"],coord_y["extreme"])
    if curseur_pos == 9 and play == 1:
        Bouton(fenetre,fond,img_bouton["entrainement"],position_bouton["entrainement"],coord_x["entrainement"],coord_y["entrainement"])

    position_curseur = position_curseur.move(bouton_x,bouton_y)
    fenetre.blit(curseur,position_curseur)
    pygame.display.flip() #Rafraichissement de la page



def jouer(fenetre,fond,titre,curseur_pos,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y):
    fenetre.blit(fond,(0,0))
    fenetre.blit(titre,(286,75))

    bouton = {"normal":Bouton(fenetre,fond,img_bouton["normal"],position_bouton["normal"],coord_x["normal"],coord_y["normal"]),
    "difficile":Bouton(fenetre,fond,img_bouton["difficile"],position_bouton["difficile"],coord_x["difficile"],coord_y["difficile"]),
    "extreme":Bouton(fenetre,fond,img_bouton["extreme"],position_bouton["extreme"],coord_x["extreme"],coord_y["extreme"]),
    "entrainement":Bouton(fenetre,fond,img_bouton["entrainement"],position_bouton["entrainement"],coord_x["entrainement"],coord_y["entrainement"])}

    Bouton(fenetre,fond,curseur,position_curseur,coord_x["normal"],coord_y["normal"])
    pygame.display.flip() #Rafraichissement de la page

    curseur_pos = 6

    return curseur_pos



def main_game(clock,fond,largeur_écran,indice_de_difficulte,retour_son,temps,mat_tuto): #Antoine BOITEAU & Nathan MELET
    mixer.music.load("audio/cloud_maze.mp3")
    mixer.music.play()

    victoire = mixer.Sound("audio/win.ogg")

    difficulte = [8,11,17,8]

    fond_jeu_gravite = fond
    fond_jeu_gravite2 = pygame.image.load("images/fond_jeu2.png")

    cdt = 0 #passe à 1 et stop le décompte du temps lorsque la balle sort du labyrinthe

    screen = pygame.display.set_mode((largeur_écran,largeur_écran))
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    img_tp = pygame.image.load("images/TP.png")

    espace = pymunk.Space()
    gravité = -200
    espace.gravity = (0.0,gravité)

    largeur = difficulte[indice_de_difficulte] #int(input("quelle largeur pour le labyrinthe ?"))

    if mat_tuto == True:
        mat = Matrice_enregistree("tuto")
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    else:
        mat = Matrice_lab(largeur)
        mat.génération()

    laby = Murs_lab(mat,espace,largeur_écran)
            
    cooldown,coul = 40,40
    coul_TP = 0

    rayon = 500/laby.largeur/2
    balle = Cercle(350,350,rayon,espace)
    
    endgame = end_game(largeur_écran,largeur_écran)

    game_is_on = True

    while game_is_on:
        screen.blit(fond,(0,0))
        clock.tick(60)
        espace.gravity = (0.0,gravité)
        if cooldown > 0:
            coul -=1
            cooldown -= 1

        if coul_TP > 0:
            coul_TP-= 1

        for event in pygame.event.get():
            if event.type == QUIT: #Croix rouge de la fenêtre
                quitter()

        if event.type == KEYDOWN and event.key == K_RIGHT or event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > largeur_écran/2: #Touche Droite du clavier ou Clique souris à gauche de l'écran
            laby.body_labyrinthe.angle = laby.body_labyrinthe.angle - numpy.pi/660

        if event.type == KEYDOWN and event.key == K_LEFT or event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] < largeur_écran/2: #Touche Gauche du clavier ou Clique souris à droite de l'écran
            laby.body_labyrinthe.angle = laby.body_labyrinthe.angle + numpy.pi/660
            #endgame.creation(screen,ti,event,retour_son)

        if event.type == KEYDOWN and event.key == K_SPACE and cooldown == 0 or event.type == MOUSEBUTTONDOWN and event.button == 3 and cooldown == 0: #Barre Espace du  clavier ou Clique droit de la souris
            if gravité < 0:
                fond = fond_jeu_gravite2
            else:
                fond = fond_jeu_gravite
            gravité = -gravité
            cooldown = 20
            coul = 20

        if event.type == KEYDOWN and event.key == K_ESCAPE: #Touche Echap du clavier
            retour_son.play()
            main_musique()

        #Téléporteurs
        if (balle.body.position[0]-largeur_écran/2-100 > -rayon) and (balle.body.position[0]-largeur_écran/2-100 < rayon):
            if (balle.body.position[1]-largeur_écran/2-100 > -rayon) and (balle.body.position[1]-largeur_écran/2-100 < rayon) and coul_TP == 0:
                balle.body.position = largeur_écran/2-100,largeur_écran/2-100
                coul_TP = 100
            if (balle.body.position[1]-largeur_écran/2+100 > -rayon) and (balle.body.position[1]-largeur_écran/2+100 < rayon) and coul_TP == 0:
                balle.body.position = largeur_écran/2-100,largeur_écran/2+100
                coul_TP = 100
        if (balle.body.position[0]-largeur_écran/2+100 > -rayon) and (balle.body.position[0]-largeur_écran/2+100 < rayon):
            if (balle.body.position[1]-largeur_écran/2-100 > -rayon) and (balle.body.position[1]-largeur_écran/2-100 < rayon) and coul_TP == 0:
                balle.body.position = largeur_écran/2+100,largeur_écran/2-100
                coul_TP = 100
            if (balle.body.position[1]-largeur_écran/2+100 > -rayon) and (balle.body.position[1]-largeur_écran/2+100 < rayon) and coul_TP == 0:
                balle.body.position = largeur_écran/2+100,largeur_écran/2+100
                coul_TP = 100
                    
        #screen.fill((0+coul*6,230-coul*2,230-coul*2))
        espace.debug_draw(draw_options)

        espace.step(1/100)

        #Affiche les Téléporteurs
        screen.blit(img_tp,(largeur_écran/2-100-10,largeur_écran/2-100-10))
        screen.blit(img_tp,(largeur_écran/2+100-10,largeur_écran/2-100-10))
        screen.blit(img_tp,(largeur_écran/2+100-10,largeur_écran/2+100-10))
        screen.blit(img_tp,(largeur_écran/2-100-10,largeur_écran/2+100-10))
        

        #Partie Nathan Melet
        if (cdt == 0):
            endgame.timeig(pygame.time.get_ticks()/1000 - temps,screen)

        if(balle.body.position[1] <= 0 or balle.body.position[1] >= largeur_écran or balle.body.position[0] <= 0 or balle.body.position[0] >= largeur_écran):
        #if (True):
            if (cdt == 0):
                ti = pygame.time.get_ticks()/1000 - temps
                a=int(endgame.time_fin(ti)[0])
                b=int(endgame.time_fin(ti)[1])
                victoire.play()
                
                f=endgame.bestscore(indice_de_difficulte)
                ecriture_score(indice_de_difficulte,a,b)
                blit_sc=1
                cdt = cdt + 1
                y=(b/100)+a
                
            if (y<f):
                endgame.bestbl(0,y,screen)
                    
            else:
                endgame.bestbl(1,f,screen)
            endgame.creation(screen,ti,event,retour_son)
        #Partie Nathan Melet

        pygame.display.flip()

    main_musique()
        


def check_la_matrice(nom_matrice): #Antoine BOITEAU
    """nom_matrice EST UNE STRING!!!"""
    try:
        with open('fichiers_clés/' + nom_matrice + '.txt'): pass  #si le fichier existe au chemin indiqué on ne fait rien
    except IOError:
        return False   #sinon on indique que le fichier n'a pas été trouvé



class Matrice_enregistree: #Antoine BOITEAU
    def __init__(self,nom_matrice):
        """nom_matrice EST UNE STRING!!!"""
        self.charger_matrice(nom_matrice)
        self.largeur = int(len(self.matrice)/2 - 1)

    def charger_matrice(self,nom_matrice):
        with open(nom_matrice + '.txt','rb') as fichier:
            self.matrice = pickle.load(fichier)
            """ce que contient self.matrice est un tableau à deux dimensions
            qui est une matrice crée à la main par nos soins"""

    def tourner_droite(self):
        self.matrice = numpy.swapaxes(self.matrice,0,1)
        self.matrice = numpy.fliplr(self.matrice)
        #permet de pivoter les coeffs de la matrice de 90° dans le sens d'une horloge, utile pour la génération des murs



class end_game: #Nathan MELET
    def __init__(self,x,y):
        self.screen_x = x
        self.screen_y = y

        # ################################################# #
                # palette de couleur
                
        self.color1=(255,255,255)#couleur fond
        self.color2=(109,114,120)#couleur text
        self.color3=(0,0,0)#couleur button
        
        # ###
        
        self.font = pygame.font.Font("polices/AlexBrush-Regular.ttf", 40)# definition des cara du texte: SysFont(name, size, bold=False, italic=False)
        self.font2 = pygame.font.Font("polices/AlexBrush-Regular.ttf", 20)# definition des cara du texte: SysFont(name, size, bold=False, italic=False)
        
        # ################################################# #
        
        self.fond = pygame.Surface((self.screen_x,250))  # la taille du rect
        self.fond.set_alpha(200)                         # alpha level ????
        
        self.button1=pygame.Surface((100,30))
        self.button2=pygame.Surface((100,30))
        
        self.text1 = self.font.render("Vous avez gagné !", True, self.color1)# definition de la box qui contient le text :render(text, antialias, color, background=None)
        self.text2 = self.font.render("Votre temps est de :", True, self.color1)# definition de la box qui contient le text :render(text, antialias, color, background=None)
        

        """gestion des bt"""
        self.bont1text = self.font2.render("Menu", True, self.color1)
        self.bont2text = self.font2.render("Quitter", True, self.color1)

    def creation(self,screen,time,event,retour_son):
        self.text3=self.time_fin(time)[2]
        
        # ################################################# #
                # position du text 1 #
                
        self.text1_x=((self.screen_x//2)-(self.text1.get_width()//2))
        self.text1_y=50
        
        # ################################################# #
                # position du text 2 #
        
        self.text2_x=(self.screen_x//2)-(self.text2.get_width()//2)
        self.text2_y=100
        
        # ################################################# #
                # position du text 3 #
        
        self.text3_x=((self.screen_x//2)-(self.text3.get_width()//2))
        self.text3_y=150
    
        # ################################################# #
                # position du bouton 1 #

        self.button1_x=50
        self.button1_y=self.screen_y-50
        
        # ################################################# #
                # position du bouton 2 #
                
        self.button2_X=self.screen_x-(self.button2.get_width())-50
        self.button2_y=self.screen_y-50
        
        self.fond.fill(self.color2)         

        self.fond.blit(self.text1,(self.text1_x ,self.text1_y) )#ajout du texte sur l'ecran
        self.fond.blit(self.text2,(self.text2_x ,self.text2_y ) )#ajout du texte sur l'ecran
        self.fond.blit(self.text3,(self.text3_x ,self.text3_y ) )#ajout du texte sur l'ecran
        
        screen.blit(self.fond, (0,30))    # (0,0) are the top-left coordinates

        self.button1.fill(self.color2)
        self.button1.blit(self.bont1text,((self.button1.get_width()//2)-(self.bont1text.get_width()//2),5))
        screen.blit(self.button1,(self.button1_x ,self.button1_y ))
    
        self.button2.fill(self.color2)
        self.button2.blit(self.bont2text,((self.button2.get_width()//2)-(self.bont2text.get_width()//2),5))
        screen.blit(self.button2,(self.button2_X ,self.button2_y ))
        
        self.button(event,retour_son)

        
    
    def timeig(self,acttime,screen):
        time_m = acttime//60
        time_s = acttime%60
        if(time_s < 10):
            time_str=str(int(time_m))+":0"+str(int(time_s))
        if(time_s >= 10):
            time_str=str(int(time_m))+":"+str(int(time_s))
        time_ig=self.font.render(time_str, True, self.color3)
        screen.blit(time_ig, (30,50))    # (0,0) are the top-left coordinates
        


    def time_fin(self,time):
        """gestion du temps"""
        time_m = time//60
        time_s = time%60
        
        timestr = str(int(time_m))+" minutes et "+str(int(time_s))+" secondes" #mettre en return
        text3 = self.font.render(timestr, True, self.color1)

        return time_m,time_s,text3


        
    def button(self,event,retour_son):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if (pygame.mouse.get_pos()[0] >= 50 and pygame.mouse.get_pos()[0] <= 150):
                if ((pygame.mouse.get_pos()[1] <= (self.screen_y-20)) and (pygame.mouse.get_pos()[1] >= self.screen_y-50)):
                    # boutton quitter ########################################################"
                    retour_son.play()
                    main_musique()
              
            if (pygame.mouse.get_pos()[0]<=self.screen_x-50 and pygame.mouse.get_pos()[0]>=self.screen_x-150):
                if ((pygame.mouse.get_pos()[1]<=(self.screen_y-20)) and (pygame.mouse.get_pos()[1]>=self.screen_y-50)):
                    # bouton menu #############################
                    retour_son.play()
                    quitter()



    def bestscore(self,indice_de_difficulte):
        
        bestscore=charger()
        best=100
        
        for i in bestscore[indice_de_difficulte] :
            if len(i)>5:
                score=float(i[0]+"."+i[5]+i[6])
                if best>score:
                    best=score
        return best



    def bestbl(self,se,time,screen):
        self.score = pygame.Surface((250,150))
        self.score.fill(self.color2)
        self.score.set_alpha(200)  
        text1 = self.font.render("Bravo !", True, self.color1)
        text2 = self.font.render("Vous avez battu", True, self.color1)
        text3 = self.font.render("le meilleur temps !", True, self.color1)
        
        if(se == 0):
            self.score.blit(text1,((self.score.get_width()/2)-(text1.get_width()/2),100-90))
            self.score.blit(text2,((self.score.get_width()/2)-(text2.get_width()/2),100-50))
            self.score.blit(text3,((self.score.get_width()/2)-(text3.get_width()/2),100-10))
            screen.blit(self.score,((self.screen_x/2)-(self.score.get_width()/2),(self.screen_y/2)-(self.score.get_width()/2)+10) )

        if(se == 1):
            
            pass



class score_screen: #Nathan MELET
    def __init__(self,x,y):
        self.screen_x = x
        self.screen_y = y
        # ################################################# #
                # palette de couleur
                
        self.color1=(255,255,255)#couleur fond
        self.color2=(109,114,120)#couleur text
        self.color3=(0,0,0)#couleur button
        
        # ###
        
        self.font = pygame.font.Font("polices/AlexBrush-Regular.ttf", 40)# definition des cara du texte: SysFont(name, size, bold=False, italic=False)
        self.font2 = pygame.font.Font("polices/AlexBrush-Regular.ttf", 20)# definition des cara du texte: SysFont(name, size, bold=False, italic=False)
        
        # ################################################# #
        
        self.rect1 = pygame.Surface((200,500))  # la taille du rect
        self.rect2 = pygame.Surface((200,500))  # la taille du rect
        self.rect3 = pygame.Surface((200,500))  # la taille du rect
        
        self.button1=pygame.Surface((150,50))
        
        self.text1 = self.font.render("Normal", True, self.color1)# definition de la box qui contient le text :render(text, antialias, color, background=None)
        self.text2 = self.font.render("Difficile", True, self.color1)# definition de la box qui contient le text :render(text, antialias, color, background=None)
        self.text3 = self.font.render("Extreme",True, self.color1)
        self.titre = self.font.render("Scores",True, self.color3)
        
        """gestion des bt"""
        self.bont1text = self.font.render("Retour", True, self.color1)

    def creation(self,screen,retour_son):
        # ################################################# #
                # position du text 1 #
                
        self.text1_x=(200//2)-(self.text2.get_width()//2)
        self.text1_y=20
        
        # ################################################# #
                # position du text 2 #
        
        self.text2_x=(200//2)-(self.text2.get_width()//2)
        self.text2_y=20
        
        # ################################################# #
                # position du text 3 #
        
        self.text3_x=(200//2)-(self.text2.get_width()//2)
        self.text3_y=20
    
        # ################################################# #
                # position du bouton 1 #

        self.button1_x=(self.screen_x//2)-(self.button1.get_width()//2)
        self.button1_y=self.screen_y-70
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT: #Croix rouge de la fenêtre
                    retour_son.play()
                    quitter()

                if event.type == KEYDOWN and event.key == K_ESCAPE: #Bouton Echap
                    retour_son.play()
                    main()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    print(pygame.mouse.get_pos())
                    if (pygame.mouse.get_pos()[0] >= 425 and pygame.mouse.get_pos()[0] <= 575):
                        if ((pygame.mouse.get_pos()[1] <= (780)) and (pygame.mouse.get_pos()[1] >= 730)):
                            # boutton retour ########################################################"
                            retour_son.play()
                            main()
            
            screen.blit(pygame.image.load("images/fond_menu.png"),(0,0))
            
            self.rect1.fill(self.color2)
            self.rect2.fill(self.color2)  
            self.rect3.fill(self.color2)  
            bestscore = charger()

            for i in range(3):
                f = 0
                d = 6
                for x in bestscore[i][::-1]:
                    d = d - 1
                    f = f + 1
                    if(i==0):
                        score = self.font2.render(x,True, self.color1)
                        self.rect1.blit(score,((200//2)-(score.get_width()//2),500-(70*f)-30))
                    if(i==1):
                        score = self.font2.render(x,True, self.color1)
                        self.rect2.blit(score,((200//2)-(score.get_width()//2),500-(70*f)-30))
                    if(i==2):
                        score = self.font2.render(x,True, self.color1)
                        self.rect3.blit(score,((200//2)-(score.get_width()//2),500-(70*f)-30))

            self.rect1.blit(self.text1,(self.text1_x ,self.text1_y) )#ajout du texte sur l'ecran
            self.rect2.blit(self.text2,(self.text2_x ,self.text2_y ) )#ajout du texte sur l'ecran
            self.rect3.blit(self.text3,(self.text3_x ,self.text3_y ) )#ajout du texte sur l'ecran
              
            screen.blit(self.titre,(500-(self.titre.get_width()//2),10) )#ajout du texte sur l'ecran

            screen.blit(self.rect1, (100,100))    # (0,0) are the top-left coordinates
            screen.blit(self.rect2, ((100*2)+200,100))    # (0,0) are the top-left coordinates
            screen.blit(self.rect3, ((100*3)+(200*2),100))    # (0,0) are the top-left coordinates

            self.button1.fill(self.color2) 
            self.button1.blit(self.bont1text,(75-(self.bont1text.get_width()//2),0))
            screen.blit(self.button1, (self.button1_x,self.button1_y))    # (0,0) are the top-left coordinates

            pygame.display.flip()



def credits(screen,fond,font,clock,retour_son):
    musique_credits = mixer.music.load("audio/reminding.mp3")
    mixer.music.play()

    screen_r = screen.get_rect()

    credits_liste = credits_liste = ["CREDITS",
    "",
    "",
    "Antoine Boiteau",
    "Génération de Matrices",
    "Labyrinthe via Pymunk",
    "Enregistrement des scores",
    "Musiques",
    "",
    "Matteo Tani",
    "Menus principal et de difficultés",
    "Cohérence entre les codes",
    "Design",
    "Gestion de la musique",
    "",
    "Nathan Melet",
    "Écran de fin",
    "Gestion du temps en jeu",
    "Menu des Scores",
    "",
    "Benoit Larragneguy",
    "Menu des commandes",
    "",
    "Baptiste Malle",
    "Crédits"]

    texte = []
    # liste vide plus simple pour manier le placement
    for i, line in enumerate(credits_liste):
        s = font.render(line, 1, (10, 10, 10))
        # permet d'organiser "l'empilment" du texte avec le fond
        # redonne les positions
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
        texte.append((r, s))
    largeur_écran = 900
    pygame.display.set_caption("un test de pymunk")
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    espace = pymunk.Space()
    gravité = -200
    espace.gravity = (0.0,gravité)

    largeur = 17 #int(input("quelle largeur pour le labyrinthe ?"))
    mat = Matrice_lab(largeur)
    mat.génération()
    
    laby = Murs_lab(mat,espace,largeur_écran)

    rayon = 500/laby.largeur/2
    
    while True:
        if (i < 61):
            if (i == 60):
                balle = Cercle(largeur_écran/2,largeur_écran/2,rayon,espace)
                i = 0
            i = i + 1
        screen.blit(fond,(0,0))
        laby.body_labyrinthe.angle = laby.body_labyrinthe.angle - numpy.pi/1500
        
        espace.debug_draw(draw_options)

        espace.step(1/70)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                quitter()

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                retour_son.play()
                main_musique()

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                for r, s in texte:
                    # mouvement de 3 pixels vers la gauche
                    r.move_ip(-3, 0)
            if event.key == K_RIGHT or event.key == K_d:
                for r, s in texte:
                    # mouvement de 3 pixels vers la droite
                    r.move_ip(3, 0)
            if event.key == K_UP or event.key == K_w:
                for r, s in texte:
                    # mouvement de un pixel vers le haut
                    r.move_ip(0, -1)
            if event.key == K_DOWN or event.key == K_s:
                    for r, s in texte:
                        # mouvement de 3 pixel vers le bas
                        r.move_ip(0, 3)

        for r, s in texte:
            # mouvement de un pixel vers le haut
            r.move_ip(0, -1)
            # affiche le texte
            screen.blit(s, r)

        # lorsque tout a quitter l'écran
        if not screen_r.collidelistall([r for (r, _) in texte]):
            main_musique()

        pygame.display.flip()

        # fixe vitesse de rafraîchissement 60 IPS
        clock.tick(60)



def commandes(screen,clock,fond_jeu,retour_son,ecran_x,ecran_y): #Benoit Larragigny
    fond = pygame.image.load("images/commandes.png")

    bouton_tuto = pygame.image.load("images/bouton_tutoriel.png")
    position_bouton_tuto = bouton_tuto.get_rect()
    dim_x_bouton_tuto = bouton_tuto.get_width()
    dim_y_bouton_tuto = bouton_tuto.get_height()
    coord_x_bouton_tuto = ecran_x/2 - dim_x_bouton_tuto/2
    coord_y_bouton_tuto = ecran_y - dim_y_bouton_tuto - 25

    screen.blit(fond,(0,0))
    screen.blit(bouton_tuto,(coord_x_bouton_tuto,coord_y_bouton_tuto))

    while True: 
        for event in pygame.event.get():
            if event.type == QUIT: 
                quitter()

            if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == MOUSEBUTTONDOWN and event.button == 3:
                retour_son.play()
                main()

            if pygame.mouse.get_pos()[0] > coord_x_bouton_tuto and pygame.mouse.get_pos()[0] < coord_x_bouton_tuto + dim_x_bouton_tuto and pygame.mouse.get_pos()[1] > coord_y_bouton_tuto and pygame.mouse.get_pos()[1] < coord_y_bouton_tuto + dim_y_bouton_tuto:
                #pygame.mouse.set_cursor(*pygame.cursors.load_xbm("images\pointeur.xbm","images\pointeur.xbm"))
                pygame.mouse.set_cursor(*pygame.cursors.diamond)

            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[0] > coord_x_bouton_tuto and event.pos[0] < coord_x_bouton_tuto + dim_x_bouton_tuto and event.pos[1] > coord_y_bouton_tuto and event.pos[1] < coord_y_bouton_tuto + dim_y_bouton_tuto: #Bouton tuto
                main_game(clock,fond_jeu,ecran_y,3,retour_son,pygame.time.get_ticks()/1000,True)

        pygame.display.flip()



def retour(fenetre,fond,titre,curseur_pos,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y):
    fenetre.blit(fond,(0,0))
    fenetre.blit(titre,(286,75))

    bouton = {"jouer":Bouton(fenetre,fond,img_bouton["jouer"],position_bouton["jouer"],coord_x["jouer"],coord_y["jouer"]),
    "scores":Bouton(fenetre,fond,img_bouton["scores"],position_bouton["scores"],coord_x["scores"],coord_y["scores"]),
    "credits":Bouton(fenetre,fond,img_bouton["credits"],position_bouton["credits"],coord_x["credits"],coord_y["credits"]),
    "commandes":Bouton(fenetre,fond,img_bouton["commandes"],position_bouton["commandes"],coord_x["commandes"],coord_y["commandes"]),
    "quitter":Bouton(fenetre,fond,img_bouton["quitter"],position_bouton["quitter"],coord_x["quitter"],coord_y["quitter"])}

    Bouton(fenetre,fond,curseur,position_curseur,coord_x["jouer"],coord_y["jouer"])
    pygame.display.flip() #Rafraichissement de la page

    curseur_pos = 1

    return curseur_pos



def quitter():
    pygame.time.delay(200)
    pygame.quit()
    mixer.quit()
    sys.exit()



def main():
    pygame.init()

    #Apparence du curseur de la souris
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    #Création fenêtre pygame
    ecran_x = 1000
    ecran_y = 800
    fenetre = pygame.display.set_mode((ecran_x,ecran_y),FULLSCREEN)

    #Icône du jeu
    pygame.display.set_icon(pygame.image.load("images/la_tournette_icone.ico"))

    #Nom de la fenêtre du jeu
    pygame.display.set_caption("La Tournette")

    #Images de fond
    fond_menu = pygame.image.load("images/fond_menu.png")
    fond_jeu = pygame.image.load("images/fond_jeu.png")
    fond_credits = pygame.image.load("images/fond_credits.png")
    fenetre.blit(fond_menu,(0,0))

    #Image de titre
    titre = pygame.image.load("images/la_tournette_titre.png")
    fenetre.blit(titre,(286,75))

    #Bruitages
    valider = mixer.Sound("audio/valider.ogg")
    retour_son = mixer.Sound("audio/retour.ogg")
    curseur_son = mixer.Sound("audio/curseur.ogg")

    #Police
    font = pygame.font.Font("polices/AlexBrush-Regular.ttf", 50)

    #Timer
    clock = pygame.time.Clock()

    #Adresses des images des boutons
    img_bouton = {"jouer": pygame.image.load("images/bouton_jouer.png"),
    "scores": pygame.image.load("images/bouton_scores.png"),
    "credits": pygame.image.load("images/bouton_credits.png"),
    "commandes": pygame.image.load("images/bouton_commandes.png"),
    "quitter": pygame.image.load("images/bouton_quitter.png"),
    "normal": pygame.image.load("images/bouton_jouer_normal.png"),
    "difficile": pygame.image.load("images/bouton_jouer_difficile.png"),
    "extreme": pygame.image.load("images/bouton_jouer_extreme.png"),
    "entrainement": pygame.image.load("images/bouton_entrainement.png")}

    #Coordonnées X des boutons
    coord_x = {"jouer": 400,
    "scores": 100,
    "credits": 700,
    "commandes": 200,
    "quitter": 600,
    "normal": 150 ,
    "difficile": 200,
    "extreme": 250,
    "entrainement": 300}

    #Coordonnées Y des boutons
    coord_y = {"jouer": 250,
    "scores": 400,
    "credits": 400,
    "commandes": 600,
    "quitter": 600,
    "normal": 300 ,
    "difficile": 400,
    "extreme": 500,
    "entrainement": 600}

    #Tranforme les boutons en rectangle de coordonnées (0,0)
    position_bouton = {"jouer": img_bouton["jouer"].get_rect(),
    "scores": img_bouton["scores"].get_rect(),
    "credits": img_bouton["credits"].get_rect(),
    "commandes": img_bouton["commandes"].get_rect(),
    "quitter": img_bouton["quitter"].get_rect(),
    "normal": img_bouton["normal"].get_rect(),
    "difficile": img_bouton["difficile"].get_rect(),
    "extreme": img_bouton["extreme"].get_rect(),
    "entrainement": img_bouton["entrainement"].get_rect()}

    curseur = pygame.image.load("images/curseur.png")
    position_curseur = curseur.get_rect()

    #Dimensions X des boutons
    dim_x = {"jouer": img_bouton["jouer"].get_width(),
    "scores": img_bouton["scores"].get_width(),
    "credits": img_bouton["credits"].get_width(),
    "commandes": img_bouton["commandes"].get_width(),
    "quitter": img_bouton["quitter"].get_width(),
    "normal": img_bouton["normal"].get_width() ,
    "difficile": img_bouton["difficile"].get_width(),
    "extreme": img_bouton["extreme"].get_width(),
    "entrainement": img_bouton["entrainement"].get_width()}

    #Dimensions Y des boutons
    dim_y = {"jouer": img_bouton["jouer"].get_height(),
    "scores": img_bouton["scores"].get_height(),
    "credits": img_bouton["credits"].get_height(),
    "commandes": img_bouton["commandes"].get_height(),
    "quitter": img_bouton["quitter"].get_height(),
    "normal": img_bouton["normal"].get_height() ,
    "difficile": img_bouton["difficile"].get_height(),
    "extreme": img_bouton["extreme"].get_height(),
    "entrainement": img_bouton["entrainement"].get_height()}

    bouton = {"jouer":Bouton(fenetre,fond_menu,img_bouton["jouer"],position_bouton["jouer"],coord_x["jouer"],coord_y["jouer"]),
    "scores":Bouton(fenetre,fond_menu,img_bouton["scores"],position_bouton["scores"],coord_x["scores"],coord_y["scores"]),
    "credits":Bouton(fenetre,fond_menu,img_bouton["credits"],position_bouton["credits"],coord_x["credits"],coord_y["credits"]),
    "commandes":Bouton(fenetre,fond_menu,img_bouton["commandes"],position_bouton["commandes"],coord_x["commandes"],coord_y["commandes"]),
    "quitter":Bouton(fenetre,fond_menu,img_bouton["quitter"],position_bouton["quitter"],coord_x["quitter"],coord_y["quitter"])}

    Bouton(fenetre,fond_menu,curseur,position_curseur,coord_x["jouer"],coord_y["jouer"])

    play = 0 #Variable de la boucle du menu Jouer : 0 = Menu principal ; 1 = Menu des difficultées
    curseur_pos = 1 #Variable de la position du curseur : 1 = Jouer ; 2 = Scores ; 3 = Crédits ; 4 = commandes ; 5 = Quitter ; 6 = Normal ; 7 = Difficile ; 8 = Extrême ; 9 = Parties Sauvegardées
    ScreenScore = score_screen(ecran_x,ecran_y)

    while True: #Boucle infinie
        pygame.time.Clock().tick(60)
        
        if charger()[0][4] != "- - -" and charger()[1][4] != "- - -" and charger()[2][4] != "- - -" and play == 0: #Affiche une petite couronne quand tous les modes de difficultés ont été terminés au moins une fois
            couronne = pygame.image.load("images/couronne.png")
            position_couronne = couronne.get_rect()
            Bouton(fenetre,fond_menu,couronne,position_couronne,400,410)
        

        for event in pygame.event.get():
            if event.type == QUIT: #Croix rouge de la fenêtre
                quitter()

            if event.type == KEYDOWN: #Boutons Clavier
                if event.key == K_ESCAPE: #Bouton Echap
                    retour_son.play()
                    if play == 0: #Quitte le jeu quand Echap est pressé
                        quitter()

                    if play == 1: #Retourne au menu principal quand Echap est pressé
                        curseur = pygame.image.load("images/curseur.png")
                        curseur_pos = retour(fenetre,fond_menu,titre,curseur_pos,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y) #Vers Jouer
                        play = 0

                if event.key == K_SPACE or event.key == K_RETURN: #Boutons Espace ou Entrée
                    if curseur_pos == 6: #Si sur Normal
                        valider.play()
                        main_game(clock,fond_jeu,ecran_y,0,retour_son,pygame.time.get_ticks()/1000,False)

                    if curseur_pos == 7: #Si sur Difficile
                        valider.play()
                        main_game(clock,fond_jeu,ecran_y,1,retour_son,pygame.time.get_ticks()/1000,False)

                    if curseur_pos == 8: #Si sur Extreme
                        valider.play()
                        main_game(clock,fond_jeu,ecran_y,2,retour_son,pygame.time.get_ticks()/1000,False)

                    if curseur_pos == 9: #Si sur Parties Sauvegardées
                        valider.play()
                        main_game(clock,fond_jeu,ecran_y,3,retour_son,pygame.time.get_ticks()/1000,True)

                    if curseur_pos == 1: #Si sur Jouer
                        valider.play()
                        curseur = pygame.image.load("images/curseur_jouer.png")
                        curseur_pos = jouer(fenetre,fond_menu,titre,curseur_pos,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y) #Vers Normal
                        play = 1

                    if curseur_pos == 2: #Si sur Scores
                        valider.play()
                        ScreenScore.creation(fenetre,retour_son)

                    if curseur_pos == 3: #Si sur Crédits
                        valider.play()
                        credits(fenetre,fond_credits,font,clock,retour_son)

                    if curseur_pos == 4: #Si sur commandes
                        valider.play()
                        commandes(fenetre,clock,fond_jeu,retour_son,ecran_x,ecran_y)

                    if curseur_pos == 5: #Si sur Quitter
                        retour_son.play()
                        quitter()

                if event.key == K_DOWN or event.key == K_s: #Boutons Bas ou S
                    if curseur_pos == 8: #Si sur Extrême
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["entrainement"],coord_y["entrainement"])
                        curseur_pos = 9 #Vers Parties Sauvegardées

                    if curseur_pos == 7: #Si sur Difficile
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["extreme"],coord_y["extreme"])
                        curseur_pos = 8 #Vers Extrême

                    if curseur_pos == 6: #Si sur Normal
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["difficile"],coord_y["difficile"])
                        curseur_pos = 7 #Vers Difficile

                    if curseur_pos == 3: #Si sur Crédits
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["quitter"],coord_y["quitter"])
                        curseur_pos = 5 #Vers Quitter

                    if curseur_pos == 2: #Si sur Scores
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["commandes"],coord_y["commandes"])
                        curseur_pos = 4 #Vers commandes

                    if curseur_pos == 1: #Si sur Jouer
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["scores"],coord_y["scores"])
                        curseur_pos = 2 #Vers Scores

                if event.key == K_UP or event.key == K_w: #Boutons Haut ou Z
                    if curseur_pos == 2: #Si sur Scores
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["jouer"],coord_y["jouer"])
                        curseur_pos = 1 #Vers Jouer

                    if curseur_pos == 3: #Si sur Crédits
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["jouer"],coord_y["jouer"])
                        curseur_pos = 1 #Vers Jouer

                    if curseur_pos == 4: #Si sur Option
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["scores"],coord_y["scores"])
                        curseur_pos = 2 #Vers Scores

                    if curseur_pos == 5: #Si sur Quitter
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["credits"],coord_y["credits"])
                        curseur_pos = 3 #Vers Crédits

                    if curseur_pos == 7: #Si sur Difficile
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["normal"],coord_y["normal"])
                        curseur_pos = 6 #Vers Normal

                    if curseur_pos == 8: #Si sur Extrême
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["difficile"],coord_y["difficile"])
                        curseur_pos = 7 #Vers Difficile

                    if curseur_pos == 9: #Si sur Parties Sauvegardées
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["extreme"],coord_y["extreme"])
                        curseur_pos = 8 #Vers Extrême

                if event.key == K_LEFT or event.key == K_a: #Boutons Gauche ou Q
                    if curseur_pos == 1: #Si sur Jouer
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["scores"],coord_y["scores"])
                        curseur_pos = 2 #Vers Scores

                    if curseur_pos == 3: #Si sur Crédits
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["scores"],coord_y["scores"])
                        curseur_pos = 2 #Vers Scores

                    if curseur_pos == 5: #Si sur Quitter
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["commandes"],coord_y["commandes"])
                        curseur_pos = 4 #Vers commandes

                if event.key == K_RIGHT or event.key == K_d: #Boutons Droite ou D
                    if curseur_pos == 1: #Si sur Jouer
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["credits"],coord_y["credits"])
                        curseur_pos = 3 #Vers Crédits

                    if curseur_pos == 2: #Si sur Scores
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["credits"],coord_y["credits"])
                        curseur_pos = 3 #Vers Crédits

                    if curseur_pos == 4: #Si sur commandes
                        curseur_son.play()
                        deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["quitter"],coord_y["quitter"])
                        curseur_pos = 5 #Vers Quitter

            if event.type == MOUSEBUTTONDOWN: #Boutons Souris
                if event.button == 1: #Boutons Clique gauche
                    if event.pos[0] > coord_x["normal"] and event.pos[0] < coord_x["normal"] + dim_x["normal"] and event.pos[1] > coord_y["normal"] and event.pos[1] < coord_y["normal"] + dim_y["normal"] and play == 1:  #Bouton Normal
                        if curseur_pos == 6: #Si sur Normal
                            valider.play()
                            main_game(clock,fond_jeu,ecran_y,0,retour_son,pygame.time.get_ticks()/1000,False)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["normal"],coord_y["normal"])
                            curseur_pos = 6 #Vers Normal

                    if event.pos[0] > coord_x["difficile"] and event.pos[0] < coord_x["difficile"] + dim_x["difficile"] and event.pos[1] > coord_y["difficile"] and event.pos[1] < coord_y["difficile"] + dim_y["difficile"] and play == 1:  #Bouton Difficile
                        if curseur_pos == 7: #Si sur Difficile
                            valider.play()
                            main_game(clock,fond_jeu,ecran_y,1,retour_son,pygame.time.get_ticks()/1000,False)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["difficile"],coord_y["difficile"])
                            curseur_pos = 7 #Vers Difficile

                    if event.pos[0] > coord_x["extreme"] and event.pos[0] < coord_x["extreme"] + dim_x["extreme"] and event.pos[1] > coord_y["extreme"] and event.pos[1] < coord_y["extreme"] + dim_y["extreme"] and play == 1:  #Bouton Extreme
                        if curseur_pos == 8: #Si sur Extrême
                            valider.play()
                            main_game(clock,fond_jeu,ecran_y,2,retour_son,pygame.time.get_ticks()/1000,False)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["extreme"],coord_y["extreme"])
                            curseur_pos = 8 #Vers Extrême

                    if event.pos[0] > coord_x["entrainement"] and event.pos[0] < coord_x["entrainement"] + dim_x["entrainement"] and event.pos[1] > coord_y["entrainement"] and event.pos[1] < coord_y["entrainement"] + dim_y["entrainement"] and play == 1:  #Bouton Parties Sauvegardées
                        if curseur_pos == 9: #Si sur Parties Sauvegardées
                            valider.play()
                            main_game(clock,fond_jeu,ecran_y,3,retour_son,pygame.time.get_ticks()/1000,True)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["entrainement"],coord_y["entrainement"])
                            curseur_pos = 9 #Vers Extrême

                    if event.pos[0] > coord_x["jouer"] and event.pos[0] < coord_x["jouer"] + dim_x["jouer"] and event.pos[1] > coord_y["jouer"] and event.pos[1] < coord_y["jouer"] + dim_y["jouer"] and play == 0:  #Bouton Jouer
                        if curseur_pos == 1: #Si sur Jouer
                            valider.play()
                            curseur = pygame.image.load("images/curseur_jouer.png")
                            curseur_pos = jouer(fenetre,fond_menu,titre,curseur_pos,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y) #Vers Jouer
                            play = 1

                            pygame.display.flip() #Rafraichissement de la page
                            pygame.time.delay(200)

                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["jouer"],coord_y["jouer"])
                            curseur_pos = 1 #Vers Jouer/Normal

                    if event.pos[0] > coord_x["scores"] and event.pos[0] < coord_x["scores"] + dim_x["scores"] and event.pos[1] > coord_y["scores"] and event.pos[1] < coord_y["scores"] + dim_y["scores"] and play == 0:  #Bouton Scores
                        if curseur_pos == 2: #Si sur Scores
                            valider.play()
                            ScreenScore.creation(fenetre,retour_son)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["scores"],coord_y["scores"])
                            curseur_pos = 2 #Vers Scores

                    if event.pos[0] > coord_x["credits"] and event.pos[0] < coord_x["credits"] + dim_x["credits"] and event.pos[1] > coord_y["credits"] and event.pos[1] < coord_y["credits"] + dim_y["credits"] and play == 0:  #Bouton Crédits
                        if curseur_pos == 3: #Si sur Crédits
                            valider.play()
                            credits(fenetre,fond_credits,font,clock,retour_son)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["credits"],coord_y["credits"])
                            curseur_pos = 3 #Vers Crédits

                    if event.pos[0] > coord_x["commandes"] and event.pos[0] < coord_x["commandes"] + dim_x["commandes"] and event.pos[1] > coord_y["commandes"] and event.pos[1] < coord_y["commandes"] + dim_y["commandes"] and play == 0:  #Bouton commandes
                        if curseur_pos == 4: #Si sur commandes
                            valider.play()
                            commandes(fenetre,clock,fond_jeu,retour_son,ecran_x,ecran_y)
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["commandes"],coord_y["commandes"])
                            curseur_pos = 4 #Vers commandes

                    if event.pos[0] > coord_x["quitter"] and event.pos[0] < coord_x["quitter"] + dim_x["quitter"] and event.pos[1] > coord_y["quitter"] and event.pos[1] < coord_y["quitter"] + dim_y["quitter"] and play == 0:  #Bouton Quitter
                        if curseur_pos == 5: #Si sur Quitter
                            retour_son.play()
                            quitter()
                        else:
                            curseur_son.play()
                            deplacer_curseur(fenetre,fond_menu,curseur_pos,play,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y,coord_x["quitter"],coord_y["quitter"])
                            curseur_pos = 5 #Vers Quitter

                if event.button == 3: #Bouton Clique droit
                    if play == 1:  #Bouton Retour (n'importe où sur l'écran)
                        retour_son.play()
                        curseur = pygame.image.load("images/curseur.png")
                        curseur_pos = retour(fenetre,fond_menu,titre,curseur_pos,curseur,position_curseur,img_bouton,position_bouton,coord_x,coord_y) #Vers Jouer
                        play = 0

if __name__ == '__main__':
    musique()
    main()