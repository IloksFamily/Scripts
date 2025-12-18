#Version 2.0 modifiee depuis 1.3

import pickle, os
import pygame, sys
import random
from pygame.locals import *
import ClassesBlocs13
pygame.init()

###### INITIALISATION DES VARIABLES #####
def autobuild(Difficulte, nom_fichier, zone, listeBMD):
    mode='graph'
    xgraph=0
    ygraph=0
##    xecran=0
    perso_type_select=0
    bloc_type_select=-1
    nb_type_perso=7
    nb_type_bloc=11 ##newbloc
    xperso=0
    yperso=0
    xbloc=0
    ybloc=0
    perso_select=0
    bloc_select=0
    type_select='bloc'
    l_select=40
    h_select=40
    l_bloc=[40,48,200,30,100,200,40,40,100,100,20] ##newbloc
    h_bloc=[40,48,60,30,160,60,40,120,20,20,20] ##newbloc
    verbose=0
##
##    BLACK = ( 0, 0, 0)                          
##    WHITE = (255, 255, 255)
##    RED = (255, 0, 0)
##    GREEN = ( 0, 255
##              , 0)
##    BLUE = ( 0, 0, 255)
##    h_mario=48
##    l_mario=36
##    #MarioGrand1 = pygame.image.load('MarioGrand.png')
##    #MarioGrand1r = pygame.transform.scale(MarioGrand1,(35,70))
##    bloc1 = pygame.image.load('interrogation.png')
##    bloc1r=pygame.transform.scale(bloc1,(40,40))
##    MarioPetit1 = pygame.image.load('MarioPetit.png')
##    MarioPetit=pygame.transform.scale(MarioPetit1,(l_mario, h_mario))
##    Goombas = pygame.image.load('goombas.png')
##    Goombas1r = pygame.transform.scale(Goombas, (48,48))
##    brique_img = pygame.transform.scale(pygame.image.load('Brique.png'), (48,48))
##    champ_img = pygame.transform.scale(pygame.image.load('champignon.png'), (48,48))
##    tortue_img = pygame.transform.scale(pygame.image.load('Tortue.png'), (48,48))
##    piece_img = pygame.transform.scale(pygame.image.load('piece.png'), (30,30))
##    tuyau_img = pygame.transform.scale(pygame.image.load('tuyau.png'), (100,160))
##    sol_img = pygame.transform.scale(pygame.image.load('Sol.png'), (200,60))
##    glace_img = pygame.transform.scale(pygame.image.load('glace.png'), (200,60))
##    inter_boules_img = pygame.transform.scale(pygame.image.load('interrogation_boules.png'), (40,40))
##    drapeau_img=pygame.transform.scale(pygame.image.load('Drapeau.png'), (40,120))
##    boule_verte_img=pygame.transform.scale(pygame.image.load('boule_verte.png'), (40,40))
##    boule_rouge_img=pygame.transform.scale(pygame.image.load('boule_rouge.png'), (40,40))
##    boule_bleue_img=pygame.transform.scale(pygame.image.load('boule_bleue.png'), (40,40))
##    barre_eclair_img=pygame.transform.scale(pygame.image.load('Barre_eclair.png'), (100,20))
##    barre_eclairV_img=pygame.transform.scale(pygame.image.load('Barre_eclair2.png'), (100,20))
##    petit_carre_img=pygame.transform.scale(pygame.image.load('carre.png'), (20,20))
##     ##newbloc


##    perso_img=[Goombas1r, MarioPetit, champ_img, tortue_img, boule_verte_img, boule_rouge_img, boule_bleue_img]
##    bloc_img=[bloc1r, brique_img, sol_img, piece_img, tuyau_img,glace_img, inter_boules_img, drapeau_img,barre_eclair_img, barre_eclairV_img,petit_carre_img]  ##newbloc
#    BlocTypeDiff=[0.1,0.3,0.2,1,3,2]
#   BlocType=[1,2,4,5,8,9]

    points=0
    #goombas_ecrase=0
    DD=1
    nb_goombas=3
    saut=0
    direction = 'right'
    Texte_2=0
    Sol=400
    a=2
    V0=20
    V=0
    Texte_1='  '
    saut =0
    Debut_saut=0
    catx = 10
    caty = Sol
    exmario=1
    V_bloc1=0

    nb_perso=1
    persox=[600]
    persoy=[50]
    direcGo=['gauche']
    exisgo=[1]
    ecrase=[0]
    perso_type=['Goombas']

    nb_bloc=1
    blocx=[240]
    blocy=[Sol-8]
    exisbloc=[1]
    bloc_type=['Brique']

    nb_decor=0
    #####
    ##### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ AUTOBUILD  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####

    hauteur=[0,24,48,72,96,-24,-48,-72,-96]
    HauteurDiff=[0.1,0.5,1,2,4,0.1,0.1,0.1,0.1]
    vide=[0,48,72,96,120]
    VideDiff=[0.1,2,3,4,6]
    BlocTypeDiff=[0.1,0.3,0.2,1,3,2]
    BlocType=[1,2,4,5,8,9]
    BlocLg=[48,200,100,200,100,100]
    PersoDiff=[1,1]
    PersoType=[0,3]


    Longueur=50+10*Difficulte
    SeuilDiffMax=Difficulte
    SeuilDiffMoy=SeuilDiffMax*6
    SeuilDiffTot=SeuilDiffMax*30
    DiffTot=0
    DiffMoy=0
    x=0
    y=Sol-8
    n=0
    diff=[0.1]
    DiffMoy=0
    NbPersoDepuisChamp=0
    resterplat=0
    dernierdecor=0

    while(DiffTot<SeuilDiffTot and n<Longueur):
        DiffMoy=0
        for i in range(n-11,n-1): #Calcule la difficulte moyenne - l'objectif est d'éviter une concentration de difficultés fortes
            if i>=0:
                DiffMoy=DiffMoy+diff[i]/12
        ok=0
##        if dernierdecor>1000 and random.radint(0,10)==1 and len(listeBMD[2]>0):
##            r=random.randint(0, len(listeBMD[2]-1))
##            

        
        while(ok==0): #Ajoute un vide de longeur aleatoire
            r=random.randint(0, 4)
            if resterplat>0:
                r=0
            if DiffMoy+VideDiff[r]/12<=SeuilDiffMoy and VideDiff[r]<SeuilDiffMax:
                x=x+vide[r]
                n=n+1
                diff.append(VideDiff[r])
                DiffTot+=VideDiff[r]
                ok=1
        ok=0
        while(ok==0): #Ajoute un objet avec une marche de hauteur aleatoire
            r=random.randint(0, 8) #Niveau de hauteur
            if resterplat>0:
                r=0
            s=getattr(ClassesBlocs13,random.choice(listeBMD[0])) #bloc
            if DiffMoy+HauteurDiff[r]/12+s.diff/12<=SeuilDiffMoy and HauteurDiff[r]+s.diff<SeuilDiffMax and y-hauteur[r]<550:  #ajoute la hauteur et sort de la boucle
                y=y-hauteur[r]
                n=n+1
                diff.append(HauteurDiff[r]+s.diff)
                DiffTot+=HauteurDiff[r]+s.diff
                ok=1
        #Ajoute le vide + le bloc
        blocx.append(x)
        blocy.append(y)  
        exisbloc.append(1)
        bloc_type.append(s.__name__)
        nb_bloc+=1
        x+=s.lgx
        resterplat-=s.lgx

        #Ajoute un ennemi
        r=random.randint(0, 8)
        s=getattr(ClassesBlocs13,random.choice(listeBMD[1]))
        if r<=Difficulte:
            if DiffMoy+HauteurDiff[r]/12+s.diff/12<=SeuilDiffMoy and s.diff<SeuilDiffMax:
                n=n+1
                diff.append(s.diff)
                DiffTot+=s.diff
                persox.append(x-30)
                persoy.append(y-s.lgy)   
                direcGo.append('gauche')
                exisgo.append(1)
                ecrase.append(0)
                perso_type.append(s.__name__)
                nb_perso+=1
                NbPersoDepuisChamp+=1
                resterplat=max(s.lgx,resterplat)
        #Ajoute une série de pièces
        r=random.randint(0, 30)
        s=random.randint(1, 12)
        t=random.randint(-2,2)
        u=random.randint(0,2)
        if t==0 and u==0: t=1
        if r>25:
            for i in range(0,s): #on n'incremente pas n qui ne sert que pour le calcul de difficulte
                blocx.append(x+40*t*i)
                blocy.append(y-80-20*u*i)  
                exisbloc.append(1)
                bloc_type.append('Piece')
                nb_bloc+=1
                if i>s/2:u=-u

        #Ajoute un Champignon
        r=random.randint(0, 50+NbPersoDepuisChamp)
        if r> 45:
            blocx.append(x)
            blocy.append(y-240)  
            exisbloc.append(1)
            bloc_type.append('Champignon')
            nb_bloc+=1
            NbPersoDepuisChamp=0

    #Ajout du drapeau
    blocx.append(x-50)
    blocy.append(y-120)  
    exisbloc.append(1)
    bloc_type.append('Drapeau')
    nb_bloc+=1

    #cree le fichier
    f = open(nom_fichier, 'wb')
    pickle.dump([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, zone], f)
    print(zone)
    print('#####################################################################################')
    if verbose==1: print([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, zone])
    f.close()

    return([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, zone])
        
