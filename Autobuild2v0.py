#Version 2.0 modifiee depuis 1.3

import pickle, os
import pygame, sys
import random, math
from pygame.locals import *
import ClassesBlocs13
pygame.init()

###### INITIALISATION DES VARIABLES #####
def autobuild(Difficulte, nom_fichier, zone, listeBMD):     #listeBMD: noms des blocs, mobiles et décors
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
    Sol = 400
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
        #est-ce vraiment utile de mettre un goombas au début?
    nb_perso = 1
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
    bloc_autre = ['']

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


    Longueur=50+5*Difficulte#50+10*Difficulte
    SeuilDiffMax=Difficulte
    SeuilDiffMoy=SeuilDiffMax*6
    SeuilDiffTot=SeuilDiffMax*30
    DiffTot=0
    DiffMoy=0
    x = 500   ################0
    y=Sol-8
    n=0
    diff=[0.1]
    DiffMoy=0
    NbPersoDepuisChamp=0
    resterplat=0
    dernierdecor=0

    resterplat = 100

    #enlève les mobiles de difficulté trop élevée pour qu'il y ait plus de méchants ( voir: "#Ajoute un ennemi" )
    for i in listeBMD[1]:
        s = getattr(ClassesBlocs13,i)
        if s.diff > Difficulte+2 or (Difficulte==1 and s.diff>1):
            listeBMD[1].remove(i)
    pass#☺print("☺☻☺☻☺☻",listeBMD[1])

    champinterro=[[],[]] #liste des objets de type champignon et interrogation dans listeBMD
    for i in listeBMD[0]:
        s = getattr(ClassesBlocs13,i)
        if issubclass(s, ClassesBlocs13.Interrogation):
            champinterro[1].append(i)
    for i in listeBMD[1]:
        s = getattr(ClassesBlocs13,i)
        if issubclass(s, ClassesBlocs13.Champignon):
            champinterro[0].append(i)


    objssursol=[]
    for a in listeBMD[0]:
        s = getattr(ClassesBlocs13,a)
        if s.ausol != True and s.ausol != False:
            objssursol.append(a)
    pass#☺print(objssursol)
    volcan=0

    
#################### BOUCLE PRINCIPALE #######################################
    
    while(DiffTot<SeuilDiffTot and n<Longueur):
        #print(resterplat)
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
            if resterplat>0 or x<130:
                r=0
            if DiffMoy+VideDiff[r]/12<=SeuilDiffMoy and VideDiff[r]<SeuilDiffMax:
                x=x+vide[r]
                n=n+1
                diff.append(VideDiff[r])
                DiffTot+=VideDiff[r]
                ok=1
        espace = [vide[r], 0]
        
        ok=0
        a=0
        while(ok==0): #Ajoute un objet avec une marche de hauteur aleatoire
            a+=1
            r=random.randint(0, 8) #Niveau de hauteur
            if y<100 and r not in [0,5,6,7,8]:
                r+=4
            if y>550 and r not in [0,1,2,3,4]:
                r-=4
            if resterplat>0:
                r=0
            s=getattr(ClassesBlocs13,random.choice(listeBMD[0])) #bloc
            if DiffMoy+HauteurDiff[r]/12+s.diff/12<=SeuilDiffMoy and HauteurDiff[r]+s.diff<SeuilDiffMax and y-hauteur[r]<550 and y - hauteur[r]>150 and s.ausol==True and (s.__name__!="Volcan" or volcan==0):  #ajoute la hauteur et sort de la boucle
                y=y-hauteur[r]
                n=n+1
                diff.append(HauteurDiff[r]+s.diff)
                DiffTot+=HauteurDiff[r]+s.diff
                ok=1
            if a>10000000:
                Diftot=10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
                print('azertyuiopoiuytrezaqsdfghjklmlkjhgfdsqwxcvbnbvcxw')
                break
        if s.__name__ == "Volcan": volcan=1
        else: volcan=0
        #Ajoute le vide + le bloc
        if s.__name__ == "Volcan": blocy.append(y-s.lgy) #crée un décalage
        else: blocy.append(y)
        blocx.append(x)
        exisbloc.append(1)
        bloc_type.append(s.__name__)
        nb_bloc+=1
        #print('nb_bloc:',nb_bloc,' | nbblocs: ',len(bloc_type), '| ',bloc_type[len(bloc_type)-1],' (', bloc_type[len(bloc_type)-2],') ')
        bloc_autre.append('')
        x+=s.lgx
        resterplat-=s.lgx
        espace[0]+=s.lgx/2
        espace[1]+=hauteur[r]
        bloc_precedent = s

        #Ajoute un ennemi
        r = random.randint(-5, 8)
        #if 'Bombe' in listeBMD[0]: s= getattr(ClassesBlocs13, 'Bombe')# and r==0
        #else:
        s=getattr(ClassesBlocs13,random.choice(listeBMD[1]))
        if r<=Difficulte or Difficulte==1: #pour qu'il y ait plus de méchants dans les nivaux de Difficulté 1
            pass#☺print("a")
            if DiffMoy+HauteurDiff[r]/12+s.diff/12<=SeuilDiffMoy and s.diff<=SeuilDiffMax and x>150:
                pass#☺print("b")
                n=n+1
                diff.append(s.diff)
                DiffTot+=s.diff
                persox.append(x-30)
                persoy.append(y-s.lgy)   
                direcGo.append('gauche')
                exisgo.append(1)
                ecrase.append(0)
                perso_type.append(s.__name__)
                perso_autre.append('')
                nb_perso+=1
                NbPersoDepuisChamp+=1
                #resterplat = max(s.lgx,resterplat)
        else: pass#☺print("abcdefghijklmnopqrstuvwxyz")
        #Ajoute une série de pièces
        r=random.randint(0, 30)
        s=random.randint(1, 12)
        t=random.randint(-2,2)
        u=random.randint(0,2)
        if t==0 and u==0: t=1
        if r>25 and 'Piece' in listeBMD:
            for i in range(0,s): #on n'incremente pas n qui ne sert que pour le calcul de difficulte
                blocx.append(x+40*t*i)
                blocy.append(y-80-20*u*i)  
                exisbloc.append(1)
                bloc_type.append('Piece')
                bloc_autre.append('')
                nb_bloc+=1
                #print('nb_bloc:',nb_bloc,' | nbblocs: ',len(bloc_type), '| ',bloc_type[len(bloc_type)-1],' (', bloc_type[len(bloc_type)-2],') ')
                if i>s/2: u=-u

        #Ajoute un Champignon
        r=random.randint(0, 50+NbPersoDepuisChamp)
        s=random.randint(0,1)
        if r> 49 and champinterro!=[[],[]]: # 
            pass#☺print(espace)
            a=''
            if champinterro[0]!=[] and champinterro[1]!=[]: #!!!!!
                if s==0:bloc_type.append(random.choice(champinterro[1]))                ;a='bloc'
                else: perso_type.append(random.choice(champinterro[0]))                 ;a='perso'
            elif champinterro[1]!=[]: bloc_type.append(random.choice(champinterro[1]))  ;a='bloc'
            elif champinterro[0]!=[]: perso_type.append(random.choice(champinterro[0])) ;a='perso'
            if a!='':
                eval(a+'x').append(x-espace[0])
                eval(a+'y').append(y-140-(espace[1]/2))
                if a=='bloc':
                    exisbloc.append(1)
                    nb_bloc+=1
                elif a=='perso':
                    direcGo.append('gauche')
                    exisgo.append(1)
                    ecrase.append(0)
                    nb_perso+=1
                eval(a+'_autre').append('')
                NbPersoDepuisChamp=0
                DiffTot-=1
                diff.append(-1)
                #print('nb_bloc:',nb_bloc,' | nbblocs: ',len(bloc_type), '| ',bloc_type[len(bloc_type)-1],' (', bloc_type[len(bloc_type)-2],') ')

            
##        #Ajoute un courbe aléatoire
##        r= random.randint(0, 30)
##        courbey = 0
##        if r>10 and resterplat<=0:
##            courbex=0
##            L = 1500 #largeur de la courbe(1000 <=> un ecran)
##            echellex = (2*math.pi) / L
##            echelley = 250
##            ok=0
##            while ok==0:
##                s = getattr(ClassesBlocs13, random.choice(listeBMD[0]))
##                if s.lgx<250 and s.ausol == True: ok=1
##            #s = 'Brique'#s = getattr(ClassesBlocs13,random.choice(listeBMD[0]))
##            coef=[]
##            for k in range(1, 20):
##                coef.append(random.randint(0, int(((1/2)**k)*2*100))/100)#importance de la courbe
##            
##            for actux in range(0, L, s.lgx): #(0, L, 50)
##                if courbey: courbeyavant = courbey
##                else: courbeyavant=y
##                courbey = 0
##                for k in range(len(coef)):
##                    courbey += echelley*coef[k]*(1+math.cos(k*actux*echellex*math.pi)) #######
##                    
##                if courbey>550: courbey=550
##                if courbey<150: courbey=150
##                if abs(courbey-courbeyavant)>100:
##                    if courbey-courbeyavant>0: courbey -= courbey-courbeyavant-100
##                    if courbey-courbeyavant<0: courbey += abs(courbey-courbeyavant)-100
##                
##            #if DiffMoy+HauteurDiff[r]/12+s.diff/12<=SeuilDiffMoy and HauteurDiff[r]+s.diff<SeuilDiffMax and y-hauteur[r]<550 and y - hauteur[r]>150 and s.ausol==True:  #ajoute la hauteur et sort de la boucle
##                n=n+1
##                diff.append(s.diff)  #0.1
##                DiffTot+=s.diff    #0.1
##                #ok=1
##                blocx.append(actux+x)
##                blocy.append(courbey)  
##                exisbloc.append(1)
##                bloc_type.append(s.__name__) #s
##                nb_bloc+=1
##                if random.randint(1,30)==1 and s.__name__=='Brique': #s
##                    nb_perso += 1
##                    persox.append(actux+x)
##                    persoy.append(50+20)
##                    direcGo.append('gauche')
##                    exisgo.append(1)
##                    ecrase.append(0)
##                    perso_type.append('BouleBleue')
####            if s.ausol != True:
####                ok=0
####                a = 0
####                while ok==0:
####                    a+=1
####                    t = getattr(ClassesBlocs13, random.choice(listeBMD[0]))
####                    if t.ausol==True and t.__name__!='Brique':
####                        ok=1
####                    if a>1000: break
####                if ok==1:
####                    for c in range(x, x+L, t.lgx):
####                        blocx.append(c)
####                        blocy.append(599)  
####                        exisbloc.append(1)
####                        bloc_type.append(t.__name__)
####                        nb_bloc+=1
##            y=courbey
##            x+=L
##            pass#☺print('fincourbe')

        #Ajoute un courbe de collines
        r= random.randint(10, 20)
        courbey = 0
        if r>19 and resterplat<=0:
            courbex=0
            L = 1500 #largeur de la courbe(1000 <=> un ecran)
            echellex = (2*math.pi) / L
            echelley = 100
            ok=0
            s = getattr(ClassesBlocs13, 'Colline')
            ## Calcul de la courbe ##
            coef=[]
            coef_derivee=[]
            for k in range(1, 20):
                coef.append(random.randint(0, int(((1/2)**k)*2*100))/100)#importance de la courbe
                coef_derivee.append(random.randint(0, int(((1/2)**k)*2*100))/300)
            courbe=[]
            c_precedent=y
            for actux in range(0, L+(s.lgx-1), s.lgx-1): ####____1111____
                c=y
                for k in range(len(coef)):
                    c += echelley*(coef[k]+int((3*actux)/L)*coef_derivee[k])*(1-math.cos(k*actux*echellex*3))
                if c>550: c=550
                if c<100: c=100
                if c<c_precedent-100: c=c_precedent-100
                if c>c_precedent+100: c=c_precedent+100
                courbe.append(c)
                c_precedent=c
            pass#☺print(courbe)

            ## Crée les collines
            for i in range(0, len(courbe)-2): #(0, L, 50)
                n=n+1
                diff.append(s.diff)  #0.1
                DiffTot+=s.diff    #0.1
                #ok=1
                
                if courbe[i]>courbe[i+1]:
                    d1=courbe[i]-courbe[i+1]
                    d2=0
                    courbe[i]-=d1
                else:
                    d1=0
                    d2=courbe[i+1]-courbe[i]
                blocx.append(int(i*(s.lgx-1)+x))#+d1/1000 ####____1111____
                blocy.append(int(courbe[i]))#+d2/1000  
                exisbloc.append(1)
                bloc_type.append(s.__name__) #s
                bloc_autre.append([['dy1',d1],['dy2',d2]])
                nb_bloc+=1
                #print('nb_bloc:',nb_bloc,' | nbblocs: ',len(bloc_type), '| ',bloc_type[len(bloc_type)-1],' (', bloc_type[len(bloc_type)-2],') ')
                pass#☺print('>>>>', i*s.lgx, int(courbe[i]), int(d1), int(d2))

                #ajoute un ennemi
                r = random.randint(0, 8)
                #if 'Bombe' in listeBMD[0]: s= getattr(ClassesBlocs13, 'Bombe')# and r==0
                #else:
                sea=getattr(ClassesBlocs13,random.choice(listeBMD[1]))
                if r<=Difficulte:
                    if DiffMoy+HauteurDiff[r]/12+sea.diff/12<=SeuilDiffMoy and sea.diff<SeuilDiffMax and x>150:
                        n=n+1
                        diff.append(sea.diff)
                        DiffTot+=sea.diff
                        persox.append(x+i*(s.lgy-1)-30)
                        persoy.append(courbe[i]-sea.lgy)   
                        direcGo.append('gauche')
                        exisgo.append(1)
                        ecrase.append(0)
                        perso_type.append(sea.__name__)
                        perso_autre.append('')
                        nb_perso+=1
                        NbPersoDepuisChamp+=1
                        #resterplat = max(sea.lgx,resterplat)


            y=courbe[len(courbe)-1]
            x+=L
            pass#☺print('fincourbe')

        if objssursol!=[]:
            s=getattr(ClassesBlocs13,random.choice(objssursol))
            if DiffMoy+s.diff/12<=SeuilDiffMoy and s.diff<SeuilDiffMax and bloc_precedent.__name__!='Volcan' and random.randint(0,3)==0:
                blocx.append(x-espace[0])
                blocy.append(y-s.ausol)  
                exisbloc.append(1)
                bloc_type.append(s.__name__)
                bloc_autre.append('')
                nb_bloc+=1
                #print('nb_bloc:',nb_bloc,' | nbblocs: ',len(bloc_type), '| ',bloc_type[len(bloc_type)-1],' (', bloc_type[len(bloc_type)-2],') ')
            


    #Ajout du drapeau
    blocx.append(x-50)
    blocy.append(y-90)  
    exisbloc.append(1)
    bloc_type.append('Drapeau')
    bloc_autre.append('')
    nb_bloc+=1
    #print('nb_bloc:',nb_bloc,' | nbblocs: ',len(bloc_type), '| ',bloc_type[len(bloc_type)-1],' (', bloc_type[len(bloc_type)-2],') ')

    #ajout des decors
    xfin=x
    [nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre]=[0,[],[],[],[],[]]
    decorsfond=[]
    decors=[]
    for i in listeBMD[2]:
        s=getattr(ClassesBlocs13,i)
        if s.fond: decorsfond.append([i,s.lgx])
        else: decors.append(i)
        print(i, s.fond)
    #print('☺', listeBMD)
    #print('☻', listeBMD[2])
    #print('☺',decors,'☻', decorsfond)
    x=0
    p=6
    while x<=xfin and decorsfond!=[]:
        for i in decorsfond:
            nb_decor+=1
            decorx.append(x)
            decory.append(0)
            decor_type.append(i[0])
            decor_profondeur.append(p)
            decor_autre.append('')
            x+=i[1]
    profondeurs=[2,3,4]
    y=[400,250,100]
    for i in range(len(profondeurs)):
        x=0
        while x<=xfin/profondeurs[i] and decors!=[]:
            x+=random.randint(100,200)
            if random.randint(0,3)>0:
                nb_decor+=1
                decorx.append(x)
                decory.append(y[i]+random.randint(-20,20))
                decor_type.append(random.choice(decors))
                decor_profondeur.append(profondeurs[i])
                decor_autre.append('')
    
    #cree le fichier
    pass#☺print(os.getcwd(), '  --  ', nom_fichier)
    f = open(nom_fichier, 'wb')
    pickle.dump([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]], f)
    #print("Y",zone)
    #print([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]])
    pass#☺print('#####################################################################################')
    if verbose==1: pass#☺print([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, zone])
    f.close()

    return([nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre,zone,[]])
        
