import sys
import os
import time
import re  #regular expression
import random

from tkinter import *
from tkinter import messagebox

from Tamagostchi_lib import *

game = T_game(nb_tamagotchi = 5, nb_croquettes = 50)  #cretion game avec 5 tamagotchi, 50 croquettes 


#variable globale
tamagotchi_list = []   #Creation list vide : tamagotchi_list
for i in range(game.nb_tamagotchi):
    tamagotchi_list.append({"name": '', "faim": game.tama_faim_initial, "soif":game.tama_soif_initial ,"ennui": game.tama_ennui_initial , "santé":200, "fatigue":200,"dormir" : 0})  #Rajout de dictionaire dans la list

jour  = 0  # intialisation - premier jour
b_fin_de_partie = False
b_redemarrer = False
b_first_launch = True
elapsed_time = 0
def quitter():
    '''
        Fonctiont pour quitter le Jeux
    '''
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter le jeux Tamagotchi?"):
        windows.destroy()        
        
def redmarrer():
    global b_redemarrer
    b_redemarrer = True
    if messagebox.askokcancel("Redmarrer", "Voulez-vous redémarrer la partie?"):
        restart_game()
        
def pause():      # a chaque appuie je pause ou continue
    global start_time_label
    global elapsed_time
    
    if  game.b_pause == False: 
        game.b_pause = True
        game.message = "Partie en pause"
        #sauvegarder le temps ecoule
        elapsed_time = int(time.time() - start_time_label)
    else:
        game.b_pause = False
        game.b_save_game = False #on remet la sauvegarde a False 
        start_time_label = start_time_label+elapsed_time  # Enregistrer le temps de départ + temps ecoule pendans la pause
        update_timer()  # Relancer on n'est plus en pause
        
    
    
def aide():
    aide_window = Toplevel(windows)
    aide_window.title("Aide")
    texte_aide = '''
    Bienvenu dans le jeux Tamagotchi
    Vous possedez 5 Tamagotchis
    Pour chaque tamagotchi  la faim, la soif, la santé, et l'ennui et la fatigue doivent etre gerées
    Pour Nourrir un Tamagotchi vous posseder 50 croquette
    Si 1 Tamagotchi possede moins de 10 point de soif il devient bleu
    Si 1 Tamagotchi est n'a plus de point d'ennui il se bat avec les autres, il est en colere
    Si 1 Tamagotchi possede moins de 100 point de faim il devient orange
    Si 1 Tamagotchi possede moins de 50 point de faim il devient rouge

    
    '''
    
    label_aide = Label(aide_window, text=texte_aide)
    label_aide.pack(padx=20, pady=20)
    
def jouer():
    global start_time_label
    global elapsed_time
    global b_first_launch
    
    if b_first_launch:
        start_time_label = time.time()  # Enregistrer le temps de départ
        update_timer()  # Mettre à jour    
        b_first_launch = False 
    
    if  game.b_pause == True: 
        game.b_pause = False
        start_time_label = start_time_label+elapsed_time  # Enregistrer le temps de départ + temps ecoule pendans la pause
        update_timer()  # Relancer on n'est plus en pause

        
        
    
def restart_game():
    global b_fin_de_partie
    global start_time_label
    global tamagotchi_list
    global b_redemarrer
    global jour
    print("restart_game")
    for  i in range(len(tamagotchi_list)):
        tamagotchi_list[i]['faim'] =  game.tama_faim_initial 
        tamagotchi_list[i]['soif'] = game.tama_soif_initial 
        tamagotchi_list[i]['ennui'] = game.tama_ennui_initial
        tamagotchi_list[i]['santé'] = 200 
        tamagotchi_list[i]['fatigue'] = 200 
        tamagotchi_list[i]['dormir'] = 0 
    jour = 0
    b_redemarrer = False
    start_time_label = time.time()  # Enregistrer le temps de départ
    b_fin_de_partie = False
    game.nb_croquettes = 50 #on commence chaque journée avec 50 croquettes
    game.b_pause = False 
    game.message = "nouvelle Partie"
    update_timer()  # Mettre à jour les etats et lancer le timer
    
def draw_tete(index = 0, color = "pink", b_sourcils = False, b_colere = False):
        color_tete = color
        if(not b_colere):
            game.tetes[index].create_oval(10, 10, 55, 55, fill=color_tete)  # Tete
        else:
            game.tetes[index].create_oval(10, 10, 55, 55, fill=game.tetes_color[i])  # On garde la couleur precedente

            
        game.tetes[index].create_oval(17, 20, 17+10, 30, fill="black")  # Oeil gauche
        game.tetes[index].create_oval(39, 20, 39+10, 30, fill="black")  # Oeil droit
        if(b_colere):
            game.tetes[index].create_arc(15, 38, 50, 58, start=0, extent=180, style=ARC)  # Bouche colere
        else:
            game.tetes[index].create_arc(15, 30, 50, 50, start=180, extent=180, style=ARC)  # Sourire
        # Ajout des sourcils en colère
        if b_sourcils:
            game.tetes[index].create_line(17, 22, 28,12, width=2)  # Sourcil gauche
            game.tetes[index].create_line(41, 12, 52, 22, width=2)  # Sourcil droit
        game.tetes[index].pack(side=LEFT, padx=10, pady=1)
        
        game.tetes_color[index] = color
    #input()
def update_states():
    global b_fin_de_partie
    global tamagotchi_list
    #print("update_states")
    
    for  i in range(len(tamagotchi_list)):

        #print("i=",i)
        '''
            Chaque seconde de sommeil fait gagner 1 point de santé, 1 point d’ennui et 1 point de fatigue.
            Chaque seconde d’éveil fait perdre 5 points de faim et 3 points d’ennui
        '''

        #Si le tamagotchi dort on retire 1
        if (tamagotchi_list[i]['dormir'] > 0) :
            tamagotchi_list[i]['dormir'] += -1
            label[5][i].configure(text='dormir' + "\n"+str(tamagotchi_list[i]['dormir']))     #maj label  dormir
            tamagotchi_list[i]['santé'] += 1         # tamagotchi gagne  1 point de santé
            tamagotchi_list[i]['ennui'] += 1        # tamagotchi gagne   1 point d'ennui 
            tamagotchi_list[i]['fatigue'] += 1        # tamagotchi gagne   1 point de fatigue 
        else: #le tamagotchi ne dort pas il est eveillé
            tamagotchi_list[i]['faim'] += -5         # tamagotchi perd   5 points de faim chaque seconde
            tamagotchi_list[i]['ennui'] += -3         # tamagotchi perd  3 points de ennui chaque seconde
            tamagotchi_list[i]['soif'] += -2         # tamagotchi perd  2 points de soif chaque seconde
            
        
        #print("Tamagotchi numero ", i+1)
        #print(" faim", tamagotchi_list[i]['faim'])
        #print(" santé", tamagotchi_list[i]['santé'])
        #print(" ennui", tamagotchi_list[i]['ennui'])


            


        if tamagotchi_list[i]['faim'] <=50 :
            draw_tete(i,"red")
        elif  tamagotchi_list[i]['faim'] <=100 :
            draw_tete(i, "orange")
         
        elif tamagotchi_list[i]['soif'] <=10 :
            draw_tete(i,"blue")
            
        elif  tamagotchi_list[i]['faim'] > 100 :
            draw_tete(i, "pink")

            
        #Si la faim ou la santé ou la fatigue d’un seul des animaux passe à zéro, la partie est perdue
        
        if tamagotchi_list[i]['faim'] <= 0:
                tamagotchi_list[i]['faim'] = 0
                label[0][i].configure(text='faim' + "\n"+str(tamagotchi_list[i]['faim']))     #maj label  faim
                game.message = game.tama_name[i]  +" est mort de faim"
                communication_label.configure(text= " " + game.message)
        if tamagotchi_list[i]['soif'] <= 0:
                tamagotchi_list[i]['soif'] = 0
                label[0][i].configure(text='soif' + "\n"+str(tamagotchi_list[i]['soif']))     #maj label  faim
                game.message = game.tama_name[i]  +" est mort de soif"
                communication_label.configure(text= " " + game.message)


        if tamagotchi_list[i]['fatigue'] < 0:
                 tamagotchi_list[i]['fatigue'] = 0
                 label[3][i].configure(text='fatigue' + "\n"+str(tamagotchi_list[i]['fatigue']))     #maj label  fatigue
                 game.message = game.tama_name[i]  + " est mort de fatigue"
                 communication_label.configure(text= " " + game.message)
        if tamagotchi_list[i]['santé'] < 0:
                tamagotchi_list[i]['santé'] = 0
                label[2][i].configure(text='santé' + "\n"+str(tamagotchi_list[i]['santé']))     #maj label  santé 
                game.message =game.tama_name[i] + " est mort de santé"
                communication_label.configure(text= " " + game.message)
                
        #Si l’ennui d’un des tamagotchis passe à zéro, il commence à se battre avec les autres et, tant  qu’il est à zéro, tous les animaux perdent 5 points de santé par seconde.
        if tamagotchi_list[i]['ennui'] <= 0:
            tamagotchi_list[i]['ennui'] = 0
            name_label[game.tama_name[i]].configure(text= " " + game.tama_name[i] + "\n est enervé")
            communication_label2.configure(text= "Bagarre Generale!")
            #axe y oriente vers le bas
            draw_tete(i, "pink",b_colere = True, b_sourcils = True)
        else:
            name_label[game.tama_name[i]].configure(text= " " + game.tama_name[i])
            
            
        label[0][i].configure(text='faim' + "\n"+str(tamagotchi_list[i]['faim']))     #maj label  faim
        label[1][i].configure(text='soif' + "\n"+str(tamagotchi_list[i]['soif']))     #maj label  soif
        label[2][i].configure(text='ennui' + "\n"+str(tamagotchi_list[i]['ennui']))     #maj label  ennui
        label[3][i].configure(text='santé' + "\n"+str(tamagotchi_list[i]['santé']))     #maj label  santé
        label[4][i].configure(text='fatigue' + "\n"+str(tamagotchi_list[i]['fatigue']))     #maj label  fatigue
            
            

    b_enervement = False     # aucun T n'est enervé
    for  i in range(len(tamagotchi_list)):
        if  tamagotchi_list[i]['ennui'] == 0: # l' ennui d’un des tamagotchis passe à zéro
            b_enervement = True
            
    if b_enervement:
         for  i in range(len(tamagotchi_list)):
             tamagotchi_list[i]['santé'] += -5  #tous les animaux perdent 5 points de santé par seconde
    else: #tous les Tama sont calme pas de bagarre generale
        communication_label2.configure(text= "")
             
             
    b_fin_de_partie = False
    for  i in range(len(tamagotchi_list)):
        if (tamagotchi_list[i]['faim'] == 0 or  tamagotchi_list[i]['fatigue'] == 0 or  tamagotchi_list[i]['santé'] == 0 or  tamagotchi_list[i]['soif'] == 0 ):
            b_fin_de_partie = True
    
    return (b_fin_de_partie)
    



def update_timer():
    global jour
    global b_fin_de_partie
    global start_time_label
    global  b_redemarrer
    global  nb_seconds
    elapsed_time = int(time.time() - start_time_label)  #temps ecoule
    nb_seconds = elapsed_time % 180
    print("elapsed_time", elapsed_time)
    timer_label.configure(text= "jour:" + str(jour) +"   {} secondes".format(elapsed_time % 180)  +  "    Croquettes =" + str(game.nb_croquettes))
    communication_label.configure(text= " " + game.message)
    '''
    La journée d’un tamagotchi dure 3 minutes avec une période de sommeil allant de 30 à 60 secondes 
    (valeur aléatoire) 
    '''
    if (elapsed_time % 180 == 0):            #si 3m (180s) on passe au jour suivant
        jour += 1
        elapsed_time = 0 #on remet a zero le compter de 180s
        game.nb_croquettes = 50 #on redonne 50 nouvelles croquettes
        for  i in range(len(tamagotchi_list)):
            dormir_secondes = random.randint(game.dormir_min, game.dormir_max)  #La journée d’un tamagotchi dure 3 minutes avec une période de sommeil allant de 30 à 60 secondes 
            tamagotchi_list[i]['dormir'] = dormir_secondes
            label[5][i].configure(text='dormir' + "\n"+str(tamagotchi_list[i]['dormir']))     #maj label  dormir
    else:
        b_fin_de_partie = update_states()
    
    #print('b_fin_de_partie', b_fin_de_partie)
    
    if b_fin_de_partie:
        b_partie_en_cours = False
    elif b_redemarrer:
        b_partie_en_cours = False
    elif game.b_pause:   #la partie est en pause
        b_partie_en_cours = False
        if game.b_save_game:
            communication_label.configure(text= " " + game.message)
    else:
        b_partie_en_cours = True 
        
    if  b_partie_en_cours :
        windows.after(1000, update_timer)  # Met à jour toutes les secondes
    if b_fin_de_partie:
        fin_de_partie()



    if game.b_save_game:  #on sauvegarde les donnees de la partie
        output_file = r'Tama_save_game.txt'
        target = open(output_file, 'w', encoding="utf-8")
        #target.write("Partie Sauvegarder \n")
        
        for  i in range(len(tamagotchi_list)):
               target.write(str(tamagotchi_list[i]['ennui']) + "\n") 
               target.write(str(tamagotchi_list[i]['santé']) + "\n") 
               target.write(str(tamagotchi_list[i]['faim']) + "\n") 
               target.write(str(tamagotchi_list[i]['soif']) + "\n") 
               target.write(str(tamagotchi_list[i]['dormir']) + "\n") 
               target.write(str(tamagotchi_list[i]['fatigue']) + "\n") 
        target.write(str(game.nb_croquettes) + "\n") 
        target.write(str(jour) + "\n") 
        target.write(str(nb_seconds) + "\n") 
        
        
        
        target.close()
        game.b_save_game = False
        
    if game.b_load_game:  #on charge les donnees de la partie enregistre
        output_file = r'Tama_save_game.txt'
        lines = tuple(open(output_file, 'r', encoding="utf8"))
        
        j=0
        for  i in range(len(tamagotchi_list)):
            tamagotchi_list[i]['ennui'] = int(lines[j].rstrip())
            tamagotchi_list[i]['santé'] =  int(lines[j+1].rstrip())
            tamagotchi_list[i]['faim'] =  int(lines[j+2].rstrip())
            tamagotchi_list[i]['soif'] =  int(lines[j+3].rstrip())
            tamagotchi_list[i]['dormir'] =  int(lines[j+4].rstrip())
            tamagotchi_list[i]['fatigue'] = int(lines[j+5].rstrip())
            j = j + 6 # 6 etats
            print(f"  dormir {tamagotchi_list[i]['dormir']}")
        game.nb_croquettes = int(lines[j].rstrip())
        jour = int(lines[j+1].rstrip())
        nb_seconds = int(lines[j+2].rstrip())
        game.b_load_game = False
                
        
    
    game.message = ""

     
def bouton_clic(num):
    actions = ['manger','boire','jouer']  #3 actions possonle


    action_en_cours = actions[num[0]]
    tamagotchi_num = num[1]
    print('action', actions[num[0]])
    print('Tamagotchi_num', num[1])
    '''
         Donner une croquette à manger à un tamagotchi pour lui faire gagner 50 points de faim 
         on  commence chaque journée avec 50 croquettes
         Jouer avec un tamagotchi pour lui faire gagner 50 points d’ennui. 
         Par contre, le tamagotchi perd aussi 50 points de fatigue.
    '''
    if (tamagotchi_list[tamagotchi_num]['dormir'] == 0) :
        if game.nb_croquettes ==  0:
            game.message = "Plus de Croquete"
        else:
            game.message = ""
        if action_en_cours == 'manger' and  game.nb_croquettes > 0:
                tamagotchi_list[tamagotchi_num]['faim'] += 50  #si le  tamagotchi ne dort pas on augmente la faim
                game.nb_croquettes = game.nb_croquettes - 1
                item= 'faim'
        elif action_en_cours == 'jouer':
                tamagotchi_list[tamagotchi_num]['ennui'] += 50     #tamagotchi gagne 50 points d’ennui
                tamagotchi_list[tamagotchi_num]['fatigue'] += -50  #tamagotchi perd aussi 50 points de fatigue
                item= 'ennui'
        elif action_en_cours == 'boire':
                tamagotchi_list[tamagotchi_num]['soif'] += 10     #tamagotchi gagne 10 de soif
                item= 'soif'

        label[num[0]][num[1]].configure(text=item + "\n"+str(tamagotchi_list[tamagotchi_num][item]))
    else:
        game.message = game.tama_name[tamagotchi_num] + " dort"
        
        

    
    


def fin_de_partie():
    #fin_de_partie_window = Toplevel(windows)
    #fin_de_partie_window.title("Fin de Partie")
    texte_fin_de_partie = '''
    Fin de Partie
    
    '''
    #label_fin_de_partie = Label(fin_de_partie_window, text=texte_fin_de_partie)
    #label_fin_de_partie.pack(padx=20, pady=20)  
    answer = messagebox.askyesno(" Partie terminer", "Voulez-vous redémarrer la partie?")
    if answer:
        print('restart_game')
        restart_game()
    else:
        windows.destroy()     
        
        
if __name__== "__main__" :
    #print(tamagotchi_list)
    
    '''
            Ajout de du Graphisme  
    
    '''
    
    # Création du widget principal
    windows = Tk()
    windows.title("Tamagotchi")
    # création des widgets "esclaves" :
    can1 = Canvas(windows, bg='dark grey', height=100, width=500)

    # Créer le menu
    menu_bar = Menu(windows)
    windows.config(menu=menu_bar)
    menu_fichier = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Menu", menu=menu_fichier)
    menu_fichier.add_command(label="Quitter", command=quitter)
    menu_fichier.add_command(label="Redmarrer", command=redmarrer)
    menu_fichier.add_command(label="Pause", command=pause)
    

    menu_bar.add_command(label="Aide", command=aide)
    
    menu_bar.add_command(label="save_game", command=game.save_game)
    menu_bar.add_command(label="load_game", command=game.load_game)
    menu_bar.add_command(label="Jouer", command=jouer)


    
    # Créer cinq formes de tête horizontales
    #creation des tetes representant les Tanagotchies
    for i in range(1):
        game.ligne_tetes_frame = Frame(windows)
        game.ligne_tetes_frame.pack()
        for j in range(game.nb_tamagotchi):
            game.tetes.append(Canvas(game.ligne_tetes_frame, width=60, height=55))  # 
            draw_tete(j, "pink")
    
    #input()  #mettre une pause
        
    
    # ajout des noms tamagotchi
    ligne_labels_frame = Frame(windows)
    ligne_labels_frame.pack()
    name_label= {}
    for name in game.tama_name:
        name_label[name] = Label(ligne_labels_frame, text=name, width=10)
        name_label[name].pack(side=LEFT, padx=5, pady=10)
    # Créer 6 lignes de 5 labels 
    label = [
                ["faim" ]*game.nb_tamagotchi,
                ["soif" ]*game.nb_tamagotchi,
                ["ennui" ]*game.nb_tamagotchi,
                ["santé" ]*game.nb_tamagotchi,
                ["fatigue" ]*game.nb_tamagotchi,
                ["dormir" ]*game.nb_tamagotchi]
    #print(label)
    #input()
    for i in range(6):
        ligne_labels_frame = Frame(windows)
        ligne_labels_frame.pack()
        if i == 0:
            data = 'faim'
        elif i ==1:
            data = 'soif'            
        elif i ==2:
            data = 'ennui'
        elif i ==3:
            data = 'santé'        
        elif i ==4:
            data = 'fatigue'
        elif i ==5:
            data = 'dormir'
            
        for j in range(game.nb_tamagotchi):
            label[i][j] = Label(ligne_labels_frame, text=data + "\n"+str(tamagotchi_list[j][data]), width=10)
            label[i][j].pack(side=LEFT, padx=5, pady=5)
            
    #input()  #mettre une pause

    #Creer 3 lignes de 5 buttons : manger et jouer et boire
    actions = ['manger','boire','jouer']
    for i in range(len(actions)):
        ligne_frame = Frame(windows)
        ligne_frame.pack()
        for j in range(game.nb_tamagotchi):
            num=i*5+j+1
            bouton = Button(ligne_frame, text= actions[i] + " ", width=10, command=lambda num=[i,j]: bouton_clic(num))
            bouton.pack(side=LEFT, padx=5, pady=5)
    #input()  #mettre une pause
    # Créer un label pour afficher le temps écoulé
    timer_label = Label(windows, text="Temps écoulé : 0 secondes")
    
    
    timer_label.pack()
    
    #ajout d'un moyen de communication
    communication_label = Label(windows, text="Cliquez sur jouer pour commencer la partie")  #communique des messages - comme : "plus de croquettes "
    communication_label.pack()
 
    communication_label2 = Label(windows, text="             ")  #communique des messages - comme : "Bagarre Generale"
    communication_label2.pack()
    
    
    #input()  #mettre une pause


    
    # démarrage du réceptionnaire d'évènements (boucle principale) :
    windows.mainloop()
    windows.destroy()
        

