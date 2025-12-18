
import pygame
from Menus11 import *
from var import *
from Cadres import *
from pygame.locals import *
import os

l_ilok_carte,h_ilok_carte=89,100
ilokImgD=pygame.transform.scale(pygame.image.load('./img/ilok_D.png'), (l_ilok_carte,h_ilok_carte)).convert()
ilokImgD.set_colorkey(WHITE)
ilokImgG=pygame.transform.flip(ilokImgD,1,0)  #pygame.transform.scale(pygame.image.load('./img/Ilok_G.png'), (l_ilok_carte,h_ilok_carte)).convert()
ilokImgG.set_colorkey(WHITE)
ilokImgB=pygame.transform.scale(pygame.image.load('./img/ilok_B.png'), (l_ilok_carte,h_ilok_carte)).convert()
ilokImgB.set_colorkey(WHITE)
ilokImgH=pygame.transform.scale(pygame.image.load('./img/ilok_H.png'), (l_ilok_carte,h_ilok_carte)).convert()
ilokImgH.set_colorkey(WHITE)
ilok_victoire_img=pygame.transform.scale(pygame.image.load('./img/ilok_victoire.png'), (226,305)).convert()
porte_img=pygame.transform.scale(pygame.image.load('./img/porte.png'), (90,100)).convert()
porte_img.set_colorkey(WHITE)
fin_img=pygame.transform.scale(pygame.image.load('./img/village.jpg'), (1000,600)).convert()
ilok_victoire_img.set_colorkey(WHITE)
hbord=166
lbord=100
bordcarte_hautbas_img= pygame.transform.scale(pygame.image.load('./img/bord_carte3.png'),(1000, 166)).convert()
bordcarte_cote_img= pygame.transform.scale(pygame.transform.rotate(pygame.image.load('./img/bord_carte3.png'),90),(100, 600)).convert() 
bordcarte_hautbas_img.set_colorkey(WHITE)
bordcarte_cote_img.set_colorkey(WHITE)
son_objet_gagne=pygame.mixer.Sound('./sons/'+'objet_gagne.wav')
son_rencontre_personnage=pygame.mixer.Sound('./sons/'+'mystere-rencontre-personnage.wav')
active_musique=1
lgx_ecran=1000
lgy_ecran=600
decor_type=['','arbre_normal','arbre_normal2','arbre_fleur','arbre_palmier','arbre_palmier2','arbre_foret_sapins','arbre_sapin_neige','arbre_porte','arbre_bleuciel','arbre_rouge','arbre_rouge2']
decor_img=[]
d_chemin=80 #d
d_arbre=80 #d
fini=0

for i in range(len(decor_type)):
    if decor_type[i]!='':
        decor_img.append(pygame.transform.scale(pygame.image.load('./img/'+str(decor_type[i])+'.png'), (d_arbre, d_arbre)))
    else:
        decor_img.append('')
chemin_img=pygame.transform.scale(pygame.image.load('./img/chemin.png'), (d_chemin, d_chemin))                         

#carte
niv_faits=[[0 for i in range(8)] for j in range(8)]
niv_faits[3][2]=1
#niv_faits[3][3]=1
#niv_faits[2][3]=1

xcarte=3
ycarte=2
direc_carte=[xcarte,ycarte]
niveau_precedent=direc_carte

def trouve(type_item,item, scenario):
        if type_item=='pers': t=1
        if type_item=='obj': t=2
        for j in range(len(scenario)):
            if scenario[j][3]==item and scenario[j][0]==t:
                print(('#trouve:: ok',j))
                return j
        print(('#trouve:: NOK',t,item,scenario))
        return 'erreur' 

def MajNiveauxFaits(partie,d):
    #met a jour niv_faits
    [xcarte, ycarte]=d
    niv_faits[d[0]][d[1]]=1
    fini=0
    os.chdir(os.path.abspath(".")+"/parties/"+str(partie))
    f = open("niv_faits", 'wb')
    pickle.dump(niv_faits, f)
    f.close()
    for i in range(len(obj)):
        obj2[i].ramasse=obj[i].ramasse    ######################################################################################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#################################################################################################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~############################################################################################
        obj2[i].utilise=obj[i].utilise    ######################################################################################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#################################################################################################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~############################################################################################
    for i in range(len(pers)):
        pers2[i].rencontre=pers[i].rencontre
        pers2[i].satisfait=pers[i].satisfait
    f=open("objpers",'wb')
    pickle.dump([obj2,pers2],f)
    f.close()
    os.chdir(os.path.abspath(".."))
    os.chdir(os.path.abspath(".."))


    

def ChargeCarte(partie):
    global partiebis, cote_carte, carte, scenario, obj2, pers2, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin
    global obj2,pers2, niv_debloque
    global xcarte, ycarte, niv_debloque, direc_carte, niveau_precedent, niv_faits
    f = open('./parties/'+str(partie)+'/format', 'rb')
    form=pickle.load(f, encoding='latin1') 
    print(form)
    f.close()
    f = open('./parties/'+str(partie)+"/scenario", 'rb')
    [partiebis, cote_carte, carte, scenario, obj2, pers2, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin] = pickle.load(f, encoding='latin1')
    f.close()
    f=open('./parties/'+str(partie)+"/objpers",'rb')
    [obj2,pers2]=pickle.load(f, encoding='latin1')
    f.close()
    f = open('./parties/'+str(partie)+"/niv_faits", 'rb')
    niv_faits=pickle.load(f, encoding='latin1')
    f.close()
##        os.chdir(os.path.abspath(".."))
##        os.chdir(os.path.abspath(".."))

    for i in range(len(obj)):
        obj[i].ramasse=obj2[i].ramasse
        obj[i].utilise=obj2[i].utilise
        obj[i].x=obj2[i].x
        obj[i].y=obj2[i].y
    for i in range(len(pers)):
        pers[i].rencontre=pers2[i].rencontre
        pers[i].satisfait=pers2[i].satisfait
        pers[i].x=pers2[i].x
        pers[i].y=pers2[i].y
    if False:
        print(('scenario',scenario))
        for d in pers:
            print(('pers',d.x,d.y))
        for d in obj:
            print(('obj',d.x,d.y))
    niv_debloque=diff_fin
    for s2 in range(0,len(scenario)):
        if scenario[s2][2]==2:
            niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario))
            niv_debloque=max(carte[pers[scenario[s2][3]].x,pers[scenario[s2][3]].y]*1.2,1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario)))
            print(('Vous avez debloque le niveau',niv_debloque))
            break            

    print('> Partie chargee')
    

def BoucleCarte(partie):
    fin=0
    global partiebis, cote_carte, carte, scenario, obj2, pers2, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin
    global obj2,pers2, niv_debloque
    global xcarte, ycarte, niv_debloque, direc_carte, niveau_precedent
    carte_direction=""
    continue_carte=1
    while continue_carte:
        #===============SCENARIO==================
        img_liste=[]
        cadre_liste=[]
        texte_pers=''
        points=0
        #objet trouvé
        for i in range (len(obj)):
            if obj[i].x==xcarte and obj[i].y==ycarte:
                if obj[i].ramasse==0:
                    obj[i].ramasse=1
                    print(('Vous avez trouve un(e) ' + obj[i].nom))
                    points+=1000
                    texte_pers+='+1000 points! Vous avez trouve un(e) ' + obj[i].nom
                    son_objet_gagne.play()
                    print('Vous avez :')
                    for j in range(len(obj)):
                        if obj[j].ramasse==1:
                            print((obj[j].nom))

        if False:
            print(scenario)
            print((xcarte,ycarte, niv_debloque))
            print('#########')
            for i in range(len(pers)):
                print(('pers',i,pers[i].nom, pers[i].x, pers[i].y, pers[i].satisfait, pers[i].rencontre))
            for i in range(len(obj)):
                print(('obj',i,obj[i].nom, obj[i].x, obj[i].y, obj[i].ramasse))
            print('#########')
        
        for i in range (len(pers)):
            if pers[i].x==xcarte and pers[i].y==ycarte:
                img_liste.append(pers[i].img) #images à afficher
                print('----<')
                s=trouve('pers',i,scenario)
                if pers[i].rencontre==0:
                    points+=1000
                    pers[i].rencontre=1
                    texte_pers+='+1000 points! '
                    son_rencontre_personnage.play()
                texte_pers+='Bonjour, Je suis '+pers[i].nom+'. '
                #Mets a jour satisfaction
                if scenario[s][1]==0:
                    pers[i].satisfait=1
                    print('satisf',i, pers[i].satisfait)
                if scenario[s][1]==1:
                    j=scenario[s+1][3]
                    if obj[j].ramasse==1:
                        pers[i].satisfait=1
                        print(('Tu as un '+obj[j].nom+' ! Je vais t\'aider'))
                        texte_pers+='Tu as un '+obj[j].nom+' ! Je vais t\'aider. '
                    print('satisf',i, pers[i].satisfait)
                if scenario[s][1]==2:
                    j=scenario[s+1][3]
                    if pers[j].rencontre==1:
                        pers[i].satisfait=1
                        print(('Tu connais '+pers[j].nom+' ! Laisse moi t\'aider'))
                        texte_pers+='Tu connais '+pers[j].nom+' ! Laisse moi t\'aider. '
                    print('satisf',i, pers[i].satisfait)
                #Execute la reaction
                if pers[i].satisfait==0:
                    if scenario[s][1]==1:
                        print(('Avez-vous un '+obj[scenario[s+1][3]].nom+' ?'))
                        texte_pers+='Avez-vous un '+obj[scenario[s+1][3]].nom+' ? '
                        print('Choisis la reponse: A-Non B-Non, mais je vais allez le chercher C-Je ne crois pas')
                        #reponse=raw_input()
                    if scenario[s][1]==2:
                        j=scenario[s+1][3]
                        print(('Connais tu '+pers[j].nom+' ?'))
                        texte_pers+='Connais tu '+pers[j].nom+' ? '
                if pers[i].satisfait==1:
                    if scenario[s][2]==0:
                        texte_pers+='Nous avons tous espoir en toi; Courage! '
                    if scenario[s][2]==1:
                        if s+2<=len(scenario)-1:
                            mot1=''
                            mot2=''
                            j=scenario[s+2][3] #s+2 ??
                            if pers[j].x-xcarte>0:
                                mot1='- Est '
                            elif pers[j].x-xcarte<0:
                                mot1='- Ouest '
                            if pers[j].y-ycarte>0:
                                mot2=' le Sud '
                            elif pers[j].y-ycarte<0:
                                mot2=' le Nord '
                            print(('Va vers '+mot2+mot1+'. Tu es sur le bon chemin'))
                            texte_pers+='Va vers '+mot2+mot1+'. '
                        else:
                            print('Tu es presque au bout de ta quete. Je ne peux plus t aider. Courage!')
                            texte_pers+='Tu es presque au bout de ta quete. Je ne peux plus t aider. Courage!'
                    if scenario[s][2]==2:
                        print('Je vais te laisser passer.')
                        texte_pers+='Je vais te laisser passer.'
                        niv_debloque=100
                        for s2 in range(s+1,len(scenario)):
                            if scenario[s2][2]==2:
                                niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario))
                                print(('Vous avez debloque le niveau',niv_debloque))
                                texte_pers+='Vous avez debloque le niveau '+str(int(niv_debloque*10)/10.)
                                break
                print('>----')
        IncrementeScore([0,0,0,0],points) #PointsJoueur
        
        #=============fin du scenario================
        #============= affiche la carte ================
        
        surf.fill(WHITE)
        stop_carte=0
        catx=450+350*(niveau_precedent[0]-xcarte)
        caty=200+100*(niveau_precedent[1]-ycarte)
        mario_marche_carte=0
        NbArbre=20
        ilokImgCarte=ilokImgD

        carte_terminee=0
        if carte[xcarte, ycarte]==diff_fin:
            carte_terminee=1
            for i in range(len(pers)):
                if pers[i].satisfait==0 and pers[i].x!=-1:
                    carte_terminee=0
            for i in range(len(obj)):                    
                if obj[i].ramasse==0 and obj[i].x!=-1:
                    carte_terminee=0
        #cherche un passage secret
        passage=None
        for ps in passages_secrets:
            if (ps.debloque) and (ps.x0,ps.y0==xcarte,ycarte):
                passage=ps
        while stop_carte==0:

            v_lat=0 #vitesse latérale de mario
            v_h=0 #vitesse horizontale "  "           
            keys=pygame.key.get_pressed()
            if keys[K_LCTRL]:
                speed=25
            else:
                speed=5
            if keys[K_RIGHT] and catx+l_ilok_carte<990:
                v_lat=speed
                ilokImgCarte=ilokImgD
            if keys[K_LEFT] and catx>10:
                v_lat=-speed
                ilokImgCarte=ilokImgG
            if keys[K_UP] and caty>10:
                v_h=-speed
                ilokImgCarte=ilokImgH
            if keys[K_DOWN] and caty+h_ilok_carte<490:
                v_h=speed
                ilokImgCarte=ilokImgB
            catx+=v_lat
            caty+=v_h

            surf.fill(MARRON)
            for d in bloc_decor:
                if d[0]>=xcarte*lgx_ecran and d[0]<(xcarte+1)*lgx_ecran:
                    if d[1]>=ycarte*lgy_ecran and d[1]<(ycarte+1)*lgy_ecran:
                        surf.blit(decor_img[int(d[2])],(d[0]-xcarte*lgx_ecran,d[1]-ycarte*lgy_ecran))
##            for d in bloc_chemin:
##                if d[0]>=xcarte*lgx_ecran and d[0]<(xcarte+1)*lgx_ecran:
##                    if d[1]>=ycarte*lgy_ecran and d[1]<(ycarte+1)*lgy_ecran:
##                        surf.blit(chemin_img,(d[0]-xcarte*lgx_ecran,d[1]-ycarte*lgy_ecran))
                        
##            couleurbord=[RED,RED,RED,RED]
            if passage!=None:
                surf.blit(passage.img(), passage.coord_ecran)
            if carte[xcarte,ycarte-1]>niv_debloque: surf.blit(bordcarte_hautbas_img,(0,-hbord/2))
            if carte[xcarte,ycarte+1]>niv_debloque: surf.blit(bordcarte_hautbas_img,(0,500-hbord/2))
            if carte[xcarte-1,ycarte]>niv_debloque: surf.blit(bordcarte_cote_img,(-lbord/2,0))
            if carte[xcarte+1,ycarte]>niv_debloque: surf.blit(bordcarte_cote_img,(1000-lbord/2,0))

            if carte[xcarte, ycarte]==diff_fin:
                surf.blit(porte_img,(400,200))
            if carte_terminee==1:
                time.sleep(2)
                f = open('./parties/'+str(partie)+"/carte_fait", 'rb')
                [a,b,c,d,e]=pickle.load(f, encoding='latin1')
                f.close()
                f = open('./parties/'+str(partie)+"/carte_fait", 'wb')
                pickle.dump([True,b,c,d,e], f)
                f.close()
                menufin=FinPartie()
                menufin.affiche(fin_img, ilok_victoire_img, phrase_fin)
                pygame.display.update()
                print("FIN")
                verifie_ferme_fenetre()
                fin=1
                continue_carte=0
                stop_carte=1
                    
            cadrecarte.affiche(niv_faits,xcarte,ycarte)
            #cadrepoints.affiche(surf,points)
            cadreobjets.affiche( obj)
            if texte_pers!='':
                cadretexte.affiche(texte_pers)
            if xcarte==3 and ycarte==2:
                cadreaide3.affiche("Ilok se deplace a l'aide des fleches du clavier. Il peut explorer les environs en allant aux bords de l'écran. Qui sait ce qui l'attendra : des rencontres, de nouveaux objets? Mais pour decouvrir l'endroit suivant il devra relever un defi!")
                cadreaide1.affiche('Ilok gardera la mémoire de son exploration sur cette carte. Sa position apparaitra en bleu')
                cadreaide2.affiche("Ici apparaitront les objets qu'Ilok va glaner") 
        
            surf.blit(ilokImgCarte, (catx, caty)) #on ajoutera l indice mario_marche_carte plus tard
            for i in range(len(img_liste)):
                surf.blit(img_liste[i], (400, 200))
                                 
            if caty<=hbord/2 and ycarte>1:
                if carte[xcarte,ycarte-1]<=niv_debloque:
                    stop_carte=1
                    time.sleep(1)
                    direc_carte=[xcarte,ycarte-1] #indique les coordonnées cible
                    carte_direction="up"
                else:
                    cadreaide4.affiche("Une onde magique empeche d'aller par la! Ilok doit trouver quelqu'un qui sache l'aider")
                
            if catx<=lbord/2 and xcarte>1:
                if carte[xcarte-1,ycarte]<=niv_debloque :
                    stop_carte=1
                    time.sleep(1)
                    direc_carte=[xcarte-1,ycarte]
                    carte_direction="left"
                else:
                    cadreaide4.affiche("Une onde magique empeche d'aller par la! Ilok doit trouver quelqu'un qui sache l'aider")
                    
            if catx>=1000-lbord/2-l_ilok_carte and xcarte<cote_carte:
                if carte[xcarte+1,ycarte]<=niv_debloque :
                    stop_carte=1
                    time.sleep(1)
                    direc_carte=[xcarte+1,ycarte]
                    carte_direction="right"
                else:
                    cadreaide4.affiche("Une onde magique empeche d'aller par la! Ilok doit trouver quelqu'un qui sache l'aider")

            if caty>=500-hbord/2-h_ilok_carte and ycarte<cote_carte :
                if carte[xcarte,ycarte+1]<=niv_debloque :
                    stop_carte=1
                    time.sleep(1)
                    direc_carte=[xcarte,ycarte+1]
                    carte_direction="down"
                else:
                    cadreaide4.affiche("Une onde magique empeche d'aller par la! Ilok doit trouver quelqu'un qui sache l'aider")
            
            verifie_ferme_fenetre()
            pygame.display.update()
            fpsClock.tick(FPS)
            #pygame.event.get()
            keys=pygame.key.get_pressed()

            #fin de la boucle affichage de la carte ###########
            
        if niv_faits[direc_carte[0]][direc_carte[1]]==1: # or debug_mode==1: #d initial=[direc_carte[0],direc_carte[1]]
            niveau_precedent=[xcarte,ycarte]
            [xcarte,ycarte]=direc_carte

        else:
            continue_carte=0
            niveau_precedent=[xcarte,ycarte]
    return [direc_carte,fin]

        #fin de la boucle carte ##################################################################


cadrecarte=CadreCarte(800,10,150,150)
cadrepoints=CadrePoints(200,10,50,30)
cadreobjets=CadreObjets(0,500,1000,100)
cadretexte=CadreTexte(0,0,250,120)
cadreaide1=CadreAide(500,10,280,120)
cadreaide2=CadreAide(20,420,220,100)
cadreaide3=CadreAide(100,10,300,180)
cadreaide4=CadreAide(100,10,250,120)


#Activation
##        self.cadrecarte=CadreCarte(800,10,150,150)
##        self.cadrepoints=CadrePoints(200,10,50,30)
##        partie.cadrecarte.affiche(surf,niv_faits,3,2)
##        partie.cadrepoints.affiche(surf,partie.points)
