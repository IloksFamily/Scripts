import pygame,sys
import inspect

surf=1
FPS=30

#niveaux=['Difficulte1','Difficulte1.5','Difficulte2', 'Difficulte2.5','Difficulte3','coucou','Niv_2py2'] #noms de fichier
niveaux=['ce_fichier_est_un_test','Difficulte1.5','Difficulte2', 'Difficulte2.5','Difficulte3','coucou','Niv_2py2'] #noms de fichier
musique=['Best_Banjo_Picker','Best_Banjo_Picker','piano-ilok1-1','savane_musique', 'savane_musique','Jingle Bells2', 'piano-ilok1-1']#'schtroumpfs'
perso_multi=['ilok','fille','roux','bebe','mario','sava','bermat','mario'] #images des joueurs en mode multijoueur
flocon_on=[0,0,0,0,0,1,0]
nb_niv=7
x_niv=[253,263,429,286,175, 44,161]
y_niv=[130,130,198, 73, 41, 74,290]

points=0

acc0=[0,0,0,0,0]
acc1=[0,0,0,0,0]
acc2=[0,0,0,0,0]
accref=[0,0,0,0,0]
accmin=[0,0,0,0,0]
seuil_marche=30 #20
seuil_saute=80 #70
ok=0
wiisport_lanceboule=[0,0,0,0,0]
seuil_cours=[0,0,0,0,0]
seuil_saut=[0,0,0,0,0]

BLACK = ( 0, 0, 0)                          
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
DGREEN = ( 0, 125, 0)
BLUE = ( 0, 0, 255)
DBLUE=(0,0,125)
YELL=(0,255,255)
CYELLOW=(255,255,185)
DYELLOW=(128,128,92)
MARRON=(150,70,40)
FOND=(255, 255, 255)
GREY=(100,100,100)

Romanfont='./img/MorrisRomanBlack.ttf'
Dumfont='./img/dum1.ttf'
Mithellafont='./img/Mithella-Regular.otf'

lgx_ecran=1000
lgy_ecran=600
fini=0

[partiebis, cote_carte, carte, scenario, obj2, pers2, diff_debut, diff_fin, bloc_decor, bloc_chemin,phrase_intro,phrase_fin]=[0 for i in range(12)]
[obj2,pers2]=[0,0]
niv_debloque=0
niv_faits=0
[NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4]=[0,0,0,0,0,0,0]
mobiles=[]

#From Menu11
nb_joueur=1
centrex=500
centrey=300
Joueur=[0,0,0,0,0]

#d = ligne de debug/test
gravite=1
debug_mode=0
phone_mode=False
musique=1
explorecarte=False

fpsClock=None

def InitialiseFenetre():
    global surf, fpsClock
    fpsClock = pygame.time.Clock()
    pygame.key.set_repeat(500,30)
    if debug_mode==0:
        surf = pygame.display.set_mode((lgx_ecran, lgy_ecran),pygame.FULLSCREEN) # 0, 32)
    else:
        surf = pygame.display.set_mode((lgx_ecran, lgy_ecran), 0, 32)
    pygame.mixer.init()
    FPS = 25

def verifie_ferme_fenetre():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  #ferme la librairie pygame
            sys.exit()     #ferme le programme

def verifie_ferme_fenetre_sansget(event):
    if event.type == pygame.QUIT:
        pygame.quit()  #ferme la librairie pygame
        sys.exit()     #ferme le programme

    
def ecrit(phrase,x,y,taille=30,couleur=WHITE):
    font=pygame.font.Font(Dumfont,taille)
    text=font.render(phrase,1,couleur)
    surf.blit(text, (x,y))
    pygame.display.update()

def ecritsansupdate(phrase,x,y,taille=30,couleur=WHITE):
    font=pygame.font.Font(Dumfont,taille)
    text=font.render(phrase,1,couleur)
    surf.blit(text, (x,y))
    
def maj_niv_faits(x,y,a):
    niv_faits[x][y]=a




