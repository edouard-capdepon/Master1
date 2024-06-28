import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import os
from datetime import datetime
import webbrowser

# Import des classes d'outils existants
from GeneratePassword import GeneratePasswordApp
from python_nmap import PythonNmapApp
from SQLmap_app import SQLMapApp
from wireshark import NetworkPacketCaptureApp

# Configuration de la base de données
db_path = "users.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la table des utilisateurs
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)''')
conn.commit()
conn.close()

class LoginApp:
    def __init__(self, master, show_home_callback):
        self.master = master
        self.master.title("Login")
        self.master.geometry("400x500")
        self.show_home_callback = show_home_callback

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

        # Termes et conditions
        self.terms_text = """Cette toolbox n'a pas pour projet de nuire à autrui.
En utilisant cette toolbox, vous acceptez de l'utiliser de manière éthique et légale.
"""
        ctk.CTkLabel(self.register_tab, text="Conditions d'utilisation :").pack(pady=10)
        self.terms_textbox = ctk.CTkTextbox(self.register_tab, width=300, height=100)
        self.terms_textbox.pack(pady=10)
        self.terms_textbox.insert(ctk.END, self.terms_text)
        self.terms_textbox.configure(state="disabled")

        self.terms_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self.register_tab, text="J'accepte les termes et conditions", variable=self.terms_var).pack(pady=10)

        ctk.CTkButton(self.register_tab, text="Créer un compte", command=self.register).pack(pady=20)

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
            self.show_home_callback()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def register(self):
        if not self.terms_var.get():
            messagebox.showerror("Erreur", "Vous devez accepter les termes et conditions")
            return

        username = self.register_username_entry.get()
        password = self.register_password_entry.get()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Succès", "Compte créé avec succès")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Nom d'utilisateur déjà pris")
        finally:
            conn.close()

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Toolbox Home")
        self.master.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.tab_view = ctk.CTkTabview(self.master)
        self.tab_view.pack(expand=1, fill='both')

        self.home_tab = self.tab_view.add("Home")
        self.results_tab = self.tab_view.add("Gestionnaire de résultats")

        self.title_label = ctk.CTkLabel(self.home_tab, text="Toolbox Home", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.generate_password_button = ctk.CTkButton(self.home_tab, text="Generate Password", command=self.open_generate_password)
        self.generate_password_button.pack(pady=10)

        self.python_nmap_button = ctk.CTkButton(self.home_tab, text="Python Nmap", command=self.open_python_nmap)
        self.python_nmap_button.pack(pady=10)

        self.sqlmap_button = ctk.CTkButton(self.home_tab, text="SQLMap", command=self.open_sqlmap)
        self.sqlmap_button.pack(pady=10)

        self.wireshark_button = ctk.CTkButton(self.home_tab, text="Wireshark", command=self.open_wireshark)
        self.wireshark_button.pack(pady=10)

        self.logout_button = ctk.CTkButton(self.home_tab, text="Déconnexion", command=self.logout)
        self.logout_button.pack(pady=10)

        self.create_results_tab()

    def create_results_tab(self):
        self.results_notebook = ttk.Notebook(self.results_tab)
        self.results_notebook.pack(expand=1, fill='both')

        self.create_tool_tab("Wireshark", "wireshark_results")
        self.create_tool_tab("Nmap", "nmap_results")
        self.create_tool_tab("SQLMap", "sqlmap_results")

    def create_tool_tab(self, tool_name, directory):
        frame = ttk.Frame(self.results_notebook)
        self.results_notebook.add(frame, text=tool_name)

        refresh_button = ctk.CTkButton(frame, text="Rafraîchir les PDF", command=lambda: self.refresh_file_list(directory, frame))
        refresh_button.pack(pady=10)

        pdf_table = ttk.Treeview(frame, columns=("Nom du fichier", "Date de création"), show='headings')
        pdf_table.heading("Nom du fichier", text="Nom du fichier")
        pdf_table.heading("Date de création", text="Date de création")
        pdf_table.bind('<Double-1>', lambda event, table=pdf_table: self.open_pdf(table))
        pdf_table.pack(pady=10, fill='both', expand=True)

        self.refresh_file_list(directory, frame)

    def open_generate_password(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = GeneratePasswordApp(self.new_window)

    def open_python_nmap(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = PythonNmapApp(self.new_window)

    def open_sqlmap(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = SQLMapApp(self.new_window)

    def open_wireshark(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = NetworkPacketCaptureApp(self.new_window)

    def logout(self):
        self.master.destroy()
        root = ctk.CTk()
        login_app = LoginApp(root, self.show_home)
        root.mainloop()

    def show_home(self):
        self.master.destroy()
        root = ctk.CTk()
        app = MainApp(root)
        root.mainloop()

    def refresh_file_list(self, directory, frame):
        pdf_table = frame.winfo_children()[1]
        try:
            for row in pdf_table.get_children():
                pdf_table.delete(row)
            if os.path.exists(directory):
                files = os.listdir(directory)
                pdf_files = [f for f in files if f.endswith(".pdf")]
                for pdf_file in sorted(pdf_files):
                    file_path = os.path.join(directory, pdf_file)
                    creation_time = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    pdf_table.insert('', 'end', values=(pdf_file, creation_time))
            else:
                pdf_table.insert('', 'end', values=("No PDF files found.", ""))
        except Exception as e:
            error_message = f"Error refreshing file list: {e}"
            print(error_message)
            pdf_table.insert('', 'end', values=(error_message, ""))

    def open_pdf(self, pdf_table):
        selected_item = pdf_table.selection()
        if selected_item:
            file_name = pdf_table.item(selected_item, "values")[0]
            directory = self.results_notebook.tab(self.results_notebook.select(), "text").lower() + "_results"
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                webbrowser.open_new(file_path)
            else:
                messagebox.showerror("Erreur", "Le fichier n'existe pas.")

if __name__ == "__main__":
    def show_home():
        root.destroy()
        home_root = ctk.CTk()
        app = MainApp(home_root)
        home_root.mainloop()

    root = ctk.CTk()
    login_app = LoginApp(root, show_home)
    root.mainloop()
