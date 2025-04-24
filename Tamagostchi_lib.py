


class T_game():
    '''Creation class T_game avec les parametres du jeux
       et 2 methodes pour sauvegader et charger la partie
    '''
    def __init__(self, nb_tamagotchi, nb_croquettes):
        '''
            call Database().get_flag()
        '''
        self.nb_tamagotchi = nb_tamagotchi
        self.nb_croquettes = nb_croquettes
        self.dormir_min = 30   #dormin minimum 30s
        self.dormir_max = 60    #dormir maximum 60s
        
        self.message = ''
        self.b_pause = False
        self.b_save_game = False
        self.b_load_game = False
        
        self.tama_faim_initial = 200
        self.tama_ennui_initial = 200
        self.tama_soif_initial = 100
        self.tama_name = ['Picachu','Babytchi','Marutchi', 'Tamatchi', 'Mametchi'];
        self.ligne_tetes_frame = None  #emplacement des tetes
        self.tetes = []  #emplacement des tetes
        self.tetes_color = ["pink","pink","pink","pink","pink"]  #couleur des tetes



    def save_game(self):
        print("=====================================>")

       

        self.message = 'Sauvegarde de la partie faite le jeux est mis en pause'
        self.b_pause = True
        self.b_save_game = True 
        
    def load_game(self):
        print("======= load Game==============================>")

        self.message = 'Partie Sauvegardé chagée le jeux est mis en pause'
        self.b_pause = True
        self.b_load_game = True 