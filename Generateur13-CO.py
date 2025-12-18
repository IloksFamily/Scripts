
import os
os.chdir("../")
import pygame
pygame.init()
DISPLAYSURF = pygame.display.set_mode((10, 6), 0, 32)

import platform
ostype=platform.system()

from numpy import *

from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from random import randint
from PersonnagesObjets import *
import os
from Autobuild2v0 import *
if ostype!='Windows':
    from pylab import *
from ClassesBlocs13 import *
verbose=0

zones=['mario','savane','bermat','aqua']
listeBMDmulti=[]
listeobjets=[]
listepersonages=[]
for j in range(len(zones)):
    listeBMDmulti.append([])
    for i in range(3):
        listeBMDmulti[j].append([])

    for name, objet in inspect.getmembers(ClassesBlocs13):
        if inspect.isclass(objet) and name!='Drapeau' and objet.zone!="virtuel":#?
            if issubclass(objet, Bloc) and name!='Mobloc':
                if zones[j] in objet.zone:
                    listeBMDmulti[j][0].append(name)
            if issubclass(objet, Mobile) and obj!=Joueur:
                if zones[j] in objet.zone:
                    listeBMDmulti[j][1].append(name)
            if issubclass(objet, Decor):
                if zones[j] in objet.zone:
                    listeBMDmulti[j][2].append(name)
                    
for name, objet in inspect.getmembers(ClassesBlocs13):
    if inspect.isclass(objet):
        if issubclass(objet, Personnage) and name!='Personnage':
            listepersonages.append(objet)
            print(name,objet)
        if issubclass(objet, Objet) and name!='Objet':
            listeobjets.append(objet)
                    
                
print(listeBMDmulti)
print(listepersonages)
print(listeobjets)
print('ok')
#001 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['Decouverte',5,0.5,1,'Pour commencer, Ilok a besoin de retrouver l epee legendaire du pays de Mako','']
#002 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['L aventure commence',6,0.5,1.5,'Avant de vous lancer dans l aventure, apprenez a faire jouer Ilok et ses amis!','']
#001 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['Decouverte',5,0.5,1,'Avant de vous lancer dans l aventure, apprenez a faire jouer Ilok et ses amis!','Bravo! Vous etes prets pour l aventure !']
#002 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['L aventure commence',6,0.5,2,'Pour commencer, Ilok a besoin de retrouver l epee legendaire du pays de Mako','Vous avez reussi a prendre l eppe legendaire! L aventure peut continuer...']

#101 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['Decouverte',4,0.5,1,'Avant de vous lancer dans l aventure, apprenez a faire jouer Ilok et ses amis!','Bravo! Vous etes prets pour l aventure !']
#103 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['L aventure continue',8,1,3,'Muni de son epee du courage, Ilok doit maintenant obtenir l arc de la prudence','Vous avez trouve l arc de la prudence! Un pas de plus vers le livre de vie...']
#[titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['Test2',8,1,4,'Muni de son epee du courage, Ilok doit maintenant obtenir l arc de la prudence','Vous avez trouve l arc de la prudence! Un pas de plus vers le livre de vie...']
#[titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['Entrainement',3,1,2,"C'est parti pour un petit entrainement","Continuez comme ça!!"]

# Release du 29 juin 2021
#201 2140 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=['Entrainement',4,0.5,2,"C'est parti pour un petit entrainement","Continuez comme ça!!"]
#202 6795 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=["L'aventure commence",5,0.5,2.5,'Pour commencer, Ilok a besoin de retrouver l epee legendaire du pays de Mako','Vous avez reussi a prendre l eppe legendaire! L aventure peut continuer...']
#203 2882 [titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin]=["L'aventure continue",8,1,3.5,'Muni de son epee du courage, Ilok doit maintenant obtenir l arc de la prudence','Vous avez trouve l arc de la prudence! Un pas de plus vers le livre de vie...']
#[titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin, precedent]=['L\'aventure commence',4,0.5,2,'Ilok prend sa cape et son courage pour partir dans cette grande aventure', "Maintenant, Ilok est parti. Il devra continuer jusqu'au bout",'']
#[titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin, precedent]=['L\'étape ultime!',15,5,12,"Ilok s'est introduit dans le repère de Kramone. Les riques sont immenses!","Ilok, le héros légendaire est parvenu à libérer son village de la tyrannie de Kramone. Il fait désormais de l'équitation! ☺", '0002 Au coeur du combat']
#[titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin, precedent]=['Au coeur de la quête',6,1.5,5,'Ilok, bien entrainer, continue sans oublier son but ultime: détruire Kramone', "Félicitations! Vous avez mené Ilok en vue du repaire de Kramone!",'0001 L\'aventure commence'
[titre,cote_carte, diff_debut, diff_fin,phrase_intro,phrase_fin, precedent]=['Au coeur de la quête',6,1.5,5,'Ilok, bien entrainer, continue sans oublier son but ultime: détruire Kramone', "Félicitations! Vous avez mené Ilok en vue du repaire de Kramone!",'0001 L\'aventure commence']

def
genere(cote_carte, diff_debut, diff_fin):
    partie=cree_repertoire()
    [carte, carte_fin]=construit_carte(cote_carte, diff_debut, diff_fin)
    [scenario, obj, personnages]=cree_scenario(cote_carte, diff_debut, diff_fin, carte)
    [bloc_decor,bloc_chemin,decor]=place_arbres(cote_carte, diff_debut, diff_fin, carte) #[[],[],[]] #
    nouvelle_partie(partie, cote_carte, carte, carte_fin, scenario, obj, personnages,diff_debut, diff_fin, bloc_decor,bloc_chemin,decor)
    return partie

##1 Construit la carte #########################################################
#de zelda_carte2_0.py
def construit_carte(cote_carte, diff_debut, diff_fin):
    carte=zeros((cote_carte+2,cote_carte+2))
    for i in range(0,cote_carte+1): #initialise les cotes du tableau de difficulte "carte"
        carte[i,0]=diff_debut*0.9+diff_fin*0.1
        carte[i,cote_carte+1]=diff_debut*0.2+diff_fin*0.8
        carte[0,i]=diff_debut*0.5+diff_fin*0.5
        carte[cote_carte+1,i]=diff_debut*0.5+diff_fin*0.5
    carte[3,2]=diff_debut
 
    carte_fin=[1,3]
    if cote_carte>3:
        while(-carte_fin[0]+carte_fin[1]<2 and carte_fin[0]+carte_fin[1]<8):
            carte_fin=[randint(1,cote_carte),randint(1,cote_carte)]

    carte[carte_fin[0], carte_fin[1]]=diff_fin
    for k in range(10): #Homogenise le tableau de difficulte
        for i in range(1,cote_carte+1):
            for j in range(1,cote_carte+1):
                if((i!=3 or j!=2) and (i!=carte_fin[0] or j!=carte_fin[1])):
                    carte[i,j]=(carte[i-1,j]+carte[i+1,j]+carte[i, j-1]+carte[i,j+1])/4
        for i in range(cote_carte,0,-1):
            for j in range(cote_carte,0,-1):
                if((i!=3 or j!=2) and (i!=carte_fin[0] or j!=carte_fin[1])):
                    carte[i,j]=int(1000*(carte[i,j]+carte[i+1,j]+carte[i, j-1]+carte[i,j+1])/4)/1000.0
    if verbose==1:
        print(carte)
        print("01 - Carte construite")
    return carte, carte_fin

### Fin carte #######################################
### Place les decors ################################

decor_type=['','arbre_normal','arbre_normal2','arbre_fleur','arbre_palmier','arbre_palmier2','arbre_foret_sapins','arbre_sapin_neige','arbre_porte','arbre_bleuciel','arbre_rouge','arbre_rouge2']
def contact2(x1, y1, l1, h1, V1, x2, y2, l2, h2, V2):
    cont=''
    for i in [[x1, y1],[x1+l1, y1],[x1, y1+h1],[x1+l1, y1+h1]]:
        if i[0]<x2+l2 and i[0]>x2 and i[1]<y2+h2 and i[1]>y2:
            cont='recouvre'
    for i in [[x2, y2],[x2+l2, y2],[x2, y2+h2],[x2+l2, y2+h2]]:
        if i[0]<x1+l1 and i[0]>x1 and i[1]<y1+h1 and i[1]>y1:
            cont='recouvre'
    return(cont)

def place_arbres(cote_carte, diff_debut, diff_fin, carte):
    long_ecran=600 #d
    larg_ecran=1000 #d
    d_chemin=80 #d
    d_arbre=80 #d
    decor=np.zeros((cote_carte+2,cote_carte+2))
    fini=0
    points_affectes=[]

    for i in range(int(cote_carte**2/5)): #place les points source de decor
        x=randint(1,cote_carte)
        y=randint(1,cote_carte)
        decor[x,y]=int(carte[x,y]*len(decor_type)/6)+randint(-2,2)
        if decor[x,y]<1: decor[x,y]=1
        if decor[x,y]>len(decor_type)-1: decor[x,y]=len(decor_type)-1
        points_affectes.append([x,y])

    if verbose==1:
        print(('#',len(points_affectes)))
        print("03 - Decor - Points source places")
        imshow(array(decor))
        colorbar()
        axis('on')
        show()
    sources_decor=[]
    for i in range(len(points_affectes)):
        sources_decor.append(points_affectes[i])

    while(fini==0):   #etend les zones de decor
        fini=1
        for i in range(1,cote_carte):
            for j in range(1,cote_carte): 
                if decor[i,j]==0: fini=0
    ##    for i in range(1,cote_carte):
    ##        for j in range(1,cote_carte):    
    ##            if decor[i,j]!=0:
        p=points_affectes
        for [i,j] in p:
                    if decor[i+1,j]==0 and i<cote_carte and randint(0,3-min(0,int(abs(carte[i+1,j]*len(decor_type)/6-decor[i,j]))))>0:
                        decor[i+1,j]=decor[i,j]
                        points_affectes.append([i+1,j])
                    if decor[i-1,j]==0 and i>1 and randint(0,3-min(0,int(abs(carte[i-1,j]*len(decor_type)/6-decor[i,j]))))>0:
                        decor[i-1,j]=decor[i,j]
                        points_affectes.append([i-1,j])
                    if decor[i,j+1]==0 and j<cote_carte and randint(0,3-min(0,int(abs(carte[i,j+1]*len(decor_type)/6-decor[i,j]))))>0:
                        decor[i,j+1]=decor[i,j]
                        points_affectes.append([i,j+1])
                    if decor[i,j-1]==0 and j>1 and randint(0,3-min(0,int(abs(carte[i,j-1]*len(decor_type)/6-decor[i,j]))))>0:
                        decor[i,j-1]=decor[i,j]
                        points_affectes.append([i,j-1])

        if verbose==1:
            print(('#',len(points_affectes)))
            imshow(array(decor))
            colorbar()
            axis('on')
            show()


    imshow(array(decor))
    colorbar()
    axis('on')
    savefig('decor.png')
    
    if verbose==1:        
        print("04 - Decor - Zones etendues")
        show()
        visu_scenario=np.zeros((cote_carte+2,cote_carte+2)) #d ??

    bloc_decor=[]  # Place les chemins
    bloc_chemin=[]
    for point in sources_decor: 
        if randint(1,4)==1:
            bloc_chemin.append([point[0],point[1]])
            for r in range(int(long_ecran/1.0),6*long_ecran,int(long_ecran/1.0)):
                for a in range(0,int(2.*3.15/(0.5*float(d_chemin)/r))):
                    alpha=a*float(d_chemin)/r
                    x=int(point[0]*larg_ecran+r*sin(alpha))
                    y=int(point[1]*long_ecran+r*cos(alpha))
                    if x>0 and x<cote_carte*larg_ecran and y>0 and y<cote_carte*long_ecran:
                        bloc_chemin.append([x,y])
            alpha=randint(0,90)
            b=randint(4,8)
            for a in range(b):
                alpha=float(alpha+a*360./b)*(2.*3.14/360.)    
                for r in range(0,int(6.*long_ecran),d_chemin):
                    x=int(point[0]*larg_ecran+r*sin(alpha))
                    y=int(point[1]*long_ecran+r*cos(alpha))
                    if x>0 and x<cote_carte*larg_ecran and y>0 and y<cote_carte* long_ecran:
                        bloc_chemin.append([x,y])
    if verbose==1 and bloc_chemin!=[]:
        print("05 - Decor - Chemins places")
        b=array(bloc_chemin)
        plot(b[:,0], b[:,1])
        show()

##    for xc in range(1,cote_carte+1): # Place les arbres
##        for yc in range(1,cote_carte+1):
##            if verbose==1: print(('place arbre ',xc,yc))
##            for i in range(int(carte[xc,yc]*24)):
##                x=xc*larg_ecran+randint(1,larg_ecran-d_arbre)
##                y=yc*long_ecran+randint(1,long_ecran-d_arbre)
##                cont=''
##                for j in range(len(bloc_chemin)):
##                    c=contact2(x, y, d_arbre, d_arbre, 0, bloc_chemin[j][0], bloc_chemin[j][1], d_chemin, d_chemin, 0)
##                    if c!='':
##                        cont=c
##                if cont=='':
##                    bloc_decor.append([x,y,decor[xc,yc]])

    if bloc_chemin!=[] and bloc_decor!=[]:
        d=array(bloc_decor)
        b=array(bloc_chemin)
        plot(b[:,0], b[:,1],'b.')
        plot(d[:,0], d[:,1],'r.')
        savefig('arbreschemins.png')
        if verbose==1:
            print("04 - Decor - Arbres places")
            print("04 - Decor - termine")
            show()    
        
    return [bloc_decor, bloc_chemin,decor]

### Fin decors ###########################################
### Scenario #############################################

def ProposeNonUtilise(liste):
    #verifie si un choix nest pas utilise
    choixpossible=0
    for i in liste:
        if i.utilise==0:
            choixpossible=1
    if choixpossible==0:
        print('/!\ Attention, utilisation de la liste pers/obj plusieurs fois') 
        for i in liste:
            i.utilise=0
    ok=0
    while(ok<=0):
        c=randint(0,len(liste)-1)
        if liste[c].utilise==0:
            liste[c].utilise=1
            #print('ProposeNonUtilise:: ' + str(c))
            return c
        ok-=1
        #if ok<50*len(liste):
        #    print('erreur',ok,liste[0],liste)

def placer(avancement,diff_debut,diff_fin,cote_carte, carte,xref=0, yref=0): #Place un objet ou un personnage sur la carte en fonction de la difficulte
    diff_cible=diff_debut+1.0*(diff_fin-diff_debut)*min(avancement,1.)
    if verbose==1: print((avancement, diff_cible))
    j=0
    while(True):
        j+=1
        if j>1000: print('Impossible de placer personnage : ',avancement,diff_debut,diff_fin,cote_carte, carte,xref,yref,diff_cible)
        x=randint(1,cote_carte)    
        y=randint(1,cote_carte)
        if carte[x][y]<diff_cible*1.3 and carte[x][y]>diff_cible*0.7 and (xref+yref==0 or (x-xref)**2+(y-yref)**2<7**2):
            CaseDejaOccupee=0
            for i in pers:
                if i.x==x and i.y==y:
                    CaseDejaOccupee=1
            if CaseDejaOccupee==0:
                if verbose==1: print(('Place: ',x,y,xref+yref==0,diff_cible,avancement,carte[x,y]))
                return [x,y]

def cree_scenario(cote_carte, diff_debut, diff_fin, carte):
    obj2=[]
    pers2=[]
    lg_scenario=int(cote_carte*cote_carte/(8))
    if verbose==1: print(('lg_scenario: '+str(lg_scenario)))
    niv_debloque=100
    visu_scenario=zeros((cote_carte+2,cote_carte+2))
    scenario=[]  #/ TYPE 1=pers, 2=obj / ENTREE 0=gratuit 1=besoin objet, 2=besoin connaissance / SORTIE 0=rien 1=indice, 2=laisser-passer / Num item (dans la liste pers ou obj)
                 #                          =ce qui est necessaire pour activer le perso ou obj          = ce que ca fait ensuite
    for i in range(lg_scenario): #Cree le scenario
        entree=randint(1,2)
        sortie=randint(1,2)
        print(listepersonages)
        num=ProposeNonUtilise(listepersonages) #choisis un personnage non utilise
        print(num)
        if sortie==2 and diff_fin>2: sortie=0 # parait bizarre...                                     ###???????????                                peut-être pour que ça soit plus difficile...         #########?????????????????????
        [x, y]=placer((i+1.1)/lg_scenario,diff_debut,diff_fin,cote_carte, carte)
        pers2.append([listepersonages[num].nom,x,y,randint(200,700)+x*1000,randint(200,300)+y*600]) #cree le personnage ??: [nom,  x,y en nombre de cases   ,x,y: position vraie]
        if verbose==1: print(('Pers ',i, [1,entree,sortie,num]))
        scenario.append([1,entree,sortie,len(pers2)-1])  
        if verbose==1: print(('###############1',i, lg_scenario,(i+1.1)/lg_scenario))
        visu_scenario[x][y]=i
        if entree==1: #Entree=objet => cree objet, le place et l ajoute au scenario
            sortie=randint(1,2)
            num=ProposeNonUtilise(listeobjets)
            [x, y]=placer((i+1.1)/lg_scenario,diff_debut,diff_fin,cote_carte, carte,x,y)
            obj2.append([listeobjets[num].nom,x,y,randint(200,700)+x*1000,randint(200,300)+y*600])
            if verbose==1: print(('Obj ',i, [2,0,0,num]))
            scenario.append([2,0,0,len(obj2)-1])
            if verbose==1: print(('###############2',i, lg_scenario,(i+1.1)/lg_scenario))
            visu_scenario[x][y]=i
        if entree==2: #Entree = connaitre perso => le cree, le place et l ajoute au scenario
            num=ProposeNonUtilise(listepersonages)
            [x, y]=placer((i+1.1)/lg_scenario, diff_debut,diff_fin,cote_carte, carte,x,y)
            pers2.append([listepersonages[num].nom,x,y,randint(200,700)+x*1000,randint(200,300)+y*600])
            if verbose==1: print(('Pers ',i, [1,0,0,num]))
            scenario.append([1,0,0,len(pers2)-1])
            if verbose==1: print(('###############3',i, lg_scenario,(i+1.1)/lg_scenario))
            visu_scenario[listepersonages[num].x][listepersonages[num].y]=i
        if sortie==2:
            if niv_debloque==100:
                niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(i+0.5)/lg_scenario)
                if verbose==1: print(('debloque ',niv_debloque))        

    #Place les passages secrets porteM
    for i in range(int(cote_carte*cote_carte/(25))):
        porte1=[randint(1, cote_carte), randint(1, cote_carte)]
        porte2=[randint(1, cote_carte), randint(1, cote_carte)]
        while((porte1[0]-porte2[0])**2+(porte1[1]-porte2[1])**2<=int(cote_carte/3)):
            porte2=[randint(1, cote_carte), randint(1, cote_carte)]
        porte1=[randint(200,700)+porte1[0]*1000,randint(200,300)+porte1[1]*600]
        porte2=[randint(200,700)+porte2[0]*1000,randint(200,300)+porte2[1]*600]
        obj2.append(['PorteM',porte2[0],porte2[1],porte1[0],porte1[1]])
        obj2.append(['PorteM',porte1[0],porte1[1],porte2[0],porte2[1]])
        if verbose: print('####>>> portes', porte1[0],porte1[1],porte2[0],porte2[1])

    imshow(array(carte))
    colorbar()
    axis('on')
    savefig('carte.png')
    
    if verbose==1:
        #fig = figure()
        #ax = Axes3D(fig)
   #ax.plot_surface(array(range(cote_carte)),array(range(cote_carte)),array(carte))
        #print("carte")
        #show()
        print("02 - Scenario cree")
        print("carte")
        show()

    imshow(array(visu_scenario))
    colorbar()
    axis('on')
    savefig('scenario.png')

    if verbose==1:        
        #contour(carte,8, alpha=.75, cmap='jet')
        imshow(array(visu_scenario))
        colorbar()
        axis('on')
        print("scenario")
        show()
    return scenario, obj2, pers2

def teste_scenario():
    if verbose==1: print('#####################################################')
    xc=3
    yc=4
    fini=False
    plan=zeros((cote_carte+2,cote_carte+2))

    plan[xc][yc]=carte[xc][yc]

    def affiche_plan(plan):
        for i in range(7):
            if verbose==1: print((plan[i]))

    def trouve(type_item,item, scenario):
        if type_item=='pers': t=1
        if type_item=='obj': t=2
        for j in range(len(scenario)):
            if scenario[j][3]==item and scenario[j][0]==t:
                if verbose==1: print(('#trouve:: ok',j))
                return j
        print(('#trouve:: erreur -NOK',t,item,scenario))
        return 'erreur'
    
    for s2 in range(0,len(scenario)):
        if scenario[s2][2]==2:
            niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/lg_scenario)
            break

    affiche_plan(plan)
    while(fini==False):

        dxc=0
        dyc=0
        a=eval(input('udlr ? '))
        if a=='u':dxc=-1
        if a=='d':dxc=1
        if a=='r':dyc=1
        if a=='l':dyc=-1
        if carte[xc+dxc][yc+dyc]>niv_debloque:
            print('!Bloque!')
            plan[xc+dxc][yc+dyc]=9
        else:
            xc+=dxc
            yc+=dyc
            plan[xc][yc]=carte[xc][yc]
        plan[xc][yc]+=10
        affiche_plan(plan)
        plan[xc][yc]-=10

        for i in range (len(obj)):
            if obj[i].x==xc and obj[i].y==yc:
                if obj[i].ramasse==0:
                    obj[i].ramasse=1
                    print(('Vous avez trouve un(e) ' + obj[i].nom))
                    print('Vous avez :')
                    for j in range(len(obj)):
                        if obj[j].ramasse==1:
                            print((obj[j].nom))                
        for i in range (len(pers)):
            if pers[i].x==xc and pers[i].y==yc:
                s=trouve('pers',i,scenario)
                pers[s].rencontre=1
                #Mets a jour satisfaction
                if scenario[s][1]==0: pers[i].satisfait=1
                if scenario[s][1]==1:
                    j=scenario[s+1][3]
                    if obj[j].ramasse==1:
                        pers[i].satisfait=1
                        print(('Bonjour, Je suis '+pers[i].nom+'. Tu as un '+obj[j].nom+' ! Je vais t\'aider'))
                if scenario[s][1]==2:
                    j=scenario[s+1][3]
                    if pers[j].rencontre==1:
                        pers[i].satisfait=1
                        print(('Tu connais '+pers[j].nom+' ! Laisse moi t\'aider'))
                #Execute la reaction
                if pers[i].satisfait==0:
                    if scenario[s][1]==1:
                        print(('Avez-vous un '+obj[scenario[s+1][3]].nom+' ?'))
                        print('Choisis la reponse: A-Non B-Non, mais je vais allez le chercher C-Je ne crois pas')
                        reponse=eval(input())
                    if scenario[s][1]==2:
                        j=scenario[s+1][3]
                        print(('Connais tu '+pers[j].nom+' ?'))
                    
                if pers[i].satisfait==1:
                    if scenario[s][2]==0:
                        print(('Bonjour, Je suis '+pers[i].nom))
                    if scenario[s][2]==1:
                        j=scenario[s+2][3] #s+2 ??
                        if pers[j].x-xc>0:
                            mot1='- Ouest (d) '
                        else:
                            mot1='- Est (u) '
                        if pers[j].y-yc>0:
                            mot2=' le Nord (r) '
                        else:
                            mot2=' le Sud (l) '
                        print(('Je suis '+pers[i].nom+'. Va vers '+mot2+mot1+'. Tu es sur le bon chemin'))
                    if scenario[s][2]==2:
                        niv_debloque=100
                        for s2 in range(s+1,len(scenario)):
                            if scenario[s2][2]==2:
                                niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/lg_scenario)
                                print(('Vous avez debloque le niveau',niv_debloque))
                                break

def cree_repertoire():
    partie=randint(1000,9999)
    while(os.path.exists(os.path.abspath(".")+str(partie))):
        partie=randint(1000,9999)
    os.makedirs(os.path.abspath(".") + '/parties/'+str(partie)+' '+titre)
    os.chdir(os.path.abspath(".") + '/parties/'+str(partie)+' '+titre)
    return partie

def nouvelle_partie(partie,cote_carte, carte, carte_fin, scenario, obj, pers, diff_debut, diff_fin,bloc_decor,bloc_chemin,decor):
    if verbose==1: print("10 - Nouvelle partie ")

    for x in range(1,cote_carte+1):
        for y in range(1,cote_carte+1):
            numzone=int(decor[x,y])%len(zones)
            if verbose: print([x,y],decor[x,y],numzone,zones[numzone])
            if verbose: print(listeBMDmulti[numzone])
            autobuild(carte[x,y]  ,  "niv "+ str([x, y]),zones[numzone],listeBMDmulti[numzone])

    niv_faits=zeros((cote_carte+2,cote_carte+2))
    etatpers=zeros((2,len(pers)))               # [ liste des attributs "rencontre" des persos dans l'ordre de pers (ou pers2 dans cree_scenario)             ,  dans le même ordre: liste des attributs "satisfait" des persos ]
    etatobj=zeros((2,len(obj)+1))               # [ liste des attributs "rencontre" ou "ramasse" des objets dans l'ordre de obj (ou obj2 dans cree_scenario)  ,  dans le même ordre: liste des attributs "satisfait" des objets qui est d'ailleur inutile... ☺ ]
##    for i in obj:
##        i.img=''
##    for i in pers:
##        i.img=''

    #Ajoute porte de fin
    ## self.obj.append(eval(obj2[i][0])(obj2[i][3],obj2[i][4],self, obj2[i][1],obj2[i][2],etatobj[0][i]))
    obj.append(['Porte',0,0,carte_fin[0]*1000+500, carte_fin[1]*600+250])
    
    print('######')
    print(obj)
    print(pers)
    f = open("format", 'wb')
    pickle.dump('F04', f) #A chaque changement de format de sauvegarde, incrementer FXX et copier-coller l'ancien format dans l'historique ci-dessous
    f.close()    
    f = open("scenario", 'wb')
    pickle.dump([partie, cote_carte, carte, scenario, obj, pers,diff_debut, diff_fin, bloc_decor,bloc_chemin, phrase_intro,phrase_fin], f) #obj, pers a la place de a
    f.close()
    f = open("niv_faits", 'wb')
    pickle.dump([niv_faits,etatpers,etatobj], f)
    f.close()
    f = open("carte_fait", 'wb')
    pickle.dump([False,precedent,[],0,0], f)
    f.close()
    os.chdir(os.path.abspath(".."))
    os.chdir(os.path.abspath(".."))
    print(("11 - Partie sauvegardee "+str(partie)))
    return partie

genere(cote_carte, diff_debut, diff_fin)
    
#Historique des formats
# F01
##    f = open("scenario", 'wb')
##    pickle.dump([partie, cote_carte, carte, scenario, diff_debut, diff_fin, bloc_decor,bloc_chemin], f)
##    f.close()
##    f = open("niv_faits", 'wb')
##    pickle.dump(niv_faits, f)
##    f.close()
#F02
##    f = open("scenario", 'wb')
##    pickle.dump([partie, cote_carte, carte, scenario, obj, pers,diff_debut, diff_fin, bloc_decor,bloc_chemin], f)
##    f.close()
##    f = open("niv_faits", 'wb')
##    pickle.dump(niv_faits, f)
##    f.close()
#F03
##    f = open("format", 'wb')
##    pickle.dump('F02', f) #A chaque changement de format de sauvegarde, incrementer FXX et copier-coller l'ancien format dans l'historique ci-dessous
##    f.close()    
##    f = open("scenario", 'wb')
##    pickle.dump([partie, cote_carte, carte, scenario, 0, 0,diff_debut, diff_fin, bloc_decor,bloc_chemin, phrase_intro,phrase_fin], f) #obj, pers a la place de a
##    f.close()
##    f=open("objpers",'wb')
##    pickle.dump([obj,pers],f)
##    f.close()
##    f = open("niv_faits", 'wb')
##    pickle.dump(niv_faits, f)
##    f.close()
##    f = open("carte_fait", 'wb')
##    pickle.dump([False,precedent,0,0,0], f)
##    f.close()
#F04
##    f = open("format", 'wb')
##    pickle.dump('F04', f) #A chaque changement de format de sauvegarde, incrementer FXX et copier-coller l'ancien format dans l'historique ci-dessous
##    f.close()    
##    f = open("scenario", 'wb')
##    pickle.dump([partie, cote_carte, carte, scenario, obj2, pers2,diff_debut, diff_fin, bloc_decor,bloc_chemin, phrase_intro,phrase_fin], f) #obj, pers a la place de a
##    f.close()
##    f = open("niv_faits", 'wb')
##    pickle.dump(niv_faits, f)
##    f.close()
##    f = open("carte_fait", 'wb')
##    pickle.dump([False,precedent,0,0,0], f)
##    f.close()
