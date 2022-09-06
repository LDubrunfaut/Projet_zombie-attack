#! /usr/bin/env python
# -*- coding: utf-8 -*-


from fonc_zombie import *


if len(sys.argv) != 2:
    sys.exit("Veuillez préciser le nombre de jours de simulation")

jours_simulation=re.compile('[0-9]+')
if not jours_simulation.search(sys.argv[1]):
    sys.exit("ERREUR : il faut indiquer en argument un nombre de jours")


carte = []
population = []
pop_graph = []

carte = extract_carte() #extrait les coordonnées du fichier SVG
carte = transform_repere(carte) #adapte les coordonnées au repère classique
x_carte, y_carte = extract_x_y(carte)

# Scénario 1 : sans résistance
villes = det_villes()
population = generation_points(carte, villes)
pop_graph = create_graph(population) #crée le graph de la population
chercheur = det_chercheur(len(pop_graph)-1)
epidemie(pop_graph, x_carte, y_carte, chercheur, [0,0]) #déroule l'épidémie

# Scénario 2 : avec résistance
leon = choix_user_leon(villes)
population.append(leon)
pop_graph = create_graph(population) #ajoute Léon au graph de la population
epidemie(pop_graph, x_carte, y_carte, chercheur, leon)
