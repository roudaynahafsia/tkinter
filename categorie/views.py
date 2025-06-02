from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
from .models import Categorie

class CategorieView(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.selected_id = None
        self.snom = StringVar()
        
        self.setup_modern_theme()
        self.create_widgets()
        
    def setup_modern_theme(self):
        """Configure a modern theme with professional colors"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Modern color palette
        self.bg_color = '#f5f7fa'
        self.header_color = '#2b2d42'
        self.footer_color = '#2b2d42'
        self.primary_color = '#007bff'
        self.success_color = '#28a745'
        self.danger_color = '#dc3545'
        self.warning_color = '#ffc107'
        self.text_color = '#212529'
        self.light_text = '#ffffff'
        self.accent_color = '#e9ecef'
        
        # Frame styles
        self.style.configure('Main.TFrame', background=self.bg_color)
        self.style.configure('Header.TFrame', background=self.header_color)
        self.style.configure('Footer.TFrame', background=self.footer_color)
        self.style.configure('Card.TFrame', background='white', relief='flat')
        
        # Label styles
        self.style.configure('Header.TLabel', 
                           background=self.header_color, 
                           foreground=self.light_text,
                           font=('Segoe UI', 16, 'bold'))
        self.style.configure('Footer.TLabel', 
                           background=self.footer_color, 
                           foreground=self.light_text,
                           font=('Segoe UI', 10))
        self.style.configure('Section.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground=self.text_color)
        
        # Button styles
        self.style.configure('Primary.TButton', 
                           background=self.primary_color,
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           padding=8)
        self.style.map('Primary.TButton',
                      background=[('active', '#0056b3')])
        
        self.style.configure('Success.TButton', 
                           background=self.success_color,
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           padding=8)
        self.style.map('Success.TButton',
                      background=[('active', '#218838')])
        
        self.style.configure('Danger.TButton', 
                           background=self.danger_color,
                           foreground='white',
                           font=('Segoe UI', 11, 'bold'),
                           borderwidth=0,
                           padding=8)
        self.style.map('Danger.TButton',
                      background=[('active', '#c82333')])
        
        # Entry style
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           foreground=self.text_color,
                           padding=10,
                           font=('Segoe UI', 11))
        
        # Treeview style
        self.style.configure('Modern.Treeview',
                           font=('Segoe UI', 11),
                           background='white',
                           fieldbackground='white',
                           foreground=self.text_color,
                           rowheight=35,
                           bordercolor='#dee2e6')
        
        self.style.configure('Modern.Treeview.Heading',
                           font=('Segoe UI', 11, 'bold'),
                           background=self.accent_color,
                           foreground=self.text_color,
                           relief='flat')
        
        self.style.map('Modern.Treeview',
                      background=[('selected', self.primary_color)],
                      foreground=[('selected', 'white')])

    def create_widgets(self):
        # Gradient background canvas within self (not self.root)
        self.canvas = Canvas(self, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)
        self._create_gradient()
        
        # Main container
        container = ttk.Frame(self.canvas, style='Main.TFrame')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.header = ttk.Frame(container, style='Header.TFrame')
        self.header.pack(fill=X, ipady=10)
        
        ttk.Label(self.header, 
                 text="GESTION DES CATÉGORIES", 
                 style='Header.TLabel').pack(side=LEFT, padx=20)
        
        # Main frame with card effect
        self.main_frame = ttk.Frame(container, style='Card.TFrame', padding=20)
        self.main_frame.pack(fill=BOTH, expand=True, pady=20)
        self.main_frame.configure(relief='raised', borderwidth=2)
        
        # Form section
        self.create_form_section()
        
        # Table section
        self.create_table_section()
        
        # Footer
        self.footer = ttk.Frame(container, style='Footer.TFrame')
        self.footer.pack(fill=X, ipady=5)
        
        ttk.Label(self.footer, 
                 text="© 2025 Système de Gestion des Catégories - Tous droits réservés", 
                 style='Footer.TLabel').pack(side=RIGHT, padx=20)

    def _create_gradient(self):
        """Create a gradient background dynamically based on widget size."""
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1 or height <= 1:  # Fallback if not yet rendered
            width, height = 1000, 700
        colors = ['#2b2d42', '#f5f7fa']
        
        for i in range(height):
            r = int(43 + (245-43) * i/height)
            g = int(45 + (247-45) * i/height)
            b = int(66 + (250-66) * i/height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def create_form_section(self):
        form_frame = ttk.Frame(self.main_frame, style='Card.TFrame', padding=15)
        form_frame.pack(fill=X, pady=(0, 20))
        
        # Section title
        ttk.Label(form_frame, 
                 text="AJOUTER / MODIFIER UNE CATÉGORIE", 
                 style='Section.TLabel').pack(anchor=W, pady=(0, 10))
        
        # Field container
        field_frame = ttk.Frame(form_frame)
        field_frame.pack(fill=X)
        
        # Name field
        ttk.Label(field_frame, 
                 text="Nom:", 
                 font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky=W)
        
        self.entry_nom = ttk.Entry(field_frame, 
                                  textvariable=self.snom,
                                  style='Modern.TEntry')
        self.entry_nom.grid(row=0, column=1, padx=10, pady=5, sticky=EW)
        self.snom.trace_add("write", self._validate_field)
        
        # Buttons
        btn_frame = ttk.Frame(field_frame)
        btn_frame.grid(row=0, column=2, padx=10)
        
        self.btn_save = ttk.Button(btn_frame, 
                                  text="ENREGISTRER", 
                                  style='Success.TButton',
                                  command=self.save)
        self.btn_save.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_save)
        
        self.btn_update = ttk.Button(btn_frame, 
                                    text="MODIFIER", 
                                    style='Primary.TButton',
                                    command=self.update,
                                    state=DISABLED)
        self.btn_update.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_update)
        
        # Responsive configuration
        field_frame.columnconfigure(1, weight=1)

    def create_table_section(self):
        table_frame = ttk.Frame(self.main_frame, style='Card.TFrame', padding=15)
        table_frame.pack(fill=BOTH, expand=True)
        
        # Section title
        ttk.Label(table_frame, 
                 text="LISTE DES CATÉGORIES", 
                 style='Section.TLabel').pack(anchor=W, pady=(0, 10))
        
        # Treeview container
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
        
        # Column configuration
        self.tree.heading('id', text="ID", anchor=CENTER)
        self.tree.heading('nom', text="NOM DE LA CATÉGORIE", anchor=W)
        self.tree.column('id', width=100, anchor=CENTER)
        self.tree.column('nom', anchor=W)
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Action buttons
        action_frame = ttk.Frame(table_frame)
        action_frame.pack(fill=X, pady=(10, 0))
        
        self.btn_delete = ttk.Button(action_frame,
                                    text="SUPPRIMER", 
                                    style='Danger.TButton',
                                    command=self.delete)
        self.btn_delete.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_delete)
        
        self.btn_clear = ttk.Button(action_frame,
                                   text="RÉINITIALISER", 
                                   style='Primary.TButton',
                                   command=self.clear_selection)
        self.btn_clear.pack(side=LEFT, padx=5)
        self._bind_button_animations(self.btn_clear)
        
        # Load data
        self.load_data()

    def _bind_button_animations(self, button):
        """Add hover animations to buttons."""
        button.bind("<Enter>", lambda e: button.configure(style=button.cget("style").replace("TButton", "Outline.TButton")))
        button.bind("<Leave>", lambda e: button.configure(style=button.cget("style").replace("Outline.TButton", "TButton")))

    def _validate_field(self, *args):
        """Real-time field validation with visual feedback."""
        value = self.snom.get().strip()
        style = 'Modern.TEntry'
        if value:
            self.style.configure('Modern.TEntry', bordercolor=self.success_color)
        else:
            self.style.configure('Modern.TEntry', bordercolor=self.danger_color)
        self.entry_nom.configure(style=style)

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
                showinfo("Succès", "Catégorie enregistrée avec succès !")
                self.snom.set('')
                self.load_data()
            else:
                showerror("Erreur", "Une erreur est survenue lors de l'enregistrement.")
        else:
            showwarning("Champ requis", "Veuillez entrer un nom de catégorie.")

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
                showinfo("Succès", "Catégorie mise à jour avec succès !")
                self.clear_selection()
                self.load_data()
            else:
                showerror("Erreur", "Une erreur est survenue lors de la mise à jour.")
        else:
            showwarning("Champ requis", "Veuillez sélectionner une catégorie et entrer un nom.")

    def delete(self):
        if self.selected_id:
            confirm = askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette catégorie ?")
            if confirm:
                result = Categorie.delete(self.selected_id)
                if result == 1:
                    showinfo("Succès", "Catégorie supprimée avec succès !")
                    self.clear_selection()
                    self.load_data()
                else:
                    showerror("Erreur", "Une erreur est survenue lors de la suppression.")
        else:
            showwarning("Sélection requise", "Veuillez sélectionner une catégorie à supprimer.")

if __name__ == "__main__":
    root = Tk()
    root.title("Gestion des Catégories")
    root.geometry("1000x700")
    app = CategorieView(root)
    root.mainloop()