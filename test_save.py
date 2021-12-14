import pickle

##### génératoin d'un nouveau fichier #####

def nouveau_fichier():
    fichier = open('save_scores/scores.txt','xb') #on créer un nouveau fichier et on l'ouvre en écriture
    liste_vide = []
    for i in range(4):
        nouvelle_ligne = []
        for i in range(5):
            nouvelle_ligne.append("- - -")
        liste_vide.append(nouvelle_ligne)
    pickle.dump(liste_vide,fichier)
    fichier.close()

##### test de l'existence du fichier des saves #####
def vérification():
    try:
        with open('save_scores/scores.txt'): pass  #si le fichier existe au chemin indiqué, on ne fait rien
    except IOError:
        nouveau_fichier()   #sinon on génère un nouveau fichier ne contenant aucun score.

##### chargement/enregistrement des scores #####

def enregistrer(nouveau_score):
    vérification()
    with open('save_scores/scores.txt','wb') as fichier:
        pickle.dump(nouveau_score,fichier)    

def charger():          #retourne le tableau à deux dimensions qui contient les scores
    vérification()
    with open('save_scores/scores.txt','rb') as fichier:
        liste = pickle.load(fichier)
        return(liste)

##### modifier la liste des scores #####

def ecriture_score(numero_de_liste, minutes, secondes):  
    """n=0 pour normal, n=1 pour difficile, n=2 pour extreme"""
    """on retourne True si une valeur est modifiée, False sinon"""

    if minutes > 9:
        #si la valeur en minute est supérieure ou égale à 10 on a des problèmes
        #de comparaisons, le cas ne devrais pas se présenter de toute façon
        return False
    
    tableau_des_scores = charger()
    liste_etudiee = tableau_des_scores[numero_de_liste]

    if (liste_etudiee[0] == "- - -"): #test si on doit effectuer la première boucle
        del liste_etudiee[0]
        liste_etudiee.append(convertir(minutes, secondes))
        liste_etudiee.sort()
        enregistrer(tableau_des_scores)
        return True
    else: #si on arrive ici alors il n'y a donc plus de cases sans valeurs
        test_ecriture = False
        for i in range(len(liste_etudiee)): #deuxième boucle, on va tester la liste en commençant par la fin, les scores étant rangés par ordre croissant
            if (liste_etudiee[4-i] > convertir(minutes, secondes)):
                test_ecriture = True
                if (i == 0):
                    liste_etudiee[4-i] = convertir(minutes, secondes)
                else:
                    liste_etudiee[4-i+1] = liste_etudiee[4-i]
                    liste_etudiee[4-i] = convertir(minutes, secondes)
        """on décale de un rang vers la droite les résultats tant qu'il sont supérieurs au score
        que l'on veut écrire, en effet plus le temps est petit et meilleure est la performance"""

    if (test_ecriture == True):
        enregistrer(tableau_des_scores)
        return True #si test est True c'est qu'on a modifié la liste, on enregistre donc la modification

    return False #si on arrive ici c'est qu'aucune valeur n'a été modifiée, on l'indique en retournant False

def convertir(minutes, secondes):
    if secondes < 10 :
        return str(minutes)+"min 0" +str(secondes)+"sec"
    else:

        return str(minutes)+"min " +str(secondes)+"sec"

print(charger())