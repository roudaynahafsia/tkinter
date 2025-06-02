from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
from .models import Produit
from categorie.models import Categorie

class ProduitView(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setup_variables()
        self.configure_styles()
        self.build_interface()
        
    def setup_variables(self):
        """Initialise les variables de contrôle"""
        self.nom = StringVar()
        self.prix = IntVar(value=0)
        self.quantite = IntVar(value=0)
        self.date_expiration = StringVar()
        self.categorie = StringVar()
        self.selected_id = None  # ID du produit sélectionné
    
    def configure_styles(self):
        """Configure les styles visuels modernes"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Palette de couleurs moderne
        self.colors = {
            'primary': '#212529',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'bg': '#f5f7fa',
            'header': '#2b2d42',
            'footer': '#2b2d42',
            'text': '#212529',
            'light_text': '#ffffff',
            'accent': '#e9ecef'
        }
        
        # Styles des frames
        self.style.configure('Main.TFrame', background=self.colors['bg'])
        self.style.configure('Header.TFrame', background=self.colors['header'])
        self.style.configure('Footer.TFrame', background=self.colors['footer'])
        self.style.configure('Card.TFrame', background='white', relief='flat')
        
        # Styles des labels
        self.style.configure('Header.TLabel', 
                           background=self.colors['header'], 
                           foreground=self.colors['light_text'],
                           font=('Segoe UI', 16, 'bold'))
        self.style.configure('Footer.TLabel', 
                           background=self.colors['footer'], 
                           foreground=self.colors['light_text'],
                           font=('Segoe UI', 10))
        self.style.configure('Section.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground=self.colors['text'])
        
        # Styles des boutons
        self.style.configure('Primary.TButton', 
                           background=self.colors['primary'],
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           padding=8)
        self.style.map('Primary.TButton',
                      background=[('active', '#212529')])
        
        self.style.configure('Success.TButton', 
                           background=self.colors['success'],
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           padding=8)
        self.style.map('Success.TButton',
                      background=[('active', '#218838')])
        
        self.style.configure('Danger.TButton', 
                           background=self.colors['danger'],
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           padding=8)
        self.style.map('Danger.TButton',
                      background=[('active', '#c82333')])
        
        # Styles pour Entry et Combobox
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           foreground=self.colors['text'],
                           padding=10,
                           font=('Segoe UI', 11))
        self.style.configure('Modern.TCombobox',
                           fieldbackground='white',
                           foreground=self.colors['text'],
                           padding=10,
                           font=('Segoe UI', 11))
        
        # Styles pour Treeview
        self.style.configure('Modern.Treeview',
                           font=('Segoe UI', 11),
                           background='white',
                           fieldbackground='white',
                           foreground=self.colors['text'],
                           rowheight=35,
                           bordercolor=self.colors['accent'])
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.colors['accent'],
                           foreground=self.colors['text'],
                           relief='flat')
        
        self.style.map('Modern.Treeview',
                      background=[('selected', self.colors['primary'])],
                      foreground=[('selected', 'white')])

    def build_interface(self):
        """Construit l'interface complète"""
        # Canvas pour fond dégradé within self (not self.root)
        self.canvas = Canvas(self, bg=self.colors['bg'], highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)
        self._create_gradient()
        
        # Conteneur principal
        container = ttk.Frame(self.canvas, style='Main.TFrame')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.setup_header(container)
        self.setup_main_frame(container)
        self.setup_footer(container)
        
    def _create_gradient(self):
        """Crée un fond dégradé dynamiquement."""
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1 or height <= 1:  # Fallback if not yet rendered
            width, height = 1000, 700
        colors = ['#2b2d42', '#2b2d42']
        
        for i in range(height):
            r = int(43 + (245-43) * i/height)
            g = int(45 + (247-45) * i/height)
            b = int(66 + (250-66) * i/height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def setup_header(self, container):
        """Configure l'en-tête"""
        header = ttk.Frame(container, style='Header.TFrame')
        header.pack(fill=X, ipady=10)
        
        ttk.Label(header, 
                 text="GESTION DES PRODUITS", 
                 style='Header.TLabel').pack(side=LEFT, padx=20)
    
    def setup_main_frame(self, container):
        """Configure la zone principale"""
        main_frame = ttk.Frame(container, style='Card.TFrame', padding=20)
        main_frame.pack(fill=BOTH, expand=True, pady=20)
        main_frame.configure(relief='raised', borderwidth=2)
        
        # Section formulaire
        form_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=15)
        form_frame.pack(fill=X, pady=(0, 20))
        
        ttk.Label(form_frame, 
                 text="FORMULAIRE PRODUIT", 
                 style='Section.TLabel').pack(anchor=W, pady=(0, 10))
        
        # Champs du formulaire
        fields = [
            ("Nom", self.nom, False),
            ("Quantité", self.quantite, False),
            ("Prix", self.prix, False),
            ("Date d'Expiration", self.date_expiration, False),
            ("Catégorie", self.categorie, True)
        ]
        
        self.entries = {}
        for label, var, is_combobox in fields:
            # Sous-frame pour chaque champ
            field_frame = ttk.Frame(form_frame)
            field_frame.pack(fill=X, pady=5)
            
            ttk.Label(field_frame, 
                     text=label,
                     font=('Segoe UI', 11),
                     width=15).pack(side=LEFT, padx=10)
            
            if is_combobox:
                entry = ttk.Combobox(field_frame, 
                                    textvariable=var,
                                    values=self.get_categories(),
                                    style='Modern.TCombobox',
                                    state='readonly')
            else:
                entry = ttk.Entry(field_frame, 
                                 textvariable=var,
                                 style='Modern.TEntry')
            
            entry.pack(side=LEFT, fill=X, expand=True, padx=10)
            self.entries[label] = entry
            var.trace_add("write", lambda *args, lbl=label: self._validate_field(lbl))
        
        # Boutons d'action
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=X, pady=10)
        
        self.btn_save = ttk.Button(btn_frame, 
                                  text="ENREGISTRER",
                                  style='Success.TButton',
                                  command=self.save)
        self.btn_save.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_save)
        
        self.btn_update = ttk.Button(btn_frame, 
                                    text="MODIFIER",
                                    style='Primary.TButton',
                                    state=DISABLED,
                                    command=self.update)
        self.btn_update.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_update)
        
        self.btn_delete = ttk.Button(btn_frame, 
                                    text="SUPPRIMER",
                                    style='Danger.TButton',
                                    command=self.delete)
        self.btn_delete.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_delete)
        
        self.btn_clear = ttk.Button(btn_frame, 
                                   text="NOUVEAU",
                                   style='Primary.TButton',
                                   command=self.clear_form)
        self.btn_clear.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_clear)
        
        # Section tableau
        table_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=15)
        table_frame.pack(fill=BOTH, expand=True)
        
        ttk.Label(table_frame, 
                 text="LISTE DES PRODUITS", 
                 style='Section.TLabel').pack(anchor=W, pady=(0, 10))
        
        self.tree = ttk.Treeview(table_frame, 
                                columns=('id', 'nom', 'quantite', 'prix', 'expiration', 'categorie'),
                                show='headings',
                                style='Modern.Treeview')
        
        columns = [
            ('id', 'ID', 80, CENTER),
            ('nom', 'Nom', 200, W),
            ('quantite', 'Quantité', 100, CENTER),
            ('prix', 'Prix', 100, CENTER),
            ('expiration', "Date d'Expiration", 120, W),
            ('categorie', 'Catégorie', 150, W)
        ]
        
        for col_id, text, width, anchor in columns:
            self.tree.heading(col_id, text=text)
            self.tree.column(col_id, width=width, anchor=anchor)
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.load_data()
    
    def setup_footer(self, container):
        """Configure le pied de page"""
        footer = ttk.Frame(container, style='Footer.TFrame')
        footer.pack(fill=X, ipady=5)
        
        ttk.Label(footer, 
                 text="© 2025 Système de Gestion des Produits - Tous droits réservés",
                 style='Footer.TLabel').pack(side=RIGHT, padx=20)
    
    def _bind_button_animations(self, button):
        """Ajoute des animations au survol des boutons"""
        button.bind("<Enter>", lambda e: button.configure(style=button.cget("style").replace("TButton", "Outline.TButton")))
        button.bind("<Leave>", lambda e: button.configure(style=button.cget("style").replace("Outline.TButton", "TButton")))
    
    def _validate_field(self, field_name):
        """Validation en temps réel des champs avec retour visuel"""
        value = self.entries[field_name]["textvariable"].get().strip()
        entry = self.entries[field_name]
        
        if field_name == "Nom":
            is_valid = bool(value)
        elif field_name == "Quantité":
            try:
                is_valid = int(value) >= 0
            except:
                is_valid = False
        elif field_name == "Prix":
            try:
                is_valid = float(value) > 0
            except:
                is_valid = False
        elif field_name == "Catégorie":
            is_valid = bool(value)
        else:  # Date d'Expiration
            is_valid = True  # Champ optionnel
        
        entry.configure(style='Modern.TEntry' if not field_name == "Catégorie" else 'Modern.TCombobox')
        self.style.configure(entry.cget("style"), bordercolor=self.colors['success'] if is_valid else self.colors['danger'])
    
    def get_categories(self):
        """Récupère la liste des catégories"""
        return [cat['nom'] for cat in Categorie.getAll()]
    
    def load_data(self):
        """Charge les données dans le tableau"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        produits = Produit.all()
        categories = {c['id']: c['nom'] for c in Categorie.getAll()}
        
        for prod in produits:
            self.tree.insert('', END, 
                           values=(prod['id'],
                                   prod['nom'],
                                   prod['quantite'],
                                   prod['prix'],
                                   prod['date_expiration'],
                                   categories.get(prod['id_categorie'], '')))
    
    def on_select(self, event):
        """Gère la sélection d'un produit"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.selected_id = values[0]
            self.nom.set(values[1])
            self.quantite.set(values[2])
            self.prix.set(values[3])
            self.date_expiration.set(values[4])
            self.categorie.set(values[5])
            
            self.btn_update.state(['!disabled'])
            self.btn_save.state(['disabled'])
    
    def clear_form(self):
        """Réinitialise le formulaire"""
        self.selected_id = None
        self.nom.set('')
        self.quantite.set(0)
        self.prix.set(0)
        self.date_expiration.set('')
        self.categorie.set('')
        
        self.btn_save.state(['!disabled'])
        self.btn_update.state(['disabled'])
        
        self.tree.selection_remove(self.tree.selection())
    
    def validate_form(self):
        """Valide les données du formulaire"""
        errors = []
        
        if not self.nom.get().strip():
            errors.append("Le nom est requis")
        
        try:
            if int(self.quantite.get()) < 0:
                errors.append("La quantité doit être positive")
        except:
            errors.append("Quantité invalide")
        
        try:
            if float(self.prix.get()) <= 0:
                errors.append("Le prix doit être positif")
        except:
            errors.append("Prix invalide")
        
        if not self.categorie.get():
            errors.append("La catégorie est requise")
        
        if errors:
            showerror("Erreurs", "\n".join(errors))
            return False
        
        return True
    
    def save(self):
        """Enregistre un nouveau produit"""
        if not self.validate_form():
            return
        
        categorie = Categorie.getByName(self.categorie.get())
        
        result = Produit.create(
            self.nom.get().strip(),
            int(self.quantite.get()),
            float(self.prix.get()),
            self.date_expiration.get().strip(),
            categorie['id']
        )
        
        if result == 1:
            showinfo("Succès", "Produit enregistré avec succès")
            self.clear_form()
            self.load_data()
        else:
            showerror("Erreur", "Échec de l'enregistrement")
    
    def update(self):
        """Met à jour le produit sélectionné"""
        if not self.selected_id:
            showwarning("Attention", "Aucun produit sélectionné")
            return
        
        if not self.validate_form():
            return
        
        categorie = Categorie.getByName(self.categorie.get())
        
        result = Produit.update(
            self.selected_id,
            self.nom.get().strip(),
            int(self.quantite.get()),
            float(self.prix.get()),
            self.date_expiration.get().strip(),
            categorie['id']
        )
        
        if result == 1:
            showinfo("Succès", "Produit mis à jour avec succès")
            self.clear_form()
            self.load_data()
        else:
            showerror("Erreur", "Échec de la mise à jour")
    
    def delete(self):
        """Supprime le produit sélectionné"""
        if not self.selected_id:
            showwarning("Attention", "Aucun produit sélectionné")
            return
        
        if askyesno("Confirmer", "Supprimer ce produit ?"):
            result = Produit.delete(self.selected_id)
            
            if result == 1:
                showinfo("Succès", "Produit supprimé avec succès")
                self.clear_form()
                self.load_data()
            else:
                showerror("Erreur", "Échec de la suppression")

if __name__ == "__main__":
    root = Tk()
    root.title("Gestion des Produits")
    root.geometry("1000x700")
    app = ProduitView(root)
    root.mainloop()
