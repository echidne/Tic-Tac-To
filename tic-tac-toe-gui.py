# un jeu morpion avec Python et GUI
"""
A tic_tac_toe game built with Python an Tkinter
"""

### les imports

import tkinter as tk
from tkinter import font as tkfont
from itertools import cycle # permet de créer un itérateur qui renvoie les éléments de l'itérable en en sauvegardant une copie
from typing import NamedTuple # on importe une version supportant le typage de collections.NamedTuple

## on crée les classes Joueur et Coup

class Joueur(NamedTuple):
    """ attributs des joueurs """
    marque: str # X ou O
    couleur: str # defini la couleur

class Coup(NamedTuple):
    """ attributs des coups à jouer """
    ligne: int
    col: int
    marque: str="" # la marque est définie vide car le coup n'a pas été joué

### les variables globales

TAILLE_PLATEAU = 3 # la taille de plateau par défaut
JOUEURS = (
    Joueur(marque="X", couleur="blue"),
    Joueur(marque="O", couleur="green"),
) # on crée 2 joueurs par défaut

class Jeu:
    """classe qui va représenter la logique du jeu
    les attributs suivant sont créés:
    ._joueurs : un iterateur sur le tuple de type de joueurs (X ou O)
    ._taille_du_plateau : la taille du plateau
    .joueur_en_jeu : le joueur entrain de jouer
    .combo_vainqueur : La combinaison de cases qui a définit un vainqueur
    ._coup_joués : les coups joués par joueur dans une partie
    ._gagnant : un booléen pour savoir si le jeu a un gagnant ou non
    ._combo_gagnant : Une liste qui continet les combinaisons de cases possibles pour gagner
    """
    def __init__(self, joueurs=JOUEURS, taille_plateau=TAILLE_PLATEAU):
        self._joueurs = cycle(joueurs)
        self.taille_plateau = taille_plateau
        self.joueur_en_jeu = next(self._joueurs)
        self.combo_vainqueur = []
        self._coups_joués = []
        self._gagnant = False
        self._combo_gagnant = []
        self._preparation_plateau()
    
    def _preparation_plateau(self):
        """fonction qui calcule les valeurs initiales pour
        les coups possibles et les combiniasons gagnantes possibles
        """
        self._coups_possibles =[
            [Coup(ligne,col) for col in range(self.taille_plateau)]
            for ligne in range(self.taille_plateau)
        ]
        self._combo_gagnant = self._obtenir_combo_gagnant() # on apelle la focntion qui calcule les alignements gagnants
    
    def _obtenir_combo_gagnant(self):
        lignes=  [
            [(coup.ligne, coup.col) for coup in ligne]
            for ligne in self._coups_possibles
        ]
        cols= [list(col) for col in zip(*lignes)]
        prem_diag = [col[i] for i, col in enumerate(lignes)]
        sec_diag = [col[j] for j, col in enumerate(reversed(cols))]
        return lignes + cols + [prem_diag + sec_diag]

    def inversion_joueur(self):
        """ retourne le joueur suivant """
        self.joueur_en_jeu = next(self._joueurs)
    
    def verification_coup(self, coup):
        """ vérifie si le coup est valide. Retourne vrai si oui """
        ligne, col = coup.ligne, coup.col # on récupère la position
        coup_pas_joué = self._coups_joués[ligne][col].marque == "" # on vérifie si la position est vide
        pas_de_gagnant = not self._gagnant # vérfie si le jeu a un gagnant
        return pas_de_gagnant and coup_pas_joué # S'il n'y avait pas de gagnant et si la position est valide alors le coup est valide
    
    def jouer(self, coup):
        """ On joue le coup et on vérifie si c'est gagnant"""
        ligne, col = coup.ligne, coup.col # on récupère la position
        self._coups_joués[ligne][col] = coup
        for combo in self._combo_gagnant:
            resultats = set(self._coups_joués[i][j].marque for i,j in combo) # on effectue un set sur une expression génratrice pour récupérer toutes les marques dans la combo gagnante actuelle
            est_gagnant = (len(resultats) ==1) and ("" not in resultats) # booléen quidétermine si le coup joué est gagnant ou pas
            if est_gagnant:
                self._gagnant = True # si le coup est gagnant alors on a un joueur gagnant
                self.combo_vainqueur = combo # on récupère la combinaison gagnante
                break # si on a un coup gagnant on arrète la boucle
    
    def gagnant(self):
        """ returne vrai si on a un joueur gagnant"""
        return self._gagnant
    
    def pat(self):
        """ retourne vrai si il ne peut plus avoir de gagnant"""
        pas_de_gagnant = not self._gagnant
        coup_jouable = all(coup.marque for ligne in self._coups_joués for coup in ligne) # vrai s'il n'y a pas une cellule vide dans les  coups joués
        return pas_de_gagnant and coup_jouable

    def reset(self):
        """ remet le jeu à l'état initial"""
        for ligne, contenu_ligne in enumerate(self._coups_joués):
            for col, _ in enumerate(contenu_ligne):
                contenu_ligne[col] = Coup(ligne, col) # comme la marque est par défaut "" on reset toutes les cases en cases vides
        self._gagnant = False
        self.combo_vainqueur = []
    



    



class PlateauMorpion(tk.Tk): # la classe hérite de la classe Tk de tkinter qui permet de créer une fenêtre
    def __init__(self, jeu):
        super().__init__() # on appelle l'init de tk.Tk
        self.title("Un jeu de Morpion") # le titre de la fenètre
        self._cells ={}  # ceci va initilaiser les boutons
        self._jeu =  jeu
        self._affichage_du_plateau()
        self._creation_de_la_grille()
        self.geometry('400x400')

    def _creer_menu(self):
        barre_menu = tk.Menu(master=self)
        self.config(menu=barre_menu)
        file_menu = tk.Menu(master=barre_menu)
        file_menu.add_command(label="Jouer Encore", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Sortir", command=quit)
        barre_menu.add_cascade(label="Fichier", menu=file_menu)

    def _affichage_du_plateau(self):
        """creation du plateau"""
        # On crée un objet Frame pour contenir l'affichage du jeu:
        affichage_frame = tk.Frame(master =self) # Notez que l'argument maître est fixé à self, ce qui signifie que la fenêtre principale du jeu sera le parent du cadre.
        # On affiche le cadre sur le bord supérieur de la fenêtre principale
        affichage_frame.pack(fill=tk.X) # tk.X permet de s'assurer que le plateau sera redimensionné en même temps que la fenêtre
        # On crée un titre. Ce titre doit être lié à la Frame. On demmande si le joueur est pret et on défini une taille et un style de caractère.
        self.affichage = tk.Label(
            master = affichage_frame,
            text = "Pret?",
            font=tkfont.Font(size=28, weight="bold"),
        )
        self.affichage.pack()

    def _creation_de_la_grille(self):
        """création de la grille du plateau"""
        # On crée le cadre qui contient la grille. En metttant l'argument master = self on précise que c'est la fenêtre principale qui contient le cadre
        cadre_grille = tk.Frame(master= self)
        cadre_grille.pack()
        # on crée les cases qui sont en fait des boutons. Ici c'est du 3x3 
        for ligne in range(self._jeu.taille_plateau):
            self.rowconfigure(ligne, weight=1, minsize =50)
            self.columnconfigure(ligne , weight=1, minsize =50)
            for col in range(self._jeu.taille_plateau):
                bouton = tk.Button(
                    master = cadre_grille,
                    text = "",
                    font = tkfont.Font(size =36, weight = 'bold'),
                    fg ="black",
                    width = 3,
                    height = 1,
                    highlightbackground = 'lightblue'
                )
                self._cells[bouton] = (ligne,col)
                bouton.grid(
                    row = ligne,
                    column = col,
                    padx = 5,
                    pady = 2,
                    sticky = "nsew"
                )
                bouton.bind("<ButtonPress-1>", self.coup_joueurs)
                bouton.grid(row=ligne, column=col, padx=5, pady=5, sticky="nsew")

    def coup_joueurs(self, evenement):
        """ ceci va permettre de gérer les coups des joueurs sur le plateau """
        bouton_cliqué = evenement.widget
        ligne, col = self._cells[bouton_cliqué]
        coup = Coup(ligne, col, self._jeu.joueur_en_jeu.marque)
        if self._jeu.verification_coup(coup):
            self._mise_a_jour_bouton(bouton_cliqué)
            self._jeu.jouer(coup)
            if self._jeu.pat():
                self._mise_a_jour_affichage(msg="Partie Nulle!", color="red")
            elif self._jeu.gagnant():
                self._rougir_cases()
                msg = f'Le joueur "{self._jeu.joueur_en_jeu.marque}" a gagné!'
                color = self._jeu.joueur_en_jeu.couleur
                self._mise_a_jour_affichage(msg, color)
            else:
                self._jeu.inversion_joueur()
                msg = f"C'est le tour de {self._jeu.joueur_en_jeu.marque}"
                self._mise_a_jour_affichage(msg)

    def _mise_a_jour_bouton(self, bouton_cliqué):
        bouton_cliqué.config(text = self._jeu.joueur_en_jeu.marque)
        bouton_cliqué.config(text = self._jeu.joueur_en_jeu.couleur)


    def _mise_a_jour_affichage(self, msg, color= "black"):
        self.display["text"] = msg
        self.display['fg'] = color

    def _rougir_cases(self):
        for bouton, coordonées in self._cells.items():
            if coordonées in self._jeu.combo_vainqueur:
                bouton.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._jeu.reset()
        self._mise_a_jour_affichage(msg="Pret?")
        for bouton in self._cells.keys():
            bouton.config(highlightbackground="lightblue")
            bouton.config(text="")
            bouton.config(fg="black")
        
def main():
    """crée le palteau de jeu et lance la boucle"""
    jeu = Jeu()
    board = PlateauMorpion(jeu)
    board.mainloop()

if __name__ == "__main__":
    main()

        