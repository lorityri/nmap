"""
MIT License

Copyright (c) 2022 nmrr (https://github.com/nmrr)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


#!/usr/bin/python3
from ippublic import *    
from sys import platform
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from os import *
from subprocess import PIPE, Popen
import sys
import webbrowser

#variable Global
result_extrat=""

fenetre = Tk()

# Limiter les dimensions d’affichage de la fenêtre principale : 
fenetre.maxsize(900,1000)
fenetre.minsize(900,1000)

# Ajout d'un titre à la fenêtre
fenetre.title("jejenmap")

# Définir un icone :
fenetre.iconbitmap("icon1.ico")

#detection os
if platform == "linux" or platform == "linux2":
    os = "shell"

elif platform == "darwin":
    os = "shell"

elif platform == "win32":
    os = "cmd"

def aidenmap():
        webbrowser.open("https://nmap.org/man/fr/index.html")


def propos():
   messagebox.showinfo("A propos", "Create by JeremieG")

def quit():
    if messagebox.askokcancel("QUITTER", "étés vous sur de vouloir quitter"):
        fenetre.quit()


def save_as():
    global result_extrat
    result_extrat = filedialog.asksaveasfilename()
    open(result_extrat, "w").write(text_editor.get(0., tk.END))



commande_nmap = StringVar()

#Definition de la liste Combobox
def action(event):
    
    # Obtenir l'élément sélectionné 
    select = listeCombo.get()
    if select == "scan simple":
        commande_nmap.set("nmap -sn ")
    elif select == "scan normal":
        commande_nmap.set("nmap -sVt ")
    elif select == "scan intence":
        commande_nmap.set("nmap -sVy ")
    elif select == "scan puissant":
        commande_nmap.set("nmap -A ")

 

#Definition du bonton scan
def bp_scan():
    global result_extrat
    readOnlyText.config(state='normal')
    readOnlyText.delete("1.0","end")
    comande_nmap5=commande_nmap.get() + ipvic.get()
    result = Popen(comande_nmap5, shell=True, stdout=PIPE, universal_newlines=True).communicate()[0]
    readOnlyText.insert(1.0, result)
    #print(type(result))
    copy_result = result.strip()
    readOnlyText.config(state='disabled')


def copie():
    global result_extrat
    #fonction copier
    fenetre.clipboard_clear()
    fenetre.clipboard_append(copy_result)

#Creation du menu bar
menubar = Menu(fenetre)

#menu bar 1
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Ouvrir")
menu1.add_command(label="Enregistrer", command=save_as)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quit)  
menubar.add_cascade(label="Fichier", menu=menu1, font=("arial", 10))

#menu bar 2
menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Copier", command=copie)
menubar.add_cascade(label="Editer", menu=menu2, font=("arial", 10))
 
#menu bar 3
menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Aide NMAP", command = aidenmap)
menu3.add_command(label="A propos", command = propos)
menubar.add_cascade(label="Aide", menu=menu3, font=("arial", 10))

#recuperation IP publique
from requests import get
ip = get('https://api.ipify.org').text     
label = Label(fenetre, text="IP Publique = " + str(ip), font=("arial", 12)) 
label.config(bg="white")                   
label.place(x=20, y=10)

# Variable IP victime
labelcible = Label(fenetre, text="Cible: ", font=("arial", 12))
labelcible.place(x=270, y=10)
ipvic = StringVar(fenetre, value="IP victime")

#entre de l'IP victime
entréevic = Entry (fenetre, textvariable=ipvic, font=("arial", 12))
entréevic.place(x=320, y=10)

#liste Combobox
listeProduits=["scan simple", "scan normal","scan intence","scan puissant"]
listeCombo = ttk.Combobox(fenetre, values=listeProduits, font=("arial", 12))
listeCombo.current(0)
listeCombo.place(x=600, y=10)
listeCombo.bind("<<ComboboxSelected>>", action)

#Boutton scan
btnscan = Button(fenetre, text ="scan", command=bp_scan, font=("arial", 12)) #command = msgCallBack
btnscan.config(bg="white")
btnscan.place(x=830, y=5)

#label commande
labelcommande = Label(fenetre, text="Commande: ", font=("arial", 12))
labelcommande.place(x=20, y=50)

#entre de la commande nmap
commande = Entry (fenetre, textvariable=commande_nmap, font=("arial", 12), width=80) #commande_nmap, textvariable=
commande.place(x=150, y=50)

#label sortie
labelcommande = Label(fenetre, text="sortie: ", font=("arial", 12))
labelcommande.place(x=20, y=130)

#text read only
readOnlyText = Text(fenetre, width=105,height=50)
readOnlyText.config(state='disabled')
readOnlyText.place(x=20, y=150)

#boucle fenetre
fenetre.config(menu=menubar)
fenetre.mainloop()
