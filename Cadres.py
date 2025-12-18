import pygame
pygame.init()
from var import*

def convertit(img):
    img=img.convert()
    img.set_colorkey(WHITE)
    return img

class Cadre:
    def __init__(self,x,y,dx,dy,fond=False,color=DBLUE, nblettresmax = ""):
        self.fond=fond
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.bord=10
        if self.fond==False:
            self.img=pygame.transform.scale(pygame.image.load('./img/'+self.__class__.__name__.lower()+'.jpg'), (self.dx,self.dy))
            self.img=convertit(self.img)
        self.color=color
        if nblettresmax=="": nblettresmax=25*dx/250
        self.nblettresmax = int(nblettresmax)
    def cadrex(self,X):
        return X+self.x
    def cadrey(self,Y):
        return Y+self.y
    def transformetexte(texte1, nblettresmax):
        ok=0
        texte2=[]
        texte1+=" "
        while ok==0:
            impossible=True
            for i in range(min(nblettresmax, len(texte1)-1), -1, -1):
                if texte1[i]==" ":
                    texte2.append(texte1[0:i])
                    texte1=texte1[i+1:len(texte1)]
                    impossible=False
                    break
            if impossible:
                texte2.append(texte1[0:nblettresmax])
                texte1=texte1[nblettresmax+1:len(texte1)]
            if texte1 in ["", " ", ".", ". ","  ",".  "]:
                ok=1
        return texte2

class CadreCarte(Cadre):
    def affiche(self,niv_faits,xc,yc):
        #displaysurf.fill(self.fond, pygame.Rect(self.x,self.y,self.dx,self.dy))
        surf.blit(self.img,(self.x,self.y))
        bordcase=2
        nx=len(niv_faits) #nombre de cases en x
        ny=len(niv_faits[0])
        lcase=(self.dx-2*self.bord)/(max(nx,ny))
        lcarre=lcase-2*bordcase
        for i in range(nx):
            for j in range(ny):
                x=self.cadrex(self.bord+i*lcase+bordcase)
                y=self.cadrey(self.bord+j*lcase+bordcase)
                if niv_faits[i][j]==1:
                    surf.fill(GREEN, pygame.Rect(x,y,lcarre,lcarre))
                if i==xc and j==yc:
                    surf.fill(BLUE, pygame.Rect(x,y,lcarre,lcarre))

class CadrePoints(Cadre):
    def affiche(self,points):
        surf.blit(self.img,(self.x,self.y))
        ecritsansupdate(str(points),self.x+self.bord,self.y+self.bord,20)

class CadreTexte(Cadre):
    def affiche(self,texte,x='',y=''):
        if x!='':self.x=x
        if y!='': self.y=y
##        nbligne=int(len(texte)/nblettres)+1
        surf.blit(self.img,(self.x,self.y))
##        for i in range(nbligne):
##            ecritsansupdate(texte[i*nblettres:min(len(texte),(i+1)*nblettres)],self.x+2*self.bord,self.y+1.5*self.bord+i*20,23,DBLUE)
        texte = Cadre.transformetexte(texte, self.nblettresmax)
        for i in range(len(texte)):
            ecritsansupdate(texte[i], self.x+2*self.bord, self.y+1.5*self.bord+i*20,23,self.color)

    

class CadreObjets(Cadre):
    def affiche(self,obj):
        surf.blit(self.img,(self.x,self.y))
        for i in range(len(obj)):
            if obj[i].ramasse==1:
                surf.blit(obj[i].img,(self.x+60+60*i,self.y+40))
                ecritsansupdate(obj[i].nom,self.x+60+60*i,self.y+20,20,DGREEN)

class CadreAccel(Cadre):
    #Montre les graphiques d'acceleration
    def __init__(self,x,y,dx,dy,seuil_marche,seuil_saute,nivmax=50,fond=GREY):
        Cadre.__init__(self,x,y,dx,dy)
        self.accelhistory=[]
        self.historymax=50
        self.seuil_saute=seuil_saute
        self.seuil_marche=seuil_marche
        self.nivmax=nivmax
    def affiche(self, acc):
        if acc>self.nivmax:
            self.nivmax=acc
        pygame.draw.line(surf,BLUE, (cadrex(0),cadrey(self.seuil_marche)),(cadrex(self.dx), cadrey(self.seuil_marche)))
        pygame.draw.line(surf,RED, (cadrex(0),cadrey(self.seuil_saute)),(cadrex(self.dx), cadrey(self.seuil_saute)))
        if len(self.accelhistory)>self.historymax:
            del self.accelhistory[0]
        self.accelhistory.append(acc)
        for i in range(len(self.accelhistory)-1):
            pygame.draw.line(surf,YELL, (cadrex(i),cadrey(self.accelhistory[i])),(cadrex(i+1), cadrey(self.accelhistory[i+1])))

class CadreAide(Cadre):
    taille=18
    font=pygame.font.Font(Mithellafont,taille) #Mithellafont
    def __init__(self,x,y,dx,dy,fond=CYELLOW,color=DGREEN, nblettresmax = ""):
        Cadre.__init__(self,x,y,dx,dy,fond, color, nblettresmax)
        self.fond=fond
    def ecritaide(phrase,x,y,color=DGREEN):
        text=CadreAide.font.render(phrase,1,color)
        surf.blit(text, (x,y))
    def affiche(self,texte,x='',y=''):
        if x!='': self.x=x
        if y!='': self.y=y
        nblettres=int(2*self.dx/CadreAide.taille)
        nbligne=int(len(texte)/nblettres)+1
        surf.fill(self.fond, pygame.Rect(self.x,self.y,self.dx,self.dy))
        pygame.draw.line(surf,WHITE, (self.x,self.y),(self.x+self.dx,self.y),4)
        pygame.draw.line(surf,WHITE, (self.x,self.y),(self.x,self.y+self.dy),4)
        pygame.draw.line(surf,self.fond, (self.x+self.dx,self.y),(self.x+self.dx,self.y+self.dy),4)
        pygame.draw.line(surf,self.fond, (self.x,self.y+self.dy),(self.x+self.dx,self.y+self.dy),4)        
##        premiercar=0
##        derniercar=1
##        nligne=0
##        while(nligne<100 and derniercar!=len(texte)-1):
####            if len(texte)<(i+1)*nblettres or texte[min(len(texte)-1,(i+1)*nblettres)]==' ' or texte[min(len(texte)-1,(i+1)*nblettres-1)]==' ' or i==nbligne-1: finligne=''
####            else: finligne='-'
##            derniercar=min(len(texte)-1,premiercar+nblettres)
##            while(texte[derniercar]!=' ' and derniercar!=1 and derniercar!=len(texte)-1):
##                derniercar-=1
##            CadreAide.ecritaide(texte[premiercar:derniercar+1],self.x+2*self.bord,self.y+1.5*self.bord+nligne*CadreAide.taille)
##            premiercar=derniercar+1
##            nligne+=1
        texte = Cadre.transformetexte(texte, self.nblettresmax)
        for i in range(len(texte)):
            CadreAide.ecritaide(texte[i], self.x+2*self.bord, self.y+1.5*self.bord+i*20,self.color)

                
class CadreWiimote(Cadre):
    def affichebase(self,seuil1=0,seuil2=0,maxi=0):
        pygame.draw.line(surf, WHITE, (self.x+self.dx/2,self.y),(self.x+self.dx/2,self.y+self.dy))
        pygame.draw.line(surf, WHITE, (self.x,self.y+self.dy/2),(self.x+self.dx,self.y+self.dy/2))
        pygame.draw.line(surf, BLUE, (self.x+self.dx/2+xx/maxi,self.y+self.dy/2+yy/maxi),(self.x+self.dx,self.y+self.dy/2))
        pygame.draw.line(surf, BLUE, (self.x,self.y+self.dy/2),(self.x+self.dx,self.y+self.dy/2))
    def affichepoint(self,xx,yy,maxi,color):
        pygame.draw.circle(surf, color, (self.x+self.dx/2+xx/maxi,self.y+self.dy/2+yy/maxi),4)
    def affichebarre(self,xx,yy,dxx,dyy,maxi,seuil1, seuil2,valeur):
        surf.fill(BLACK, pygame.Rect(xx,yy,dxx,dyy))
        surf.fill(YELL, pygame.Rect(xx,yy,dxx,valeur/maxi))
        pygame.draw.line(surf, WHITE, (xx,yy+dyy*seuil1/maxi),(xx+dxx,yy+dyy*seuil1/maxi))
        pygame.draw.line(surf, RED, (xx,yy+dyy*seuil2/maxi),(xx+dxx,yy+dyy*seuil2/maxi))
    def affichewiimote(self,wiib):
        pass
