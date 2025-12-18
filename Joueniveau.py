print('Iloksfamily by FC - v2.1')
print('> loading modules...')
import pygame, math, time, random
import os
try:
    print(fichier)
except:
    demarreparconstructeur=False
    os.chdir("../") #a enlever pour freeze, a remettre pour executer. python setup.py build   (ou bdist_msi)
pygame.init()

from var import *
InitialiseFenetre()

from AfficheCarte import *
from ClassesBlocs13 import *
from Menus11 import *
import ClassesBlocs13


fin=0
print('>...modules loaded')

while True:
    a=pygame.event.get()
    if a!=[]:print(a)

for name, objet in inspect.getmembers(ClassesBlocs13):
    if inspect.isclass(objet):
        if issubclass(objet, Mobile) and name not in['Boule', 'Barre', 'CaptFeu', 'Mobile', 'Joueur', '', 'Mongolfier', 'JoueurCarte'] and issubclass(eval(name), Boule)==False:
            mobiles.append(name)

#Bienvenue()
#com=Com()
if phone_mode:
    Connexion()

#### Pour test seulement #########
##jeu=Jeu(-1,None)
##jeu.run()
##################################
ok=0
while ok==0:
    try:
        try: f = open(fichier, 'rb')
        except: f = open("./" + fichier, 'rb')
        pick=pickle.load(f, encoding='latin1')
        f.close
        ok=1
    except:
        print('fichier à utiliser? : ')
        fichier = input(os.getcwd()+'/')
print(pick)
while True:
    jeu=Jeu(-2, 0, pick)
    time.sleep(1)
    [cont, points]=jeu.run()
    if cont ==1 and demarreparconstructeur:
        if input('modifier?'):
            break
    del jeu
try:del jeu
except: pass
print("FIN")
#pygame.quit()  #ferme la librairie pygame
