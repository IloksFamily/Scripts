##import time
##
##import pickle, os
##
##import pygame, sys
##from pygame.locals import *
##pygame.init()
##from var import*
##InitialiseFenetre()
##os.chdir("../")
##print(os.getcwd())
##
##import ClassesBlocs13

print('Iloksfamily by FC - v2.1')
print('> loading modules...')
import pygame, math, time, random
import os
os.chdir("../") #a enlever pour freeze, a remettre pour executer. python setup.py build   (ou bdist_msi)
pygame.init()

from var import *
if debug_mode==0 or phone_mode==True: raise ValueError('désactiver phone_mode et activer debug_mode')
InitialiseFenetre()

from AfficheCarte import *
from ClassesBlocs13 import *
from Menus11 import *
import ClassesBlocs13


fin=0
print('>...modules loaded')


def constructeur(fichier, listeBMD, listeimgBMD, listelgBMD):
    mode='graph'
    xgraph=0
    ygraph=0
    xecran=0
    perso_type_select=0
    bloc_type_select=-1
    BLACK = ( 0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = ( 0,255, 0)
    BLUE = ( 0, 0, 255)
    h_mario=48
    l_mario=36

    xperso=0
    yperso=0
    xbloc=0
    ybloc=0
    xdecor=0
    ydecor=0
    perso_select=0
    bloc_select=0
    decor_select=0
    type_select='bloc'
    l_select=40
    h_select=40
    points=0
    #goombas_ecrase=0
    DD=1
    nb_goombas=3
    saut=0
    direction = 'right'
    Texte_2=0
    Sol=500
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
    mode='graph'
    nb_decor=0
    nb_perso = 1
    decor_type_select=-1


    if fichier=='' or fichier=='./':
        nb_perso=1
        persox=[500]
        persoy=[Sol]
        direcGo=['gauche']
        exisgo=[1]
        ecrase=[0]
        perso_type=[0]
     
        nb_bloc=1
        blocx=[240]
        blocy=[Sol-8]
        exisbloc=[1]
        bloc_type=[0]
     
        nb_decor=0
        nb_perso = 1
        decor_type_select=-1
        
        persox = [600]
        persoy = [50]
        direcGo = ['gauche']
        exisgo = [1]
        ecrase = [0]
        perso_type = ['Goombas']
        perso_autre = ['']

        nb_bloc = 1
        blocx = [0] #240
        blocy = [Sol-8]
        exisbloc = [1]
        bloc_type = ['Sol']
        bloc_autre=['']

        decorx=[]
        decory=[]
        decor_type=[]
        decor_profondeur=[]
        decor_autre=['']
        zone=''
        
    else:
        f = open(fichier, 'rb')
        pick=pickle.load(f, encoding='latin1')
        print(pick)
        try:
            [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,direc_bloc, bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,a]=pick
            print('format 4')
        except:
            try:
                [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,a]=pick
                print('format 3')
            except:
                try:
                    [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, a]=pick
                    [perso_autre, bloc_autre, decorx, decory, decor_type, decor_profondeur, decor_autre, zone]=[['']*nb_perso,['']*nb_bloc,[],[],[],[],[],'']
                    print('format 2')
                except:
                    [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type,direc_bloc, a]=pick
                    [perso_autre, bloc_autre, decorx, decory, decor_type, decor_profondeur, decor_autre, zone]=[['']*nb_perso,['']*nb_bloc,[],[],[],[],[],'']
                    print('format 1')
                    
        f.close()
    
    FPS = 15 # frames per second settingperso_autre
    fpsClock = pygame.time.Clock()
    pygame.key.set_repeat(500,30)
    
    DISPLAYSURF = pygame.display.set_mode((1000, 600), 0, 32)
    DISPLAYSURF.fill(WHITE)
    #DISPLAYSURF.set_colorkey(WHITE)

    
############################################################################################################################################################################################
######################################################################       Boucle Principale         #####################################################################################
############################################################################################################################################################################################

    pygame.key.set_repeat(0)
    def cont(mouse, t, i):
        type = ["bloc", "perso", "decor"][t]
        return eval(f"{type}x")[i] < mouse[0] < eval(f"{type}x")[i] + listelgBMD[t][listeBMD.index(eval(f"{type}_type")[i])][0] and eval(f"{type}y")[i] < mouse[1] < eval(f"{type}y")[i] + listelgBMD[t][listeBMD.index(eval(f"{type}_type")[i])][1]
    while True:
        keysi=[]
        keys=pygame.key.get_pressed()
        clic = [None, None]
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keysi.append(event.key)
            if event.type == pygame.MOUSEBUTTONUP and event.button==1:
                clic[0] = pygame.mouse.get_pos()
                if mode == 'graph': xgraph, ygraph = clic[0]
            if event.type == pygame.MOUSEBUTTONUP and event.button==3:
                clic[1] = pygame.mouse.get_pos()

        if mode=='graph':
            if keys[K_LCTRL]:
                speed=10
            elif keys[K_p]:
                speed=1000
            else:
                speed=1
            if keys[K_LEFT]:
                xgraph -=5*speed
                if xgraph<xecran+100 and xecran>0:
                    xecran-=5*speed
            if keys[K_RIGHT]:
                xgraph +=5*speed
                if xgraph>xecran+900:
                    xecran+=5*speed
            if keys[K_DOWN]:
                ygraph +=5*speed
            if keys[K_UP]:
                ygraph -=5*speed
            if K_RETURN in keysi or clic[0] is not None: # touche ,
                print('a')
                if perso_type_select>=0:
                    persox.append(int(xgraph))
                    persoy.append(int(ygraph))
                    direcGo.append('gauche')
                    exisgo.append(1)
                    ecrase.append(0)
                    perso_type.append(listeBMD[1][perso_type_select])
                    perso_autre.append('')
                    nb_perso+=1
                if bloc_type_select>=0:
                    blocx.append(int(xgraph))
                    blocy.append(int(ygraph))
                    exisbloc.append(1)
                    bloc_type.append(listeBMD[0][bloc_type_select])
                    if listeBMD[0][bloc_type_select]=="Colline": bloc_autre.append([['dy1',0],['dy2',0]])
                    else: bloc_autre.append('')
                    nb_bloc+=1
                if decor_type_select>=0:
                    decorx.append(int(xgraph-xecran*1/2))
                    decory.append(int(ygraph))
                    direcGo.append('gauche')
                    exisgo.append(1)
                    ecrase.append(0)
                    decor_type.append(listeBMD[2][decor_type_select])
                    decor_profondeur.append(2)
                    decor_autre.append('')
                    nb_decor+=1
                   

        if mode=='modif':
            if keys[K_LCTRL]:
                speed=5
            elif keys[K_p]:
                speed=1000
            else:
                speed=1
            if keys[K_LEFT]:
                xgraph -=5*speed
                if xgraph<xecran+100 and xecran>0:
                    xecran-=5*speed
                if mode=='modif':
                    if type_select=='perso':
                        persox[perso_select] -=5*speed
                    if type_select=='bloc':
                        blocx[bloc_select] -=5*speed
                    if type_select=='decor':
                        decorx[decor_select] -=5*speed
            if keys[K_RIGHT]:
                xgraph +=5*speed
                if xgraph>xecran+900:
                    xecran+=5*speed
                if mode=='modif':
                    if type_select=='perso':
                        persox[perso_select] +=5*speed
                    if type_select=='bloc':
                        blocx[bloc_select] +=5*speed
                    if type_select=='decor':
                        decorx[decor_select] +=5*speed
            if keys[K_DOWN]:
                ygraph +=5*speed
                if mode=='modif':
                    if type_select=='perso':
                        persoy[perso_select] +=5*speed
                    if type_select=='bloc':
                        blocy[bloc_select] +=5*speed
                    if type_select=='decor':
                        decory[decor_select] +=5*speed
            if keys[K_UP]:
                ygraph -=5*speed
                if mode=='modif':
                    if type_select=='perso':
                        persoy[perso_select] -=5*speed
                    if type_select=='bloc':
                        blocy[bloc_select] -=5*speed
                    if type_select=='decor':
                        decory[decor_select] -=5*speed
            if K_DELETE in keysi: #suppr
                if type_select=='perso':
                    for a in ['persox','persoy','direcGo','exisgo','ecrase','perso_type', 'perso_autre']:
                        #eval(a).remove(eval(a)[perso_select])  #problème: peut supprimer le mauvais élément
                        del eval(a)[perso_select]               #problème résolu
                    nb_perso-=1
                    if perso_select!=0: perso_select-=1
                    if nb_perso==0:
                        if nb_bloc==0:
                            constructeur(fichier, listeBMD, listeimgBMD)
                        type_select='bloc'
                    else:
                        xgraph=persox[perso_select]
                        ygraph=persoy[perso_select]
                if type_select=='bloc':
                    for a in ['blocx','blocy','exisbloc','bloc_type', 'bloc_autre']:
                        #eval(a).remove(eval(a)[bloc_select])
                        del eval(a)[bloc_select]
                    nb_bloc-=1
                    if bloc_select!=0: bloc_select-=1
                    if nb_bloc==0:
                        if nb_perso==0:
                            constructeur(fichier, listeBMD, listeimgBMD)
                        type_select='perso'
                    else:
                        xgraph=blocx[bloc_select]
                        ygraph=blocy[bloc_select]
                if type_select=='decor':
                    for a in ['decorx','decory','exisdecor','decor_type', 'decor_profondeur', 'decor_autre']:
                        #eval(a).remove(eval(a)[decor_select])
                        del eval(a)[decor_select]
                    nb_decor-=1
                    if decor_select!=0: decor_select-=1
                    if nb_decor==0:
                        if nb_perso==0:
                            constructeur(fichier, listeBMD, listeimgBMD)
                        type_select='perso'
                    else:
                        xgraph=decorx[decor_select]
                        ygraph=decory[decor_select]

            if keys[K_n]:
                if type_select=='perso':
                    x1=persox[perso_select]
                    y1=persoy[perso_select]
                    sel=perso_select
                if type_select=='bloc':
                    x1=blocx[bloc_select]
                    y1=blocy[bloc_select]
                    sel=bloc_select
                if type_select=='decor':
                    x1=decorx[decor_select]+xecran*1/decor_profondeur[decor_select]
                    y1=decory[decor_select]
                    sel=decor_select
                x2=10000000
                y2=10000000
                sel=0
                for i in range(nb_perso):
                    if (persox[i]>x1 and persox[i]<=x2) or (persox[i]==x1 and persoy[i]>y1 and x1==x2 and persoy[i]<y2) or (persox[i]==x1 and persoy[i]>y1 and x2>x1):
                        x2=persox[i]
                        y2=persoy[i]
                        sel=i
                        type_select='perso'
                for i in range(nb_bloc):
                    if (blocx[i]>x1 and blocx[i]<=x2) or (blocx[i]==x1 and blocy[i]>y1 and x1==x2 and blocy[i]<y2) or (blocx[i]==x1 and blocy[i]>y1 and x2>x1):
                        x2=blocx[i]
                        y2=blocy[i]
                        sel=i
                        type_select='bloc'
                for i in range(nb_decor):
                    if (decorx[i]+xecran*1/decor_profondeur[i]>x1 and decorx[i]+xecran*1/decor_profondeur[i]<=x2) or (decorx[i]+xecran*1/decor_profondeur[i]==x1 and decory[i]>y1 and x1==x2 and decory[i]<y2) or (decorx[i]+xecran*1/decor_profondeur[i]==x1 and decory[i]>y1 and x2>x1):
                        x2=decorx[i]+xecran*1/decor_profondeur[i]
                        y2=decory[i]+xecran*1/decor_profondeur[i]
                        sel=i
                        type_select='decor'
                if type_select=='perso':
                    perso_select=sel
                    xgraph=persox[perso_select]
                    ygraph=persoy[perso_select]
                    l_select=listelgBMD[1][listeBMD[1].index(perso_type[perso_select])][0]
                    h_select=listelgBMD[1][listeBMD[1].index(perso_type[perso_select])][1]
                if type_select=='bloc':
                    bloc_select=sel
                    xgraph=blocx[bloc_select]
                    ygraph=blocy[bloc_select]
                   # l_select=l_bloc[bloc_type[bloc_select]]
                   # h_select=h_bloc[bloc_type[bloc_select]]
                    l_select=listelgBMD[0][listeBMD[0].index(bloc_type[bloc_select])][0]
                    h_select=listelgBMD[0][listeBMD[0].index(bloc_type[bloc_select])][1]
                if type_select=='decor':
                    decor_select=sel
                    xgraph=decorx[decor_select]
                    ygraph=decory[decor_select]
                    l_select=listelgBMD[2][listeBMD[2].index(decor_type[decor_select])][0]
                    h_select=listelgBMD[2][listeBMD[2].index(decor_type[decor_select])][1]
                    if xgraph+xecran*1/decor_profondeur[decor_select]<xecran+100 and xecran>0:
                        xecran=(xgraph-100)*decor_profondeur[decor_select]/(decor_profondeur[decor_select]-1)
                    if xgraph+xecran*1/decor_profondeur[decor_select]>xecran+900:
                        xecran=(xgraph-900)*decor_profondeur[decor_select]/(decor_profondeur[decor_select]-1)
                    if xecran<0: xecran=0
                else:
                    if xgraph<xecran+100 and xecran>0:
                        xecran=xgraph-100
                    if xgraph>xecran+900:
                        xecran=xgraph-900

            if keys[K_b]:
                if type_select=='perso':
                    x1=persox[perso_select]
                    y1=persoy[perso_select]
                if type_select=='bloc':
                    x1=blocx[bloc_select]
                    y1=blocy[bloc_select]
                if type_select=='decor':
                    x1=decorx[decor_select]+xecran*1/decor_profondeur[decor_select]
                    y1=decory[decor_select]
                    sel=decor_select
                x2=0
                y2=0
                sel=-1
                for i in range(nb_perso):
                    if (persox[i]<x1 and persox[i]>=x2) or (persox[i]==x1 and persoy[i]<y1 and x1==x2 and persoy[i]>y2) or (persox[i]==x1 and persoy[i]<y1 and x2<x1):
                        x2=persox[i]
                        y2=persoy[i]
                        sel=i
                        type_select='perso'
                for i in range(nb_bloc):
                    if (blocx[i]<x1 and blocx[i]>=x2) or (blocx[i]==x1 and blocy[i]<y1 and x1==x2 and blocy[i]>y2) or (blocx[i]==x1 and blocy[i]<y1 and x2<x1):
                        x2=blocx[i]
                        y2=blocy[i]
                        sel=i
                        type_select='bloc'
                for i in range(nb_decor):
                    if (decorx[i]+xecran*1/decor_profondeur[i]<x1 and decorx[i]+xecran*1/decor_profondeur[i]>=x2) or (decorx[i]+xecran*1/decor_profondeur[i]==x1 and decory[i]<y1 and x1==x2 and decory[i]>y2) or (decorx[i]+xecran*1/decor_profondeur[i]==x1 and decory[i]<y1 and x2<x1):
                        x2=decorx[i]+xecran*1/decor_profondeur[i]
                        y2=decory[i]+xecran*1/decor_profondeur[i]
                        sel=i
                        type_select='decor'
                if sel==-1:
                    for i in ['perso', 'bloc', 'decor']:
                        for j in range(len(eval(i+'_type'))):
                            if eval(i+'x'+'['+str(j)+']')>x2:
                                x2=eval(i+'x'+'['+str(j)+']')
                                y2=eval(i+'y'+'['+str(j)+']')
                                sel=j
                                type_select=i
 
                if type_select=='perso':
                    perso_select=sel
                    xgraph=persox[perso_select]
                    ygraph=persoy[perso_select]
                    l_select=10
                    h_select=10
                    l_select=listelgBMD[1][listeBMD[1].index(perso_type[perso_select])][0]
                    h_select=listelgBMD[1][listeBMD[1].index(perso_type[perso_select])][1]
                if type_select=='bloc':
                    bloc_select=sel
                    xgraph=blocx[bloc_select]
                    ygraph=blocy[bloc_select]
                    l_select=listelgBMD[0][listeBMD[0].index(bloc_type[bloc_select])][0]
                    h_select=listelgBMD[0][listeBMD[0].index(bloc_type[bloc_select])][1]
                if type_select=='decor':
                    decor_select=sel
                    print(decorx, decor_select)
                    xgraph=decorx[decor_select]
                    ygraph=decory[decor_select]
                    l_select=listelgBMD[2][listeBMD[2].index(decor_type[decor_select])][0]
                    h_select=listelgBMD[2][listeBMD[2].index(decor_type[decor_select])][1]
                    if xgraph+xecran*1/decor_profondeur[decor_select]<xecran+100:
                        if (xgraph-100)*decor_profondeur[decor_select]/(decor_profondeur[decor_select]-1)<0: xecran=0
                        else: xecran=(xgraph-100)*decor_profondeur[decor_select]/(decor_profondeur[decor_select]-1)
                    if xgraph+xecran*1/decor_profondeur[decor_select]>xecran+900:
                        xecran=(xgraph-900)*decor_profondeur[decor_select]/(decor_profondeur[decor_select]-1)                    
                else:
                    if xgraph<xecran+100:
                        if xgraph-100<0: xecran=0
                        else: xecran=xgraph-100
                    if xgraph>xecran+900:
                        xecran=xgraph-900
            if clic[1]:
                candidates = []
                for i in range(len(bloc_type)):
                    if cont(clic[1],0,i):
                        candidate.append([0,i])
                for i in range(len(perso_type)):
                    if cont(clic[1],1,i):
                        candidate.append([1,i])
                if candidates == []:
                    for i in range(len(decor_type)):
                        if cont(clic[1],2,i):
                            candidate.append([2,i])
                if candidates != []:
                    if len(candidates) > 1:
                        ls = []
                        for i in candidates:
                            ls.append(sum(listelgBMD[listeBMD.index(eval(f"{i[1]}_type"))]))
                        candidates = [candidates[ls.index(max(ls))]]
                    t = ["bloc", "perso", "decor"][candidates[0][0]]
                    type_select = t
                    exec(f"{t}_select = i")

            if type_select=='bloc' and bloc_type[bloc_select]=='Colline':
                d1=bloc_autre[bloc_select][0][1]
                d2=bloc_autre[bloc_select][1][1]
                if keys[K_i]: d1-=speed
                if keys[K_k]: d1+=speed
                if keys[K_o]: d2-=speed
                if keys[K_l]: d2+=speed
                if d1<0: d1=0
                if d2<0: d2=0
                bloc_autre[bloc_select][0][1]=d1
                bloc_autre[bloc_select][1][1]=d2
            if type_select=='decor':
                if keys[K_a]:
                   decor_profondeur[decor_select]+=speed*0.1
                   decor_profondeur[decor_select]=int(100*decor_profondeur[decor_select])/100
                if keys[K_q]:
                    if decor_profondeur[decor_select]<speed*0.1+0.05: decor_profondeur[decor_select]=0.1
                    else: decor_profondeur[decor_select]-=speed*0.1
                    decor_profondeur[decor_select]=int(100*decor_profondeur[decor_select])/100

                    
        if mode=='perso':
            if keys[K_LEFT] and xperso>0:
                xperso -=1
                if xperso+yperso*10<=len(listeBMD[1])-1:
                    perso_type_select=xperso+yperso*11
            if keys[K_RIGHT] and xperso<10:
                xperso +=1
                if xperso+yperso*10<=len(listeBMD[1])-1:
                    perso_type_select=xperso+yperso*11
            if keys[K_DOWN] and yperso<5:
                yperso +=1
                if xperso+yperso*10<=len(listeBMD[1])-1:
                    perso_type_select=xperso+yperso*11
            if keys[K_UP] and yperso>0:
                yperso -=1
                if xperso+yperso*10<=len(listeBMD[1])-1:
                    perso_type_select=xperso+yperso*11
    
        if mode=='bloc':
            nb_larg=11
            if keys[K_LEFT] and xbloc>0:
                xbloc -=1
                #print(xbloc+ybloc*10)
                if xbloc+ybloc*nb_larg<=len(listeBMD[0])-1:
                    bloc_type_select=xbloc+ybloc*nb_larg
                #print(listeBMD[0][xbloc+ybloc*nb_larg])
            if keys[K_RIGHT] and xbloc<nb_larg:
                xbloc +=1
                #print(xbloc+ybloc*10)
                if xbloc+ybloc*nb_larg<=len(listeBMD[0])-1:
                    bloc_type_select=xbloc+ybloc*nb_larg
                #print(listeBMD[0][xbloc+ybloc*nb_larg])
            if keys[K_DOWN] and ybloc<nb_larg:
                ybloc +=1
                #print(xbloc+ybloc*10)
                if xbloc+ybloc*nb_larg<=len(listeBMD[0])-1:
                    bloc_type_select=xbloc+ybloc*nb_larg
                #print(listeBMD[0][xbloc+ybloc*nb_larg])
            if keys[K_UP] and ybloc>0:
                ybloc -=1
                #print(xbloc+ybloc*10)
                if xbloc+ybloc*nb_larg<=len(listeBMD[0])-1:
                    bloc_type_select=xbloc+ybloc*nb_larg
                #print(listeBMD[0][xbloc+ybloc*nb_larg])
            #print(xbloc, ybloc,bloc_type_select)
                    
        if mode=='decor':
            if keys[K_LEFT] and xdecor>0:
                xdecor -=1
                if xdecor+ydecor*10<=len(listeBMD[2])-1:
                    decor_type_select=xdecor+ydecor*11
            if keys[K_RIGHT] and xdecor<10:
                xdecor +=1
                if xdecor+ydecor*10<=len(listeBMD[2])-1:
                    decor_type_select=xdecor+ydecor*11
            if keys[K_DOWN] and ydecor<5:
                ydecor +=1
                if xdecor+ydecor*10<=len(listeBMD[2])-1:
                    decor_type_select=xdecor+ydecor*11
            if keys[K_UP] and ydecor>0:
                ydecor -=1
                if xdecor+ydecor*10<=len(listeBMD[2])-1:
                    decor_type_select=xdecor+ydecor*11

           
        if keys[K_1] or keys[K_KP1] or (mode in ['perso','bloc','decor'] and keys[K_RETURN]):
            mode='graph'
        if keys[K_2] or keys[K_KP2]:
            mode='perso'
            perso_type_select=0
            bloc_type_select=-1
            decor_type_select=-1
        if keys[K_3] or keys[K_KP3]:
            mode='bloc'
            perso_type_select=-1
            bloc_type_select=0
            decor_type_select=-1
        if keys[K_4] or keys[K_KP4]:
            mode='decor'
            perso_type_select=-1
            bloc_type_select=-1
            decor_type_select=0
        if keys[K_5] or keys[K_KP5]:
            mode='modif'
            if type_select=='perso':
                xgraph=persox[perso_select]
                ygraph=persoy[perso_select]
            if type_select=='bloc':
                xgraph=blocx[bloc_select]
                ygraph=blocy[bloc_select]
            if type_select=='decor':
                xgraph=decorx[decor_select]
                ygraph=decory[decor_select]

        if keys[K_r]:
            xgraph = 200+xecran
            ygraph = 200
            if mode=='modif':
                if type_select=='bloc':
                    blocx[bloc_select]=200+xecran
                    blocy[bloc_select]=200
                elif type_select=='perso':
                    persox[perso_select]=200+xecran
                    persoy[perso_select]=200
                elif type_select=='decor':
                    decorx[decor_select]=200+xecran/decor_profondeur[decor_select]
                    decory[decor_select]=200
        if (keys[K_LCTRL] and keys[K_s]):  #enregistrer
            if fichier=='' or fichier=='./':
                fichier='./'+input('fichier à créer?'+os.getcwd()+'/')
            #os.remove('save.p')
            ok=0
            while ok==0:
                for i in range(len(perso_type)):
                    if perso_type[i]=='Joueur':
                        for a in ['persox','persoy','direcGo','exisgo','ecrase','perso_type']:
                            eval(a).remove(eval(a)[i])
                        nb_perso-=1
                        break
                    if i==len(perso_type)-1:
                        ok=1
            if zone=='': zone = input('quelle zone(mario, bermat, sava, aqua, rien)(détermine en particulier la musique)?')
            print([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]])
            f = open(fichier, 'wb')
            pickle.dump([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]], f)#[2 for i in decor_type]
            print([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]])
            f.close()
            print('fichier enregistré')
            print(fichier[2:len(fichier)])
            if input('Jouer le niveau?').lower() in ['true','oui','1','vrai','yes','y','o']:
                script_path = os.path.join(os.getcwd(), 'scripts', 'Joueniveau.py')
                exec(open(script_path).read(), {'fichier': fichier, 'demarreparconstructeur':True})
            elif input("modifier la liste?"):
                a=input("[nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]]=")
                if a!='':
                    try: [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]]=eval(a)
                    except: print("impossible: liste non modifiée")
############################################################################################################################################################################################
######################################################################            Affichage            #####################################################################################
############################################################################################################################################################################################

    ### Préparation de l'affichage
            Texte_1='§§§§§§ SAUVEGARDE FAITE §§§§§§§'
     
    ### Mise à jour de l'écran / Gestion de la fermeture
        DISPLAYSURF.fill(WHITE)
        if mode=='graph':
#            DISPLAYSURF.blit(MarioPetit, (catx-xecran, caty))

            for i in range(len(decor_type)): DISPLAYSURF.blit(listeimgBMD[2][listeBMD[2].index(decor_type[i])], ((decorx[i]-xecran*1/decor_profondeur[i]), decory[i]))
            
            if decor_type_select>=0: DISPLAYSURF.blit(listeimgBMD[2][decor_type_select], (xgraph-xecran,ygraph))

            for i in range(nb_perso):
                #print(perso_type, i)
                DISPLAYSURF.blit(listeimgBMD[1][listeBMD[1].index(perso_type[i])], (persox[i]-xecran,persoy[i])) 

            for i in range(nb_bloc):
                if bloc_type[i] == 'Colline':
                    lgx=50
                    lgy=200
                    [x,y,dy1,dy2]=[int(blocx[i]),int(blocy[i]),bloc_autre[i][0][1],bloc_autre[i][1][1]]
                    img="texture.jpg"
                    imgtxt=pygame.image.load('./img/'+img)
                    img = pygame.Surface((lgx,lgy), depth=32)  
                    for xx in range(0, lgx, imgtxt.get_width()):
                        for yy in range(0, lgy, imgtxt.get_height()):
                            img.blit(imgtxt,(xx,yy))
                    mask = pygame.Surface((lgx,lgy), depth=8)
                    # Create sample mask:
                    pygame.draw.polygon(mask, 255, [(0,dy1),(0,lgy),(lgx,lgy),(lgx,dy2)] , 0)
                    img = img.convert_alpha()
                    target = pygame.surfarray.pixels_alpha(img)
                    target[:] = pygame.surfarray.array2d(mask)
                    del target
                    surf.blit(img, (x-xecran, y))
                    DISPLAYSURF.blit(img, (x-xecran, y))
                    
                else: DISPLAYSURF.blit(listeimgBMD[0][listeBMD[0].index(bloc_type[i])], (blocx[i]-xecran, blocy[i]))

            if perso_type_select>=0:
                DISPLAYSURF.blit(listeimgBMD[1][perso_type_select], (xgraph-xecran,ygraph))###azertyuiopoiuytrezaqsdfghjklmlkjhgfdsqwxcvbnbvcxw

            if bloc_type_select>=0:

                DISPLAYSURF.blit(listeimgBMD[0][bloc_type_select], (xgraph-xecran,ygraph))
               

            pygame.draw.rect(DISPLAYSURF, RED, Rect(xgraph-xecran, ygraph, 4,4))

     

        if mode=='modif':

            DISPLAYSURF.blit(listeimgBMD[1][0], (catx-xecran, caty))

            for i in range(len(decor_type)): DISPLAYSURF.blit(listeimgBMD[2][listeBMD[2].index(decor_type[i])], ((decorx[i]-xecran*1/decor_profondeur[i]),decory[i]))
            for i in range(nb_perso):
                DISPLAYSURF.blit(listeimgBMD[1][listeBMD[1].index(perso_type[i])], (persox[i]-xecran,persoy[i]))
            for i in range(nb_bloc):
                if bloc_type[i] == 'Colline':
                    lgx=50
                    lgy=200
                    [x,y,dy1,dy2]=[int(blocx[i]),int(blocy[i]),bloc_autre[i][0][1],bloc_autre[i][1][1]]
                    img="texture.jpg"
                    imgtxt=pygame.image.load('./img/'+img)
                    img = pygame.Surface((lgx,lgy), depth=32)  
                    for xx in range(0, lgx, imgtxt.get_width()):
                        for yy in range(0, lgy, imgtxt.get_height()):
                            img.blit(imgtxt,(xx,yy))
                    mask = pygame.Surface((lgx,lgy), depth=8)
                    # Create sample mask:
                    pygame.draw.polygon(mask, 255, [(0,dy1),(0,lgy),(lgx,lgy),(lgx,dy2)] , 0)#[(x,y+dy1),(x,y+lgy),(x+lgx,y+lgy),(x+lgx,y+dy2)] , 0)
                    img = img.convert_alpha()
                    target = pygame.surfarray.pixels_alpha(img)
                    target[:] = pygame.surfarray.array2d(mask)
                    del target
                    DISPLAYSURF.blit(img, (x-xecran, y))

                else: DISPLAYSURF.blit(listeimgBMD[0][listeBMD[0].index(bloc_type[i])], (blocx[i]-xecran, blocy[i]))

            
            
            if type_select=='decor':
                font=pygame.font.Font(None,30)
                text=font.render(str(decor_profondeur[decor_select]),1,RED)
                DISPLAYSURF.blit(text, (xgraph-xecran*1/decor_profondeur[decor_select]+20, ygraph+20))
                pygame.draw.rect(DISPLAYSURF, RED, Rect(xgraph-xecran*1/decor_profondeur[decor_select], ygraph, l_select,h_select),5)#xgraph-xecran+xecran*1/decor_profondeur[decor_select]
            else:
                pygame.draw.rect(DISPLAYSURF, RED, Rect(xgraph-xecran, ygraph, l_select,h_select),5)

        if mode=='perso':
            j=0
            k=0
            for i in range(len(listeBMD[1])-1):
                DISPLAYSURF.blit(pygame.transform.scale(listeimgBMD[1][i],(48,48)), (j*60+60, k*60+60))
                if j<10:
                    j+=1
                else:
                    j=0
                    k+=1
            pygame.draw.rect(DISPLAYSURF, RED, Rect(xperso*60+60, yperso*60+60, 50,50),2)
       
        if mode=='bloc':
            j=0
            k=0
            for i in range(len(listeBMD[0])-1):
                DISPLAYSURF.blit(listeimgBMD[0][i], (j*60+60, k*60+60))
                if j<10:
                    j+=1
                else:
                    j=0
                    k+=1
            pygame.draw.rect(DISPLAYSURF, RED, Rect(xbloc*60+60, ybloc*60+60, 50,50),2)
            
        if mode=='decor':
            j=0
            k=0
            for i in range(len(listeBMD[2])-1):
                DISPLAYSURF.blit(listeimgBMD[2][i], (j*60+60, k*60+60))
                if j<10:
                    j+=1
                else:
                    j=0
                    k+=1
            pygame.draw.rect(DISPLAYSURF, RED, Rect(xdecor*60+60, ydecor*60+60, 50,50),2)

     
        font=pygame.font.Font(None,26) #chiffre=taille des lettres
        phrase = '1: Creation  |  2: Personnages  |  3: Blocs  |  4: Decors  |  5: Modification  |  CTRL+S: Sauvergarde'
        text=font.render(phrase,1,BLUE)
        DISPLAYSURF.blit(text, (10,1))
        font=pygame.font.Font(None,30)
        if mode=='modif':
            Texte_1='n pour selectionner à droite, b pour selectionner à gauche | r: recentrer curseur'
            if type_select=='bloc' and bloc_type[bloc_select]=='Colline':
                Texte_1+=' | I/K/O/L pour modifier la colline'
        elif mode=='graph':
            Texte_1=' Ctrl+Flèches: se deplacer vite | entrée: ajouter un objet | r: recentrer curseur'
        elif mode in ["perso","bloc","decor"]:
            Texte_1='Flèches: choisir un '+mode+'  |  entrée pour valider'
        else: Texte_1=''
     
        phrase = str(Texte_1)+'     '
        text=font.render(phrase,1,RED)

        DISPLAYSURF.blit(text, (50,35))

       

        for event in pygame.event.get():

            if event.type == QUIT:

                pygame.quit()  #ferme la librairie pygame

                sys.exit()     #ferme le programme

               

        pygame.display.update()

        fpsClock.tick(FPS)
############################################################################################################################################################################################
############################################################################################################################################################################################
########################################################                 fin fonction principale            ################################################################################
############################################################################################################################################################################################
############################################################################################################################################################################################

##### Version de base Mario 1.2

##### INITIALISATION DES VARIABLES #####

fichier='./'+input('fichier à utiliser ? '+os.getcwd()+'/')

mode='graph'

xgraph=0

ygraph=0

xecran=0

perso_type_select=0

bloc_type_select=-1

nb_type_perso=9

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

direc_bloc=[0]*len(h_bloc)

 

BLACK = ( 0, 0, 0)                         

WHITE = (255, 255, 255)

RED = (255, 0, 0)

GREEN = ( 0,255, 0)

BLUE = ( 0, 0, 255)

h_mario=48

l_mario=36

listeBMD=[[],['Joueur'],[]]
s=getattr(ClassesBlocs13,'Joueur')
listeimgBMD=[[],[pygame.transform.scale(pygame.image.load('./img/ilok.png'), (s.lgx,s.lgy)).convert()],[]]
listeimgBMD[1][0].set_colorkey(WHITE)
listelgBMD=[[],[[s.lgx,s.lgy]],[]]
for name, objet in inspect.getmembers(ClassesBlocs13):
    if inspect.isclass(objet):
        i=-1
        if issubclass(objet, Bloc) and objet.zone!='virtuel': i=0
        elif issubclass(objet, Mobile) and objet.zone!='virtuel': i=1
        elif issubclass(objet, Decor) and objet.zone!='virtuel':i=2
        elif issubclass(objet, Colline): i=0
        if i!=-1:
            try:
                listeimgBMD[i].append(pygame.transform.scale(pygame.image.load('./img/'+name.lower()+'constructeur.png'), (objet.lgx,objet.lgy)).convert())
            except:
                try:
                    listeimgBMD[i].append(pygame.transform.scale(pygame.image.load('./img/'+name.lower()+'constructeur.jpg'), (objet.lgx,objet.lgy)).convert())
                except:
                    try:
                        listeimgBMD[i].append(pygame.transform.scale(pygame.image.load('./img/'+name.lower()+'.png'), (objet.lgx,objet.lgy)).convert())
                    except:
                        try:
                            listeimgBMD[i].append(pygame.transform.scale(pygame.image.load('./img/'+name.lower()+'.jpg'), (objet.lgx,objet.lgy)).convert())
                        except:
                            print('image non chargée: ', name, '(', name.lower(), ')')
                            if input('montrer générer l\'erreur?'): raise ValueError('')
                            continue
            
           # print(listeimgBMD[i][len(listeimgBMD[i]-1)])
            listeimgBMD[i][len(listeimgBMD[i])-1].set_colorkey(WHITE)
            listeBMD[i].append(name)
            listelgBMD[i].append([objet.lgx,objet.lgy])
print(listeBMD)
constructeur(fichier, listeBMD, listeimgBMD, listelgBMD)
