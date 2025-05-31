import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from connection import CONNECTION

class LoginPage(tk.Frame):
    """Page de connexion avec un design moderne et professionnel."""
    
    def __init__(self, master, on_success_callback, register_callback):
        super().__init__(master, bg="#f0f2f5")
        self.on_success = on_success_callback
        self.go_to_register = register_callback
        
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
            text="Connexion",
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

        # Champ username
        tk.Label(
            form_frame,
            text="Nom d'utilisateur",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ttk.Entry(
            form_frame,
            style="Modern.TEntry",
            width=25
        )
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.focus_set()

        # Champ password
        tk.Label(
            form_frame,
            text="Mot de passe",
            **field_style
        ).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ttk.Entry(
            form_frame,
            show="*",
            style="Modern.TEntry",
            width=25
        )
        self.password_entry.pack(pady=(0, 20))

        # Bouton de connexion
        login_btn = tk.Button(
            form_frame,
            text="Se connecter",
            command=self._authenticate,
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
        login_btn.pack(fill="x")
        
        # Lien vers inscription
        register_link = tk.Label(
            form_frame,
            text="Créer un nouveau compte",
            fg="#1877f2",
            bg="white",
            font=("Segoe UI", 9),
            cursor="hand2"
        )
        register_link.pack(pady=(20, 0))
        register_link.bind("<Button-1>", lambda e: self.go_to_register())

        # Style au survol
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#166fe5"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#1877f2"))
        register_link.bind("<Enter>", lambda e: register_link.config(font=("Segoe UI", 9, "underline")))
        register_link.bind("<Leave>", lambda e: register_link.config(font=("Segoe UI", 9)))

    def _create_db_table(self):
        """Crée la table users si elle n'existe pas."""
        try:
            with CONNECTION.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
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

    def _authenticate(self):
        """Tente d'authentifier l'utilisateur."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
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