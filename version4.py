#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Stocke les coordonnées de la carte dans une liste,
et les transforme pour correspondre à un repère classique.
'''

import matplotlib.pyplot as plt
import numpy as np
import random
import re
import math
import sys
import time

if len(sys.argv) != 2:
    sys.exit("Veuillez préciser le nombre de jours de simulation")

jours_simulation=re.compile('[0-9]+')
if not jours_simulation.search(sys.argv[1]):
    sys.exit("ERREUR : il faut indiquer en argument un nombre de jours")

# Stocke les coordonnées de la carte dans une liste

repere_regex = re.compile('^ +<path')
marqueur_france=0
filin = open('france.svg','r')
ligne=filin.readline()
while ligne != "":
    debut_coord_france=repere_regex.search(ligne)
    if debut_coord_france:
        if marqueur_france==1:
            break
        marqueur_france+=1
    ligne=filin.readline()
coord=filin.readline()
filin.close()

coord_regex=re.compile('[0-9]+\.?[0-9]*')
coord_list=coord_regex.findall(coord)
france=[]

for i in xrange(0,len(coord_list),2):
    france.append( [float(coord_list[i]) , float(coord_list[i+1]) ])
    

# Transforme les coordonnées pour qu'elles correspondent à un repère classique

min_max_xy={}
min_max_xy['maxX']=0
min_max_xy['minX']=france[0][0]
min_max_xy['maxY']=0
min_max_xy['minY']=france[0][1]
for i in xrange(len(france)-1):
    if france[i][1]>min_max_xy['maxY']:
        min_max_xy['maxY'] = france[i][1]
    if france[i][1]<min_max_xy['minY']:
        min_max_xy['minY'] = france[i][1]
    if france[i][0]>min_max_xy['maxX']:
        min_max_xy['maxX'] = france[i][0]
    if france[i][0]<min_max_xy['minX']:
        min_max_xy['minX'] = france[i][0]

for i in xrange(len(france)-1):
    france[i][1] = min_max_xy['maxY']-france[i][1]

#Pour afficher la carte de France
x=[]
y=[]
for i in xrange(len(france)-1):
    x.append(france[i][0])
    y.append(france[i][1])

#plt.plot(x,y)
#plt.show()
carte=france

# Vérifie si le point est dans la France

def point_dans_france(x,y,carte):
    n = len(carte)
    inside =False
    
    p1x,p1y = carte[0]
    for i in range(n+1):
        p2x,p2y = carte[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    
    return inside


# Génération d'un point aléatoirement

def point_random(min_max_xy):
    x=random.uniform(min_max_xy['minX'],min_max_xy['maxX'])
    y=random.uniform(min_max_xy['minY'],min_max_xy['maxY'])
    return [x,y]
    

# Création du premier point

chercheurX,chercheurY = point_random(min_max_xy)
verif_chercheur = point_dans_france(chercheurX, chercheurY, carte)
while verif_chercheur == False:
    #print chercheurX, chercheurY
    chercheurX,chercheurY = point_random(min_max_xy)
    verif_chercheur = point_dans_france(chercheurX,chercheurY,carte)

#print verif_chercheur
#plt.plot(x,y)
#plt.plot(chercheurX,chercheurY,'or')
#plt.show()


# Création des points voisins

def coord_range(x0,y0,rayon):
    plus_moins = (-1,1)
    div = random.randint(0,24)
    angle = float(div)/48*math.pi
    randX = random.choice(plus_moins)
    randY = random.choice(plus_moins)
    x_new = randX * (math.cos(angle)*rayon) + x0
    y_new = randY * (math.sin(angle)*rayon) + y0
    return [x_new,y_new]


def generation_points(x0, y0, indiv_max, rayon_max, carte):
    map_point = []
    for i in xrange(indiv_max):
        rayon = random.uniform(0, rayon_max)
        x_new,y_new = coord_range(x0, y0, rayon)
        verif_new_point = point_dans_france(x_new, y_new, carte)
        while verif_new_point == False:
            #print verif_new_point
            rayon=random.uniform(0,rayon_max)
            x_new,y_new = coord_range(x0,y0,rayon)
            verif_new_point = point_dans_france(x_new, y_new, carte)
        map_point.append([x_new,y_new])
    return map_point


# Génération de la population française, oui madame

paris,lille,marseille,nice={},{},{},{}
toulouse,rennes,lyon,nantes={},{},{},{}
montpellier,bordeaux,strasbourg={},{},{}

paris['x'], paris['y'] = 275, 340
lille['x'], lille['y'] = 285, 455
marseille['x'], marseille['y'] = 365, 65
nice['x'], nice['y'] = 460, 85
toulouse['x'], toulouse['y'] = 220, 93
rennes['x'], rennes['y'] = 115, 335
montpellier['x'], montpellier['y'] = 315, 65
bordeaux['x'], bordeaux['y'] = 145, 150
nantes['x'], nantes['y'] = 100, 280
strasbourg['x'], strasbourg['y'] = 456, 355
lyon['x'], lyon['y'] = 340, 200

villes=[paris,lille,marseille,nice,toulouse,rennes,\
montpellier,bordeaux,nantes,lyon,strasbourg]

population = generation_points(paris['x'],paris['y'],200,75,carte)
for ville in villes:
    population = population + generation_points(ville['x'],ville['y'],175,100,carte)

popX=[]
popY=[]
for i in xrange(len(population)):
    popX.append(population[i][0])
    popY.append(population[i][1])

#plt.plot(x,y)
#plt.plot(popX,popY,'or')
#plt.show()


# Création du graph qui stocke la population

#création de la liste des voisins
distance = []
voisins = []
for i in xrange(len(population)):
    for j in xrange(len(population)):
        if i!=j:
            vec_distance = \
            math.sqrt( (popX[i]-popX[j])**2 + (popY[i]-popY[j])**2 )
            if vec_distance<25:
                distance.append([vec_distance,j])
    distance.sort()
    voisins.append(distance)
    distance = []

#testeur de proximité
#marqueur=0
#for i in xrange(len(voisins)):
#    if len(voisins[i])==0:
#        marqueur+=1
#print marqueur

#création de la liste qui stocke les sommets
#chaque individu est caractérisé par :
#0: son x, 1: son y,
#2: la liste de ses voisins du plus proche au plus loin,
#3: son marqueur (marqueur: 0:mort 1:sain 2:contaminé 3:zombie)
pop_graph = []
for i in xrange(len(population)):
    pop_graph.append([popX[i],popY[i],voisins[i],1])


# Epidémie

#le chercheur
chercheur = random.randint(0,2124)
pop_graph[chercheur][3] = 3 #le chercheur est devenu zombie

liste_zombie = [chercheur]
liste_contamine = []
liste_sain = range(2125)
#le chercheur n'est plus sain, donc il faut le supprimer de ce listing
liste_sain.remove(chercheur)
liste_mort = []


#la propagation de l'épidémie

#for i in xrange(15):
#    for i in liste_zombie:
#        for j in xrange(len(pop_graph[i][2])):
#        #le zombie a 1 chance sur 5 de contaminer ses voisins sains
#            if pop_graph[pop_graph[i][2][j][1]][3]==1 \
#            and random.randint(1,5)==1:
#                pop_graph[pop_graph[i][2][j][1]][3] = 2
#                #le voisin est ainsi contamine
#                #puis il est ajouté à la liste des contaminés
#                #et retiré de la liste des sains
#                liste_contamine.append(pop_graph[i][2][j][1])
#                liste_sain.remove(pop_graph[i][2][j][1])


#voisins_zombie = []
#for i in liste_zombie:
#    for j in xrange(len(pop_graph[i][2])):
#    #on regarde les voisins des zombies
#        if pop_graph[pop_graph[i][2][j][1]][3]==1:
#        #si le voisin est sain, alors on le stocke dans une liste
#            voisins_zombie.append(pop_graph[i][2][j][1])
#    for k in voisins_zombie:
#    #le zombie a 1 chance sur 5 de contaminer ses voisins sains
#        if random.randint(1,5)==1:
#            pop_graph[k][3] = 2 #le voisin est contamine
#            liste_contamine.append(k)
#            liste_sain.remove(k)
#    voisins_zombie = []
nb_jour = 0
plt.ion()

for i in xrange(int(sys.argv[1])):
    for i in liste_zombie:
        for j in xrange(len(pop_graph[i][2])):
        #le zombie a 1 chance sur 5 de contaminer ses voisins sains
            if pop_graph[pop_graph[i][2][j][1]][3]==1 \
            and random.randint(1,5)==1:
                pop_graph[pop_graph[i][2][j][1]][3] = 2
                #le voisin est ainsi contamine
                #puis il est ajouté à la liste des contaminés
                #et retiré de la liste des sains
                liste_contamine.append(pop_graph[i][2][j][1])
                liste_sain.remove(pop_graph[i][2][j][1])
    
    for i in liste_sain:
        #si des voisins sont contaminés, alors il va tenter de les tuer
        for j in xrange(len(pop_graph[i][2])):
            if pop_graph[pop_graph[i][2][j][1]][3]==2:
            #il a 1 chance sur 100 de les tuer
                if random.randint(1,100)==1:
                    pop_graph[pop_graph[i][2][j][1]][3] = 0
                    liste_contamine.remove(pop_graph[i][2][j][1])
                    liste_mort.append(pop_graph[i][2][j][1])
    
    for i in liste_contamine:
        if random.randint(1,10)<8:
        #un contaminé à 7chances sur 10 de se transformer
            pop_graph[i][3] = 3
            liste_contamine.remove(i)
            liste_zombie.append(i)
    
    #pour afficher sur le graphique
    zombieX,zombieY = [],[]
    contamineX,contamineY = [],[]
    sainX,sainY = [],[]
    mortX,mortY = [],[]
    
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
    
    nb_jour+=1
    
    ax = plt.subplot(111) #pour l'ajout d'une légende
    p1, = ax.plot(sainX, sainY, 'go', label="Sains")
    p2, = ax.plot(mortX, mortY, 'ko', label="Morts")
    p3, = ax.plot(contamineX, contamineY, 'yo', label="Contamines")
    p4, = ax.plot(zombieX, zombieY, 'ro', label="Zombies")
    plt.plot(x, y, 'b')
    titre='Jour {0}'.format(nb_jour)
    plt.title(titre)
    
    
    if nb_jour==1:
        #affichage de la légende
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper left')
        #bbox_to_anchor=(0.9, 0.9)
        plt.show()
        plt.pause(0.05)
    else:
        plt.pause(0.05)
        plt.draw()

plt.ioff()
plt.pause(600)



