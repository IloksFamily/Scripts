print('Iloksfamily by FC - v2.1')
print('> loading modules...')
import pygame, math, time, random
import os, sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0]))) # se remet sur le chemin du fichier
os.chdir("../") #a enlever pour freeze, a remettre pour executer. python setup.py build   (ou bdist_msi)
pygame.init()

from var import *
InitialiseFenetre()

from AfficheCarte import *
from Menus11 import *
from ClassesBlocs13 import *
import ClassesBlocs13


fin=0
print('>...modules loaded')

for name, objet in inspect.getmembers(ClassesBlocs13):
    if inspect.isclass(objet):
        if issubclass(objet, Mobile) and name not in['Boule', 'Barre', 'CaptFeu', 'Mobile', 'Joueur', '', 'Mongolfier', 'JoueurCarte'] and issubclass(eval(name), Boule)==False:
            mobiles.append(name)

Bienvenue()
#com=Com()
if phone_mode:
    Connexion()

#### Pour test seulement #########
##jeu=Jeu(-1,None)
##jeu.run()
##################################

ChoixJoueurs()

while(True):
    partie=ChoixPartie()
    carte=JeuCarte(partie)
    fin=0
    while(fin==0):
        [continu,points,direct_carte]=carte.run()
        if continu==-1: cont=-1
        else:
            cont=0
            if continu==-2: fin=1        
        print(fin)
        while(cont==-1):
            jeu=Jeu(partie,direct_carte)
            [cont, points]=jeu.run()
            del jeu
        if cont>0:
            carte.valide_niveau(direct_carte[0],direct_carte[1])
            print('Valide_niveau', direct_carte[0], direct_carte[1])
            FinNiveau(points) 
            carte.majniveauxfaits(partie, direct_carte)
            #comp.comfinniveau(partie,direct_carte)
    del carte
print("FIN")
pygame.quit()  #ferme la librairie pygame
