import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import re
from connection import CONNECTION

class RegisterPage(tk.Frame):
    """Page d'inscription avec un design moderne et professionnel."""
    
    def __init__(self, master, login_callback):
        """
        Initialise la page d'inscription.
        
        Args:
            master: Widget parent
            login_callback: Fonction pour rediriger vers la page de connexion
        """
        super().__init__(master)
        self.configure(bg="#f5f7fa")
        self.go_to_login = login_callback
        
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
        main_frame = tk.Frame(self.canvas, bg="#f5f7fa", width=600)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # En-tête
        header_frame = tk.Frame(main_frame, bg="#f5f7fa")
        header_frame.pack(pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Créer un compte",
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
        self.full_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        # Champs du formulaire
        fields = [
            ("Nom complet", self.full_name_var, False),
            ("Adresse email", self.email_var, False),
            ("Nom d'utilisateur", self.username_var, False),
            ("Mot de passe", self.password_var, True),
            ("Confirmer le mot de passe", self.confirm_password_var, True)
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
                style="Modern.TEntry",
                width=40,
                show="*" if is_password else ""
            )
            entry.pack(pady=(0, 20), fill="x")
            self.entries[label_text] = entry
            var.trace_add("write", lambda *args, lbl=label_text: self._validate_field(lbl))
        
        self.entries["Nom complet"].focus_set()

        # Bouton d'inscription
        self.register_btn = tk.Button(
            form_frame,
            text="S'inscrire",
            command=self._register_user,
            bg="#212529",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            borderwidth=0,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.register_btn.pack(fill="x")
        self._bind_button_animations(self.register_btn)
        
        # Lien vers connexion
        self.login_link = tk.Label(
            form_frame,
            text="Déjà un compte ? Se connecter",
            fg="#212529",
            bg="white",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        self.login_link.pack(pady=(20, 0))
        self.login_link.bind("<Button-1>", lambda e: self.go_to_login())
        self.login_link.bind("<Enter>", lambda e: self.login_link.config(font=("Segoe UI", 9, "underline")))
        self.login_link.bind("<Leave>", lambda e: self.login_link.config(font=("Segoe UI", 9)))

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
        value = self.entries[field_name]["textvariable"].get().strip()
        
        if field_name == "Adresse email":
            is_valid = bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value))
        elif field_name == "Mot de passe":
            is_valid = len(value) >= 8
        elif field_name == "Confirmer le mot de passe":
            is_valid = value == self.password_var.get().strip() and value != ""
        else:
            is_valid = len(value) > 0

        self.style.configure('Modern.TEntry', 
                           bordercolor=self.colors['success'] if is_valid else self.colors['danger'])
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

    def _register_user(self):
        """Enregistre un nouvel utilisateur après validation."""
        full_name = self.full_name_var.get().strip()
        email = self.email_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()

        # Validation des champs
        if not all([full_name, email, username, password, confirm_password]):
            messagebox.showwarning(
                "Champs manquants",
                "Tous les champs sont obligatoires"
            )
            return

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            messagebox.showerror(
                "Email invalide",
                "Veuillez entrer une adresse email valide"
            )
            return

        if password != confirm_password:
            messagebox.showerror(
                "Erreur",
                "Les mots de passe ne correspondent pas"
            )
            return

        if len(password) < 8:
            messagebox.showwarning(
                "Mot de passe faible",
                "Le mot de passe doit contenir au moins 8 caractères"
            )
            return

        try:
            with CONNECTION.cursor() as cursor:
                # Vérifie si le nom d'utilisateur existe déjà
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    messagebox.showerror(
                        "Nom d'utilisateur indisponible",
                        "Ce nom d'utilisateur est déjà pris"
                    )
                    return

                # Vérifie si l'email existe déjà
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    messagebox.showerror(
                        "Email déjà utilisé",
                        "Un compte existe déjà avec cette adresse email"
                    )
                    return

                # Insertion du nouvel utilisateur
                cursor.execute("""
                    INSERT INTO users (full_name, email, username, password)
                    VALUES (%s, %s, %s, %s)
                """, (full_name, email, username, password))
                CONNECTION.commit()

                messagebox.showinfo(
                    "Inscription réussie",
                    "Votre compte a été créé avec succès!\nVous pouvez maintenant vous connecter."
                )
                self.go_to_login()

        except pymysql.Error as e:
            CONNECTION.rollback()
            messagebox.showerror(
                "Erreur d'inscription",
                f"Une erreur est survenue lors de l'inscription: {str(e)}"
            )