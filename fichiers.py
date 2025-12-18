import os
import pickle

def changeos(t=''):
    a = input(t+'Chemin actuel: '+str(os.getcwd())+' . Modifier? :')
    if a!='':
        try:
            os.chdir(a)
            return None
        except:
            changeos('Erreur. ')

def lirefichier(nom):
    try: f=open(nom, 'rb')
    except: f=open('./'+ nom, 'rb')
    try: a = pickle.load(f)
    except EOFError: a='fichier vide'
    f.close()
    return(a)

def printfichier(nom, a):
    try: f=open(nom, 'wb')
    except: f=open('./'+ nom, 'wb')
    pickle.dump(eval(a),f)
    f.close()

def main():
    while input('Changer os( '+str(os.getcwd())+' )?') not in ('non','0'):
        changeos()
    while True:
        nom = input('lire un fichier le fichier:')
        try:
            print(lirefichier(nom))
            break
        except:
            print('erreur')
            if input(): raise ValueError()
    while True:
        a = input('Imprimer dans le fichier? :')
        if a=='':break
        try:
            printfichier(nom, a)
            print('effectué')
            break
        except: print('erreur')
    main()
def abc():
    os.chdir("D:/Iloksfamily/IloksClass/parties/0002 Au coeur du combat")
    for x in range(1,7):
        for y in range(1,7):
            a=lirefichier("niv [{}, {}]".format(x,y))
            if 1:#"Poisson" in a:
                print(a)
#main()
abc()
