import pygame, math, time
from var import *

from AfficheCarte import *
import PersonnagesObjets
import senstream
import random, time, os, sys

nb_joueurs=0
CGjoueurs=[0,0]

class Points():
    def __init__(self):
        self.solde=0
    def diviserpar(self,a):
        self.solde=int(self.solde/a)
    def soldenul(self):
        self.solde=0
    def pointsajoute(self,a):
        self.solde+=a

points=Points()
    
class Vide():
    pass

class Item:
    img=[]
    [diff, zone, mode]=[0.1, 'virtuel','niveau']
    def __init__(self,x,y,jeu):
        self.x=x
        self.y=y
        self.existe=1
        self.actif=1
        if not hasattr(self, 'lgx'): self.lgx=type(self).lgx
        if not hasattr(self, 'lgy'): self.lgy=type(self).lgy
        if hasattr(self, 'type'):
            if self.type=='decor': #pour que les décors s'affichent dans le bon ordre
                i=-1
                for i in range(len(jeu.items)):
                    if jeu.items[i].type=='decor':
                        if self.profondeur <= jeu.items[i].profondeur: break
                jeu.items.insert(i+1,self)
            else: jeu.items.append(self)
        else: jeu.items.append(self)
        self.compteur=0
        self.type=""
        self.texte=""
        self.typeimg=''
        #if self.zone!='virtuel': self.texte=str(type(self).__name__)+' est un '+self.type
        if not hasattr(type(self),'imgchargee') or self.typeimg!=type(self): #(ou: "if type(self).imgchargee==False:" ?)
            ok=1
            type(self).imgchargee=True
            type(self).img=[]
            type(self).imgG=[]
            try:
                type(self).img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+'.jpg'), (self.lgx,self.lgy)).convert())
                type(self).img[0].set_colorkey(WHITE)
            except :
                try:
                    type(self).img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+'.png'), (self.lgx,self.lgy)))
                    type(self).img[0].set_colorkey(WHITE)
                except:
                    try:
                        for i in range(10):
                            type(self).img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+str('%02d'%i)+'.jpg'), (self.lgx,self.lgy)))
                    except :
                        try:
                            for i in range(10):
                                type(self).img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+str('%02d'%i)+'.png'), (self.lgx,self.lgy)))
                        except :
                            if i==0:
                                print('couldnt find '+self.__class__.__name__.lower()+str('%02d'%i)+'.jpg or .png . '+os.getcwd()+'/img')
                                ok=0
                               # type(self).img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+'.jpg'), (self.lgx,self.lgy)).convert())
                                #type(self).img[0].set_colorkey(WHITE)

    ##        type(self).img=pygame.transform.scale(pygame.image.load(self.__class__.__name__.lower()+'.jpg'), (self.lgx,self.lgy))
            if ok:
                type(self).img_ecrase=pygame.transform.scale(type(self).img[0], (self.lgx,int(self.lgy/3)))        
                for image in type(self).img:
                    image=image.convert()
                    image.set_colorkey(WHITE)
                    self.imgG.append(pygame.transform.flip(image, True, False))
                self.typeimg=type(self)
            
    def bouge(self,jeu): pass
    def supprime(self,jeu):
        if self.type=='joueur':
            self.perd()
        else:
            print(self.type,' supprimé!')
            jeu.items.remove(self)
            del(self)

    def affiche(self,xecran,yecran,x='',y=''):
        if x=='': x=self.x
        if y=='': y=self.y
        if hasattr(self, 'vx'):
            if self.vx>=0:
                surf.blit(type(self).img[int(self.compteur)], (x-xecran, y-yecran))
            if self.vx<0:
                surf.blit(type(self).imgG[int(self.compteur)], (x-xecran, y-yecran))
        else:
           surf.blit(type(self).img[int(self.compteur)], (x-xecran, y-yecran))
        self.compteur+=0.3
        if self.compteur>=len(type(self).img):
            self.compteur=0
    def affiche_ecrase(self,xecran, yecran):
        surf.blit(type(self).img_ecrase, (self.x-xecran, self.y+self.lgy*2/3-yecran))
        self.estecrase-=1
        if self.estecrase<0:
            self.existe=0#modif!!!
            #delete(self)
    def interagit(self): pass
    #Fonctions de classe qui agissent sur tous les elements qui derivent de Item
    def activetout(jeu):
        for d in jeu.items:
            if d.x>jeu.xecran-d.lgx-100 and d.x<jeu.xecran+lgx_ecran+100 and d.y-jeu.yecran<600 and d.y+d.lgy>jeu.yecran: d.actif=1
            else: d.actif=0
    def saisittout(jeu):
        for d in jeu.items:
            if isinstance(d,Joueur):
                r=d.entree.metajour(jeu)
        return r
    def bougetout(jeu):
        global CGjoueurs
        [CGx, CGy]=[0,0]
        for d in jeu.items:
            if d.existe==1 and d.actif==1:
                d.bouge(jeu)
                if d.__class__.__name__.lower()=='joueur':
                    CGx+=d.x
                    CGy+=d.y
        CGjoueurs[0]=CGx/nb_joueurs
        CGjoueurs[1]=CGy/nb_joueurs
    def interagittout(jeu):
        for d in jeu.items:
            if d.existe==1 and d.actif==1:
                if d.type=='bloc':
                    for e in jeu.items:
                        if e.type!='bloc' and e.existe==1 and e.actif==1:
                            c=contact(d,e)
                            if c!='':
                                if e.type=='joueur': d.interagit_joueur(e,c,jeu)
                                if e.type=='mobile': d.interagit_mobile(e,c)
                            elif type(d).__name__=='Colline' and (e.type=='mobile' or e.type=='joueur'):
                                d.interagit_interieur(jeu,e)                                    
                if d.type=='mobile':
                    demi_tour=0
                    for e in jeu.items:
                        if e.type=='joueur' and e.existe==1 and e.actif==1:
                            c=contact(d,e)
                            if c!='': d.interagit_joueur(e,c,jeu)
                        elif e.type=='mobile' and e.existe==1 and e.actif==1:
                            c=contact(d,e)
                            if c!='': d.interagit_mobile(e,c)                            
                        
    def affichetout(jeu, xecran, yecran):
        for d in jeu.items:
            if d.type=="decor" and d.plan=="arriere": ## prendre en compte les profondeurs (ou le faire avec l'ordre de la liste dans l'initialisation du niveau?
                d.affiche(xecran, yecran)
            if d.actif==1 and d.type=="decorcarte" and d.plan=="arriere":
                d.affiche(xecran,yecran)
        for d in jeu.items:
            if d.existe==1 and d.actif==1 and d.type!='decor' and d.type!='decorcarte': d.affiche(xecran, yecran)
            elif d.existe==0.5 and d.actif==1 and d.zone!='virtuel': d.affiche_ecrase(xecran, yecran)
        for d in jeu.items:
            if d.type=="decor" and d.plan=="avant":d.affiche(xecran, yecran)
    def interagit_mobile(self,a,b):pass
    def interagit_joueur(self,a,b,jeu):pass
    
class Bloc(Item):
    [diff, zone]=[0.1, 'virtuel']
    ausol=False
    def __init__(self,x,y,jeu):
        Item.__init__(self,x,y,jeu)
        self.solide=1
        self.type='bloc'
    def attaque(self): pass

class Piece(Bloc):
    [lgx,lgy]=[30,30]
    [diff, zone]=[0, 'commun']
    #img=pygame.transform.scale(pygame.image.load('piece.jpg'), (lgx,lgy))
    #son=pygame.mixer.Sound("piece.wav")
    def interagit_joueur(self, joueur,cont, jeu):
        Points.pointsajoute(points,2)
        #Piece.sonPiece.play()
        self.existe=0

PieceSava=type("PieceSava",(Piece,Vide),{"zone":'savane'})
PieceBermat=type("PieceBermat",(Piece,Vide),{"zone":'bermat'})
        
class Drapeau(Bloc):
    [lgx,lgy]=[50,90]
    [diff, zone]=[0, 'commun']
    def interagit_joueur(self, joueur,cont, jeu):
        jeu.continu=1

class Solide(Bloc):
    [diff, zone]=[0.1, 'virtuel']
    ausol=True
    plan='devant'
    def interagit_mobile(self,mobile,cont):
        mobile.surbloc=1

        if cont=='dessus':
            mobile.forcey=self.y+self.lgy
            mobile.forcey_dir=-1
            mobile.vy=0
        if cont=='dessous':
            mobile.forcey=self.y-mobile.lgy
            if mobile.vy>0:
                mobile.vy=0
            mobile.forcey_dir=1
            mobile.surbloc=1

        if cont=='gauche':
            mobile.forcex=self.x+self.lgx
            mobile.forcex_dir=-1
        if cont=='droite':
            mobile.forcex=self.x-mobile.lgx
            mobile.forcex_dir=1
        
        if cont=='gauche': mobile.vx=abs(mobile.vx)
        if cont=='droite': mobile.vx=-abs(mobile.vx)

    def interagit_joueur(self, joueur,cont,jeu):
        self.interagit_mobile(joueur,cont)
        if cont=='dessus':
            self.attaque()
        if cont=='dessous':
            joueur.vy=0
            if not joueur.entree.saute:
                joueur.TempsImpulsionSaut=0

    
class Colline(Solide):
    [lgx,lgy]=[50,200]
    [diff, zone]=[0, 'virtuel']
    imgchargee = True #evite de faire charger une image par defaut
    def __init__(self,x,y,jeu,dy1='',dy2='', lgx=50,lgy=200,img="texture.jpg"):  #dy1 est l'intervalle de vide entre (x,y) et le point haut gauche de la colline. dy2 est la même chose à droite.
        Bloc.__init__(self,x,y,jeu)
        self.lgx=lgx
        self.lgy=lgy
        self.dy1=dy1
        self.dy2=dy2
        if dy1=='': self.dy1=(self.x-int(self.x))*1000
        if dy2=='': self.dy2=(self.y-int(self.y))*1000
        #self.dy1=dy1+random.randint(0,10)
        #self.dy2=dy2+random.randint(0,10)
        #self.screen = pygame.display.set_mode(SIZE)
        self.imgtxt=pygame.image.load('./img/'+img)
        self.img = pygame.Surface((self.lgx,self.lgy), depth=32)  
        for x in range(0, self.lgx, self.imgtxt.get_width()):
            for y in range(0, self.lgy, self.imgtxt.get_height()):
                self.img.blit(self.imgtxt,(x,y))
        self.mask = pygame.Surface((self.lgx,self.lgy), depth=8)
        # Create sample mask:
        pygame.draw.polygon(self.mask, 255, [(x,y+self.dy1),(x,y+self.lgy),(x+self.lgx,y+self.lgy),(x+self.lgx,y+self.dy2)] , 0)
        self.img = self.img.convert_alpha()
        self.target = pygame.surfarray.pixels_alpha(self.img)
        self.target[:] = pygame.surfarray.array2d(self.mask)
        del self.target
    def affiche(self,xecran,x=0,y=0):
        surf.blit(self.img, (self.x-xecran, self.y))
    def interagit_interieur(self,jeu,e):
#        print("###1",self,e)
#        print(e.x, self.x, e.x+e.lgx,self.x+self.lgx , e.y,self.y , e.y+e.lgy,self.y+self.lgy)
        if e.x+e.lgx>=self.x and e.x<=self.x+self.lgx and e.y+e.lgy>=self.y and e.y<=self.y+self.lgy:  
                if e.type=='joueur': self.interagit_joueur(e,'dessous',jeu)
                if e.type=='mobile':
                    self.interagit_mobile(e,'dessous')
#                    print('###2')
    def interagit_joueur(self, joueur,cont,jeu):
        if cont=='dessus':
            joueur.forcey=self.y+self.lgy
            joueur.forcey_dir=-1
            joueur.vy=0
            if type(joueur)==Joueur:self.attaque()
        if cont=='dessous':
            mobX=joueur.x+joueur.lgx/2
            mobY=joueur.y+joueur.lgy
            solY=self.y+self.dy1+(mobX-self.x)*(self.dy2-self.dy1)/self.lgx
#            print('###3',mobile.x, self.x, mobY, solY) 
            if abs(mobY-solY)<8+abs(joueur.vy):
                joueur.forcey=solY-joueur.lgy
                joueur.vy=0
                joueur.forcey_dir=1
                joueur.surbloc=1
                if type(joueur)==Joueur and not joueur.entree.saute:
                    joueur.TempsImpulsionSaut=0
        if cont=='gauche':
            if joueur.y+joueur.lgy>self.y+self.dy2 and abs(self.x+self.lgx-joueur.x)<10:
                joueur.forcex=self.x+self.lgx
                joueur.forcex_dir=-1
        if cont=='droite':
            if joueur.y+joueur.lgy>self.y+self.dy1 and abs(self.x-joueur.x-joueur.lgx)<10:
                joueur.forcex=self.x-joueur.lgx
                joueur.forcex_dir=1
                

    def interagit_mobile(self,mobile,cont):
        mobile.surbloc=1
        f = 0.5 #frottements
        if cont=='dessus':
            #accélère ou ralentit le mobile qui descent ou qui monte
            #if dy1>dy2:
            if self.dy1!=self.dy2:
                mobile.y -= mobile.gravite/f
                mobile.x -=(mobile.gravite/f)*mobile.lgx/(self.dy1-self.dy2)

            mobile.forcey=self.y+self.lgy
            mobile.forcey_dir=-1
            mobile.vy=0
        if cont=='dessous':
            #accélère ou ralentit le mobile qui descent ou qui monte
            #if dy1>dy2:
            if self.dy1!=self.dy2:
                mobile.y -= mobile.gravite/f
                mobile.x -=(mobile.gravite/f)*mobile.lgx/(self.dy1-self.dy2)

            mobX=mobile.x+mobile.lgx/2
            mobY=mobile.y+mobile.lgy
            solY=self.y+self.dy1+(mobX-self.x)*(self.dy2-self.dy1)/self.lgx
            if abs(mobY-solY)<8:
                mobile.forcey=solY-mobile.lgy
                mobile.vy=0
                mobile.forcey_dir=1
                mobile.surbloc=1
        if cont=='gauche':
            if mobile.y+mobile.lgy>self.y+self.dy2 and abs(self.x+self.lgx-mobile.x)<10:
                mobile.forcex=self.x+self.lgx
                mobile.forcex_dir=-1
                mobile.vx=abs(mobile.vx)
        if cont=='droite':
            if mobile.y+mobile.lgy>self.y+self.dy1 and abs(self.x-mobile.x-mobile.lgx)<10:
                mobile.forcex=self.x-mobile.lgx
                mobile.forcex_dir=1
                mobile.vx=-abs(mobile.vx)
                
class Interrogation(Solide):
    [lgx,lgy]=[40,40]
    [diff, zone]=[0.1, 'commun']
    ausol = lgy + 100 #Joueur.lgy*2
    def __init__(self,x,y,jeu):
        Solide.__init__(self,x,y,jeu)
        self.utilise=0
        self.jeu = jeu
    def attaque(self):
        if self.utilise==0:
            Champignon(self.x+20, self.y-Champignon.lgy, self.jeu)
            self.utilise=1

InterrogationSava=type("InterrogationSava",(Interrogation,Vide),{"zone":'savane'})
InterrogationBermat=type("InterrogationBermat",(Interrogation,Vide),{"zone":'bermat'})

class Sol(Solide):
    [lgx,lgy]=[500,50]
    [diff, zone]=[0.3, 'mario']

#SolSava=type("SolSava",(Sol,Vide),{"zone":'savane'})
class SolSava(Sol): zone='savane'
SolBermat=type("SolBermat",(Sol,Vide),{"zone":'bermat'})
SolAqua=type("SolAqua",(Sol,Vide),{"zone":'aqua', 'lgx':500,'lgy':500})
SolMusic=type("SolMusic",(Sol,Vide),{"zone":'music','lgx':1200,'lgy':100})

class Tuyau(Solide):
    [lgx,lgy]=[100,160]
    [diff, zone]=[0.2, 'mario']

TuyauSava=type("TuyauSava",(Tuyau,Vide),{"zone":'savane'})
TroncBermat=type("TroncBermat",(Tuyau,Vide),{"zone":'bermat'})


class Brique(Solide):
    [lgx,lgy]=[40,40]
    [diff, zone]=[0.1, 'mario']
    def interagit_joueur(self, joueur,cont,jeu):
        if cont=='dessus':
            joueur.forcey=self.y+self.lgy
            joueur.forcey_dir=-1
            joueur.vy=0
            #~if type(joueur)==Joueur:self.attaque()
        if cont=='dessous':
            joueur.forcey=self.y-joueur.lgy
            joueur.vy=0
            joueur.forcey_dir=1
            #joueur.saute=0
            if type(joueur)==Joueur and not joueur.entree.saute:
                joueur.TempsImpulsionSaut=0
        if cont=='gauche':
            joueur.forcex=self.x+self.lgx
            joueur.forcex_dir=-1
        if cont=='droite':
            joueur.forcex=self.x-joueur.lgx
            joueur.forcex_dir=1
    def attaque(self):
        self.existe=0
#BriqueSava=type("BriqueSava",(Brique,Vide),{"zone":'savane'})
BriqueBermat=type("BriqueBermat",(Brique,Vide),{"zone":'bermat'})


class Shadow():
    img=pygame.transform.scale(pygame.image.load('./img/piece.jpg'), (3,3))
    def __init__(self,x,y,jeu):
        self.lgx=3
        self.lgy=3
        self.x=x
        self.y=y
    def bouge(self,x,y):
        self.x=x
        self.y=y   
        
class Glace(Solide):
    [lgx,lgy]=[100,50]
    [diff, zone]=[1, 'mario']
    def interagit_joueur(self, joueur,cont, jeu):
        Solide.interagit_joueur(self, joueur,cont, jeu)
        joueur.update_patinage()
        joueur.forcex=joueur.x+Joueur.vpatinage*joueur.patinage

class Decor(Item):
    [diff, zone]=[0, 'virtuel']
    plan="arriere"
    fond=False
    [lgx,lgy]=[lgx_ecran,lgy_ecran]
    profondeur = 2 #1: bouge en même temps que le reste; n: bouge n fois moins vite que le reste   privilégier des entiers supérieurs à 1 (sinon: DecorDevant) et surtout pas 0
    def __init__(self,x,y,jeu,lgx='',lgy='',profondeur=''):
        self.type='decor'
        if profondeur=='': profondeur=type(self).profondeur
        self.profondeur=profondeur
        if lgx=='':
            if type(self).fond: lgx=type(self).lgx
            else: lgx=int(type(self).lgx*math.sqrt(self.profondeur))
        if lgy=='':
            if type(self).fond: lgy=type(self).lgy
            else: lgy=int(type(self).lgy*math.sqrt(self.profondeur))
        self.xbase=x
        self.ybase=y
        self.lgx=lgx
        self.lgy=lgy
        Item.__init__(self,x,y,jeu)
        self.type='decor'
        self.plan="arriere"
        self.jeu=jeu
##        self.type="decor"
##        self.plan="arriere"
##    def bouge(self,jeu):
##        if type(jeu)!=JeuCarte: self.x=self.xbase+jeu.xecran*(1/self.profondeur)
    def affiche(self,xecran,yecran,x='',y=''):
        if x=='': x=self.x
        if y=='': y=self.y
        if type(self.jeu)!=JeuCarte: x=self.x+self.jeu.xecran- (self.jeu.xecran/self.profondeur)
        Item.affiche(self,xecran,yecran,x,y)
        
DecorSava=type("DecorSava",(Decor,Vide),{"zone":'savane',"fond":True})
DecorBermat=type("DecorBermat",(Decor,Vide),{"zone":'bermat',"fond":True})
DecorAqua=type("DecorAqua",(Decor,Vide),{"zone":'aqua',"fond":True,'lgx':int(5.9*lgy_ecran)})
DecorMusic=type("DecorMusic",(Decor,Vide),{"zone":'music',"fond":True})

Arbre=type("Arbre",(Decor,Vide),{"decor":True,"lgx":40,"lgy":80,"zone":'mario',"fond":False})
Coline=type("Coline",(Decor,Vide),{"decor":True,"lgx":300,"lgy":500,"zone":'mario',"fond":False})

class DecorDevant(Decor):
    [diff, zone]=[0, 'virtuel']
#                    ___
    profondeur=0.5 #|!=0|
#                    ¨¨¨
    [lgx,lgy]=[lgx_ecran,lgy_ecran]
    def __init__(self,x,y,jeu,lgx='',lgy='',profondeur=''):
        Decor.__init__(self,x,y,jeu)
        if lgx=='': lgx=DecorDevant.lgx
        if lgy=='': lgy=DecorDevant.lgy
        if profondeur=='': profondeur=DecorDevant.profondeur
        self.type="decor"
        self.plan="avant"
        self.xbase=x
        self.ybase=y
        self.lgx=lgx
        self.lgy=lgy
        self.profondeur=profondeur
    def bouge(self,jeu):
        self.x=self.xbase+jeu.xecran*(1/self.profondeur)
        

Flocon=type("Flocon",(DecorDevant,Vide),{"decor":True,"lgx":20,"lgy":20,"zone":'mario'})

class Neige(DecorDevant):
    [lgx,lgy]=[8,8]
    [diff, zone]=[0, 'mario']
    def __init__(self,x,y,jeu,lgx='',lgy='',profondeur=''):
        DecorDevant.__init__(self,x,y,jeu,lgx,lgy,profondeur)
        self.temps=0
        self.nb_flocon=20
        self.rand=120
        self.floconx=[10,110,220,330,440,550,660,770,430,250,240,670,720,880,930,810,120,230,450,560]
        self.flocony=[340,140,370,480,150,360,234,350,460,570,80,350,560,340,230,120,340,120,140,150]
        self.phase=[0,1,2,3,4,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
    def affiche(self, xecran,yecran,x=0,y=0):    
            self.temps+=1
##            if self.temps==30:
##                self.temps=0  
            if self.nb_flocon<100:
                if int(self.temps/40.)==self.temps/40.:
                    self.nb_flocon+=1
                    self.rand+=self.rand/10+(self.temps/100-int(self.temps/100))*50+(1000-self.rand)/5
                    while self.rand>1000:
                        self.rand-=1000
                    self.floconx.append(self.rand)
                    self.flocony.append(0)
                    self.phase.append((self.temps/100-int(self.temps/100))*10)
            for i in range(self.nb_flocon):
                self.flocony[i]+=0.2
                if self.flocony[i]>600:
                    self.flocony[i]-=600
                self.floconx[i]+=10*(math.sin(self.temps/48+self.phase[i])-math.sin((self.temps-1)/48+self.phase[i]))
                surf.blit(type(self).img[int(self.compteur)], (self.floconx[i],self.flocony[i]))

class Mobile(Item):
    resiste='tout' #nombre de contact avec le feu supportés avant de mourir
    inflige=0 #nombre de dégat infligé au feu par contact avec le feu(10avant de mourir)
    [diff, zone]=[0, 'virtuel']
    vy0=-12
    vy0base=-12
    def __init__(self,x,y,jeu):
        Item.__init__(self,x,y,jeu)
        self.vx=1
        self.vy=0
        self.forcex=-1 #donne x ou y imposé par un bloc
        self.forcey=-1
        self.forcex_dir=1 #donne la direction interdite par forcex
        self.forcey_dir=1
        self.estecrase=0
        self.type='mobile'
        self.demitour_auto=1
        self.surbloc=0
        self.gravite=1
    def bouge(self,jeu):
        if self.existe<1: self.supprime(jeu)
        if self.resiste==0: self.ecraser()
        if self.demitour_auto==1 and self.forcey!=-1: #fait demi tour au bord
            demitour=1
            jeu.shadow.bouge(self.x+self.lgx/2+math.copysign(self.lgx/2,self.vx),self.y+self.lgy)
            for d in jeu.items:
                if d.existe==1 and d.actif==1 and issubclass(type(d),Solide):
                    c=contact(d,jeu.shadow)
                    if c!='': demitour=0
                if type(d).__name__=='Colline':   
                    if self.x>d.x and self.x<d.x+d.lgx: 
                        demitour=0 
            if demitour==1: self.vx=-self.vx
        if self.forcex==-1 or signeoppose(self.forcex_dir, self.vx):
            self.x+=self.vx
        else:
            self.x=self.forcex
        self.forcex=-1
        if self.forcey==-1 or signeoppose(self.forcey_dir, self.vy):
            self.vy+=self.gravite
            self.y+=self.vy
        else:
            self.y=self.forcey
        self.forcey=-1
        if self.y>600:
            a=0
            if type(self)=='Joueur':
                print(self.entree, '  !')
                if self.entree.cheet:
                    self.existe=1
                    self.y=100
                    self.vy=0
                    self.x-=50
                    self.clignote=60
                    time.sleep(0.5)
                    print('c')
                    a=1
            if a==0:self.existe=0
        
    def interagit_joueur(self, joueur,cont, jeu):
        if type(self).interaction[cont] == 'perd' or (pygame.key.get_pressed()[K_c] and debug_mode==1) or joueur.entree.cheet:
            Points.pointsajoute(points,self.diff)
            self.ecraser()
 #           print('!!!!!')

        elif type(self).interaction[cont] == 'gagne':
            joueur.perd()
#            print('??????')
    def interagit_mobile(self, mobile,cont):pass#if ( cont=='droite' or cont=='gauche' ) and mobile.type!=feu: self.vx=-self.vx
    def ecraser(self):
        self.existe=0.5
        self.estecrase=30
    def impulsion_saut(self):
        self.vy=Mobile.vy0
        print(Mobile.vy0)
    def attaque(self):pass
        
class Joueur(Mobile):
    lgx=50
    lgy=50
    vx0=4
    vy0=-12
    vy0base=-12
    vpatinage=3
    TempsImpulsionMax=10
    def __init__(self,x,y,jeu, nj,etat=1):
        self.type='joueur'
        self.gravite=0.5
        self.soustype=str(nj)+'-'
        Mobile.__init__(self,x,y,jeu)
        self.nj=nj
        self.contact_glace=0
        self.entree=Inputs(nj)
        self.patinage=0
        self.impulsion_saut()
        self.type='joueur'
        self.demitour_auto=0
        self.TempsImpulsionSaut=0
        self.accel=0
        self.clignote=0
        self.lgx=Joueur.lgx
        self.lgy=Joueur.lgy
        self.etat=etat #1 petit, 2 grand
        self.img=[]
        try:
            for i in range(10):
                self.img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+self.soustype+str('%02d'%i)+'.jpg'), (self.lgx,self.lgy)).convert())
                self.img[i].set_colorkey(WHITE)
        except :
            try:
                for i in range(10):
                    self.img.append(pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+self.soustype+str('%02d'%i)+'.png'), (self.lgx,self.lgy)).convert())
                    self.img[i].set_colorkey(WHITE)
            except :
                pass
        
        self.imgsaut=pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+self.soustype+'saute'+'.png'), (self.lgx,self.lgy)).convert()
        self.imgsaut.set_colorkey(WHITE)
        self.imgsautgrand=pygame.transform.scale(self.imgsaut,(int(1.5*self.lgx),int(1.5*self.lgy)))
        self.img_petit=self.img
        self.img_grand=[]
        for i in range(len(self.img)):
            self.img_grand.append(pygame.transform.scale(self.img[i], (type(self).lgx,int(1.5*type(self).lgy))))
    def interagit_joueur(self, joueur,cont, jeu):pass  
    def update_patinage(self):
        if self.entree.direction >= 0:
            self.patinage=1
        else: self.patinage=-1
    
    def revient(self):pass
    def perd(self):
        if self.clignote<=0:
            self.clignote = 60
            if self.etat>1:
                self.rapetit()
            elif self.etat==1 and self.entree.cheet==0:
                self.etat=0
                self.existe=0
    def bouge(self,jeu):
        self.accel = 1
        if self.entree.accelere:
            self.accel *= 2
        if self.entree.court:
            self.accel *= 2
        if self.surbloc:
            if self.entree.marche or self.entree.court:
                self.vx = Joueur.vx0 * self.accel * self.entree.direction
            else:
                self.vx = 0
        
        if self.entree.saute and (self.TempsImpulsionSaut < Joueur.TempsImpulsionMax or self.entree.cheet==1):
            if jeu.zone!='aqua':self.TempsImpulsionSaut += 1
            self.vy = Joueur.vy0
            self.vx = Joueur.vx0 * 2 * self.entree.direction
            
        Mobile.bouge(self,jeu)
        
        if self.y > lgy_ecran:
            if self.entree.cheet:
                self.existe=1
                self.y=100
                self.vy=0
                self.x-=50
                self.clignote=60
                print('c')
            else: self.perd()
        if self.vy < -20: self.vy = -19
        if self.y<1: self.y=1
    def affiche(self,xecran,yecran):
        self.compteur+=0.3
        if self.compteur>=len(self.img) or not(self.entree.marche or self.entree.court):
            self.compteur=0
        
        if self.clignote==0:
            if self.vy==0:
                surf.blit(self.img[int(self.compteur)], (self.x-xecran, self.y-yecran))
            else:
                if self.etat==1: surf.blit(self.imgsaut, (self.x-xecran, self.y-yecran))
                else: surf.blit(self.imgsautgrand, (self.x-xecran, self.y-yecran))
        else:
            if self.clignote/10.-int(self.clignote/10.)>0.5:
               surf.blit(self.img[int(self.compteur)], (self.x-xecran, self.y-yecran))
            self.clignote-=1
           
    def grandit(self):
        if self.etat==1:
            self.lgy=1.5*Joueur.lgy
            self.y-=0.5*Joueur.lgy #0.5*Joueur.lgy sans marge
            self.img=self.img_grand
            self.etat=2
    def rapetit(self):
        if self.etat==2:
            self.lgy=Joueur.lgy
            self.y+=0.5*Joueur.lgy
            self.img=self.img_petit
            self.etat=1
        
class Goombas(Mobile):
    resiste=1
    inflige=1
    [lgx,lgy]=[56,40]
    [diff, zone]=[1, 'mario music']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    def __init__(self,x,y,jeu):
        Mobile.__init__(self,x,y,jeu)
        self.vx=0.8
    def bouge(self,jeu):
        Mobile.bouge(self,jeu)
        if self.existe==0: self.supprime(jeu)
        
class Goomies(Mobile):
    [lgx,lgy]=[40,40]
    [diff, zone]=[3, 'mario']
    interaction=dict(dessus='neutre',dessous='neutre',gauche='neutre',droite='neutre')
    def __init__(self,x,y,jeu):
        Mobile.__init__(self,x,y,jeu)
        self.goomies=[]
        for i in range(10):
            self.goomies.append(Goomy(x+random.randint(-20,20),y+random.randint(-20,20), jeu))
    def bouge(self,jeu):
        pass
    def affiche(self,xecran,yecran,x=0,y=0):
        pass
    def interagit_joueur(self, joueur,cont, jeu):
        pass
    def interagit_mobile(self, mobile,cont):
        pass  

class Goomy(Mobile):
    resiste=2
    inflige=0.5
    [lgx,lgy]=[15,15]
    [diff, zone]=[1, 'virtuel']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    def __init__(self,x,y,jeu):
        Mobile.__init__(self,x,y,jeu)
        self.vx=random.randint(-50,20)/10
        self.vy=random.randint(-50,-5)/3
        self.tsaut=0
        self.x0=x
        self.gravite=3
    def bouge(self,jeu):
        if self.resiste<=0: self.ecraser()
        if self.surbloc==1:
            self.tsaut+=1
            if abs(self.x-self.x0)>100:
                self.vx=-self.vx
            if self.tsaut>30:#150+random.randint(0,20):
                self.surbloc=0
                self.forcey=-1
                self.y-=5
                self.vy=random.randint(-50,-30)/3
                self.vx=random.randint(-50,50)/10
                self.tsaut=0
                self.vy-=self.gravite
        #Mobile.bouge(self,jeu)
        
        if self.demitour_auto==1 and self.forcey!=-1: #fait demi tour au bord
            demitour=1
            jeu.shadow.bouge(self.x+self.lgx/2+math.copysign(self.lgx/2,self.vx),self.y+self.lgy)
            for d in jeu.items:
                if d.existe==1 and d.actif==1 and d.type=='bloc':
                    c=contact(d,jeu.shadow)
                    if c!='': demitour=0
            if demitour==1: self.vx=-self.vx
        if self.forcex==-1 or signeoppose(self.forcex_dir, self.vx):
            self.x+=self.vx
        else:
            self.x=self.forcex
        self.forcex=-1
        if self.forcey==-1 or signeoppose(self.forcey_dir, self.vy):
            self.vy+=self.gravite
            self.y+=self.vy
        else:
            self.y=self.forcey
        self.forcey=-1


    def interagit_mobile(self, mobile,cont):
        if isinstance(mobile,Goomy):
            if self.surbloc==1 or mobile.surbloc==1:
                if cont=='dessus':
                    mobile.forcey=self.y+self.lgy
                if cont=='dessous':
                    mobile.forcey=self.y-mobile.lgy
                if cont=='gauche':
                    mobile.forcex=self.x+self.lgx
                    mobile.forcex_dir=-1
                if cont=='droite':
                    mobile.forcex=self.x-mobile.lgx
                    mobile.forcex_dir=1
                if cont=='gauche': mobile.vx=abs(mobile.vx)
                if cont=='droite': mobile.vx=-abs(mobile.vx)
            if self.vy==0 and cont=='dessus':
                mobile.forcey=self.y+self.lgy
                mobile.vy=0
                
class Tortue(Mobile):
    resiste=3
    inflige=3
    [lgx,lgy]=[40,40]
    [diff, zone]=[1, 'mario']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')

ChasseurSava=type("ChasseurSava",(Tortue,Vide),{"zone":'savane'})
ChatBermat=type("ChatBermat",(Tortue,Vide),{"zone":'bermat'})
class Poisson(Mobile):
    zone='virtuel'
    interaction=dict(dessus='gagne',dessous='gagne',gauche='gagne',droite='gagne')
    [lgx,lgy]=[125,50]
class Balene(Poisson):
    zone='aqua'
    resiste=2
    inflige=1000
    [lgx,lgy]=[125,50]
    [diff, zone]=[3, 'aqua']
    interaction=dict(dessus='gagne',dessous='gagne',gauche='gagne',droite='gagne')
    
Petitpoisson=type("Petitpoisson", (Poisson, Vide), {'lgx':55, 'lgy':40, "zone":"aqua"})
#Petitpoissonpics=type("Petitpoissonpics", (Poisson, Vide), {'lgx':70, 'lgy':70, "zone":"aqua"})
class Petitpoissonpics(Poisson):
    zone='aqua'
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    [lgx,lgy]=[90,99]
    def __init__(self,x,y,jeu):
        Poisson.__init__(self,x,y,jeu)
        self.pics=0
        self.temps=time.time()
        self.temps_aléatoire=random.randint(3,8)
    def bouge(self,jeu):
        Poisson.bouge(self, jeu)
        if self.temps_aléatoire<=time.time()-self.temps:
            if self.pics==0:
                self.pics=1
            else:
                self.pics=0
            self.temps_aléatoire=random.randint(3,8)
            self.temps=time.time()
        self.compteur=self.pics
    def interagit_joueur(self, joueur,cont, jeu):
        if self.pics:
            Poisson.interagit_joueur(self, joueur,"dessus", jeu)
        else:
            Poisson.interagit_joueur(self, joueur,cont, jeu)
Poisson1=type("Poisson1", (Poisson, Vide), {'lgx':80, 'lgy':60, "zone":"aqua"})

class Feu(Mobile):
    touche=0
    [lgx,lgy]=[35,35]
    [diff, zone]=[1.5, 'bermat']
    interaction=dict(dessus='gagne',dessous='gagne',gauche='gagne',droite='gagne')
    def __init__(self,x,y,jeu,vx=-5):
        Mobile.__init__(self,x,y,jeu)
        self.demitour_auto=0
        self.vx=vx
        self.lif=15
    def bouge(self,jeu):
        Mobile.bouge(self,jeu)
        if self.lif<=0: self.ecraser()

    def interagit_mobile(self,d,c):
        self.touche=0
        if self.vx>=0:
            if d.vx>=0 and self.x+self.lgx-(self.vx-d.vx)<d.x: self.touche=1
            elif d.vx<=0 and self.x+self.lgx-(self.vx+d.vx)<d.x: self.touche=1
        else:
            if d.vx>=0 and self.x-(self.vx-d.vx)<d.x+d.lgx: self.touche=1
            elif d.vx<=0 and self.x-(self.vx+d.vx)<d.x+d.lgx: self.touche=1

        if self.touche==1:
            if d.resiste!='tout':d.resiste-=1
            self.lif-=d.inflige

class Dragon(Mobile):
    inflige=5
    resiste=5
    [lgx,lgy]=[160,80]
    [diff, zone]=[3, 'mario bermat savane music']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    def __init__(self,x,y,jeu):
        Mobile.__init__(self,x,y,jeu)
        self.temps=time.time()
        self.vx=0.8
    def crache(self, jeu):
        print('crache')
        if(self.vx>0):
            Feu(self.x+Dragon.lgx+Feu.lgx, self.y+60,jeu,5)
        else:   
            Feu(self.x-Feu.lgx, self.y+60,jeu, -5)
        self.temps=time.time()
    def bouge(self,jeu):
        Mobile.bouge(self,jeu)
        self.lgx=2*Dragon.lgx
        if self.vx<0: self.x-=Dragon.lgx
        for i in jeu.items:
            if type(i) in ('Joueur', 'Mongolfier') and i.actif:
                if contact(self,i)!='': self.crache(jeu)
        self.lgx=Dragon.lgx
        if self.vx<0: self.x+=Dragon.lgx
        if (time.time()-self.temps)>4: self.crache(jeu)
    
##    def interagit_joueur(self, joueur,cont, jeu):
##        if self.vx>=0:
##            Dragon.interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='perd')
##        if self.vx<0:
##            Dragon.interaction=dict(dessus='gagne',dessous='perd',gauche='perd',droite='gagne')
##        Mobile.interagit_joueur(self, joueur,cont, jeu)

class CaptFeu(Mobile):
    mongolfier=0
    [diff, zone]=[0, 'virtuel']
    interaction=dict(dessus='neutre',dessous='neutre',gauche='neutre',droite='neutre')
    [lgx, lgy]=[45, 600]
    def __init__(self,x,y,jeu,mongolfier):
        self.mongolfier=mongolfier
        Mobile.__init__(self,x,y,jeu)
    def bouge(self, jeu):
        self.x=self.mongolfier.x
    def affiche(self,xecran,yecran,x=0,y=0): pass
    def interagit_joueur(self, joueur,cont, jeu): pass
    def interagit_mobile(self, d,c):
        if type(d).__name__=='Feu':self.mongolfier.envole()
##
class Mongolfier(Mobile):
    inflige=0
    resiste='tout'
    [lgx,lgy]=[45,80]
    [diff, zone]=[2, 'mario bermat savane']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    def __init__(self, x,y, jeu):
        Mobile.__init__(self,x,y,jeu)
        #self.capt=CaptFeu(self.x,0,jeu,self)
        self.gravite=0.45
        #self.jeu=jeu
    def bouge(self, jeu):
        if self.existe==0:
            self.capt.supprime(jeu)
            self.supprime(jeu)
        Mobile.bouge(self, jeu)
        y=self.y
        lgy=self.lgy
        self.y=0
        self.lgy=1000
        for i in jeu.items:
            if type(i).__name__=='Feu':
                if contact(self, i)!='': self.envole(jeu)
        self.y=y
        self.lgy=lgy
    def envole(self, jeu): #1:appelé par bouge ;; 0 appelé par interagit_mobile
##        if a==0: self.y0=self.y; self.monte=1
##        if self.y0-self.y>150: self.monte=-1
##        self.vy=(-(self.y0-self.y)+152)*self.monte
        if jeu.zone=='aqua': self.vy-=0.625
        else: self.vy-=2.5


##class Mongolfierbisterquater(Mobile):
##    inflige=0
##    resiste='tout'
##    [lgx,lgy]=[45,80]
##    [diff, zone]=[2, 'bermat']
##    interaction=dict(dessus='perd',dessous='gagne',gauche='gagne',droite='gagne')
##    def __init__(self, x,y):
##        Mobile.__init__(self,x,y,jeu)
##        self.gravite=0.45
##    def bouge(self, jeu):
##        Mobile.bouge(self, jeu)
##        capt=0
##        self.yalt=self.y
##        self.lgy=600
##        self.y=0
##        for d in jeu.items:
##            if contact(self,d)!='' and self.y<=d.y and type(d)=='Feu':
##                capt=100-d.y-self.y
##        self.lgy=80
##        self.y=self.yalt
##        print(capt)
##        self.vy+=capt

##class Pied(Brique):
##    [diff, zone]=[0.3, 'virtuel']
##    def interagit_mobile(self, joueur,cont): pass
##    def interagit_joueur(self, joueur,cont, jeu): pass
##
##
##class Blob(Mobile):
##    [lgx,lgy]=[40,40]
##    [diff, zone]=[1, 'mario']
##    def __init__(self,x,y,jeu):
##        Solide.__init__(self,x,y,jeu)
##        Mobile.__init__(self,x,y,jeu)
##        self.vy=-0.1
##        self.vx=0
##        self.conteur=0
##        self.lgy=40
##        self.pied=Pied(self.x,(self.y+40))
##        print('☺☻')
##    def bouge(self,jeu):
##        self.pied.y=self.y+40
##        if self.conteur: self.lgy=40; self.conteur=0
##        self.lgy+=0.1
##        self.y-=0.1
##       # self.y-=0.1
##        if self.lgy>=80:
##            self.conteur=1
##            Bblob(self.x,self.y+40)
##         #   print('==',self.x,self.y)
####            print(self.x,self.y)
####            self.y+=40#(self.lgy-Blob.lgy)
####            self.lgy=40#Blob.lgy
####            Blob(self.x,self.y-40)#Blob.lgy)
####        for d in jeu.items:
####            if contact(self,d)=='dessous' and d.type=='Mobile': d.y=self.y+d.lgy
##    def interagit_joueur(self, joueur,cont,jeu):
##        if cont=='dessus':
##            joueur.forcey=self.y+self.lgy
##            joueur.forcey_dir=-1
##            joueur.vy=0
##        if cont=='dessous':
##            joueur.forcey=self.y-joueur.lgy
##            joueur.vy=0
##            joueur.forcey_dir=1
##            #joueur.saute=0
##            if type(joueur)==Joueur and not joueur.entree.saute:
##                joueur.TempsImpulsionSaut=0
##        if cont=='gauche':
##            joueur.forcex=self.x+self.lgx
##            joueur.forcex_dir=-1
##        if cont=='droite':
##            joueur.forcex=self.x-joueur.lgx
##            joueur.forcex_dir=1
##    def interagit_mobile(self,mobile,cont):
##        if mobile.type!='Blob':
##            #self.interagit_joueur(mobile,cont, '')
##            mobile.surbloc=1
##    #        print("ça, c'est pour faire plaisir à Gregoire☺")
##            if cont=='dessus':
##                mobile.forcey=self.y+self.lgy
##                mobile.forcey_dir=-1
##                mobile.vy=0
##                #if type(mobile)==Joueur:self.attaque()
##     #           print("ça aussi, c'est pour faire plaisir à Gregoire☻")
##            if cont=='dessous':
##                mobile.forcey=self.y-mobile.lgy
##                mobile.vy=0
##                mobile.forcey_dir=1
##                mobile.surbloc=1
##                mobile.y=self.y+mobile.lgy
##     #           print("merci Timothée factorielle")
##                #mobile.saute=0
##                #if type(joueur)==Joueur and not joueur.entree.saute:
##                #    joueur.TempsImpulsionSaut=0
##            if cont=='gauche':
##                mobile.forcex=self.x+self.lgx
##                mobile.forcex_dir=-1
##            if cont=='droite':
##                mobile.forcex=self.x-mobile.lgx
##                mobile.forcex_dir=1
##            
##            if cont=='gauche': mobile.vx=abs(mobile.vx)
##            if cont=='droite': mobile.vx=-abs(mobile.vx)
####        else:
####            if cont=='dessous':
####                mobile.y=self.y+mobile.lgy
##class Bblob(Blob):
##    [diff, zone]=[2, 'virtuel']#'virtuel'
##    [lgx,lgy]=[40,40]
##    def __init__(self,x,y,jeu):
##        Solide.__init__(self,x,y,jeu)
##        Mobile.__init__(self,x,y,jeu)
##        self.vy=-0.1
##        self.vx=0
##        self.conteur=0
##        self.pied=Pied(self.x,(self.y+40))
##        print('gfhgfdx')
##    def interagit_mobile(self, d,c):
##        if (d.type=='Bblob' or d.type=='Blob') and c=='dessous':
##            d.y=self.y-d.lgy
##    def interagit_joueur(self, joueur,cont, jeu): pass

class Volcan(Bloc):
    [lgx,lgy]=[550,200]
    [diff, zone]=[3, 'mario']
    ausol=True
    def __init__(self,x,y,jeu):
        Bloc.__init__(self,x,y,jeu)
        self.cratere    = Cratere(x+250,y-200+self.lgy, jeu)
        self.cotegauche = Colline(x,    y-200+self.lgy, jeu, 200, 0,   250,200, "texture_volcan.jpg")
        self.cotedroite = Colline(x+300,y-200+self.lgy, jeu, 0,   200, 250,200, "texture_volcan.jpg")
        self.milieu     = Colline(x+250,y-180+self.lgy, jeu, 0,   0,   50, 180, "texture_volcan.jpg")
        #                        (x,    y,            , jeu,dy1,dy2,  lgx, lgy,  img)
        self.time=time.time()
        self.h=random.randint(5,15)
        self.compt=-1.5
        self.x0=self.x

    def vibre(self):
        self.cratere.x+=self.compt
        self.cotegauche.x+=self.compt
        self.cotedroite.x+=self.compt
        self.milieu.x+=self.compt
        self.compt=-self.compt

    def bouge(self,jeu):
        if time.time()-self.time>self.h or time.time()-self.time<0.5:
            self.vibre()
            if time.time()-self.time>self.h+2:
                self.cratere.crache(jeu)
##                print('azertyuioppppoiuytrezaaaazertyuioppppqsdfghjklmwxcvbnnbvcxw')
                h=random.randint(5,15)
                self.time=time.time()
                self.x=self.x0
    



class Cratere(Solide):
    inflige=-2
    [lgx,lgy]=[50,20]
    [diff, zone]=[3, 'virtuel']
   # mobiles=[Goombas, Tortue]
    def crache(self, jeu):
##        print('☺☺☻☻')
       # classe=getattr(random.choice(mobiles))
        #objet=classe(self.x, self.y+s.lgy)
        sea=random.choice(mobiles)
        if sea=='Mobloc':
            if random.randint(0, 100)!=0:
                sea=random.choice(mobiles)
                if sea=='Mobloc':
                    if random.randint(0, 100)!=0:
                        sea=random.choice(mobiles)
        print(sea)
        objet=eval(sea)(self.x+int(self.lgx/2)-eval(sea).lgx, self.y-eval(sea).lgy, jeu)
        objet.vy=-15
        if sea=='Goomy': objet.vy=-1
        objet.vx=-abs(objet.vx)
##        print(classe, objet)
##        classe=getattr(random.choice(mobiles))
##        objet=classe(self.x+self.lgx-s.lgx, self.y+s.lgy)
        sea=random.choice(mobiles)
        if sea=='Mobloc':
            if random.randint(0, 100)!=0:
                sea=random.choice(mobiles)
                if sea=='Mobloc':
                    if random.randint(0, 100)!=0:
                        sea=random.choice(mobiles)
      #  print(sea)
        objet=eval(sea)(self.x+int(self.lgx/2), self.y-eval(sea).lgy, jeu)
        objet.vy=-15
        if sea=='Goomy': objet.vy=-1
        objet.vx=abs(objet.vx)



class Bombe(Solide):
    [lgx,lgy]=[40,40]
    [diff, zone]=[1.5, 'mario']
    ausol = lgy
##    img=[pygame.transform.scale(pygame.image.load('./img/bombe.png'),(40,40))]
##    img_explose=[pygame.image.load('./img/onde_choc.png')]
    rayon_max=200
    colors=[RED, GREEN, BLUE]
    def __init__(self,x,y,jeu,color=''):
        Solide.__init__(self,x,y,jeu)
        self.rayon_actuel=0
        self.compt=3
        self.compteur=0
        if color=='': self.color=random.choice(Bombe.colors)
        else: self.color=color
        if self.color==RED: self.colornumber=1
        if self.color==GREEN: self.colornumber=2
        if self.color==BLUE: self.colornumber=3
        self.time=0
    def explose(self):
        self.rayon_actuel+=4
##        for rayon_actuel in range(Bombe.rayon_max):
##            Item.affichetout()
##            surf.blit(pygame.transform.scale(onde_de_choc,(2*rayon_actuel,2*rayon_actuel),(self.x+0.5*self.lgx-0.5*rayon_actuel,self.y+0.5*self.lgy-0.5*rayon_actuel)))
##            pygame.display.update()
##            for it in jeu.items:
##                if self.actif and self.type=='mobile' (it.x-self.x+self.lgx)**2+(it.y-self.y+0.5*self.lgy)**2<=rayon_actuel:
##                    it.supprime()
##    def affiche(self,xecran,x=0,y=0):
##        if self.compteur==0:
##            Item.affiche(self,xecran,x,y)
##        else:
##            surf.blit(pygame.transform.scale(type(self).img_explose[self.compteur],self.rayon_actuel,self.rayon_actuel),x_ecran,x-rayon_actuel+int(Bombe.lgx/2),y-rayon_actuel+int(Bombe.lgy/2))
    def bouge(self, jeu):
        if self.rayon_actuel!=0:
            self.compteur=self.colornumber
            self.compt=0
            self.rayon_actuel+=5
##            surf.blit(pygame.transform.scale(Bombe.img_explose,(2*self.rayon_actuel,2*self.rayon_actuel),(self.x+0.5*self.lgx-0.5*self.rayon_actuel,self.y+0.5*self.lgy-0.5*self.rayon_actuel))) #onde_de_choc
##            pygame.display.update()
            for it in jeu.items:   ##
                if math.sqrt((it.x-self.x+(self.lgx/2))**2+(it.y-self.y+0.5*self.lgy)**2)<=self.rayon_actuel:
                    if issubclass(type(it),Mobile):
                        if it.__class__.__name__.lower()=='joueur' and self.color==RED:
                            it.perd()
                        elif  it.__class__.__name__.lower()!='joueur' and self.color==GREEN:
                            it.supprime(jeu)
                    elif it.__class__.__name__.lower()=='bombe' and it!=self: #class 'ClassesBlocs13.Bombe'
                        it.explose()
                    elif it.__class__.__name__.lower()=='brique' and self.color==BLUE:
                        it.supprime(jeu)
            if self.rayon_actuel>=Bombe.rayon_max:
                self.supprime(jeu)
        elif self.time!=0:
            if time.time()-self.time>random.randint(100,200)/100: self.rayon_actuel+=1
            else:
                if self.compteur<1: self.compteur=1
        elif random.randint(1,300)==1:
            self.time=time.time()
        else:
            self.compteur=0            
        
    def affiche(self,xecran,yecran,x=0,y=0):
        if x==0: x=self.x
        if y==0: y=self.y
        if hasattr(self, 'vx'):
            if self.vx>=0:
                surf.blit(type(self).img[int(self.compteur)], (x-xecran, y-yecran))
            if self.vx<0:
                surf.blit(type(self).imgG[int(self.compteur)], (x-xecran, y-yecran))
        else:
            sys.stdout.write(str(self)+str(self.compteur)+"\n")
            surf.blit(type(self).img[int(self.compteur)], (x-xecran, y-yecran))
        self.compteur+=0.3
        if self.compteur>=len(type(self).img) and self.rayon_actuel==0:
            self.compteur=0
        if self.rayon_actuel!=0:
            pygame.draw.circle(surf, self.color,(self.x-xecran+(self.lgx/2),self.y+(self.lgy/2)-yecran), self.rayon_actuel, 5)
            pygame.draw.circle(surf, self.color,(self.x-xecran+(self.lgx/2),self.y+(self.lgy/2)-yecran), self.rayon_actuel-10, 5)
    def interagit_mobile(self, d,c):
        if type(d).__name__=='Feu':self.explose()

class Bombebleue(Bombe):
    diff=1
    def __init__(self,x,y,jeu):
        Bombe(x,y,jeu,BLUE)
        del(self)
class Bombeverte(Bombe):
    diff=-1
    def __init__(self,x,y,jeu):
        Bombe(x,y,jeu,GREEN)
        del(self)
class Bomberouge(Bombe):
    diff=2.5
    def __init__(self,x,y,jeu):
        Bombe(x,y,jeu,RED)
        del(self)



class Tortue_pics(Mobile):
    inflige=5
    resiste=6
    [lgx,lgy]=[80,40]
    [diff, zone]=[2, 'mario bermat savane music']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    def interagit_joueur(self, joueur,cont, jeu):
        if self.vx>=0:
            Tortue_pics.interaction=dict(dessus='gagne',dessous='gagne',gauche='perd',droite='gagne')
        if self.vx<0:
            Tortue_pics.interaction=dict(dessus='gagne',dessous='gagne',gauche='gagne',droite='perd')
        Mobile.interagit_joueur(self, joueur,cont, jeu)
        
class Dino(Mobile):
    inflige=4.5
    resiste=8
    [lgx,lgy]=[40,80]
    [diff, zone]=[1.5, 'savane']
    interaction=dict(dessus='gagne',dessous='perd',gauche='gagne',droite='gagne')
    def interagit_joueur(self, joueur,cont, jeu):
        if self.vx>=0:
            Dino.interaction=dict(dessus='gagne',dessous='gagne',gauche='gagne',droite='perd')
        if self.vx<0:
            Dino.interaction=dict(dessus='gagne',dessous='gagne',gauche='perd',droite='gagne')
        Mobile.interagit_joueur(self, joueur,cont, jeu)
        
class BouleChercheuse(Mobile):
    [lgx,lgy]=[30,30]
    [diff, zone]=[4, 'savane']
    interaction=dict(dessus='gagne',dessous='gagne',gauche='gagne',droite='gagne')
    v0=2.5
    def bouge(self,jeu):
        d=math.sqrt((self.x-CGjoueurs[0])**2+(self.y-CGjoueurs[1])**2)
        self.x+=BouleChercheuse.v0*(+CGjoueurs[0]-self.x)/d
        self.y+=BouleChercheuse.v0*(+CGjoueurs[1]-self.y)/d

class Boule(Mobile):
    [diff, zone]=[0, 'virtuel']
    v0=4
    def __init__(self,x,y,jeu,vx=3,vy=-3):
        Mobile.__init__(self,x,y,jeu)
        self.demitour_auto=0
        self.vx=vx
        self.vy=vy
    def interagit_joueur(self, joueur,cont, jeu):pass
    def bouge(self,jeu):
        if self.y>lgy_ecran-10: self.vy=-Boule.v0
        if self.y<10: self.vy=Boule.v0
        if self.x<jeu.xecran+10: self.vx=Boule.v0
        if self.x>jeu.xecran+lgx_ecran-10: self.vx=-Boule.v0
        for d in jeu.items:
            if d.existe==1 and d.actif==1 and d!=self and d.type!="decor":
                c=contact(d,self)
                if not issubclass(type(d),Piece):
                    if c=='dessous': self.vy=-Boule.v0
                    if c=='dessus': self.vy=Boule.v0
                    if c=='gauche': self.vx=Boule.v0
                    if c=='droite': self.vx=-Boule.v0
                if c!='':
                    self.interagit(d)
        self.x+=self.vx
        self.y+=self.vy

class BouleVerte(Boule): #attaque les mobiles
    [lgx,lgy]=[20,20]
    [diff, zone]=[-1, 'mario music']
    def interagit(self,d):
        if type(d)==Joueur: pass
        elif d.type=='mobile' and type(d)!=BouleVerte and type(d)!=BouleRouge and type(d)!=BouleBleue : d.ecraser()
        elif d.type=='bloc': pass
class BouleRouge(Boule): #attaque le joueur
    [lgx,lgy]=[20,20]
    [diff, zone]=[2.5, 'mario']
    def interagit(self,d):
        if type(d)==Joueur: d.perd()
        elif d.type=='mobile': pass
        elif d.type=='bloc': pass
class BouleBleue(Boule): #attaque les bloc
    [lgx,lgy]=[20,20]
    [diff, zone]=[1, 'mario']
    def interagit(self,d):
        if type(d)==Joueur: pass
        elif d.type=='mobile': pass
        elif type(d).__name__=='Brique': d.attaque()

##class Mobloc(Solide,Boule):
##    [lgx,lgy]=[90,60]
##    [diff, zone]=[5, 'savane']
##    ausol = lgy
##    def __init__(self, x,y,jeu):
##        Boule.__init__(self, x,y,jeu)
##        Solide.__init__(self, x,y,jeu)
##        self.H=0     # nb au hasard............ suspens :-) !
##        self.ax=0
##        self.ay=0
##        self.vya=0
##        self.vxa=0
##        for i in range(100):
##            if self.y>20: self.y-=1
##    def interagit_joueur(self,e,cont,jeu):
##        Solide.interagit_joueur(self,e,cont,jeu)
##        if cont=='dessous':
##            e.x=self.x
##            e.y=self.y-e.lgy
##            
##    def interagit_mobile(self,e,cont):
##        if cont=='dessous':
##            e.vx+=self.vx
##        Solide.interagit_mobile(self,e,cont)
##    
##    def bouge(self,jeu):
##        self.ax+=random.randint(-25,25)/30
##        self.ay+=random.randint(-25,25)/30
##        self.vx+=self.ax
##        self.vy+=self.ay
##        if signeoppose(self.vxa, self.vx):
##            if random.randint(0,25)<25: self.vx=self.vxa
####        if signeoppose(self.vya, self.vy):
####            self.vy=self.vya  ##if random.randint(0,25)<25: 
##        if abs(self.vx)+abs(self.vy)>1:
##            if random.randint(0,1)==1: self.vx=0.2*math.copysign(1,self.vx)
##        if self.y<500: self.vy=-1
####            self.H=random.randint(0,1)
####            if self.H==0:
####                if self.vy<0: self.vy+=0.5
####                if self.vy>0: self.vy-=0.5
####            else:
####                if self.vx<0: self.vy+=0.5
####                if self.vx>0: self.vy-=0.5
##
##            
####        if self.vy==0:
####            self.vy=random.randint(-1,1)
####            if self.vx>0:
####                self.vx=int(math.sqrt(self.vx**2-self.vy**2)) #car normeaucarre=self.vx**2
####            else:
####                self.vx=-int(math.sqrt(self.vx**2-self.vy**2))
####        else:
####            normeaucarre=self.vx**2+self.vy**2
####            self.vx+=random.randint(-1,1)
####            if self.vy>0:
####                self.vy=int(math.sqrt(normeaucarre-self.vx**2))
####            else:
####                self.vy=-int(math.sqrt(normeaucarre-self.vx**2))
##        if self.y>lgy_ecran-10: self.vy=-abs(self.vy)
##        if self.y<10: self.vy=abs(self.vy)
##        if self.x<jeu.xecran+10: self.vx=-self.vx
##        if self.x>jeu.xecran+lgx_ecran-10: self.vx=-self.vx
####        for d in jeu.items:
####            if d.existe==1 and d.actif==1:
####                c=contact(d,self)
####                if c=='dessous': self.vy=-self.vy
####                if c=='dessus': self.vy=-self.vy
####                if c=='gauche': self.vx=self.vx
####                if c=='droite': self.vx=-self.vx
##        self.x+=self.vx
##        self.y+=self.vy
##        self.vya=self.vy
##        self.vxa=self.vx

##class Aigle(Mobloc):
##    coef_dir=10
##    def __init__(self, x,y):
##        Mobloc.__init__(self,x,y,jeu)
##        self.pique=False
##    self.coef_dir=10
##    def bouge(self,jeu):
##        Mobloc.bouge(self,jeu)
##        if self.pique:
##            for joueur in jeu.joueurs:
##                if contact(self,joueur):
                    
                
class Champignon(Mobile):
    resiste=4
    inflige=7
    [lgx,lgy]=[40,40]
    [diff, zone]=[-1, 'mario']
    def __init__(self,x,y,jeu):
        Mobile.__init__(self,x,y,jeu)
        self.demitour_auto=0
    def interagit_joueur(self,d,cont, jeu):
        points.pointsajoute(1)
        if isinstance(d,Joueur):
            self.existe=0
            d.grandit()
class ChampignonSava    (Champignon):   zone="savane"
class ChampignonBermat  (Champignon):   zone='bermat'


class Barre(Mobile):
    [lgx,lgy]=[150,20]
    [diff, zone]=[1.5, 'mario']
    v0=2
    def __init__(self,x,y,jeu):
        Mobile.__init__(self,x,y,jeu)
        self.dx=300
        self.dy=200
        self.x0=x
        self.y0=y
        self.vx=0
        self.vy=0
    def bouge(self,jeu):
        if self.x-self.x0>self.dx:
            self.vx=-Barre.v0
        if self.x-self.x0<=0 and self.dx!=0:
            self.vx=Barre.v0
        self.x+=self.vx
        if self.y-self.y0>self.dy:
            self.vy=-Barre.v0
        if self.y-self.y0<=0 and self.dy!=0:
            self.vy=Barre.v0
        self.y+=self.vy     
    def interagit_mobile(self, mobile,cont):
        Solide.interagit_mobile(self,mobile,cont) #joueurs: pas impultion saut #Solide.interagit_joueur(self,mobile,cont, '') bug récurrences   !!!☺!!!   4041174212
        if cont=='dessous':
            mobile.x+=self.vx
            mobile.y+=self.vy
    def interagit_joueur(self, joueur,cont, jeu):
        self.interagit_mobile(joueur,cont)
        if not joueur.entree.saute:  # and cont=="dessus"
            joueur.TempsImpulsionSaut=0

##class Bombe(Solide):
##    def explose(self):
##        rayon_actuel=0
##        rayon_max=300
##    def bouge(self):
##        if random.randint(1,10)==0:
##            self.explose()


#####################################################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FIN NIVEAU ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##########################################################
############################################################################################################################################################################################
#####################################################~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CARTE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##########################################################



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
class Personnage(Solide): 
    mode='carte'
    [lgx,lgy]=[80,160]
    [x,y]=[0,0] #seulement utile pour creer scenario
    utilise=0
    def __init__(self,x,y, jeu,xcarte, ycarte,rencontre,satisfait):
        Bloc.__init__(self,x,y,jeu)
        self.xcarte=xcarte
        self.ycarte=ycarte
        self.utilise=0 #passe a 1 lorsqu'integre au scenario
        self.satisfait=satisfait #passe a 1 lorsque le critere d'entree est satisfait
        self.rencontre=rencontre #passe a 1 lorsqu'on le rencontre
        self.utilise=0
        self.texte=''
    def trouve(type_item,item, scenario):
        if type_item=='pers': t=1
        if type_item=='obj': t=2
        for j in range(len(scenario)):
            if scenario[j][3]==item and scenario[j][0]==t:
                print(('#trouve:: ok',j))
                return j
        print(('#trouve:: NOK',t,item,scenario))
        return 'erreur'
    def enregistre (self, jeu):
        f = open('./parties/'+str(jeu.partie)+"/niv_faits", 'rb')
        [self.niv_faits,etatpers,etatobj]=pickle.load(f, encoding='latin1')
        f.close()
        f=open('./parties/'+str(jeu.partie)+"/niv_faits", 'wb')
        etatpers[0][self.num]=self.rencontre
        etatpers[0][self.num]=self.satisfait
        pickle.dump([self.niv_faits,etatpers,etatobj],f)
        f.close()

    def affiche(self,xecran,yecran):
        Solide.affiche(self,xecran,yecran)
        if self.texte!='':
            self.cadretexte.affiche(self.texte,x=self.x+self.lgx-xecran, y=self.y-120+30-yecran)
        if not( xecran <= self.x <= xecran+1000 and yecran <= self.y <= yecran+600): self.texte='' #lgx_ecran, lgy_ecran
            
    def interagit_joueur(self, joueur,c, jeu):
        Solide.interagit_joueur(self,joueur, c, jeu)
        if jeu.joueurs[0].entree.entree:
            print('ok')
            texte_pers=''
            scenario=jeu.scenario
            s=trouve('pers',self.num,scenario) #!!!!!!!!!
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
                if jeu.obj[j].ramasse==1: #!!!!!!!!PersonnagesObjets
                    self.satisfait=1
                    texte_pers+='Tu as un '+jeu.obj[j].nom+' ! Je vais t\'aider. '
            if scenario[s][1]==2:
                j=scenario[s+1][3]
                print('pers=', pers, ' ; j=', j, ' ; s=', s, ' ; scenario=', scenario)
                if jeu.pers[j].rencontre==1: #!!!!!!!!PersonnagesObjets
                    self.satisfait=1
                    texte_pers+='Tu connais '+jeu.pers[j].nom+' ! Laisse moi t\'aider. '  #PersonnagesObjets
            #Execute la reaction
            if self.satisfait==0:
                if scenario[s][1]==1: 
                    texte_pers+='Avez-vous un '+jeu.obj[scenario[s+1][3]].nom+' ? '  #PersonnagesObjets
                if scenario[s][1]==2:
                    j=scenario[s+1][3]
                    texte_pers+='Connais tu '+jeu.pers[j].nom+' ? ' #PersonnagesObjets
            if self.satisfait==1:
                if scenario[s][2]==0:
                    texte_pers+='Nous avons tous espoir en toi; Courage! '
                if scenario[s][2]==1:
                    if s+2<=len(scenario)-1:
                        mot1=''
                        mot2=''
                        j=scenario[s+2][3] #prend un perso qui n'a pas de rapport avec lui
                        if j>=len(pers): texte_pers+='Tu es presque au bout de ta quete. Je ne peux plus t aider. Courage!'
                        else:
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
            print(texte_pers)
            self.texte=texte_pers
            self.cadretexte = CadreTexte(self.x+self.lgx-jeu.xecran, self.y-120+30-jeu.yecran, 250, 120)
            self.enregistre(jeu)
##            if texte_pers!='':
##                print("!!!!!!!")
##                cadretexte = CadreTexte(self.x+self.lgx-jeu.xecran, self.y-120+30-jeu.yecran, 250, 120)
##                cadretexte.affiche(texte_pers)
##                print("x:", self.x+self.lgx-jeu.xecran, " ; y:", self.y-120+30-jeu.yecran, " ; texte:", texte_pers)
##                pygame.display.update()
##                Item.affichetout(jeu,jeu.xecran, jeu.yecran)
##                attendtouchecarte()
        

Princesse=type("Princesse",(Personnage,Vide),{"nom":'Princesse',"hf":'f',"bonte":'1',"utilise":0})
Magicien=type("Magicien",(Personnage,Vide),{"nom":'Magicien',"hf":'h',"bonte":'0.8',"utilise":0})
Chevalier=type("Chevalier",(Personnage,Vide),{"nom":'Chevalier',"hf":'h',"bonte":'0.7',"utilise":0})

def attendtouchecarte():
    suite=0
    while suite==0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                suite=1
    time.sleep(0.1)

class Objet(Bloc):
    [lgx,lgy]=[40,40]
    utilise=0
    def __init__(self, x,y,jeu,xcarte, ycarte, ramasse):
        Bloc.__init__(self,x,y,jeu)
        self.xcarte=xcarte
        self.ycarte=ycarte
        self.ramasse=ramasse
        self.utilise=0
        self.texte=''
    def enregistre (self, jeu):
        f = open('./parties/'+str(jeu.partie)+"/niv_faits", 'rb')
        [self.niv_faits,etatpers,etatobj]=pickle.load(f, encoding='latin1')
        f.close()
        f=open('./parties/'+str(jeu.partie)+"/niv_faits", 'wb')
        etatobj[0][self.num]=self.ramasse
        pickle.dump([self.niv_faits,etatpers,etatobj],f)
        f.close()
    def affiche(self,xecran,yecran):
        Bloc.affiche(self,xecran,yecran)
        if self.texte!='':
            self.cadretexte.affiche(self.texte,x=self.x+self.lgx-xecran, y=self.y-120+30-yecran)
        if not( xecran <= self.x <= xecran+1000 and yecran <= self.y <= yecran+600): self.texte='' #lgx_ecran, lgy_ecran
    def interagit_entree(self, jeu):
        if self.ramasse==0:
            self.ramasse=1
            IncrementeScore([0,0,0,0],1000) 
            self.texte='+1000 points! Vous avez trouve un(e) ' + self.nom #!!!!!!!! cadre a afficher
            print(self.texte)
            son_objet_gagne.play()
            self.enregistre(jeu)
        self.cadretexte = CadreTexte(self.x+self.lgx-jeu.xecran, self.y-120+30-jeu.yecran, 250, 120)
    def interagit_joueur(self, joueur,c, jeu):
        Bloc.interagit_joueur(self, joueur,c, jeu)
        if jeu.joueurs[0].entree.entree: self.interagit_entree(jeu)
        print(self.num)
        


Grimoire=type("grimoire",(Objet,Vide),{"nom":'Grimoire'})
Cles=type("cles",(Objet,Vide),{"nom":'Cles'})
Corde=type("corde",(Objet,Vide),{"nom":'Corde'})
Parchemin=type("parchemin",(Objet,Vide),{"nom":'Parchemin'})
Moulin=type("moulin",(Objet,Vide),{"nom":'Moulin'})
Appat=type("appat",(Objet,Vide),{"nom":'Appat'})

class EntreeNiveau(Solide):
    [lgx,lgy]=[80,100]
    def __init__(self, x,y,jeu,direction):
        Bloc.__init__(self,x,y,jeu)
        self.direction=direction
    def interagit_joueur(self, joueur,c, jeu):
        Solide.interagit_joueur(self,joueur, c, jeu)
        if jeu.joueurs[0].entree.entree:
            jeu.continu=-1
            jeu.direction=self.direction
            
class PorteM(Solide):
    [lgx,lgy]=[80,100]
    def __init__(self, x,y,jeu, sortiex, sortiey,ramasse):
        Bloc.__init__(self,x,y,jeu)
        self.sortiex=sortiex
        self.sortiey=sortiey
        self.ramasse=ramasse #ne sert à rien sauf eviter un bug
        self.son=pygame.mixer.Sound("./sons/Teleport.mp3")
    def interagit_joueur(self, joueur, c, jeu):
        Solide.interagit_joueur(self,joueur, c, jeu)
        if jeu.joueurs[0].entree.entree:
            jeu.joueurs[0].x=self.sortiex+100
            jeu.joueurs[0].y=self.sortiey
            jeu.joueurs[0].forcex=-1
            jeu.joueurs[0].forcey=-1
            pygame.mixer.Sound.play(self.son)
            #print('### x:', int(self.sortiex/1000), '  y:', int(self.sortiey/600))
            jeu.valide_niveau(int(self.sortiex/1000), int(self.sortiey/600))
            jeu.majniveauxfaits(jeu.partie, [int(self.sortiex/1000), int(self.sortiey/600)])

class Porte(Solide):
    [lgx,lgy]=[80,100]
    def __init__(self, x,y,jeu,sortiex, sortiey,ramasse):  #self.obj.append(eval(obj2[i][0])(obj2[i][3],obj2[i][4],self, obj2[i][1],obj2[i][2],etatobj[0][i]))
        Bloc.__init__(self,x,y,jeu)
        self.ramasse=ramasse #ne sert à rien sauf eviter un bug
    def interagit_joueur(self, joueur, c, jeu):
        Solide.interagit_joueur(self,joueur, c, jeu)
        if jeu.joueurs[0].entree.entree:
            jeu.valide_carte()
            print('a')
            
def convertit(img):
    img=img.convert()
    img.set_colorkey(WHITE)
    return img

class DecorCarte(Decor):
    [lgx,lgy]=[50,100]
    type="decorcarte"
    plan="arriere"

decor_type=['arbre_normal','arbre_normal','arbre_normal2','arbre_fleur','arbre_palmier','arbre_palmier2','arbre_foret_sapins','arbre_sapin_neige','arbre_porte','arbre_bleuciel','arbre_rouge','arbre_rouge2']
d_arbre=80
for i in decor_type:
    if i!='':
        exec(i+"=type('"+i+"',(DecorCarte,Vide),{})")
#        print('cree classe',i,eval(i))

class BordCarteHor(Solide):
    [lgx,lgy]=[1000,80]

class BordCarteVert(Solide):
    [lgx,lgy]=[80,600]

class PontFermeHor(Solide): #Solide
    [lgx,lgy]=[1000,50] #80
    def interagit_joueur(self, joueur,cont,jeu):
        if debug_mode==0 or pygame.key.get_pressed()[K_c]==False: Solide.interagit_joueur(self, joueur,cont,jeu)
##        print("#pontH",self.x, self.y)

class PontFermeVert(Solide): #Solide
    [lgx,lgy]=[50,600] #80
    def interagit_joueur(self, joueur,cont,jeu):
        if debug_mode==0 or pygame.key.get_pressed()[K_c]==False: Solide.interagit_joueur(self, joueur,cont,jeu)
##        print("#pontV",self.x, self.y)

class PontHor(DecorCarte):
    [lgx,lgy]=[1000,50]
    type='decorcarte'

class PontVert(DecorCarte):
    [lgx,lgy]=[50,600]
    
class JeuCarte():
    def __init__(self,partie):
        self.partie = partie
        print('pers',pers)
        self.items=[]
        self.xecran=3000
        self.yecran=2*600
        self.continu=0 #0 continue, -1 pour recommencer, 1 pour jeu suivant
        self.direction=''
        self.pers=[]
        self.obj=[]
        self.charge_joueurs()
        self.charge_carte(partie)
        self.cadrecarte=CadreCarte(800,10,150,150)
        self.cadreobjets=CadreObjets(0,500,1000,100)
        
    def charge_carte(self,partie):
        #global partiebis, cote_carte, carte, scenario, obj, pers, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin
        global xcarte, ycarte, niv_debloque, direc_carte, niveau_precedent
        f = open('./parties/'+str(partie)+'/format', 'rb')
        form=pickle.load(f, encoding='latin1') 
        print(form)
        f.close()
        f = open('./parties/'+str(partie)+"/scenario", 'rb')
        [partiebis, cote_carte, carte, scenario, obj2, pers2, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin] = pickle.load(f, encoding='latin1')
        f.close()
        f = open('./parties/'+str(partie)+"/niv_faits", 'rb')
        [self.niv_faits,etatpers,etatobj]=pickle.load(f, encoding='latin1')
        f.close()
        #Transforme liste obj2 et pers2 en liste d objets obj et pers
        for i in range(len(pers2)):
            self.pers.append(eval(pers2[i][0])(pers2[i][3],pers2[i][4],self, pers2[i][1],pers2[i][2],etatpers[0][i],etatpers[1][i]))
            self.pers[len(pers)-1].num=i
        for i in range(len(obj2)):
            #print('######################')
            #print(etatobj)
            #print(etatobj[0])
            #print(eval(obj2[i][0]),obj2[i][3],obj2[i][4], obj2[i][1],obj2[i][2],etatobj[0][i])
            self.obj.append(eval(obj2[i][0])(obj2[i][3], obj2[i][4], self, obj2[i][1],obj2[i][2], etatobj[0][i]))
            #print(obj2[i][0],'#',obj2[i][3],obj2[i][4],obj2[i][1],obj2[i][2],etatobj[0][i])
            self.obj[len(obj)-1].num=i
                        
        niv_debloque=diff_fin
        self.scenario=scenario
##        print('########################################')
##        print(scenario)
##        print('self',self.scenario)
##        print(carte)
##        print(pers)
##        print(self.pers)
##        print('########################################')
        for s2 in range(0,len(scenario)):
            if scenario[s2][2]==2:
                niv_debloque=1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario))
                niv_debloque=max(carte[PersonnagesObjets.pers[scenario[s2][3]].x  ,  PersonnagesObjets.pers[scenario[s2][3]].y]*1.2  ,  1.2*(diff_debut+(diff_fin-diff_debut)*(s2+0.5)/len(scenario))) #PersonnagesObjets ?
                #print(('Vous avez debloque le niveau',niv_debloque))
                break
        #print('creee les decors...')
        #print(bloc_decor)
        for b in bloc_decor:
            a=eval(decor_type[int(b[2])])(b[0],b[1],self)

        self.ponts=[]
        for xa in range(cote_carte+1):
            self.ponts.append([])
            for ya in range(cote_carte+1):
                self.ponts[xa].append([])
        ###################qwerty######################################################################################################################################################################################################################
        for xa in range(1,1+cote_carte):
            for ya in range(1,1+cote_carte):
                self.ponts[xa][ya]=[]
                if xa>1:
                    EntreeNiveau(xa*1000+20,ya*600+250,self,[xa-1,ya])
                    if self.niv_faits[xa][ya] or explorecarte: self.ponts[xa][ya].append(PontVert(xa*1000,ya*600,self))
                    else: self.ponts[xa][ya].append(PontFermeVert(xa*1000,ya*600,self))
                else: BordCarteVert(xa*1000,ya*600,self)
                if xa<cote_carte:
                    EntreeNiveau(xa*1000+1000-120,ya*600+250,self,[xa+1,ya])
                    print(xa,ya,self.niv_faits[xa][ya])
                    if self.niv_faits[xa][ya] or explorecarte: self.ponts[xa][ya].append(PontVert((xa+1)*1000-50,ya*600,self))
                    else: self.ponts[xa][ya].append(PontFermeVert((xa+1)*1000-50,ya*600,self))
                else: BordCarteVert((xa+1)*1000-50,ya*600,self)
                if ya>1:
                    EntreeNiveau(xa*1000+460,ya*600+20,self,[xa,ya-1])
                    if self.niv_faits[xa][ya] or explorecarte: self.ponts[xa][ya].append(PontHor(xa*1000,ya*600,self))
                    else: self.ponts[xa][ya].append(PontFermeHor(xa*1000,ya*600,self))
                else: BordCarteHor(xa*1000,ya*600,self)
                if ya<cote_carte:
                    EntreeNiveau(xa*1000+460,ya*600+600-120,self,[xa,ya+1])                
                    if self.niv_faits[xa][ya] or explorecarte: self.ponts[xa][ya].append(PontHor(xa*1000,(ya+1)*600-50,self))
                    else: self.ponts[xa][ya].append(PontFermeHor(xa*1000,(ya+1)*600-50,self))
                else: BordCarteHor(xa*1000,(ya+1)*600-50,self)
        self.niv_faits[3][2]=1
        self.valide_niveau( 3,2)

    def charge_joueurs(self):
        global nb_joueurs
        self.joueurs=[JoueurCarte(100+3000,300+2*600,self, 0,1)]
        nb_joueurs=len(self.joueurs)
    def bouge_ecran(self):
        if self.joueurs[0].x-self.xecran>600:
            self.xecran+=self.joueurs[0].x-600-self.xecran
        if self.joueurs[0].x-self.xecran<400 and self.xecran>0:
            self.xecran-=400-self.joueurs[0].x+self.xecran
            
        if self.joueurs[0].y-self.yecran>350:
            self.yecran+=self.joueurs[0].y-350-self.yecran
        if self.joueurs[0].y-self.yecran<250 and self.yecran>0:
            self.yecran-=250-self.joueurs[0].y+self.yecran

    def valide_niveau(self,xa,ya):
        print('###p',self.ponts[xa][ya])
        for d in self.ponts[xa][ya]:
            print(d)
            try: self.items.remove(d)
            except: print('in valide_niveau(',self, ',', xa, ',', ya, '): ValueError: self.items.remove(d): ', d, ' not in list')
            #self.ponts.remove(d)
            del(d)
        if xa>1:
            self.ponts[xa][ya].append(PontVert(xa*1000,ya*600,self))
        if xa<cote_carte:
            self.ponts[xa][ya].append(PontVert((xa+1)*1000-50,ya*600,self))
        if ya>1:
            self.ponts[xa][ya].append(PontHor(xa*1000,ya*600,self))
        if ya<cote_carte:              
            self.ponts[xa][ya].append(PontHor(xa*1000,(ya+1)*600-50,self))

    def valide_carte(self, partie=''):
        if partie=='': partie=self.partie
        os.chdir(os.path.abspath(".")+"/parties/"+str(partie))
        f = open("carte_fait", 'rb')
        [a,precedent,b,c,d]=pickle.load(f)
        f.close()
        f = open("carte_fait", 'wb')
        pickle.dump([True,precedent,b,c,d], f)
        f.close()
        os.chdir(os.path.abspath(".."))
        os.chdir(os.path.abspath(".."))
        self.continu=-2

        
           
    def musique_niveau(self):
        
        #pygame.mixer.music.load("./sons/savane_musique.mp3")
        #pygame.mixer.music.play(-1,0)
        pass
    def musique_carte(self):
        pygame.mixer.music.load("./sons/Untitled2-8.mp3")
        pygame.mixer.music.play(-1,0)
    
    def majniveauxfaits(self, partie, d):
        [xcarte, ycarte]=d
        self.niv_faits[d[0]][d[1]]=1
        fini=0
        etatpers=[[],[]]
        etatobj=[[],[]]
        for i in range(len(self.pers)):
            etatpers[0].append(self.pers[i].rencontre)
            etatpers[1].append(self.pers[i].satisfait)
        for i in range(len(self.obj)):
            etatobj[0].append(self.obj[i].ramasse)                  
                    
        os.chdir(os.path.abspath(".")+"/parties/"+str(partie))
        f = open("niv_faits", 'wb')
        pickle.dump([self.niv_faits,etatpers,etatobj], f)
        f.close()

        os.chdir(os.path.abspath(".."))
        os.chdir(os.path.abspath(".."))
    
    def run(self):
        self.musique_niveau()
        self.musique_carte()
        self.continu=0
        while(self.continu==0):
            surf.fill(MARRON)
            self.bouge_ecran()
            Item.activetout(self)
            r=self.joueurs[0].entree.metajourCarte(self)
            if self.joueurs[0].entree.efface: self.continu=-1
            Item.bougetout(self)
            Item.interagittout(self)
            Item.affichetout(self,self.xecran, self.yecran)
            self.cadrecarte.affiche(self.niv_faits,int(self.joueurs[0].x/1000),int(self.joueurs[0].y/600))
            self.cadreobjets.affiche( obj)
            #self.cadrewiimote.affichebarre(200,10,20,50,4,1,2,self.J1.vy)
            #d Item.affiche(shadow, self.DISPLAYSURF,self.xecran)
            pygame.display.update()
            fpsClock.tick(FPS)
        return [self.continu,points.solde, self.direction]

class JoueurCarte(Mobile):
    lgx=89
    lgy=100
    v0=2
    def __init__(self,x,y, jeu, nj,etat):
        self.gravite=0
        Mobile.__init__(self,x,y,jeu)
        self.entree=Inputs(0)
        self.type='joueur'
        self.direction=3
        ilokImgD=pygame.transform.scale(pygame.image.load('./img/ilok_D.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgD.set_colorkey(WHITE)
        ilokImgG=pygame.transform.flip(ilokImgD,1,0)  #pygame.transform.scale(pygame.image.load('./img/Ilok_G.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgG.set_colorkey(WHITE)
        ilokImgB=pygame.transform.scale(pygame.image.load('./img/ilok_B.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgB.set_colorkey(WHITE)
        ilokImgH=pygame.transform.scale(pygame.image.load('./img/ilok_H.png'), (l_ilok_carte,h_ilok_carte)).convert()
        ilokImgH.set_colorkey(WHITE)
        self.img=[ilokImgD,ilokImgG, ilokImgH, ilokImgB]
    def interagit_joueur(self, joueur,cont, jeu):pass  
    def bouge(self,jeu):
        if self.entree.accelere:
            self.accel=10
        else:
            self.accel=2
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
        if self.entree.gauche:  self.direction=1
        elif self.entree.droite:self.direction=0
        elif self.entree.haut:  self.direction=2
        elif self.entree.bas:   self.direction=3
        surf.blit(self.img[self.direction], (self.x-xecran, self.y-yecran))


    
###################################################### FIN CARTE #################################################
##################################################################################################################
####################################################### COMMUN ###################################################
        
tolerance_contact=20
def contact(T1,T2):
    x1=T1.x
    y1=T1.y
    l1=T1.lgx
    h1=T1.lgy
    x2=T2.x
    y2=T2.y
    l2=T2.lgx
    h2=T2.lgy
    V1=0
    V2=0
    if type(T2)=='Joueur':
        V2=abs(self.vy)
    if hasattr(T2,'vy'):
        vy2=T2.vy
    else: vy2=0
    if vy2<tolerance_contact: vy2=tolerance_contact
    cont='' #1 est à ... de 2
    if x1+l1>=x2 and x1+l1<=x2+tolerance_contact and y1+h1>y2 and y1<y2+h2:
        cont='gauche'
    if x1<=x2+l2 and x1>=x2+l2-tolerance_contact and y1+h1>y2 and y1<y2+h2:
        cont='droite'
    if (x1+l1<=x2+l2 and x1+l1>=x2) or (x1<=x2+l2 and x1>=x2) or (x1<=x2 and x1+l1>=x2):
        if y1+h1>=y2 and y1+h1<=y2+tolerance_contact:
            cont='dessus' #1 au dessus de 2
        if y2+h2>=y1 and y2+h2<=y1+vy2:
            cont='dessous'
    return(cont)

def contact2(T1,T2):
    try:
        vx1=abs(T1.vx)
        vy1=abs(T1.vy)
    except:
        vx1=0
        vy1=0
    try:
        vx2=abs(T2.vx)
        vy2=abs(T2.vy)
    except:
        vx2=0
        vy2=0
    if vy2==0 and vy1==0: vy1=20

    x1=T1.x
    y1=T1.y
    l1=T1.lgx
    h1=T1.lgy
    x2=T2.x
    y2=T2.y
    l2=T2.lgx
    h2=T2.lgy
    V1=0
    V2=0
    if type(T2)=='Joueur':
        V2=abs(self.vy)
    cont='' #1 est à ... de 2
    if x1+l1>=x2 and x1+l1<=x2+tolerance_contact and y1+h1>y2 and y1<y2+h2:
        cont='gauche'
    if x1<=x2+l2 and x1>=x2+l2-tolerance_contact and y1+h1>y2 and y1<y2+h2:
        cont='droite'
    if (x1+l1<=x2+l2 and x1+l1>=x2) or (x1<=x2+l2 and x1>=x2) or (x1<=x2 and x1+l1>=x2):
        if y1+h1>=y2 and y1+h1<=y2+vy1+vy2:
            cont='dessus' #1 au dessus de 2
        if y2+h2>=y1 and y2+h2<=y1+vy1+vy2:
            cont='dessous'
    return(cont)


def contact3(T1,T2):
    try:
        vx1=abs(T1.vx)
        vy1=abs(T1.vy)
    except:
        vx1=0
        vy1=0
    try:
        vx2=abs(T2.vx)
        vy2=abs(T2.vy)
    except:
        vx2=0
        vy2=0
    x1=T1.x
    y1=T1.y
    l1=T1.lgx
    h1=T1.lgy
    x2=T2.x
    y2=T2.y
    l2=T2.lgx
    h2=T2.lgy
    V1=0
    V2=0
    if type(T2)=='Joueur':
        V2=abs(self.vy)
    cont='' #1 est à ... de 2
    if x1+l1>=x2 and x1+l1<=x2+tolerance_contact and y1+h1>y2 and y1<y2+h2:
        cont='gauche'
    if x1<=x2+l2 and x1>=x2+l2-tolerance_contact and y1+h1>y2 and y1<y2+h2:
        cont='droite'
    if (x1+l1<=x2+l2 and x1+l1>=x2) or (x1<=x2+l2 and x1>=x2) or (x1<=x2 and x1+l1>=x2):
        if y1+h1>=y2 and y1+h1<=y2+vy1+vy2:
            cont='dessus' #1 au dessus de 2
        if y2+h2>=y1 and y2+h2<=y1+vy1+vy2:
            cont='dessous'
    return(cont)

def supprime(self,jeu):
    jeu.items.remove(self)
    del(self)

def signeoppose(a,b):
    if math.copysign(1,a)!=math.copysign(1,b):
        return True
    else:
        return False


class Inputs():
    touche_demi_tour = [eval(f'K_{i}') for i in range(1,10)] # le joueur i fait demi-tour avec la touche i
    touche_demi_tour2= [eval(f'K_KP{i}') for i in range(1,10)] # touches du pavé numérique
    
    def __init__(self,nj):
        assert nj < len(Inputs.touche_demi_tour), "Trop de joueurs. Il faut definir d'autres touches de demi-tour."   #nj > len... ?
        self.nj=nj
        [self.saute, self.court, self.marche, self.accelere]=[False, False, False, False]
        self.direction = 1 #+1 si regarde a droite (meme si n'avance pas), -1 si regarde à gauche (meme si n'avance pas), 0 si en position repos (valeur optionnelle)
        self.last_demi_tour = 0 #date du dernier demi-tour en secondes (pour eviter les repetitions quand la touche demitour reste enfoncee)
        self.cheet=0 #super debug_mode activé seulement avec le raccourci: Ctrl+Alt+Maj+I+L+O+K
        
    def metajour(self,jeu):
        pygame.event.get()
        keys=pygame.key.get_pressed()
        #print('(',keys[K_RCTRL] ,'or', keys[K_LCTRL],'and (',keys[K_RALT] ,'or', keys[K_LALT],') and (',keys[K_RSHIFT] ,'or', keys[K_LSHIFT],') and', keys[K_i]  ,'and', keys[K_l] ,'and', keys[K_o] ,'and', keys[K_k])
        if (keys[K_RCTRL] or keys[K_LCTRL]) and (keys[K_RALT] or keys[K_LALT]) and (keys[K_RSHIFT] or keys[K_LSHIFT]) and keys[K_i]  and keys[K_l]:# and keys[K_o] and keys[K_k]:
            self.cheet=1
            print('幹得好，你已經解鎖了蒂莫西·科利爾  在2024年程式設計的伊洛克家族的獵豹模式')
        self.marche = False
        
        if phone_mode: #idee: ajouter un mode test_phone_mode = faire marcher et sauter avec le clavier sans connecter de telephone
            [self.saute, self.court, self.marche, self.accelere]=[False, False, False, False]
            if senstream.intnegpos[self.nj+1]>60+100*senstream.sensitivity[self.nj+1]: #100 calib 312
                self.saute=True
            elif senstream.intnegpos[self.nj+1]>12+15*senstream.sensitivity[self.nj+1]: #23 calib 50 
                self.court=True
            elif senstream.intnegpos[self.nj+1]>4+3*senstream.sensitivity[self.nj+1]  : #7 calib 16  and wiisport_court[self.nj]==0
                self.marche=True

        if (keys[Inputs.touche_demi_tour[self.nj]] or keys[Inputs.touche_demi_tour2[self.nj]])and time.time() - self.last_demi_tour > 0.25:
                print('☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺☺')#,self.gauche,self.droite)
                self.direction *= -1
                self.last_demi_tour = time.time()

        if not phone_mode or self.cheet:
            
            if keys[K_RIGHT] :
                self.marche = True
                self.direction = 1
            if keys[K_LEFT]:
                self.marche = True
                self.direction = -1
            
            self.saute=keys[K_w]
            self.accelere=keys[K_x]
            
        self.map=keys[K_u]
        self.retry=keys[K_r]
        self.recup=True #keys[K_p]

        if self.recup:
            x=0
            n=0
            j=0
            for d in jeu.items:
                if d.type=='joueur':
                    if d.existe>0:
                        x+=d.x
                        n+=1
                    elif d.existe==0:
                       j=d
            if (points.solde>2 or self.cheet) and j!=0 and n>0:
                j.existe=1
                j.y=100
                j.vy=0
                j.x=int(x/n)
                j.clignote=60
                points.diviserpar(1.2)
                time.sleep(0.5)
        if self.retry:
            return 'Retry'
        elif self.map:
            return 'Map'
        else:
            return None
    
    def metajourCarte(self,jeu):
        pygame.event.get()
        keys=pygame.key.get_pressed()
        self.droite=keys[K_RIGHT]
        self.gauche=keys[K_LEFT]
        self.bas=keys[K_DOWN]
        self.haut=keys[K_UP]
        self.entree=keys[K_RETURN]
        if self.entree:
            print('self.entree')
        self.efface=keys[K_DELETE]
        self.accelere=keys[K_x]
        
class Jeu():
    def __init__(self,partie,direct_carte, pick=0):
        self.shadow=Shadow(0,0,self)
        self.items=[]
        self.zone=''
        self.charge_joueurs()
        self.charge_jeu(partie,direct_carte, pick)
        self.xecran=0
        self.yecran=0
        self.continu=0 #0 continue, -1 pour recommencer, 1 pour jeu suivant
        self.cadrecarte=CadreCarte(800,10,150,150)
        self.cadrepoints=CadrePoints(200,10,50,30)
        self.cadretemps=CadrePoints(300,10,50,30)
        self.cadrewiimote=CadreWiimote(200,50,100,50,GREY)
        points.soldenul()
        print('pers2',pers)
    def charge_jeu(self, partie,direct_carte, pick=0):
        self.partie=partie
        self.cadreaides=[]
        self.cadreaidex=700
        if partie==-2: #partie fournie (cree a la volee)
            try:
                if type(pick[len(pick)-1])==str: raise ValueError('')
                [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre, zone, a]=pick
                ok=1
            except:
                [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, zone]=pick
                ok=0
            if zone=='aqua':
                Mobile.vy0=Mobile.vy0base/4
                Joueur.vy0=Joueur.vy0base/3
            #print(bloc_type)
            for i in range(nb_perso):
                t=''
                if ok:
                    if perso_autre[i] not in ['',[]]:
                        for j in perso_autre[i]:
                            t+=','+j[0]+'='+str(j[1])
                a=eval(perso_type[i]+"(persox[i],persoy[i],self"+t+")")
                
            for i in range(nb_bloc):
                t=''
                if ok:
                    if bloc_autre[i] not in ['',[]]:
                        for j in bloc_autre[i]:
                            t+=','+j[0]+'='+str(j[1])
                a=eval(bloc_type[i]+"(blocx[i],blocy[i],self"+t+")")
                #a=eval(bloc_type[i])(blocx[i],blocy[i],self)
                #print(a,bloc_type[i],blocx[i],blocy[i],sep=',')
            if ok:
                for i in range(len(decor_type)):
                    t=''
                    if decor_autre[i] not in ['',[]]:
                        for j in decor_autre[i]:
                            t+=','+j[0]+'='+str(j[1])
                    a=eval(decor_type[i]+"(decorx[i],decory[i],self, profondeur=decor_profondeur[i]"+t+")")
                    #a=eval(decor_type[i])(decorx[i],decory[i],self, profondeur=decor_profondeur[i])
            self.zone=zone
        elif partie!=-1: # partie a charger sur le disque
            nom_fichier='./parties/'+ str(partie)+'/niv ' + str(direct_carte)
            f = open(nom_fichier, 'rb')
            pick=pickle.load(f, encoding='latin1')
            try:
                [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,perso_autre,nb_bloc,blocx,blocy,exisbloc,bloc_type,bloc_autre, nb_decor,decorx, decory, decor_type,decor_profondeur,decor_autre, zone, a]=pick
                ok=1
            except:
                [nb_perso,persox,persoy,direcGo,exisgo,ecrase,perso_type,nb_bloc,blocx,blocy,exisbloc,bloc_type, zone]=pick
                ok=0

            #sens=[1]*nb_bloc
            f.close()
            f = open('./parties/'+ str(partie)+'/carte_fait', 'rb')
            #print(f)
            #print(pickle.load(f, encoding='latin1'))
            [a,precedent,mobilesrencontres,d,e]=pickle.load(f, encoding='latin1')
            if mobilesrencontres==0: mobilesrencontres=[]
            f.close()
            mobilesrencontres=[]#!!§§!!§§??,,??,,
            if precedent!='':
                f = open('./parties/'+ str(precedent)+'/carte_fait', 'rb')
                [a2,precedent2,mobilesrencontresprecedent,d2,e2]=pickle.load(f, encoding='latin1')
                f.close()
                if mobilesrencontresprecedent==0: mobilesrencontresprecedent=[]
                else:
                    for i in mobilesrencontresprecedent:
                        if i not in mobilesrencontres:
                            mobilesrencontres.append(i)
                    f = open('./parties/'+ str(partie)+'/carte_fait', 'wb')
                    pickle.dump([a,precedent,mobilesrencontres,d,e],f)
                    f.close()
                    
            for i in range(nb_perso):
                t=''
                if ok:
                    if perso_autre[i] not in ['',[]]:
                        for j in perso_autre[i]:
                            t+=','+j[0]+'='+str(j[1])
                a=eval(perso_type[i]+"(persox[i],persoy[i],self"+t+")")
##                if perso_type[i] not in mobilesrencontres:
##                    self.cadreaides.append([a.x,a.texte,'',type(a).__name__,0])
##                    mobilesrencontres.append(perso_type[i])
            for i in range(nb_bloc):
                t=''
                if ok:
                    if bloc_autre[i] not in ['',[]]:
                        for j in bloc_autre[i]:
                            t+=','+j[0]+'='+str(j[1])
                a=eval(bloc_type[i]+"(blocx[i],blocy[i],self"+t+")")
##                if bloc_type[i] not in mobilesrencontres:
##                    self.cadreaides.append([a.x,a.texte,'',type(a).__name__,0])
##                    mobilesrencontres.append(bloc_type[i])
            if ok: 
                for i in range(len(decor_type)):
                    t=''
                    if decor_autre[i] not in ['',[]]:
                        for j in decor_autre[i]:
                            t+=','+j[0]+'='+str(j[1])
                    a=eval(decor_type[i]+"(decorx[i],decory[i],self, profondeur=decor_profondeur[i]"+t+")")
            self.zone=zone
        else:
            pass
        if self.zone=='aqua':
            for i in self.items:
                if hasattr(i,'gravite'):i.gravite=i.gravite/4
            
    def charge_joueurs(self):
        global nb_joueurs
        if phone_mode:
            self.joueurs=[]
            for i in range(senstream.nbj):
                self.joueurs.append(Joueur(100+i*40,300,self,i,1))
        else:
            self.joueurs=[Joueur(100,300,self,0,1)] #,Joueur(150,300,self,1,1),Joueur(200,300,self,2,1)]
        nb_joueurs=len(self.joueurs)
    def bouge_ecran(self):
##        print(self.joueurs)
##        joueurs_en_vie=self.joueurs
##        for j in joueurs_en_vie:
##            if not j.existe:
##                joueurs_en_vie.remove(j)
##        xmax=max(i.x for i in joueurs_en_vie) ##d
##        xmin=min(i.x for i in joueurs_en_vie)
##        print(self.joueurs)
#        xmax=max([self.joueurs[0].x]) ##d
        xmax=max(i.x for i in self.joueurs) ##d
        xmin=min(i.x for i in self.joueurs)
        if xmin-self.xecran<200 and self.xecran>0:
            self.xecran-=200-xmin+self.xecran
        if xmax-self.xecran>600:
            self.xecran=xmax-600
            for i in self.joueurs:
                if i.x<self.xecran:
                    i.x=self.xecran
                    #print('i', i.forcex, i.forcex_dir, sep='  |  ')
                    if i.forcex-i.lgx<self.xecran and i.forcex_dir==1:
                        i.perd()
                        #print('a')
##            for i in range(len(self.cadreaides)):
##                if self.cadreaides[i][0]<self.xecran+600:
##                    if self.cadreaides[i][1]!='' and (self.cadreaidex>=0 or self.cadreaides[i][2]!=''):
##                        if self.cadreaides[i][2]=='':
##                            self.cadreaides[i][2]=CadreAide(self.cadreaidex,0,250,100)
##                            self.cadreaides[i][4]=self.cadreaidex
##                            self.cadreaidex-=255
##                        self.cadreaides[i][2].affiche(self.cadreaides[i][1])
            
##        for i in range(len(self.cadreaides)):
##            if self.cadreaides[i][2]!='' and (self.cadreaides[i][0]<self.xecran or self.cadreaides[i][0]>self.xecran+800):
##                f = open('./parties/'+ str(self.partie)+'/carte_fait', 'rb')
##                [a,b,mobilesrencontres,d,e]=pickle.load(f, encoding='latin1')
##                f.close()
##                mobilesrencontres.append(self.cadreaides[i][3])
##                f = open('./parties/'+ str(self.partie)+'/carte_fait', 'wb')
##                pickle.dump([a,b,mobilesrencontres,d,e],f)
##                f.close()
##                #print(mobilesrencontres)
##                self.cadreaidex=max(self.cadreaides[i][4],self.cadreaidex)
##                #print(self.cadreaidex)
##                del(self.cadreaides[i])
##                break
        #please wait azertyuiopqsdfghjklmwxcvbnaqwzsxedcrfvtgbyhnujikolpmnbvcxwmlkjhgfdsqpoiuytrezapmolikuyhntgbrfvedczsxaqwwqaxszcdevfrbgtnhyjukilompmplokijunhybgtvfrcdexszwqa

    def musique_niveau(self):
       # zone=input("zone?")
        print(self.zone,'B')
        if self.zone=='savane':
            pygame.mixer.music.load("./sons/savane_musique.mp3")
        elif self.zone=='bermat':
            pygame.mixer.music.load("./sons/schtroumpfs.mp3")
        elif self.zone=='aqua':
            pygame.mixer.music.load("./sons/piano-ilok.mp3")  #oe5xe3b9bs8c2g7x3f
        elif self.zone=='music':
            pygame.mixer.music.load("./sons/Happy_Birthday.mp3")
        else:
            pygame.mixer.music.load("./sons/piano-ilok.mp3")
        pygame.mixer.music.play(-1,0)
    def run(self):
        self.musique_niveau()
        tps=time.time()
        while(self.continu==0):
            surf.fill(WHITE)
            self.bouge_ecran()
            Item.activetout(self)
            r=Item.saisittout(self)
            self.cadretemps.affiche(int(tps-time.time()+120))
            if 120-time.time()+tps<1:
                CadrePoints(300,10,125,30).affiche("Temps écoulé")
                #time.sleep(1)
                #self.continu=-1
            if r=='Retry': self.continu=-1
            if r=='Map': self.continu=-2
            if pygame.key.get_pressed()[K_f] and debug_mode==1: self.continu=1
            Item.bougetout(self)
            Item.interagittout(self)
            Item.affichetout(self,self.xecran,self.yecran)
            self.cadrepoints.affiche(points.solde)
##            for i in self.cadreaides:
##                if i[2]!='':
##                    i[2].affiche(i[1])
            #self.cadrewiimote.affichebarre(200,10,20,50,4,1,2,self.J1.vy)
            #d Item.affiche(shadow, self.DISPLAYSURF,self.xecran)
            pygame.display.update()
            fpsClock.tick(FPS)
        for i in self.items:
            del i
        self.items=[]
        return [self.continu,points.solde]


