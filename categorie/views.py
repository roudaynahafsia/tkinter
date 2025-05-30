from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
import tkinter.font as tkFont
from .models import Categorie

class CategorieView(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.selected_id = None
        self.snom = StringVar()
        
        # Style moderne
        self.style = ttk.Style()
        self.setup_modern_theme()
        self.create_widgets()
        
    def setup_modern_theme(self):
        """Configure un thème moderne avec des couleurs professionnelles"""
        self.style.theme_use('clam')
        
        # Palette de couleurs moderne
        self.bg_color = '#f8f9fa'
        self.header_color = '#343a40'
        self.footer_color = '#343a40'
        self.primary_color = '#007bff'
        self.success_color = '#28a745'
        self.danger_color = '#dc3545'
        self.warning_color = '#ffc107'
        self.text_color = '#212529'
        self.light_text = '#f8f9fa'
        
        # Configuration des styles
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Header.TFrame', background=self.header_color)
        self.style.configure('Footer.TFrame', background=self.footer_color)
        self.style.configure('Header.TLabel', 
                           background=self.header_color, 
                           foreground=self.light_text,
                           font=('Segoe UI', 14, 'bold'))
        self.style.configure('Footer.TLabel', 
                           background=self.footer_color, 
                           foreground=self.light_text,
                           font=('Segoe UI', 9))
        
        # Styles pour les boutons
        self.style.configure('Primary.TButton', 
                           background=self.primary_color,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'),
                           borderwidth=1)
        self.style.map('Primary.TButton',
                      background=[('active', '#0069d9')])
        
        self.style.configure('Success.TButton', 
                           background=self.success_color,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('Danger.TButton', 
                           background=self.danger_color,
                           foreground='white',
                           font=('Segoe UI', 10, 'bold'))
        
        # Style pour les entrées
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           foreground=self.text_color,
                           bordercolor='#ced4da',
                           lightcolor='#ced4da',
                           darkcolor='#ced4da',
                           padding=8,
                           font=('Segoe UI', 10))
        
        # Style pour le Treeview
        self.style.configure('Modern.Treeview',
                           font=('Segoe UI', 10),
                           background='white',
                           fieldbackground='white',
                           foreground=self.text_color,
                           rowheight=30,
                           bordercolor='#dee2e6')
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 10, 'bold'),
                           background='#e9ecef',
                           foreground=self.text_color,
                           relief='flat')
        
        self.style.map('Modern.Treeview',
                      background=[('selected', self.primary_color)])

    def create_widgets(self):
        # Header
        self.header = ttk.Frame(self.root, style='Header.TFrame', height=60)
        self.header.pack(fill=X, side=TOP)
        
        ttk.Label(self.header, 
                 text="SYSTÈME DE GESTION DES CATÉGORIES", 
                 style='Header.TLabel').pack(side=LEFT, padx=20)
        
        # Corps principal
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Formulaire
        self.create_form_section()
        
        # Tableau
        self.create_table_section()
        
        # Footer
        self.footer = ttk.Frame(self.root, style='Footer.TFrame', height=40)
        self.footer.pack(fill=X, side=BOTTOM)
        
        ttk.Label(self.footer, 
                 text="© 2023 Système de Gestion - Tous droits réservés", 
                 style='Footer.TLabel').pack(side=RIGHT, padx=20)

    def create_form_section(self):
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=X, pady=(0, 20))
        
        # Titre section
        ttk.Label(form_frame, 
                 text="AJOUTER / MODIFIER UNE CATÉGORIE",
                 font=('Segoe UI', 11, 'bold'),
                 foreground=self.text_color).pack(anchor=W, pady=(0, 10))
        
        # Conteneur des champs
        field_frame = ttk.Frame(form_frame)
        field_frame.pack(fill=X)
        
        # Champ Nom
        ttk.Label(field_frame, 
                 text="Nom :",
                 font=('Segoe UI', 10)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        
        self.entry_nom = ttk.Entry(field_frame, 
                                  textvariable=self.snom,
                                  style='Modern.TEntry')
        self.entry_nom.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        
        # Boutons
        btn_frame = ttk.Frame(field_frame)
        btn_frame.grid(row=0, column=2, padx=10)
        
        self.btn_save = ttk.Button(btn_frame, 
                                  text="ENREGISTRER",
                                  style='Success.TButton',
                                  command=self.save)
        self.btn_save.pack(side=LEFT, padx=3)
        
        self.btn_update = ttk.Button(btn_frame, 
                                    text="MODIFIER",
                                    style='Primary.TButton',
                                    command=self.update,
                                    state=DISABLED)
        self.btn_update.pack(side=LEFT, padx=3)
        
        # Configuration responsive
        field_frame.columnconfigure(1, weight=1)

    def create_table_section(self):
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Titre section
        ttk.Label(table_frame, 
                 text="LISTE DES CATÉGORIES",
                 font=('Segoe UI', 11, 'bold'),
                 foreground=self.text_color).pack(anchor=W, pady=(0, 10))
        
        # Conteneur Treeview + Scrollbar
        tree_container = ttk.Frame(table_frame)
        tree_container.pack(fill=BOTH, expand=True)
        
        # Scrollbar
        scroll_y = ttk.Scrollbar(tree_container)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        # Treeview
        self.tree = ttk.Treeview(tree_container,
                                columns=('id', 'nom'),
                                show='headings',
                                style='Modern.Treeview',
                                yscrollcommand=scroll_y.set)
        
        scroll_y.config(command=self.tree.yview)
        
        # Configuration des colonnes
        self.tree.heading('id', text="ID", anchor=CENTER)
        self.tree.heading('nom', text="NOM DE LA CATÉGORIE", anchor=W)
        self.tree.column('id', width=80, anchor=CENTER)
        self.tree.column('nom', anchor=W)
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Boutons d'action
        action_frame = ttk.Frame(table_frame)
        action_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Button(action_frame,
                  text="SUPPRIMER",
                  style='Danger.TButton',
                  command=self.delete).pack(side=LEFT, padx=5)
        
        ttk.Button(action_frame,
                  text="VIDER LA SÉLECTION",
                  style='Primary.TButton',
                  command=self.clear_selection).pack(side=LEFT, padx=5)
        
        # Chargement des données
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for cat in Categorie.getAll():
            self.tree.insert('', 'end', values=(cat['id'], cat['nom']))

    def save(self):
        nom = self.snom.get().strip()
        if nom:
            result = Categorie.create(nom)
            if result == 1:
                showinfo("Succès", "Catégorie enregistrée avec succès!")
                self.snom.set('')
                self.load_data()
            else:
                showerror("Erreur", "Une erreur est survenue lors de l'enregistrement.")
        else:
            showwarning("Champ requis", "Veuillez saisir un nom pour la catégorie.")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.selected_id = values[0]
            self.snom.set(values[1])
            self.btn_save.config(state=DISABLED)
            self.btn_update.config(state=NORMAL)

    def clear_selection(self):
        self.tree.selection_remove(self.tree.selection())
        self.selected_id = None
        self.snom.set('')
        self.btn_save.config(state=NORMAL)
        self.btn_update.config(state=DISABLED)

    def update(self):
        nom = self.snom.get().strip()
        if self.selected_id and nom:
            result = Categorie.update(self.selected_id, nom)
            if result == 1:
                showinfo("Succès", "Catégorie mise à jour avec succès!")
                self.clear_selection()
                self.load_data()
            else:
                showerror("Erreur", "Une erreur est survenue lors de la modification.")
        else:
            showwarning("Champ requis", "Veuillez sélectionner une catégorie et saisir un nom.")

    def delete(self):
        if self.selected_id:
            confirm = askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette catégorie?")
            if confirm:
                result = Categorie.delete(self.selected_id)
                if result == 1:
                    showinfo("Succès", "Catégorie supprimée avec succès!")
                    self.clear_selection()
                    self.load_data()
                else:
                    showerror("Erreur", "Une erreur est survenue lors de la suppression.")
        else:
            showwarning("Sélection requise", "Veuillez sélectionner une catégorie à supprimer.")

if __name__ == "__main__":
    root = Tk()
    root.title("Gestion des Catégories")
    root.geometry("900x600")
    app = CategorieView(root)
    root.mainloop()