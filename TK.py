#### Import standard de Maingame ###########
import pygame, math, time, random
import os
os.chdir("../") #a enlever pour freeze, a remettre pour executer. python setup.py build   (ou bdist_msi)
pygame.init()

from var import *
#if phone_mode: raise ValueError("Ce programme n'accepte pas le mode téléphone! Merci de modifier dans le fichier var (D:\Iloksfamily\IloksClass\scripts\var.py) la valeur phone_mode ligne 68: phone_mode=False")

debug_mode=1
InitialiseFenetre()

#from AfficheCarte import *
from ClassesBlocs13 import *
from Menus11 import *
############################################


import tkinter, inspect
import ClassesBlocs13
import Autobuild2v0


for name, objet in inspect.getmembers(ClassesBlocs13):
    if inspect.isclass(objet):
        if issubclass(objet, Mobile) and name not in['Boule', 'Barre', 'CaptFeu', 'Mobile', 'Joueur','JoueurCarte' '', 'Mongolfier'] and not issubclass(eval(name), Boule) and objet.zone!='virtuel':
            mobiles.append(name)
        
listeBMD=[]
for i in range(3):
    listeBMD.append([])
    
for name, obj in inspect.getmembers(ClassesBlocs13):
    if inspect.isclass(obj) and name!='Drapeau':
        if issubclass(obj, Bloc):
            if obj.zone!='virtuel':
                listeBMD[0].append(name)
        if issubclass(obj, Mobile) and obj!=Joueur:
            if obj.zone!='virtuel':
                listeBMD[1].append(name)
        if issubclass(obj, Decor):
            if obj.zone!='virtuel':
                listeBMD[2].append(name)
        
##listeBlocs=['a','b','c','dsdcqsdcqsdc','b','c','d','b','c','d','b','c','d']
##listeMobiles=['aa','bb','cdc','d']
##FamChoix=[['Blocs',listeBlocs],['Mobiles',listeMobiles]]

def listesChoix(FamillesChoix):
    fenetre=tkinter.Tk()
    #fenetre.geometry('300x300')
    #tkinter.Label(fenetre,text='Que veux-tu tester?').pack()
    
    frame1=tkinter.LabelFrame(fenetre, borderwidth=3)
    frame1.grid(row=0,column=0,padx=10, pady=10)
    #value=tkinter.IntVar()
    bouton=[]
    cadre=[]
    boutonTout=[]
    boutonRien=[]
    var=[]
    def toutselectionner(i):
        for j in bouton[i]:
            j.select()
    def rienselectionner(i):
        for j in bouton[i]:
            j.deselect()
    def afficher():
        for i in var:
            for j in i:
                print(j.get())
    def quitter():
        global choix
        choix=[]
        for i in var:
            choix.append([])
            for j in i:
                choix[len(choix)-1].append(j.get())
        print(choix)
        fenetre.quit()

    global i
    i=0
    colonne=0
    for famille in FamillesChoix:
        cadre.append(tkinter.LabelFrame(frame1, text=famille[0], borderwidth=3, width=120, height=100))
        cadre[i].grid(row=0, column=colonne,padx=10, pady=10)
        bouton.append([])
        var.append([])
        colonnelocale=0
        rangee=0
        for texte in famille[1]:
            var[i].append(tkinter.IntVar())
            bouton[i].append(tkinter.Checkbutton(cadre[i],text=texte, variable=var[i][len(bouton[i])], anchor='w'))
            bouton[i][len(bouton[i])-1].grid(row=rangee, column=colonnelocale, padx=5, pady=1) #pack()
            rangee+=1
            if rangee>9:
                rangee-=10
                colonne+=1
                colonnelocale+=1
        print(i, eval('i',globals()))

        i+=1
        colonne+=1

    boutonTout.append(tkinter.Button(cadre[0],text='Tout', command=lambda: toutselectionner(0)))
    boutonTout[0].grid(row=11, column=colonnelocale) 
    boutonRien.append(tkinter.Button(cadre[0],text='Rien', command=lambda: rienselectionner(0)))
    boutonRien[0].grid(row=11, column=colonnelocale+1)
        
    boutonTout.append(tkinter.Button(cadre[1],text='Tout', command=lambda: toutselectionner(1)))
    boutonTout[1].grid(row=11, column=colonnelocale) 
    boutonRien.append(tkinter.Button(cadre[1],text='Rien', command=lambda: rienselectionner(1)))
    boutonRien[1].grid(row=11, column=colonnelocale+1)

    boutonTout.append(tkinter.Button(cadre[2],text='Tout', command=lambda: toutselectionner(2)))
    boutonTout[2].grid(row=11, column=colonnelocale) 
    boutonRien.append(tkinter.Button(cadre[2],text='Rien', command=lambda: rienselectionner(2)))
    boutonRien[2].grid(row=11, column=colonnelocale+1)
    
    difficulte=tkinter.IntVar()
    boutonDiff=tkinter.Scale(frame1,orient='horizontal', from_=0, to=10, variable=difficulte)
    boutonDiff.grid(row=1, column=0)
    boutonOk=tkinter.Button(frame1,text='OK', command=quitter) #fenetre.quit
    boutonOk.grid(row=1, column=1) #pack() #side=RIGHT,padx=5,pady=5)

    liste_defaut=['Sol','Brique','Goombas','Tortue']
    for i in range(len(listeBMD)-1):
        for j in range(len(listeBMD[i])-1):
            if listeBMD[i][j] in liste_defaut:
                var[i][j].set(1)
    difficulte.set(2)

    fenetre.mainloop()
    return([difficulte.get(),choix])

zones=["savane"]#['mario','savane','bermat','aqua']
########################################"""
listeBMDmulti=[]
for j in range(len(zones)):
    listeBMDmulti.append([])
    for i in range(3):
        listeBMDmulti[j].append([])

    for name, objet in inspect.getmembers(ClassesBlocs13):
        if inspect.isclass(objet) and name!='Drapeau':
            if issubclass(objet, Bloc) and name!='Mobloc':
                if zones[j] in objet.zone:
                    listeBMDmulti[j][0].append(name)
            if issubclass(objet, Mobile) and obj!=Joueur:
                if zones[j] in objet.zone:
                    listeBMDmulti[j][1].append(name)
            if issubclass(objet, Decor):
                if zones[j] in objet.zone:
                    listeBMDmulti[j][2].append(name)
##########################################"
random.randint(0,len(zones)) #z=2#
zone=random.choice(zones)
print(zone)
#listeBMD=listeBMDmulti[z]
[difficulte,choix]=listesChoix([['Blocs',listeBMD[0]],['Mobiles',listeBMD[1]],['Decors',listeBMD[2]]])

listeBMDfiltre=[[],[],[]]
for i in range(len(choix)):
    for j in range(len(choix[i])):
         if choix[i][j]==1:
             listeBMDfiltre[i].append(listeBMD[i][j])
print(difficulte)
print(listeBMDfiltre)
pick=Autobuild2v0.autobuild(difficulte, 'Niv_TK', zone, listeBMDfiltre)
print('2:', pick)
if phone_mode:
    Connexion()
while True:
    jeu=Jeu(-2,0,pick)
    time.sleep(1)
    jeu.run()
