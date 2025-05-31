import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
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
        super().__init__(master, bg="#f0f2f5")
        self.go_to_login = login_callback
        
        self._setup_ui()
        self._create_db_table()

    def _setup_ui(self):
        """Configure l'interface avec un design moderne."""
        # Cadre principal pour centrer le contenu
        main_frame = tk.Frame(self, bg="#f0f2f5", padx=40, pady=30)
        main_frame.pack(expand=True)
        
        # Logo/En-tête
        header_frame = tk.Frame(main_frame, bg="#f0f2f5")
        header_frame.pack(pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Créer un compte",
            font=("Segoe UI", 24, "bold"),
            fg="#1877f2",
            bg="#f0f2f5"
        ).pack()

        # Cadre du formulaire avec ombre visuelle
        form_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=30,
            pady=30,
            relief="flat",
            borderwidth=0,
            highlightbackground="#dddfe2",
            highlightthickness=1
        )
        form_frame.pack()

        # Style des champs
        field_style = {"font": ("Segoe UI", 11), "bg": "white"}
        entry_style = {
            "font": ("Segoe UI", 11),
            "relief": "flat",
            "borderwidth": 1,
            "highlightbackground": "#dddfe2",
            "highlightthickness": 1,
            "highlightcolor": "#1877f2"
        }

        # Variables de contrôle
        self.full_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        # Champ Nom complet
        tk.Label(
            form_frame,
            text="Nom complet",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.full_name_entry = ttk.Entry(
            form_frame,
            textvariable=self.full_name_var,
            style="Modern.TEntry",
            width=25
        )
        self.full_name_entry.pack(pady=(0, 15))
        self.full_name_entry.focus_set()

        # Champ Email
        tk.Label(
            form_frame,
            text="Adresse email",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.email_entry = ttk.Entry(
            form_frame,
            textvariable=self.email_var,
            style="Modern.TEntry",
            width=25
        )
        self.email_entry.pack(pady=(0, 15))

        # Champ Nom d'utilisateur
        tk.Label(
            form_frame,
            text="Nom d'utilisateur",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ttk.Entry(
            form_frame,
            textvariable=self.username_var,
            style="Modern.TEntry",
            width=25
        )
        self.username_entry.pack(pady=(0, 15))

        # Champ Mot de passe
        tk.Label(
            form_frame,
            text="Mot de passe",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ttk.Entry(
            form_frame,
            textvariable=self.password_var,
            show="*",
            style="Modern.TEntry",
            width=25
        )
        self.password_entry.pack(pady=(0, 15))

        # Champ Confirmation mot de passe
        tk.Label(
            form_frame,
            text="Confirmer le mot de passe",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.confirm_password_entry = ttk.Entry(
            form_frame,
            textvariable=self.confirm_password_var,
            show="*",
            style="Modern.TEntry",
            width=25
        )
        self.confirm_password_entry.pack(pady=(0, 20))

        # Bouton d'inscription
        register_btn = tk.Button(
            form_frame,
            text="S'inscrire",
            command=self._register_user,
            bg="#1877f2",
            fg="white",
            activebackground="#166fe5",
            activeforeground="white",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        register_btn.pack(fill="x")
        
        # Lien vers connexion
        login_link = tk.Label(
            form_frame,
            text="Déjà un compte ? Se connecter",
            fg="#1877f2",
            bg="white",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        login_link.pack(pady=(20, 0))
        login_link.bind("<Button-1>", lambda e: self.go_to_login())

        # Style au survol
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg="#166fe5"))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg="#1877f2"))
        login_link.bind("<Enter>", lambda e: login_link.config(font=("Segoe UI", 9, "underline")))
        login_link.bind("<Leave>", lambda e: login_link.config(font=("Segoe UI", 9)))

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
        except Exception as e:
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