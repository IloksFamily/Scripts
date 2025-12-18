import pygame,os
from var import *
import ClassesBlocs13

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
passages_secrets=[]
pers=[]
obj=[]
class PassageSecret():
    def __init__(self, x0,y0,x_fin, y_fin,debloque=True, img=pygame.image.load('./img/princesse.jpg')):
        self.x0,self.y0,self.x_fin, self.y_fin,self.debloque, self.img=x0,y0,x_fin, y_fin, img
        passages_secrets.append(self)



# definir xcarte et ycarte (courants)
class Personnage(Bloc): 
    mode='carte'
    [lgx,lgy]=[40,80]
    [x,y]=[0,0] #seulement utile pour creer scenario
    def __init__(self,x,y, xcarte, ycarte):
        Bloc__init__(self,x,y)
        self.xcarte=xcarte
        self.ycarte=ycarte
        self.utilise=0 #passe a 1 lorsqu'integre au scenario
        self.satisfait=0 #passe a 1 lorsque le critere d'entree est satisfait
        self.rencontre=0 #passe a 1 lorsqu'on le rencontre
    def interagit_entree(self, scenario):
        s=trouve('pers',i,scenario) #!!!!!!!!!
        if self.rencontre==0:
            IncrementeScore([0,0,0,0],1000)
            self.rencontre=1
            texte_pers+='+1000 points! '
            son_rencontre_personnage.play()
        texte_pers+='Bonjour, Je suis '+self.nom+'. '
        #Mets a jour satisfaction
        if scenario[s][1]==0:
            self.satisfait=1
        if scenario[s][1]==1:
            j=scenario[s+1][3]
            if obj[j].ramasse==1: #!!!!!!!!
                self.satisfait=1
                texte_pers+='Tu as un '+obj[j].nom+' ! Je vais t\'aider. '
        if scenario[s][1]==2:
            j=scenario[s+1][3]
            if pers[j].rencontre==1: #!!!!!!!!
                self.satisfait=1
                texte_pers+='Tu connais '+pers[j].nom+' ! Laisse moi t\'aider. ' 
        #Execute la reaction
        if self.satisfait==0:
            if scenario[s][1]==1: 
                texte_pers+='Avez-vous un '+obj[scenario[s+1][3]].nom+' ? ' 
            if scenario[s][1]==2:
                j=scenario[s+1][3]
                texte_pers+='Connais tu '+pers[j].nom+' ? ' 
        if self.satisfait==1:
            if scenario[s][2]==0:
                texte_pers+='Nous avons tous espoir en toi; Courage! '
            if scenario[s][2]==1:
                if s+2<=len(scenario)-1:
                    mot1=''
                    mot2=''
                    j=scenario[s+2][3] #s+2 ??
                    if pers[j].xcarte-xcarte>0:
                        mot1='- Est '
                    elif pers[j].xcarte-xcarte<0:
                        mot1='- Ouest '
                    if pers[j].ycarte-ycarte>0:
                        mot2=' le Sud '
                    elif pers[j].ycarte-ycarte<0:
                        mot2=' le Nord '
                    texte_pers+='Va vers '+mot2+mot1+'. '
                else:
                    texte_pers+='Tu es presque au bout de ta quete. Je ne peux plus t aider. Courage!'
            if scenario[s][2]==2:
                texte_pers+='Je vais te laisser passer.'
                niv_debloque=100
                for s2 in range(s+1,len(scenario)):
                    if scenario[s2][2]==2:
                        niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario)) #!!!!!!!! fonction a creer dans Jeu
                        texte_pers+='Vous avez debloque le niveau '+str(int(niv_debloque*10)/10.)
                        break
        

Princesse=type("Princesse",(Personnage,Vide),{"nom":'Princesse',"hf":'f',"bonte":'1'})
Magicien=type("Magicien",(Personnage,Vide),{"nom":'Magicien',"hf":'h',"bonte":'0.8'})
Chevalier=type("Chevalier",(Personnage,Vide),{"nom":'Chevalier',"hf":'h',"bonte":'0.7'})

class Objet(Bloc):
    [lgx,lgy]=[40,40]
    def __init__(self, x,y, xcarte, ycarte):
        Bloc__init__(self,x,y)
        self.xcarte=xcarte
        self.ycarte=ycarte
        self.ramasse=0
        self.utilise=0
    def interagit_entree(self, scenario):
        if self.ramasse==0:
            self.ramasse=1
            IncrementeScore([0,0,0,0],1000) 
            texte_pers+='+1000 points! Vous avez trouve un(e) ' + self.nom #!!!!!!!! cadre a afficher
            son_objet_gagne.play()       

Grimoire=type("grimoire",(Objet,Vide),{"nom":'grimoire'})
Cles=type("cles",(Objet,Vide),{"nom":'cles'})
Corde=type("corde",(Objet,Vide),{"nom":'corde'})
Parchemin=type("parchemin",(Objet,Vide),{"nom":'parchemin'})
Moulin=type("moulin",(Objet,Vide),{"nom":'Moulin a poivre'})
Appat=type("appat",(Objet,Vide),{"nom":'appat'})

def convertit(img):
    img=img.convert()
    img.set_colorkey(WHITE)
    return img


class JeuCarte():
    def __init__(self,partie):
        self.items=[]
        self.charge_joueurs()
        self.charge_carte(partie)
        self.xecran=0
        self.yecran=0
        self.continu=0 #0 continue, -1 pour recommencer, 1 pour jeu suivante

    def charge_carte(self,partie):
        global partiebis, cote_carte, carte, scenario, obj, pers, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin
        global xcarte, ycarte, niv_debloque, direc_carte, niveau_precedent, niv_faits
        f = open('./parties/'+str(partie)+'/format', 'rb')
        form=pickle.load(f, encoding='latin1') 
        print(form)
        f.close()
        f = open('./parties/'+str(partie)+"/scenario", 'rb')
        [partiebis, cote_carte, carte, scenario, obj2, pers2, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin] = pickle.load(f, encoding='latin1')
        f.close()
        f = open('./parties/'+str(partie)+"/niv_faits", 'rb')
        niv_faits=pickle.load(f, encoding='latin1')
        f.close()
        #Transforme liste obj2 et pers2 en liste d objet obj et pers
        for i in range(len(pers2)):
            pers.append(eval(pers2[i][0])(pers2[i][3],pers2[i][4],pers2[i][1],pers2[i][2])) 
        for i in range(len(obj2)):
            obj.append(eval(obj2[i][0])(obj2[i][3],obj2[i][4],obj2[i][1],obj2[i][2])) 
                        
        niv_debloque=diff_fin
        for s2 in range(0,len(scenario)):
            if scenario[s2][2]==2:
                niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario))
                niv_debloque=max(carte[pers[scenario[s2][3]].x,pers[scenario[s2][3]].y]*1.2,1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario)))
                print(('Vous avez debloque le niveau',niv_debloque))
                break
        print('> Partie chargee')

    def charge_joueurs(self):
        global nb_joueurs
        self.joueurs=[JoueurCarte(100+3000,300+2*600,0,1)]
        nb_joueurs=len(self.joueurs)
    def bouge_ecran(self):
        if self.joueurs[0].x-self.xecran>600:
            self.xecran+=self.joueurs[0].x-600-self.xecran
        if self.joueurs[0].x-self.xecran<400 and self.xecran>0:
            self.xecran-=400-self.joueurs[0].x+self.xecran
        if self.joueurs[0].y-self.yecran>350:
            self.xecran+=self.joueurs[0].y-350-self.xecran
        if self.joueurs[0].y-self.xecran<250 and self.xecran>0:
            self.xecran-=250-self.joueurs[0].y+self.xecran
           
    def musique_niveau(self):
        #pygame.mixer.music.load("./sons/savane_musique.mp3")
        #pygame.mixer.music.play(-1,0)
        pass
    def run(self):
        self.musique_niveau()
        while(self.continu==0):
            surf.fill(MARRON)
            self.bouge_ecran()
            Item.activetout(self.xecran)
            r=self.joueurs[0].entree.metajourCarte()
            if self.joueurs[0].entree.efface: self.continu=-1
            Item.bougetout(self)
            Item.interagittout(self)
            Item.affichetout(self,self.xecran, self.yecran)
            #self.cadrewiimote.affichebarre(200,10,20,50,4,1,2,self.J1.vy)
            #d Item.affiche(shadow, self.DISPLAYSURF,self.xecran)
            pygame.display.update()
            fpsClock.tick(FPS)
        for i in self.items:
            del i
        self.items=[]
        return [self.continu,points.solde]

class JoueurCarte(Mobile):
    lgx=89
    lgy=100
    v0=2
    def __init__(self,x,y, nj,etat):
        self.gravite=0
        Mobile.__init__(self,x,y)
        self.entree=Inputs(0)
        self.type='joueur'
        ilokImgD=pygame.transform.scale(pygame.image.load('./img/ilok_D.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgD.set_colorkey(WHITE)
        ilokImgG=pygame.transform.flip(ilokImgD,1,0)  #pygame.transform.scale(pygame.image.load('./img/Ilok_G.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgG.set_colorkey(WHITE)
        ilokImgB=pygame.transform.scale(pygame.image.load('./img/ilok_B.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgB.set_colorkey(WHITE)
        ilokImgH=pygame.transform.scale(pygame.image.load('./img/ilok_H.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgH.set_colorkey(WHITE)
    def interagit_joueur(self, joueur,cont, jeu):pass  
    def bouge(self,jeu):
        if self.entree.accelere:
            self.accel=2
        else:
            self.accel=1
            self.vx=0
            self.vy=0
        if self.entree.gauche:
            self.x-=self.v0*self.accel
            self.vx=-self.v0
        elif self.entree.droite:
            self.x+=self.v0*self.accel
            self.vx=self.v0
        if self.entree.haut:
            self.y-=self.v0*self.accel
            self.vy=-self.v0
        elif self.entree.bas:
            self.y+=self.v0*self.accel
            self.vy=self.v0
        if self.forcex==-1 or signeoppose(self.forcex_dir, self.vx):
            self.x+=self.vx
        else:
            self.x=self.forcex
        self.forcex=-1
        if self.forcey==-1 or signeoppose(self.forcey_dir, self.vy):
            self.y+=self.vy
        else:
            self.y=self.forcey
        self.forcey=-1

    def affiche(self,xecran,yecran):
        if self.entree.gauche:
            surf.blit(ilokImgG, (self.x-xecran, self.y-yecran))
        elif self.entree.droite:
            surf.blit(ilokImgD, (self.x-xecran, self.y-yecran))
        elif self.entree.haut:
            surf.blit(ilokImgH, (self.x-xecran, self.y-yecran))
        elif self.entree.bas:
            surf.blit(ilokImgB, (self.x-xecran, self.y-yecran))
        elif:
            surf.blit(ilokImgB, (self.x-xecran, self.y-yecran))

    
##pers=[]
##pers.append(Personnage('Roumir','h',1))
##pers.append(Personnage('Bachir','h',0))
##pers.append(Personnage('Yellet','f',0.3))
##pers.append(Personnage('Kzamara','h',0.5))
##pers.append(Personnage('Oyea','f',1))
##pers.append(Personnage('Ulud','h',1))
##pers.append(Personnage('Latram','f',1))
##pers.append(Personnage('Froyx','h',1))
##pers.append(Personnage('Madrij','f',1))
##pers.append(Personnage('Idril','f',1))
##pers.append(Personnage('Reejad','f',1))
##pers.append(Personnage('Prokof','h',1))
##pers.append(Personnage('Zadig','f',1))
##pers.append(Personnage('Seamol','h',0.2))
##pers.append(Personnage('Gargot','h',1))
##pers.append(Personnage('Druz','h',1))
##pers.append(Personnage('Parax','h',1))
##pers.append(Personnage('Qrohel','h',1))
##pers.append(Personnage('Ktaf','f',1))
##
##obj=[]
##obj.append(Objet('grimoire'))
##obj.append(Objet('cles'))
##obj.append(Objet('corde'))
##obj.append(Objet('parchemin'))
##obj.append(Objet('moulin a poivre'))
##obj.append(Objet('appat'))
##obj.append(Objet('codex'))
##obj.append(Objet('pelle'))
##obj.append(Objet('bandeau'))
##obj.append(Objet('echelle'))
##obj.append(Objet('radeau'))
##obj.append(Objet('scie'))
##obj.append(Objet('fouet'))
##obj.append(Objet('liane'))
##obj.append(Objet('sextant'))
##obj.append(Objet('drapeau'))
##obj.append(Objet('eperon'))
