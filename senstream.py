#!/usr/bin/python3

### Senstream 1.1 ###

# Lance en // le serveur et mets à jour les variables phonacc et intnegpos
import http.server, socket
import sys, os, time
from threading import Thread
import socket
from math import sqrt

#from Var import tabj
nbjmax=5
def tabj(a):
    return [a for i in range(nbjmax)]

calibrer=False
verb=True
showaccel=False
showfreq=True
affichefreq=True
PORT = 8080
phoneacc='pas encore de connexion'  #norme acceleration 3D 
ipphone=tabj(0)                 #ip des telephones
njparip=dict()                    #numero de joueur en fonction de IP
nbj=0
msgtophone= tabj(['vibre','msg:Bonjour!','vce: hey! tu es connecter!']) # [[],['vibre','msg:Bonjour!'],[],[],[],[]]    #pile messages a envoyer au telephone, par joueur 
nbreq=0
freq=tabj(0)
treq=0
tn=0
intnegpos=tabj(0)                         
intneg=tabj(0)
intpos=tabj(0)
compass=tabj([])
sensitivity=tabj(0)


class Senstream(Thread):
    def __init__(self,showaccel=False, showfreq=False):
        Thread.__init__(self)
        if showaccel:
            thread_2=AfficheStd()
            thread_2.start()
        global affichefreq
        affichefreq=showfreq
        self.start()            
    def run(self): #Code à exécuter pendant l'exécution du thread. Lance le serveur.
        print("Serveur actif : "+ get_ip()+":"+ str(PORT))
        http.server.HTTPServer(("", PORT), Serveur).serve_forever()
    def vibre(self,nj):
        print('vibre')##D
        msgtophone[nj].append('vibre')
        print(msgtophone)
    def message(self,nj,text):
        msgtophone[nj].append('msg:'+text)
    def parle(self,nj,text):
        print('parle',text)##D
        msgtophone[nj].append('vce:'+text)
        print(msgtophone)

class Serveur(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def log_message(self,format,*args): #evite d afficher les requetes
        return
    def do_POST(self):
        #'''Reads post request body'''
        global freq,phoneacc,ipphone,ip,njparip,nbj,nbreq,treq,msgtophone,tn,intnegpos, intneg, intpos, affichefreq, compass, sensitivity
        ip=self.client_address[0]
        if not(ip in ipphone) and nbj<4:
            nbj+=1
            ipphone[nbj]=ip
            njparip[ip]=nbj
        nj=njparip[ip]
        if True: #affichefreq:
            nbreq+=1
            if time.time()-treq>=5: #affiche toutes les 5 sec
                if affichefreq:
                    print('# '+str(nbreq)+' requetes par seconde #')
                freq[nj]=nbreq
                nbreq=0
                treq=time.time()
                tn+=1
        self._set_headers()
        #print(msgtophone[njparip[ip]])
        if len(msgtophone[nj])>0: #njparip[ip]
            print('envoie:: '+msgtophone[nj][0]) ##D
            self.wfile.write(bytes(msgtophone[nj][0],"utf-8")) #bytes("<body><p>"+msgtophone[nj]+"</p>","utf-8")) 
            del msgtophone[nj][0]
        post_body = self.rfile.read(int(self.headers.get('content-length', 0)))
        post_acc=str(post_body).split('u')
        #print(post_acc)
##        print(round(float(post_acc[19]),1))
        if isinstance(post_acc,list) and len(post_acc)>=12 and post_acc[1]!='.':
            phoneacc=round(sqrt(float(post_acc[1])**2+float(post_acc[3])**2+float(post_acc[5])**2),1)
            intnegprecedent=intneg[nj]
            if phoneacc<10:
                intneg[nj]=phoneacc-10+min(0,intnegprecedent)
            else:
                intneg[nj]=0
            intposprecedent=intpos[nj]
            if phoneacc>=10:
                intpos[nj]=phoneacc-10+max(0,intposprecedent)
            else:
                intpos[nj]=0
            if intpos[nj]>0 and intnegprecedent<0:
                intnegpos[nj]=intpos[nj]-intnegprecedent
            elif intpos[nj]>0:
                intnegpos[nj]+=intpos[nj]
            else:
                intnegpos[nj]=0
            if post_acc[7]!='.':
                compass[nj]=[round(float(post_acc[7]),2),round(float(post_acc[9]),2), round(float(post_acc[11]),2)]
##            if post_acc[19]!='.':
##                sensitivity[nj]=round(float(post_acc[19]),1)
        else:
            print('Erreur Senstream 1: ',post_acc)
            phoneacc=post_acc
##        print(sensitivity,post_acc[19])
        #print('Senstream:',phoneacc,intnegpos) #ip,,post_acc
            
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = ''
    finally:
        s.close()
    return IP

class AfficheStd(Thread):
    def run(self):
        t0=time.time()
        while(True):
            if time.time()>t0+0.1:
                t0=time.time()
                print(phoneacc)               

def calibration():
    from matplotlib.pyplot import plot,show
    import csv
    global phoneacc, ipphone, msgtophone
    print('>> run calibration')
    print('ouvre l application Phonepi sur ton téléphone android, et saisis:'+ get_ip()+':8080')
    while(ipphone[1]==0):
        pass
    print('Quel est ton nom? ')
    nom=input()
    print('pret? appuie sur Entree')
    input()

    continu=True
    acc=[]
    accel=[]
    t0=time.time()
    tetape=10
    etape=1
    time.sleep(3)
    print("Ne bouge pas")
    instruction=["","Ne bouge pas","Marche tranquillement","Marche vite","Cours sur place", "SAUTE!","repose toi..."]
    msgtophone[njparip[ip]].append('vibre')

    while(continu==True):
        accel.append(phoneacc)
        if time.time()-t0>etape*tetape:
            etape+=1
            print(instruction[etape])
            msgtophone[1].append('vibre')
            accel.append(-10.0)
            if etape==6:
                continu=False
        time.sleep(0.04)

    plot(accel)
    show()

    with open(nom+'.csv','w', newline='') as csvfile:
        xwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for a in accel:
            xwriter.writerow({a})
    csvfile.close()



if calibrer:
    senstream=Senstream(showaccel=showaccel, showfreq=showfreq)
    calibration()

#s=Senstream()   
# Attend que les threads se terminent

#thread_1.join()
#thread_2.join()

