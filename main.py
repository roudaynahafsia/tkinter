from tkinter import Tk, Frame, Menu, Message

from categorie.views import CategorieView
from produits.views import ProduitView

class Main:

    def __init__(self):
        self.root = Tk()
        self.root.geometry('700x600')
        self.root.title('GESTION DE STOCK')

        # Frame pour le message en haut
        self.top_message = Message(self.root, text='Application de gestion de stock', width=600)
        self.top_message.pack(pady=10)

        # Frames des différentes vues, initialement None
        self.frame_produit = None
        self.frame_categorie = None

        # Menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label='Categorie', command=self.show_categorie)
        self.menu.add_command(label='Produit', command=self.show_produit)

        # Affiche la catégorie par défaut au démarrage
        self.show_categorie()

        self.root.mainloop()

    def hide_all_frames(self):
        '''Cache toutes les frames si elles existent'''
        if self.frame_categorie is not None:
            self.frame_categorie.pack_forget()
        if self.frame_produit is not None:
            self.frame_produit.pack_forget()

    def show_categorie(self):
        self.hide_all_frames()
        if self.frame_categorie is None:
            self.frame_categorie = Frame(self.root)
            CategorieView(self.frame_categorie)
        self.frame_categorie.pack(fill='both', expand=True)

    def show_produit(self):
        self.hide_all_frames()
        if self.frame_produit is None:
            self.frame_produit = Frame(self.root)
            ProduitView(self.frame_produit)
        self.frame_produit.pack(fill='both', expand=True)


if __name__ == "__main__":
    Main()
