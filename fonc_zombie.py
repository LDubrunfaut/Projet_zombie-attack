# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import random
import re
import math
import sys
import time
import pylab

def extract_carte():
    '''
    Récupère les coordonnées de la carte svg qui correspondent à la France.
    Renvoie :
        > une liste de listes des coordonnées x et y de chacun des points
        de la carte de France.
    '''
    repere_france = re.compile('france')
    
    filin = open('france.svg','r')
    ligne = filin.readline()
    coord_france = repere_france.search(ligne)
    while not coord_france:
        #stocker la ligne afin de la conserver, au cas où la ligne suivante
        #nous informe que c'était les coordonnées de la france
        coord = ligne
        ligne = filin.readline()
        coord_france = repere_france.search(ligne)
    
    filin.close()
    
    coord_regex = re.compile('[0-9]+\.?[0-9]*')
    coord_list = coord_regex.findall(coord)
    carte = []
    
    for i in xrange(0,len(coord_list),2):
        #stock dans une liste les coordonnées x et y
        #de chaque point de la France
        carte.append([float(coord_list[i]), float(coord_list[i+1])])
    
    return carte


def transform_repere(carte):
    '''
    Transforme les coordonnées afin qu'elles correspondent à un repère
    classique.
    Prend en argument :
        > la liste des coordonnées des points de la carte.
    Renvoie :
        > la liste transformée des coordonnées des points de la carte.
    '''
    maxY = 0
    for i in xrange(len(carte)-1):
        if carte[i][1] > maxY:
            maxY = carte[i][1]
    
    for i in xrange(len(carte)-1):
        #pour trouver la nouvelle valeur y,
        #on la retranche à la valeur y maximale de la carte.
        carte[i][1] = maxY-carte[i][1]
    
    return carte


def extract_x_y(carte):
    '''
    Stocke les coordonnées x et y dans deux listes différentes,
    afin de pouvoir afficher les points sur un graphique.
    Prend en argument :
        > la liste des coordonnées des points de la carte.
    Renvoie deux listes :
        > la première contient les coordonnées x,
        > la seconde les coordonnées y.
    '''
    x_carte = []
    y_carte = []
    for i in xrange(len(carte)-1):
        x_carte.append(carte[i][0])
        y_carte.append(carte[i][1])
    
    return x_carte,y_carte


def point_dans_france(x, y, carte):
    '''
    Indique si un point est contenu dans la carte ou non.
    Prend en arguments :
        > les coordonnées du point,
        > la liste contenant les coordonnées de la carte.
    Renvoie True si le point est contenu dans la carte, et False si non.
    '''
    n = len(carte)
    inside = False
    
    p1x,p1y = carte[0]
    for i in xrange(n+1):
        p2x,p2y = carte[i % n]
        if y > min(p1y,p2y) and y <= max(p1y,p2y):
            if x <= max(p1x,p2x):
                if p1y != p2y:
                    xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
        p1x,p1y = p2x,p2y
    
    return inside


def coord_range(x0, y0, rayon):
    '''
    Calcule les coordonnées d'un nouveau point sur la carte,
    voisin du précédent.
    Prend en arguments :
        > les coordonnées du point existant,
        > le rayon autour de celui-ci dans lequel on souhaite créer de
        nouveaux points.
    Renvoie :
        > les coordonnées x et y du nouveau point.
    '''
    plus_moins = (-1,1) #afin de parcourir 2pi
    div = random.randint(0,24)
    angle = float(div)/48*math.pi #on trouve un angle sur le demi-cercle
    randX = random.choice(plus_moins)
    randY = random.choice(plus_moins)
    
    #calcul des nouvelles coordonnées,
    #à partir de l'angle et des coordonnées du point précédent :
    x_new = randX * (math.cos(angle)*rayon) + x0
    y_new = randY * (math.sin(angle)*rayon) + y0
    return [x_new,y_new]


def generation_villes(x0, y0, indiv_max, rayon_max, carte):
    '''
    Génère la population.
    Prend en arguments :
        > les coordonnées du point existant,
        > le nombre d'individus qu'on souhaite créer,
        > le rayon dans lequel doit être créer l'individu voisin,
        > la liste des coordonnées des points de la France.
    Renvoie :
        > une liste de listes de coordonnées des points à afficher.
    '''
    map_point = []
    for i in xrange(indiv_max):
        rayon = random.uniform(0, rayon_max)
        x_new,y_new = coord_range(x0, y0, rayon)
        verif_new_point = point_dans_france(x_new, y_new, carte)
        while verif_new_point == False:
            rayon=random.uniform(0, rayon_max)
            x_new,y_new = coord_range(x0,y0,rayon)
            verif_new_point = point_dans_france(x_new, y_new, carte)
        map_point.append([x_new,y_new])
        #liste contenant les coordonnées de tous les points
    return map_point


def det_villes():
    '''
    Détermine les coordonnées des zones de densité de population en France
    Renvoie :
      > un dictionnaire contenant les coordonnées des villes
    '''
    paris,lille,marseille,nice={},{},{},{}
    toulouse,rennes,lyon,nantes={},{},{},{}
    montpellier,bordeaux,strasbourg={},{},{}
    
    #on indique les points de départ des villes
    nice['x'], nice['y'] = 460, 85
    lyon['x'], lyon['y'] = 340, 200
    paris['x'], paris['y'] = 275, 340
    lille['x'], lille['y'] = 285, 455
    rennes['x'], rennes['y'] = 115, 335
    nantes['x'], nantes['y'] = 100, 280
    toulouse['x'], toulouse['y'] = 220, 93
    bordeaux['x'], bordeaux['y'] = 145, 150
    marseille['x'], marseille['y'] = 365, 65
    strasbourg['x'], strasbourg['y'] = 456, 355
    montpellier['x'], montpellier['y'] = 315, 65
    
    villes={'paris':paris,'lille':lille,'marseille':marseille,'nice':nice,\
    'toulouse':toulouse,'rennes':rennes,'montpellier':montpellier,\
    'bordeaux':bordeaux,'nantes':nantes,'lyon':lyon,'strasbourg':strasbourg}
    
    return villes


def generation_points(carte, villes):
    '''
    Créer les individus des zones de densité de population.
    Renvoie :
        > la liste des coordonnées des points de la population.
    '''
    #on insiste sur la région parisienne, zone très densément peuplée
    population = generation_villes(villes['paris']['x'],\
    villes['paris']['y'], 200, 75, carte)
    for ville in villes:
        population = population + \
        generation_villes(villes[ville]['x'], villes[ville]['y'], 175, 100, carte)
    
    return population


def create_graph(population):
    '''
    Création du graph qui stocke la population.
    Prend en argument :
        > la liste des coordonnées des points de la population.
    Renvoie :
        > une liste contenant une liste par individu de la population,
        dans laquelle est indiqués pour chaque individu :
        0: son x, 1: son y,
        2: la liste de ses voisins du plus proche au plus loin,
        3: son marqueur (marqueur: 0:mort 1:sain 2:contaminé 3:zombie)
    '''
    #création de deux listes contenant séparément les coordonnées x et y
    #de la population
    popX = []
    popY = []
    for i in xrange(len(population)):
        popX.append(population[i][0])
        popY.append(population[i][1])
    
    #pour chaque point, il faut faire la liste de ses voisins
    distance = []
    voisins = []
    for i in xrange(len(population)):
        for j in xrange(len(population)):
            if i != j:
                vec_distance = \
                math.sqrt((popX[i]-popX[j])**2 + (popY[i]-popY[j])**2)
                #pour chaque point on retient uniquement les voisins dans
                #un périmètre donné :
                if vec_distance < 25:
                    distance.append([vec_distance,j])
        distance.sort()
        voisins.append(distance)
        distance = []
    
    #Création de la liste qui stocke les individus.
    pop_graph = []
    for i in xrange(len(population)):
        pop_graph.append([popX[i], popY[i], voisins[i],1])
    
    return pop_graph

def det_chercheur(taille_pop):
    '''
    Crée le chercheur distrait, premier zombie
    Renvoie :
      > le numéro de l'individu qui est le chercheur
    '''
    chercheur = random.randint(0,taille_pop)
    return chercheur

def epidemie(pop_graph, x_carte, y_carte, chercheur, leon):
    '''
    Affiche l'évolution de l'épidémie dans la population.
    Prend en argument :
      > une liste contenant une liste pour chaque individu de la population,
        dans laquelle doit être indiqués :
        0: son x, 1: son y,
        2: la liste de ses voisins du plus proche au plus loin,
        3: son marqueur (marqueur: 0:mort 1:sain 2:contaminé 3:zombie)
      > la liste des coordonnées x de la carte
      > la liste des coordonnées y de la carte
    '''
    if leon == [0,0]:
        secours = 0
    else:
        secours = 1
    
    #le chercheur est tiré au sort aléatoirement dans la population
    pop_graph[chercheur][3] = 3 #le chercheur est devenu zombie
    
    #création de listes qui répertorie les individus de la population,
    #en fonction de leur statut face à la maladie
    liste_zombie = [chercheur]
    liste_contamine = []
    liste_mort = []
    liste_sain = range(len(pop_graph))
    #le chercheur n'est plus sain, donc il faut le supprimer de ce listing
    liste_sain.remove(chercheur)
    if secours == 1:
        liste_leon = [len(pop_graph)-1]
    
    #la propagation de l'épidémie
    nb_jour = 0
    plt.ion()
    
    for i in xrange(int(sys.argv[1])):
        
        #parcours des zombies pour attaquer leurs voisins
        for i in liste_zombie:
            for j in xrange(len(pop_graph[i][2])):
            #le zombie a 1 chance sur 10 de contaminer ses voisins sains
                if pop_graph[pop_graph[i][2][j][1]][3] == 1 \
                and random.randint(1,10) == 1:
                    pop_graph[pop_graph[i][2][j][1]][3] = 2
                    #le voisin est ainsi contamine
                    #puis il est ajouté à la liste des contaminés
                    #et retiré de la liste des sains
                    liste_contamine.append(pop_graph[i][2][j][1])
                    liste_sain.remove(pop_graph[i][2][j][1])
                #le zombie a 1 chance sur 25 de contaminer les "léons"
                if pop_graph[pop_graph[i][2][j][1]][3] == 4 \
                and random.randint(1,25) == 1:
                    pop_graph[pop_graph[i][2][j][1]][3] = 2
                    liste_contamine.append(pop_graph[i][2][j][1])
                    liste_leon.remove(pop_graph[i][2][j][1])
        
        #parcours des sains pour tuer les contaminés
        for i in liste_sain:
            #si des voisins sont contaminés, alors il va tenter de les tuer
            for j in xrange(len(pop_graph[i][2])):
                if pop_graph[pop_graph[i][2][j][1]][3] == 2 \
                and random.randint(1,70) == 1 :
                #il a 1 chance sur 70 de les tuer
                        pop_graph[pop_graph[i][2][j][1]][3] = 0
                        liste_contamine.remove(pop_graph[i][2][j][1])
                        liste_mort.append(pop_graph[i][2][j][1])
        
        #parcours des contaminés pour qu'ils se zombifient
        for i in liste_contamine:
            if random.randint(1,10) < 8:
            #un contaminé à 7chances sur 10 de se transformer
                pop_graph[i][3] = 3
                liste_contamine.remove(i)
                liste_zombie.append(i)
        
        #parcours pour que Léon et ses "soldats" communiquent leur savoir
        if secours == 1:
            for i in liste_leon:
                for j in xrange(len(pop_graph[i][2])):
                    if pop_graph[pop_graph[i][2][j][1]][3] == 3:
                    #il a 1 chance sur 3 de les tuer
                        if random.randint(1,3) == 1:
                            pop_graph[pop_graph[i][2][j][1]][3] = 0
                            liste_zombie.remove(pop_graph[i][2][j][1])
                            liste_mort.append(pop_graph[i][2][j][1])
                    if pop_graph[pop_graph[i][2][j][1]][3] == 1:
                    #il a 1 chance sur 200 de les entrainer
                        if random.randint(1,200)==1:
                            pop_graph[pop_graph[i][2][j][1]][3] = 4
                            liste_leon.append(pop_graph[i][2][j][1])
                            liste_sain.remove(pop_graph[i][2][j][1])
        
        #pour afficher sur le graphique
        zombieX,zombieY = [],[]
        contamineX,contamineY = [],[]
        sainX,sainY = [],[]
        mortX,mortY = [],[]
        leonX,leonY = [],[]
        for i in liste_zombie:
            zombieX.append(pop_graph[i][0])
            zombieY.append(pop_graph[i][1])
        for i in liste_contamine:
            contamineX.append(pop_graph[i][0])
            contamineY.append(pop_graph[i][1])
        for i in liste_sain:
            sainX.append(pop_graph[i][0])
            sainY.append(pop_graph[i][1])
        for i in liste_mort:
            mortX.append(pop_graph[i][0])
            mortY.append(pop_graph[i][1])
        if secours==1:
            for i in liste_leon:
                leonX.append(pop_graph[i][0])
                leonY.append(pop_graph[i][1])
        
        nb_jour+=1
        #placement du titre
        titre='Jour {0}'.format(nb_jour)
        plt.title(titre)
        #placement des points
        plt.plot(sainX, sainY, 'go', label="Sains")
        plt.plot(mortX, mortY, 'ko', label="Morts")
        plt.plot(contamineX, contamineY, 'yo', label="Contamines")
        plt.plot(zombieX, zombieY, 'ro', label="Zombies")
        plt.plot(x_carte, y_carte, 'b')
        if secours == 1:
            plt.plot(leonX, leonY, 'bo', label="Combattants")
        
        if nb_jour == 1:
            #affichage de la légende
            plt.legend(bbox_to_anchor = (1, 1),\
            bbox_transform=plt.gcf().transFigure)
            #premier affichage de la carte
            plt.show()
            pylab.waitforbuttonpress(timeout=-1)
        else:
            pylab.waitforbuttonpress(timeout=-1)
            #raffraichissement de la carte
            plt.draw()
    
    plt.ioff()
    plt.close()

def choix_user_leon(villes):
    choix_ville = ''
    print "\nIl est possible de choisir une ville où Léon S. Kennedy,"
    print "agent fédéral venant des USA, pourrait entrainer une partie"
    print "de la population à tuer les zombies."
    print "\nVous pouvez choisir les villes :"
    for ville in villes:
        print "{0:^11}".format(ville)
    choix_ville = raw_input("\nEcrivez la ville souhaitée : ")
    while choix_ville not in villes:
        choix_ville = raw_input("\nEcrivez la ville souhaitée : ")
    leon = [villes[choix_ville]['x'],villes[choix_ville]['y']]
    return leon
