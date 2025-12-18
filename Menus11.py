import pygame,time, socket, os, pickle, cv2
from pygame.locals import *
from var import *
from Cadres import *
from PersonnagesObjets import *
import senstream
import smtplib, ssl
from email.message import EmailMessage


centrex=500
centrey=300
fin_niveau_img=pygame.image.load('./img/fin_niveau.png')            
menu_img=pygame.image.load('./img/menu.png')

def ecrit(surf, phrase,x,y,taille=30,couleur=WHITE):
    font=pygame.font.Font(Dumfont,taille)
    text=font.render(phrase,1,couleur)
    surf.blit(text, (x,y))
    pygame.display.update()

def ecritsansupdate(DISPLAYSURF, phrase,x,y,taille=30,couleur=WHITE):
    font=pygame.font.Font(Dumfont,taille)
    text=font.render(phrase,1,couleur)
    DISPLAYSURF.blit(text, (x,y))
    
def faire_choix(avis):
    nb_voix=[0,0,0,0]
    for i in range(nb_joueur):
        nb_voix[avis[i]]+=1
    choix=1
    voix=0
    for i in range(4):    
        if nb_voix[i]>voix:
            choix=1
            voix=nb_voix[i]
    return choix

def attendtouche():
    suite=0
    while suite==0:
        for i in range(1, nb_joueur+1):
            pygame.event.get()
            keys=pygame.key.get_pressed()
            if keys[K_0] or keys[K_PLUS] or keys[K_a] or keys[K_RIGHT]:
                suite=1
    time.sleep(0.02)#☺0.1)

def attend_touche(suite=debug_mode):
    while suite==0:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                suite=1
            verifie_ferme_fenetre_sansget(event)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
#marche aussi: print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

def IncrementeScore(P,points):
    global NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4
    for i in range(1, nb_joueur+1):
        PointsJoueur[Joueur[i]]+=int(points/nb_joueur)
    points=0
    f = open('./parties/joueurs', 'wb')
    pickle.dump([NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4], f)
    f.close()

def AfficheScore(P):
    global NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4
    surf.fill(BLACK)
    font=pygame.font.Font(Dumfont,25)
    text=font.render('Scores  -  Appuyer sur une touche',1,DGREEN)
    surf.blit(text, (50,50))   
    xl=1
    yl=0
    for i in range(0,len(NomJoueur)):
            yl+=1
            if yl>8:
                yl-=8
                xl+=1
            text=font.render(NomJoueur[i],1,DBLUE)
            surf.blit(text, (170*xl,100+40*yl))        
            text=font.render(str(int(PointsJoueur[i])),1,BLUE)
            surf.blit(text, (170*xl+100,100+40*yl))
    pygame.display.update()
    attend_touche()
    
class Menu:
    def __init__(self):
        self.musique=""
        self.fond=BLACK

class MenuAvis(Menu):
    avis=[0,0,0,0]
    def __init__(self):
        Menu.__init__(self)
    def demander_avis(self, surf, options):
        print(a)
        surf.fill(self.fond)
        deltax=[-100, 0, +100 ,0]
        deltay=[0, -100, 0, +100]
        for i in range(4):
            ecrit(surf, options[i],centrex-deltax[i]-100,centrey-deltay[i])
        pygame.display.update()
        suite=0
##        while suite<nb_joueur:
##            for i in range(1, nb_joueur+1):
##                wiib=EntreeWiimote(mawiimote[i])
##                if avis[i-1]==0:
##                    if wiib[11]==1: avis[i-1]=1
##                    if wiib[0]==1: avis[i-1]=2 ##maj
##                    if wiib[10]==1: avis[i-1]=3
##                    if wiib[0]==1: avis[i-1]=4 ##maj
##                    if avis[i-1]!=0:
##                        suite+=1
##                        ecrit(surf, 'J'+i+' OK',200*i,60,GREEN)
        time.sleep(0.3)#☺1)
        return avis

class MenuInfo(Menu):
    def __init__(self,surf,fond=BLACK, imgfond="",musique="",txt1="",txt2="",couleur=WHITE):
        if musique!="" and musique!='none':
            pygame.mixer.music.load(musique)
            pygame.mixer.music.play(-1,0)
        if imgfond=="":
            surf.fill(fond)
        else:
            surf.blit(imgfond, (0,0))
        pygame.display.update()
        time.sleep(1)
        ecrit(surf, txt1,100,100,30,couleur)
        ecrit(surf, 'Appuye sur une touche',300,500,50,DGREEN)    
        attendtouches()
        if musique!="" and musique!='none': pygame.mixer.music.fadeout(1000)


class MenuGrille(Menu):
    def __init__(self):
        Menu.__init__(self)
    def demander_choix(self,surf, message, options,nb_joueur,debloque=[]):
        if debloque==[]:
            for i in options:
                debloque.append(1)
        choix=[0,0,0,0]
        XJ=[1,1,1,1,1]
        YJ=[1,1,1,1,1]
        ok=[0,0,0,0,0]
        wiib=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        suite=0
        taille_police=25

        pygame.key.set_repeat(0)
        while suite==0:
            keysi=[]
            keys=pygame.key.get_pressed()
            a=pygame.event.get()
            for event in a:
                if event.type == pygame.KEYDOWN:
                    keysi.append(event.key)
            #print(keysi, a)
            
            surf.fill(self.fond)
            ecrit(surf, message,100,60,40,GREEN)
            xl=1
            yl=0
            for i in range(0,len(options)):
                    yl+=1
                    if yl>8:
                        yl-=8
                        xl+=1
                    if debloque[i]==1:
                        ecrit(surf, options[i],100*xl,100+40*yl,taille_police,WHITE)
                    else:
                        ecrit(surf, '?',100*xl,100+40*yl,taille_police,WHITE)
           # pygame.event.get()
            if xl>1: yl=8
            if ok[0]+ok[1]+ok[2]+ok[3]+ok[4]==nb_joueur: #Si tous les choix sont faits, termine
                suite=1
                for i in range(1, nb_joueur+1):
                    choix[i-1]=(XJ[i]-1)*8+YJ[i]-1
            for i in range(1, nb_joueur+1):
                keys=pygame.key.get_pressed()
                if ok[i]==0:
                    if keys[K_LEFT]:
                        if XJ[i]>1: XJ[i]-=1
                    if keys[K_RIGHT]:
                        if XJ[i]<xl: XJ[i]+=1
                    if keys[K_UP] :
                        if YJ[i]>1: YJ[i]-=1
                    if keys[K_DOWN]:
                        if YJ[i]<yl: YJ[i]+=1
                    pygame.draw.rect(surf, WHITE, Rect(100*XJ[i]-5-i, 100+40*YJ[i]-i-5, 90+2*i,25+2*i),2) 
                    if nb_joueur>1: ecrit(surf, str(i),100*XJ[i]-5-i-10, 90+40*YJ[i]-i+8,taille_police,YELL)  
                if ok[i]==1:
                    pygame.draw.rect(surf, RED, Rect(100*XJ[i]-5-i, 100+40*YJ[i]-i-5, 90+2*i,25+2*i),4)
                    if nb_joueur>1: ecrit(surf, str(i),100*XJ[i]-5-i-10, 90+40*YJ[i]-i+8,taille_police,RED)             
                if (keys[K_z] or keys[K_2] or K_RETURN in keysi) and debloque[(XJ[i]-1)*8+YJ[i]-1]==1:
                    ok[i]=1
                    pygame.draw.rect(surf, RED, Rect(100*XJ[i]-5-i, 100+40*YJ[i]-i-5, 90+2*i,25+2*i),4)
            pygame.display.update()
            time.sleep(0.2)
        #☺time.sleep(0.3)#1)
        return choix


class MenuPartie(Menu):
    def __init__(self):
        Menu.__init__(self)
    def demander_choix(self,surf, nb_joueur):
        liste_parties=os.listdir(os.path.abspath(".")+'/parties')
        liste_parties.remove('joueurs')
        os.chdir(os.path.abspath(".")+"/parties/")
        try:
            f = open("log", 'rb')
            log=pickle.load(f)
            f.close()
            os.chdir(os.path.abspath(".."))
        except:
            log=[liste_parties,[10]*len(liste_parties),['debloque']+(len(liste_parties)-1)*['bloque']]
            
        os.chdir(os.path.abspath(".."))


class Score(Menu):
    def IncrementeEtAfficheScore(surf,P, N,C,points):
        global NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4
        surf.fill(BLACK)
        ecrit(surf, 'Scores  -  Appuyer sur a ou 2',50,50,60,YELL)


class Bienvenue(Menu):
    def __init__(self):
        font=pygame.font.Font(Dumfont,30) #chiffre=taille des lettres
        surf.fill(BLACK)
        pygame.mixer.init()
        if musique==1: pygame.mixer.music.load("./sons/Untitled2-8.mp3")#"./sons/Aventures intro - FULL.mp3"
        pygame.display.update()
        if musique==1: pygame.mixer.music.play(-1,0)
        suite=0
        pygame.display.update()
        time.sleep(0.5*(1-debug_mode))
        accueil_img=pygame.image.load('./img/accueil.png')
        surf.blit(accueil_img, (0,0))
        pygame.display.update()
        time.sleep(0.5*(1-debug_mode)) #4.4
        phrase = 'Booste le son et rentre dans l\'ambiance!' 
        text=font.render(phrase,1,DGREEN)
        surf.blit(text, (300,400))
        pygame.display.update()
        time.sleep(0.5*(1-debug_mode))#4.4
        phrase = 'Es-tu vraiment pret a relever le defi ?' 
        text=font.render(phrase,1,RED)
        surf.blit(text, (320,450))
        if musique==1: pygame.display.update()
        time.sleep(0.5*(1-debug_mode)) #8.7
        phrase = 'Alors appuye sur une touche...' 
        text=font.render(phrase,1,DGREEN)
        surf.blit(text, (350,500))
        pygame.display.update()
        attend_touche()
        pygame.mixer.music.load("./sons/intro1_son.mp3")
        pygame.mixer.music.play(-1,0)
        playvideo('./sons/intro1.mp4')
        if musique==1: pygame.mixer.music.load("./sons/Untitled2-8.mp3")#"./sons/Aventures intro - FULL.mp3"
        pygame.display.update()
        if musique==1: pygame.mixer.music.play(-1,0)

def playvideo(video):
    print('playing video')
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(video)
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
      print("Error opening video  file")
    #cv2.setWindowProperty("fullscreen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)  
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:
        # Display the resulting frame
        cv2.namedWindow('Frame', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Frame', frame)
        # Press Q on keyboard to  exit
        if cv2.waitKey(38) & 0xFF == ord('q'):
          break
      # Break the loop
      else: 
        break
       
    # When everything done, release 
    # the video capture object
    cap.release()
       
    # Closes all the frames
    cv2.destroyAllWindows()
    print('finished')
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
#marche aussi: print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

class Connexion(Menu):
    def __init__(self):
        senstream1=senstream.Senstream(False,False)
        senstream.nbj=0
        ### Connection des telephones
        while(senstream.nbj==0):
            font=pygame.font.Font(Dumfont,30) 
            self.affiche(font)
            a=0
            text=font.render('aucun joueur connecté...',1,GREEN)
            surf.blit(text, (50,550)) 
            pygame.display.update()
            suite=0
            while suite==0:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        suite=1
                    verifie_ferme_fenetre_sansget(event)
                if senstream.nbj!=a:
                    if senstream.nbj==1: text=font.render(str(senstream.nbj)+' joueur connecté...',1,GREEN)
                    else: text=font.render(str(senstream.nbj)+' joueurs connectés...',1,GREEN)
                    self.affiche(font)
                    surf.blit(text, (50,550)) 
                    pygame.display.update()
                    a=senstream.nbj
            if senstream.nbj==0:
                text=font.render('aucun joueur connecté(s)! on recommence...',1,DGREEN)
                surf.blit(text, (50,550))
                pygame.display.update()
                time.sleep(1)
        for i in range(1,senstream.nbj+1):
            senstream1.message(i,'J'+str(i))
            senstream1.parle(i,'c est parti!')
        text=font.render(str(senstream.nbj)+' joueur(s) sont connecté(s)!',1,DGREEN)
        surf.blit(text, (50,550))
        pygame.display.update()
        nb_joueur=senstream.nbj
        time.sleep(1)
    def affiche(self,font):
            surf.fill(BLACK)
            text=font.render('Ouvrez l application Iloksens sur vos téléphones android, saisisez: ',1,DGREEN)
            surf.blit(text, (130,50))
            CadreAide(130,100,130,40).affiche(get_ip()) #AM
            icone_img=pygame.transform.scale(pygame.image.load('./img/Ilok.png'),(60,60)).convert() #AM
            icone_img.set_colorkey(WHITE)
            surf.blit(icone_img, (50,50))
            text=font.render('et cliquez sur Connecter',1,DGREEN)
            surf.blit(text, (130,150))
            capture_img=pygame.transform.scale(pygame.image.load('./img/capture.jpg'),(170,156)) #AM
            surf.blit(capture_img, (530,100))
            text=font.render('PROTEGER LE TELEPHONE ET LE PLACER DANS UNE POCHE FERMEE',1,DGREEN)
            surf.blit(text, (50,350))        
            text=font.render('Desactiver la mise en veille du telephone ou ilok s arretera tout seul!',1,DGREEN)
            surf.blit(text, (50,400)) 
            text=font.render('En cas d erreur verifie que telephone et pc sont connectes au meme wifi.',1,DGREEN)
            surf.blit(text, (50,450)) 
            pygame.display.update()
            text=font.render('Appuyez sur une touche lorsque tous les joueurs sont connectes...',1,GREEN)
            surf.blit(text, (50,500)) 
            pygame.display.update()
            suite=0


class ChoixJoueurs(Menu):
    def __init__(self):
        #Choix des joueurs
        global NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4
        f = open('./parties/joueurs', 'rb')
        [NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4]=pickle.load(f)#, encoding='latin1'        
        f.close()

        surf.fill(BLACK)
        suite=0 #Pas activé pour le moment
        XJ=[1,1,1,1,1]
        YJ=[1,1,1,1,1]
        ok=[0,0,0,0,0]
        font=pygame.font.Font(Dumfont,30)

        pygame.key.set_repeat(0)
        while suite==0:
            keysi=[]
            keys=pygame.key.get_pressed()
            a=pygame.event.get()
            for event in a:
                if event.type == pygame.KEYDOWN:
                    keysi.append(event.key)
            #print(keysi, a)

            surf.fill(BLACK)
            text=font.render('Choisis ton joueur: Selectionne avec les fleches du clavier, appuie sur entrée pour valider',1,DGREEN)
            surf.blit(text, (20,80))
            if len(NomJoueur)==1:
                CadreAide(50,20,600,40).affiche('Pour commencer cree un profil par personne en appuyant sur n')
            else:
                CadreAide(650,150,300,80).affiche('Nouveau joueur: n  Annuler selection: c')    
            xl=1
            yl=0
            for i in range(0,len(NomJoueur)):
                    yl+=1
                    if yl>8:
                        yl-=8
                        xl+=1
                    text=font.render(NomJoueur[i],1,WHITE)
                    surf.blit(text, (100*xl,100+40*yl))        
            for event in pygame.event.get():
                verifie_ferme_fenetre_sansget(event)
            if xl>1: yl=8
            if ok[0]+ok[1]+ok[2]+ok[3]+ok[4]==nb_joueur:
                suite=1
                for i in range(1, nb_joueur+1):
                    Joueur[i]=(XJ[i]-1)*8+YJ[i]-1
                    print((i, NomJoueur[Joueur[i]]))
            j=1
            while(ok[j]==1): #definit j comme le joueur en train d'etre choisi
                j+=1
            #pygame.key.set_repeat(0)
            for i in range(1, nb_joueur+1):
                if i==j:
                    if ok[i]==0:
                        if keys[K_LEFT]:
                            if XJ[i]>1: XJ[i]-=1
                        if keys[K_RIGHT]:
                            if XJ[i]<xl: XJ[i]+=1
                        if keys[K_UP]:
                            if YJ[i]>1: YJ[i]-=1
                        if keys[K_DOWN]:
                            if YJ[i]<yl: YJ[i]+=1
                        pygame.draw.rect(surf, YELL, Rect(100*XJ[i]-5-i, 100+40*YJ[i]-i-5, 100+2*i,25+2*i+10),2) 
                        text=font.render(str(i),1,YELL)
                        surf.blit(text, (100*XJ[i]-5-i-10, 100+40*YJ[i]-i+8))   
                        if keys[K_p] or K_RETURN in keysi:                       #à changer
                            ok[i]=1
                            pygame.draw.rect(surf, RED, Rect(100*XJ[i]-5-i, 100+40*YJ[i]-i-5, 100+2*i,25+2*i+10),4)
                            pygame.display.update()
                            time.sleep(0.02)#1)
                if keys[K_c]==1:
                    for j in range(0,5):
                        ok[j]=0
                if ok[i]==1:
                    pygame.draw.rect(surf, RED, Rect(100*XJ[i]-5-i, 100+40*YJ[i]-i-5, 100+2*i,25+2*i+10),4)
                    text=font.render(str(i),1,RED)
                    surf.blit(text, (100*XJ[i]-5-i-10, 100+40*YJ[i]-i+8))   
                if keys[K_0] or keys[K_PLUS] or keys[K_n]:
        ##    for event in pygame.event.get():
        ##        if event.type== KEYDOWN:
        ##            print(event.unicode)
        ##            if event.unicode=='+' or event.unicode=='0': #event.key==K_PLUS or event.key==K_0: #Ajouter un joueur
                    ajouter=1
                    nomj=''
                    couleurj='WHITE'
                    text=font.render('Nouveau joueur, ecris ton nom sans accent:',1,DGREEN)
                    surf.blit(text, (50,500))
                    pygame.display.update()
                    while ajouter==1:
                        for event in pygame.event.get():
                            if event.type == KEYDOWN and event.key!=K_RETURN and event.key!=K_BACKSPACE and event.key!=304:
                                nomj=nomj+event.unicode #event.str.encode('ascii','ignore')
                                surf.fill(BLACK)
                                text=font.render(nomj,1,WHITE)
                                surf.blit(text, (200,500))
                                pygame.display.update()
                            if event.type== KEYDOWN and event.key==K_BACKSPACE and len(nomj)>0:
                                nomj=nomj[0:-1]
                                surf.fill(BLACK)
                                text=font.render(nomj,1,WHITE)
                                surf.blit(text, (200,500))
                                pygame.display.update()
                            if event.type== KEYDOWN and event.key==K_RETURN and nomj!='':
                                if nomj!='':                                 
                                    Profils.append(0)
                                    NomJoueur.append(nomj)
                                    CouleurJoueur.append(couleurj)
                                    PointsJoueur.append(0)
                                    reserve2.append(0)
                                    reserve3.append(0)
                                    reserve4.append(0)
                                    f = open('./parties/joueurs', 'wb')
                                    pickle.dump([NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4], f)
                                    print([NomJoueur, CouleurJoueur, PointsJoueur,Profils, reserve2, reserve3, reserve4])
                                    f.close()
                                ajouter=0 #event.key==pygame.K_BACKSPACE
            pygame.display.update()
            time.sleep(0.05)#0.1)

def ChoixPartie():
    #============choix de la partie==============
    print('> Charge la partie... ')
    liste_parties=os.listdir(os.path.abspath(".")+'/parties')
    liste_parties.remove('joueurs')

    liste_noms=[]
    partie_fait=[]
    for i in liste_parties:
        f = open('./parties/'+str(i)+'/carte_fait', 'rb')
        [fait,precedent,b,c,d]=pickle.load(f, encoding='latin1')
        f.close()
        print(precedent)
        if precedent!='':
            f = open('./parties/'+str(precedent)+'/carte_fait', 'rb')
            [fait,a,b,c,d]=pickle.load(f, encoding='latin1')
            f.close()
            if fait: partie_fait.append(1)
            else: partie_fait.append(0)
        else: partie_fait.append(1)
        liste_noms.append(i[5:])  #enlève les chiffres au début du nom de la partie
    print(partie_fait)
    
##    partie_verrouillee=[]
##    for p in liste_parties:
##        f = open('./parties/joueurs'+str(partie)+'carte', 'wb')        
##        pickle.
##    
    menu=MenuGrille()
    ok=0
##        while(ok==0):
    partie=liste_parties[menu.demander_choix(surf,'Choisis ton aventure, et appuie sur entrée',liste_noms, 1, partie_fait)[0]]#########################################################################################################
    return partie
##                try:
##                    os.chdir(os.path.abspath(".")+"/parties/"+str(partie))
##                    ok=1
##                except:
##                    pass




class FinNiveau(Menu):
    def __init__(self, points):
        points=points+int(1000) #points+=int(1000)
        pygame.mixer.music.fadeout(300)
        if musique==1: pygame.mixer.music.load("./sons/victoire.mp3")
        if musique==1: pygame.mixer.music.play(0,0)
        if debug_mode==0: time.sleep(3)#☺7)
        surf.fill(BLACK)
        if musique==1: pygame.mixer.music.load("./sons/Anti-Stress music.mp3")
        if musique==1: pygame.mixer.music.play(-1,0)
        pygame.display.update()
        time.sleep(1)
        surf.blit(fin_niveau_img, (0,0))
        pygame.display.update()
        time.sleep(1)
        font=pygame.font.Font(Dumfont,60) #chiffre=taille des lettres
        phrase = str(points)+' points!' 
        text=font.render(phrase,1,RED)
        surf.blit(text, (400,300))
        pygame.display.update()
        time.sleep(1)
        font=pygame.font.Font(Dumfont,30)
        phrase = 'Appuye sur une touche' 
        text=font.render(phrase,1,DGREEN)
        surf.blit(text, (400,500))
        pygame.display.update()    
        attend_touche()
        pygame.mixer.music.fadeout(2000)
        print("Level completed !")
        font=pygame.font.Font(Dumfont,20)
        IncrementeScore(PointsJoueur,points)
        AfficheScore(PointsJoueur)
        CadreAide(800,500,200,80).affiche('Je charge la suite...')
        pygame.display.update()
        next
        IncrementeScore(PointsJoueur,points) #Joueur.points
        AfficheScore(PointsJoueur)


class FinPartie(Menu):
    def affiche(self,fin_img,victoire_img, phrase_fin):
        surf.fill(BLACK)
        surf.blit(fin_img, (1,1))
        surf.blit(victoire_img, (10,200))
        ecrit(surf, phrase_fin,100,100,taille=30,couleur=WHITE)
        ecrit(surf, 'Tout le peuple est en liesse et plein d espoir !',100,150,taille=30,couleur=WHITE)
        if musique==1:
            pygame.mixer.music.load('./sons/triomphe.mp3')
            pygame.mixer.music.play(0,0)
            time.sleep(5.5)
            pygame.mixer.music.fadeout(3000)
        attend_touche()
        print("retour main")

class Com():
    def __init__(self):
##        self.smtp_address = 'smtp-relay.gmail.com'
##        self.smtp_port = 465
##        self.email_address = 'iloksfamilysender@gmail.com'
##        self.email_password = 'Ilokspass99'
##        self.email_receiver = 'iloksfamilyrecevier@gmail.com'
##        if True: #try:
##            self.context = ssl.create_default_context()
##            with smtplib.SMTP_SSL(self.smtp_address, self.smtp_port, context=self.context) as server:
##              server.login(self.email_address, self.email_password)
##              server.sendmail(self.email_address, self.email_receiver, 'Ilok:nouveaujeu')
        print('com init')
        self.msg = EmailMessage()
        self.msg.set_content("Ilok:nouveaujeu")
        self.msg["Subject"] = "Iloksfamily"
        self.msg["From"] = "iloksfamilysender@gmail.com"
        self.msg["To"] = "iloksfamilyreceiver@gmail.com"
        self.context=ssl.create_default_context()
        print('com with')
        with smtplib.SMTP("smtp.gmail.com", port=587) as smtp: #587 ou 465?
            print('1')
            smtp.starttls(context=self.context)
            print('2')
            smtp.login(self.msg["From"], "Ilokspass99")
            print('3')
            smtp.send_message(self.msg)

            print('com')
        #except:
        print('comexcept')
    def comfinniveau(self,partie, niveau):
        try:
            with smtplib.SMTP_SSL(self.smtp_address, self.smtp_port, context=self.context) as server:
              server.login(self.email_adress, self.email_password)
              server.sendmail(self.email_address, self.email_receiver, 'Ilok:finniveau:'+str(partie)+':'+str(niveau))
            print('com')
        except:
            print('comexcept')
        
              

##        xl=1
##        yl=0
##        for i in range(1, nb_joueur+1):
##            PointsJoueur[Joueur[i]]+=points/nb_joueur
##        points=0
##        f = open('joueurs', 'wb')
##        pickle.dump([NomJoueur, CouleurJoueur, PointsJoueur,reserve1, reserve2, reserve3, reserve4], f)
##        f.close()
##
##        for i in range(0,len(NomJoueur)):
##                yl+=1
##                if yl>8:
##                    yl-=8
##                    xl+=1
##                text=font.render(NomJoueur[i],1,WHITE)
##                surf.blit(text, (150*xl,100+40*yl))        
##                text=font.render(str(PointsJoueur[i]),1,WHITE)
##                surf.blit(text, (150*xl+130,100+40*yl))
##        pygame.display.update()
        attendtouche()


    
