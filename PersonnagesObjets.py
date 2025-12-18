import pygame,os
from var import *

##try:
##    print(pygame.transform.scale(pygame.image.load('./img/princesse.jpg'),(50,100)))
##except:
##    os.chdir(os.path.abspath('..'))
passages_secrets=[]
class PassageSecret():
    def __init__(self, x0,y0,x_fin, y_fin,debloque=True, img=pygame.image.load('./img/princesse.jpg')):
        self.x0,self.y0,self.x_fin, self.y_fin,self.debloque, self.img=x0,y0,x_fin, y_fin, img
        passages_secrets.append(self)
class Personnage():
    compt=0
    def __init__(self,nom, hf, bonte):
        self.nom=nom
        self.hf=hf
        self.bonte=bonte
        self.utilise=0 #passe a 1 lorsqu'integre au scenario
        self.satisfait=0 #passe a 1 lorsque le critere d'entree est satisfait
        self.rencontre=0 #passe a 1 lorsqu'on le rencontre
        self.x=-1
        self.y=-1
        Personnage.compt+=1
        if Personnage.compt>2:
            Personnage.compt=0
        if Personnage.compt==1:
            self.img=pygame.transform.scale(pygame.image.load('./img/princesse.jpg'),(50,100)) #self.nom+'.jpg'), (40,40))
##
##            try:
##                self.img=pygame.transform.scale(pygame.image.load('./img/princesse.jpg'),(50,100)) #self.nom+'.jpg'), (40,40))
##            except:
##                self.img=pygame.transform.scale(pygame.image.load('../img/princesse.jpg'),(50,100))
        if Personnage.compt==2:
            pass
            self.img=pygame.transform.scale(pygame.image.load('./img/Magicien.jpg'),(70,100)) #self.nom+'.jpg'), (40,40))
##            try:
##                self.img=pygame.transform.scale(pygame.image.load('./img/Magicien.jpg'),(70,100)) #self.nom+'.jpg'), (40,40))
##            except:
##                self.img=pygame.transform.scale(pygame.image.load('../img/Magicien.jpg'),(70,100))
            #self.img=pygame.transform.scale(pygame.image.load('./img/Magicien.jpg'),(70,100)) #self.nom+'.jpg'), (40,40))
        if Personnage.compt==0:
            self.img=pygame.transform.scale(pygame.image.load('./img/Chevalier.jpg'),(50,100))
##            try:
##                self.img=pygame.transform.scale(pygame.image.load('./img/Chevalier.jpg'),(50,100)) #self.nom+'.jpg'), (40,40))
##            except:
##                self.img=pygame.transform.scale(pygame.image.load('../img/Chevalier.jpg'),(50,100))
            #self.img=pygame.transform.scale(pygame.image.load('./img/Chevalier.jpg'),(50,100)) #self.nom+'.jpg'), (40,40))
        self.img=convertit(self.img)

class Objet():
    def __init__(self, nom):
        self.nom=nom
        self.ramasse=0
        self.utilise=0
        self.x=-1
        self.y=-1
        self.img=pygame.transform.scale(pygame.image.load('./img/'+self.nom+'.jpg'),(40,40)) #self.nom+'.jpg'), (40,40))
        self.img=convertit(self.img)
        
def convertit(img):
    img=img.convert()
    img.set_colorkey(WHITE)
    return img

pers=[]
pers.append(Personnage('Roumir','h',1))
pers.append(Personnage('Bachir','h',0))
pers.append(Personnage('Yellet','f',0.3))
pers.append(Personnage('Kzamara','h',0.5))
pers.append(Personnage('Oyea','f',1))
pers.append(Personnage('Ulud','h',1))
pers.append(Personnage('Latram','f',1))
pers.append(Personnage('Froyx','h',1))
pers.append(Personnage('Madrij','f',1))
pers.append(Personnage('Idril','f',1))
pers.append(Personnage('Reejad','f',1))
pers.append(Personnage('Prokof','h',1))
pers.append(Personnage('Zadig','f',1))
pers.append(Personnage('Seamol','h',0.2))
pers.append(Personnage('Gargot','h',1))
pers.append(Personnage('Druz','h',1))
pers.append(Personnage('Parax','h',1))
pers.append(Personnage('Qrohel','h',1))
pers.append(Personnage('Ktaf','f',1))

obj=[]
obj.append(Objet('grimoire'))
obj.append(Objet('cles'))
obj.append(Objet('corde'))
obj.append(Objet('parchemin'))
obj.append(Objet('moulin a poivre'))
obj.append(Objet('appat'))
obj.append(Objet('codex'))
obj.append(Objet('pelle'))
obj.append(Objet('bandeau'))
obj.append(Objet('echelle'))
obj.append(Objet('radeau'))
obj.append(Objet('scie'))
obj.append(Objet('fouet'))
obj.append(Objet('liane'))
obj.append(Objet('sextant'))
obj.append(Objet('drapeau'))
obj.append(Objet('eperon'))
