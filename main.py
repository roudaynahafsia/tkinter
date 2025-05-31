from tkinter import Tk, Frame, Menu, Message
from categorie.views import CategorieView
from produits.views import ProduitView
from auth.login import LoginPage
from auth.register import RegisterPage

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('700x600')
        self.root.title('GESTION DE STOCK')

        self.current_frame = None
        self.show_login()

        self.root.mainloop()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginPage(self.root, self.show_main_menu, self.show_register)
        self.current_frame.pack(fill='both', expand=True)

    def show_register(self):
        self.clear_frame()
        self.current_frame = RegisterPage(self.root, self.show_login)
        self.current_frame.pack(fill='both', expand=True)

    def show_main_menu(self):
        self.clear_frame()

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label='Categorie', command=self.show_categorie)
        self.menu.add_command(label='Produit', command=self.show_produit)
        self.menu.add_command(label='Déconnexion', command=self.logout)

        self.top_message = Message(self.root, text='Application de gestion de stock', width=600)
        self.top_message.pack(pady=10)

        self.frame_categorie = None
        self.frame_produit = None
        self.show_categorie()

    def hide_all_frames(self):
        if self.frame_categorie:
            self.frame_categorie.pack_forget()
        if self.frame_produit:
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

    def logout(self):
        self.menu.delete(0, 'end')
        self.top_message.destroy()
        if self.frame_categorie: self.frame_categorie.destroy()
        if self.frame_produit: self.frame_produit.destroy()
        self.show_login()

if __name__ == "__main__":
    App()
