import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from connection import CONNECTION

class LoginPage(tk.Frame):
    """Page de connexion avec un design moderne et professionnel."""
    
    def __init__(self, master, on_success_callback, register_callback):
        """
        Initialise la page de connexion.
        
        Args:
            master: Widget parent
            on_success_callback: Fonction à appeler après une connexion réussie
            register_callback: Fonction pour rediriger vers la page d'inscription
        """
        super().__init__(master)
        self.configure(bg="#f5f7fa")
        self.on_success = on_success_callback
        self.go_to_register = register_callback
        
        self._setup_styles()
        self._setup_ui()
        self._create_db_table()

    def _setup_styles(self):
        """Configure les styles modernes."""
        self.colors = {
            'primary': '#212529',
            'success': '#28a745',
            'danger': '#dc3545',
            'bg': '#f5f7fa',
            'header': '#2b2d42',
            'text': '#212529',
            'light_text': '#ffffff'
        }
        
        self.style = ttk.Style()
        self.style.configure('Modern.TEntry',
                           fieldbackground='white',
                           foreground='#212529',
                           padding=8,
                           font=('Segoe UI', 11),
                           bordercolor='#cccccc')
        self.style.map('Modern.TEntry',
                      bordercolor=[('focus', '#212529')])

    def _setup_ui(self):
        """Configure l'interface avec un design moderne."""
        # Canvas pour fond dégradé
        self.canvas = tk.Canvas(self, bg="#f5f7fa", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self._create_gradient()
        
        # Cadre principal pour centrer le contenu
        main_frame = tk.Frame(self.canvas, bg="#f5f7fa", width=500)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # En-tête
        header_frame = tk.Frame(main_frame, bg="#f5f7fa")
        header_frame.pack(pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Connexion",
            font=("Segoe UI", 28, "bold"),
            fg="#2b2d42",
            bg="#f5f7fa"
        ).pack()

        # Cadre du formulaire avec effet carte
        form_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=40,
            pady=40,
            relief="raised",
            borderwidth=2
        )
        form_frame.pack(fill="x")

        # Variables de contrôle
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Champs du formulaire
        fields = [
            ("Nom d'utilisateur", self.username_var, False),
            ("Mot de passe", self.password_var, True)
        ]
        
        self.entries = {}
        for label_text, var, is_password in fields:
            tk.Label(
                form_frame,
                text=label_text,
                font=("Segoe UI", 11),
                bg="white",
                fg="#212529"
            ).pack(anchor="w", pady=(15, 5))
            
            entry = ttk.Entry(
                form_frame,
                textvariable=var,
                show="*" if is_password else "",
                style="Modern.TEntry",
                width=40
            )
            entry.pack(pady=(0, 20), fill="x")
            self.entries[label_text] = entry
            var.trace_add("write", lambda *args, lbl=label_text: self._validate_field(lbl))
        
        self.entries["Nom d'utilisateur"].focus_set()

        # Bouton de connexion
        self.login_btn = tk.Button(
            form_frame,
            text="Se connecter",
            command=self._authenticate,
            bg="#212529",
            fg="white",
            activebackground="#212529",
            activeforeground="white",
            borderwidth=0,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.login_btn.pack(fill="x")
        self._bind_button_animations(self.login_btn)
        
        # Lien vers inscription
        self.register_link = tk.Label(
            form_frame,
            text="Créer un nouveau compte",
            fg="#212529",
            bg="white",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        self.register_link.pack(pady=(20, 0))
        self.register_link.bind("<Button-1>", lambda e: self.go_to_register())
        self.register_link.bind("<Enter>", lambda e: self.register_link.config(font=("Segoe UI", 9, "underline")))
        self.register_link.bind("<Leave>", lambda e: self.register_link.config(font=("Segoe UI", 9)))

    def _create_gradient(self):
        """Crée un fond dégradé."""
        width, height = 800, 600
        self.canvas.config(width=width, height=height)
        colors = ['#2b2d42', '#f5f7fa']
        
        for i in range(height):
            r = int(43 + (245-43) * i/height)
            g = int(45 + (247-45) * i/height)
            b = int(66 + (250-66) * i/height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color)

    def _bind_button_animations(self, button):
        """Ajoute des animations au survol des boutons."""
        button.bind("<Enter>", lambda e: button.config(bg="#212529"))
        button.bind("<Leave>", lambda e: button.config(bg="#212529"))

    def _validate_field(self, field_name):
        """Validation en temps réel des champs avec retour visuel."""
        value = self.entries[field_name].get().strip()
        is_valid = len(value) > 0
        
        self.style.configure('Modern.TEntry', 
                           bordercolor='#28a745' if is_valid else '#dc3545')
        self.entries[field_name].configure(style='Modern.TEntry')

    def _create_db_table(self):
        """Crée la table users si elle n'existe pas."""
        try:
            with CONNECTION.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        full_name VARCHAR(100) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(100) NOT NULL
                    )
                """)
                CONNECTION.commit()
        except pymysql.Error as e:
            if e.args[0] != 1050:  # Ignore "Table already exists" warning
                messagebox.showerror(
                    "Erreur base de données", 
                    f"Impossible de créer la table: {str(e)}"
                )

    def _authenticate(self):
        """Tente d'authentifier l'utilisateur."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showwarning(
                "Champs manquants",
                "Veuillez saisir un nom d'utilisateur et un mot de passe"
            )
            return
        
        try:
            with CONNECTION.cursor() as cursor:
                query = """
                    SELECT id FROM users 
                    WHERE username = %s AND password = %s
                """
                cursor.execute(query, (username, password))
                if cursor.fetchone():
                    self.on_success()
                else:
                    messagebox.showerror(
                        "Authentification échouée",
                        "Identifiants incorrects"
                    )
        except pymysql.Error as e:
            messagebox.showerror(
                "Erreur base de données",
                f"Erreur lors de l'authentification: {str(e)}"
            )