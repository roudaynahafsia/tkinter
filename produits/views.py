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
        """Configure les styles visuels"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Palette de couleurs moderne
        colors = {
            'primary': '#3498db',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'bg': '#f5f6fa',
            'header': '#2f3640',
            'text': '#2c3e50'
        }
        
        # Configuration des styles
        self.style.configure('TFrame', background=colors['bg'])
        self.style.configure('Header.TFrame', background=colors['header'])
        self.style.configure('Header.TLabel', 
                          background=colors['header'], 
                          foreground='white',
                          font=('Helvetica', 14, 'bold'))
        
        # Styles des boutons
        self.style.configure('Primary.TButton', 
                          background=colors['primary'],
                          foreground='white',
                          font=('Helvetica', 10, 'bold'),
                          padding=8)
        
        self.style.map('Primary.TButton',
                     background=[('active', '#2980b9')])
        
        self.style.configure('Success.TButton', 
                          background=colors['success'],
                          foreground='white',
                          padding=8)
        
        self.style.configure('Danger.TButton', 
                          background=colors['danger'],
                          foreground='white',
                          padding=8)
    
    def build_interface(self):
        """Construit l'interface complète"""
        self.setup_header()
        self.setup_main_frame()
        self.setup_footer()
        
    def setup_header(self):
        """Configure l'en-tête"""
        header = ttk.Frame(self.root, style='Header.TFrame')
        header.pack(fill=X, pady=(0, 20))
        
        ttk.Label(header, 
                text="GESTION DES PRODUITS", 
                style='Header.TLabel').pack(pady=10)
    
    def setup_main_frame(self):
     """Configure la zone principale"""
     main_frame = ttk.Frame(self.root)
     main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    
    # Formulaire
     form_frame = ttk.Frame(main_frame)
     form_frame.pack(fill=X, pady=(0, 20))
    
     ttk.Label(form_frame, 
              text="Formulaire Produit",
              font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky=W, pady=(0, 10))
    
    # Champs du formulaire
     fields = [
        ("Nom", self.nom),
        ("Quantité", self.quantite),
        ("Prix", self.prix),
        ("Date Expiration", self.date_expiration),
        ("Catégorie", self.categorie)
     ]
    
     for i, (label, var) in enumerate(fields, start=1):
        ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=W)
        
        if label == "Catégorie":
            entry = ttk.Combobox(form_frame, 
                                 textvariable=var,
                                 values=self.get_categories(),
                                 state='readonly')
        else:
            entry = ttk.Entry(form_frame, textvariable=var)
        
        entry.grid(row=i, column=1, padx=5, pady=5, sticky=EW)
    
    # Boutons d'action
     btn_frame = ttk.Frame(form_frame)
     btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)
    
     self.btn_save = ttk.Button(btn_frame, 
                               text="Enregistrer",
                               style='Success.TButton',
                               command=self.save)
     self.btn_save.pack(side=LEFT, padx=5)
    
     self.btn_update = ttk.Button(btn_frame, 
                                 text="Modifier",
                                 style='Primary.TButton',
                                 state=DISABLED,
                                 command=self.update)
     self.btn_update.pack(side=LEFT, padx=5)
    
     ttk.Button(btn_frame, 
               text="Supprimer",
               style='Danger.TButton',
               command=self.delete).pack(side=LEFT, padx=5)
    
     ttk.Button(btn_frame, 
               text="Nouveau",
               command=self.clear_form).pack(side=LEFT, padx=5)
    
    # Tableau
     table_frame = ttk.Frame(main_frame)
     table_frame.pack(fill=BOTH, expand=True)
    
     ttk.Label(table_frame, 
              text="Liste des Produits",
              font=('Helvetica', 12, 'bold')).pack(anchor=W, pady=(0, 10))
    
     self.tree = ttk.Treeview(table_frame, 
                             columns=('id', 'nom', 'quantite', 'prix', 'expiration', 'categorie'),
                             show='headings')
    
     columns = [
        ('id', 'ID', 50),
        ('nom', 'Nom', 200),
        ('quantite', 'Quantité', 100),
        ('prix', 'Prix', 100),
        ('expiration', 'Expiration', 120),
        ('categorie', 'Catégorie', 150)
     ]
    
     for col_id, text, width in columns:
        self.tree.heading(col_id, text=text)
        self.tree.column(col_id, width=width)
    
     self.tree.pack(fill=BOTH, expand=True)
     self.tree.bind('<<TreeviewSelect>>', self.on_select)
      
     scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
     self.tree.configure(yscroll=scrollbar.set)
     scrollbar.pack(side=RIGHT, fill=Y)
    
     self.load_data()

    
    def setup_footer(self):
        """Configure le pied de page"""
        footer = ttk.Frame(self.root)
        footer.pack(fill=X, pady=(20, 0))
        
        ttk.Label(footer, 
                text="© 2023 Système de Gestion - Tous droits réservés",
                font=('Helvetica', 9)).pack(pady=10)
    
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
            
            # Activer le bouton Modifier
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
        
        # Réactiver Enregistrer, désactiver Modifier
        self.btn_save.state(['!disabled'])
        self.btn_update.state(['disabled'])
        
        # Désélectionner dans le tableau
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
            showinfo("Succès", "Produit enregistré")
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
            showinfo("Succès", "Produit mis à jour")
            self.clear_form()
            self.load_data()
        else:
            showerror("Erreur", "Échec de la mise à jour")
    
    def delete(self):
        """Supprime le produit sélectionné"""
        if not self.selected_id:
            showwarning("Attention", "Aucun produit sélectionné")
            return
        
        if askyesno("Confirmer", "Supprimer ce produit?"):
            result = Produit.delete(self.selected_id)
            
            if result == 1:
                showinfo("Succès", "Produit supprimé")
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