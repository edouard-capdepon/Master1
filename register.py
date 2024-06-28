from tkinter import filedialog

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x350")

        self.create_widgets()

    def create_widgets(self):
        # Onglets pour se connecter et créer un compte
        self.tab_view = ctk.CTkTabview(self.master)
        self.tab_view.pack(expand=1, fill='both')

        self.login_tab = self.tab_view.add("Se connecter")
        self.register_tab = self.tab_view.add("Créer un compte")

        # Widgets de l'onglet de connexion
        ctk.CTkLabel(self.login_tab, text="Nom d'utilisateur").pack(pady=10)
        self.login_username_entry = ctk.CTkEntry(self.login_tab)
        self.login_username_entry.pack(pady=10)

        ctk.CTkLabel(self.login_tab, text="Mot de passe").pack(pady=10)
        self.login_password_entry = ctk.CTkEntry(self.login_tab, show="*")
        self.login_password_entry.pack(pady=10)

        ctk.CTkButton(self.login_tab, text="Se connecter", command=self.login).pack(pady=20)

        # Widgets de l'onglet de création de compte
        ctk.CTkLabel(self.register_tab, text="Nom d'utilisateur").pack(pady=10)
        self.register_username_entry = ctk.CTkEntry(self.register_tab)
        self.register_username_entry.pack(pady=10)

        ctk.CTkLabel(self.register_tab, text="Mot de passe").pack(pady=10)
        self.register_password_entry = ctk.CTkEntry(self.register_tab, show="*")
        self.register_password_entry.pack(pady=10)

        ctk.CTkButton(self.register_tab, text="Télécharger un PDF", command=self.upload_pdf).pack(pady=10)

        self.terms_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self.register_tab, text="J'accepte les termes et conditions", variable=self.terms_var).pack(pady=10)

        ctk.CTkButton(self.register_tab, text="Créer un compte", command=self.register).pack(pady=20)

        # Texte des termes et conditions
        self.terms_text = """Cette toolbox n'a pas pour projet de nuire à autrui.
En utilisant cette toolbox, vous acceptez de l'utiliser de manière éthique et légale.
"""
        self.terms_button = ctk.CTkButton(self.register_tab, text="Lire les termes et conditions", command=self.show_terms)
        self.terms_button.pack(pady=10)

        self.pdf_path = None

    def show_terms(self):
        messagebox.showinfo("Termes et Conditions", self.terms_text)

    def upload_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.pdf_path:
            messagebox.showinfo("Succès", "PDF téléchargé avec succès")

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Succès", "Connexion réussie")
            # Logic for successful login (e.g., open main application)
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def register(self):
        if not self.terms_var.get():
            messagebox.showerror("Erreur", "Vous devez accepter les termes et conditions")
            return

        username = self.register_username_entry.get()
        password = self.register_password_entry.get()

        pdf_data = None
        if self.pdf_path:
            with open(self.pdf_path, 'rb') as file:
                pdf_data = file.read()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, pdf) VALUES (?, ?, ?)", (username, password, pdf_data))
            conn.commit()
            messagebox.showinfo("Succès", "Compte créé avec succès")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Nom d'utilisateur déjà pris")
        finally:
            conn.close()

if __name__ == "__main__":
    root = ctk.CTk()
    app = LoginApp(root)
    root.mainloop()
