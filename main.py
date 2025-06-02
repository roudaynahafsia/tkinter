from tkinter import Tk, Frame, Menu, Canvas
from categorie.views import CategorieView
from produits.views import ProduitView
from auth.login import LoginPage
from auth.register import RegisterPage

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('1000x700')  # Standardized size
        self.root.title('GESTION DE STOCK')

        self.colors = {
            'primary': '#007bff',
            'success': '#28a745',
            'danger': '#dc3545',
            'bg': '#f5f7fa',
            'header': '#2b2d42',
            'text': '#212529',
            'light_text': '#ffffff'
        }

        self._setup_ui()
        self.current_frame = None
        self.show_login()

        self.root.mainloop()

    def _setup_ui(self):
        """Configure l'interface principale avec un design moderne."""
        # Canvas pour fond dégradé
        self.canvas = Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        # Cadre principal pour centrer le contenu
        self.main_container = Frame(self.canvas, bg=self.colors['bg'])
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

    def _create_gradient(self):
        """Crée un fond dégradé."""
        width, height = 1000, 700
        self.canvas.config(width=width, height=height)
        
        for i in range(height):
            r = int(43 + (245-43) * i/height)
            g = int(45 + (247-45) * i/height)
            b = int(66 + (250-66) * i/height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def clear_frame(self):
        """Supprime le cadre actuel."""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login(self):
        """Affiche la page de connexion."""
        self.clear_frame()
        self.current_frame = LoginPage(self.main_container, self.show_main_menu, self.show_register)
        self.current_frame.pack(fill='both', expand=True)

    def show_register(self):
        """Affiche la page d'inscription."""
        self.clear_frame()
        self.current_frame = RegisterPage(self.main_container, self.show_login)
        self.current_frame.pack(fill='both', expand=True)

    def show_main_menu(self):
        """Affiche le menu principal et la vue par défaut (catégories)."""
        self.clear_frame()

        # Configure le menu moderne
        self.menu = Menu(self.root, bg=self.colors['header'], fg=self.colors['light_text'], 
                        font=('Segoe UI', 11), activebackground=self.colors['primary'], 
                        activeforeground=self.colors['light_text'], borderwidth=0)
        self.root.config(menu=self.menu)
        self.menu.add_command(label='Catégories', command=self.show_categorie)
        self.menu.add_command(label='Produits', command=self.show_produit)
        self.menu.add_command(label='Déconnexion', command=self.logout)

        # Cadre pour les vues (catégories/produits)
        self.view_frame = Frame(self.main_container, bg='white', relief='raised', borderwidth=2)
        self.view_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.frame_categorie = None
        self.frame_produit = None
        self.show_categorie()

    def hide_all_frames(self):
        """Cache tous les cadres de vues."""
        if self.frame_categorie:
            self.frame_categorie.pack_forget()
        if self.frame_produit:
            self.frame_produit.pack_forget()

    def show_categorie(self):
        """Affiche la vue des catégories."""
        self.hide_all_frames()
        if self.frame_categorie is None:
            self.frame_categorie = Frame(self.view_frame, bg='white')
            CategorieView(self.frame_categorie).pack(fill='both', expand=True)
        self.frame_categorie.pack(fill='both', expand=True)

    def show_produit(self):
        """Affiche la vue des produits."""
        self.hide_all_frames()
        if self.frame_produit is None:
            self.frame_produit = Frame(self.view_frame, bg='white')
            ProduitView(self.frame_produit).pack(fill='both', expand=True)
        self.frame_produit.pack(fill='both', expand=True)

    def logout(self):
        """Gère la déconnexion."""
        if hasattr(self, 'menu'):
            self.menu.delete(0, 'end')
            self.root.config(menu='')
        if hasattr(self, 'view_frame'):
            self.view_frame.destroy()
        self.frame_categorie = None
        self.frame_produit = None
        self.show_login()

if __name__ == "__main__":
    App()
