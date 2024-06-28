import subprocess
import requests
import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox
from threading import Thread
import webbrowser
import re
import os
from datetime import datetime
import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip or not self.text:
            return
        self.tooltip = ctk.CTkLabel(self.widget, text=self.text, bg_color="yellow", text_color="black")
        self.tooltip.place(x=event.x_root + 10, y=event.y_root + 10)

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class SQLMapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SQLMap GUI")
        self.master.geometry("800x600")  # Taille initiale de la fenêtre
        self.master.resizable(True, True)  # Permettre la redimensionnement de la fenêtre

        self.sqlmap_path = r'C:\Users\Public\Documents\Master1\outils\sqlmap-master\sqlmap.py'
        self.process = None  # Pour stocker le processus en cours
        self.create_widgets()

    def create_widgets(self):
        # URL Entry
        ctk.CTkLabel(self.master, text="URL à tester :").pack(padx=10, pady=5)
        self.url_entry = ctk.CTkEntry(self.master, width=400)
        self.url_entry.pack(padx=10, pady=5)

        # Options
        self.random_agent_var = ctk.BooleanVar()
        self.crawl_var = ctk.BooleanVar()
        self.tamper_var = ctk.BooleanVar()
        self.dbs_var = ctk.BooleanVar()
        self.tables_var = ctk.BooleanVar()
        self.columns_var = ctk.BooleanVar()
        self.dump_var = ctk.BooleanVar()
        self.os_shell_var = ctk.BooleanVar()
        self.banner_var = ctk.BooleanVar()
        self.flush_session_var = ctk.BooleanVar()

        frame = ctk.CTkFrame(self.master)
        frame.pack(padx=10, pady=5)

        random_agent_check = ctk.CTkCheckBox(frame, text="Random Agent", variable=self.random_agent_var)
        random_agent_check.grid(row=0, column=0, sticky="w", padx=5)
        ToolTip(random_agent_check, "Utilise un User-Agent aléatoire pour chaque requête HTTP, ce qui peut aider à contourner certaines protections.")

        crawl_check = ctk.CTkCheckBox(frame, text="Crawl 2", variable=self.crawl_var)
        crawl_check.grid(row=1, column=0, sticky="w", padx=5)
        ToolTip(crawl_check, "Explore le site à la recherche d'URL supplémentaires à tester. Un niveau plus élevé permet de trouver plus de liens.")

        tamper_check = ctk.CTkCheckBox(frame, text="Tamper Scripts", variable=self.tamper_var)
        tamper_check.grid(row=2, column=0, sticky="w", padx=5)
        ToolTip(tamper_check, "Utilise des scripts pour obfusquer les requêtes et éviter la détection par les systèmes de protection.")

        dbs_check = ctk.CTkCheckBox(frame, text="List Databases", variable=self.dbs_var)
        dbs_check.grid(row=3, column=0, sticky="w", padx=5)
        ToolTip(dbs_check, "Liste toutes les bases de données disponibles.")

        tables_check = ctk.CTkCheckBox(frame, text="List Tables", variable=self.tables_var)
        tables_check.grid(row=4, column=0, sticky="w", padx=5)
        ToolTip(tables_check, "Liste toutes les tables dans une base de données spécifique.")

        columns_check = ctk.CTkCheckBox(frame, text="List Columns", variable=self.columns_var)
        columns_check.grid(row=5, column=0, sticky="w", padx=5)
        ToolTip(columns_check, "Liste toutes les colonnes dans une table spécifique.")

        dump_check = ctk.CTkCheckBox(frame, text="Dump Data", variable=self.dump_var)
        dump_check.grid(row=6, column=0, sticky="w", padx=5)
        ToolTip(dump_check, "Exporte les données d'une table spécifique.")

        os_shell_check = ctk.CTkCheckBox(frame, text="OS Shell", variable=self.os_shell_var)
        os_shell_check.grid(row=7, column=0, sticky="w", padx=5)
        ToolTip(os_shell_check, "Ouvre une shell système si possible.")

        banner_check = ctk.CTkCheckBox(frame, text="Get Banner", variable=self.banner_var)
        banner_check.grid(row=8, column=0, sticky="w", padx=5)
        ToolTip(banner_check, "Récupère la bannière de la base de données.")

        flush_session_check = ctk.CTkCheckBox(frame, text="Flush Session", variable=self.flush_session_var)
        flush_session_check.grid(row=9, column=0, sticky="w", padx=5)
        ToolTip(flush_session_check, "Vide toutes les données de session.")

        # Run and Stop Buttons
        self.run_button = ctk.CTkButton(self.master, text="Run SQLMap", command=self.run_sqlmap)
        self.run_button.pack(padx=10, pady=20)
        
        self.stop_button = ctk.CTkButton(self.master, text="Arrêter", command=self.stop_sqlmap)
        self.stop_button.pack(pady=10)
        self.stop_button.pack_forget()  # Hide initially

        # Results Box
        self.result_text = scrolledtext.ScrolledText(self.master, wrap='word', width=80, height=20)
        self.result_text.pack(padx=10, pady=10, expand=True, fill='both')

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.master)
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar.set(0)

        # Download PDF Button (initially hidden)
        self.download_pdf_button = ctk.CTkButton(self.master, text="Télécharger PDF", command=self.download_pdf)
        self.download_pdf_button.pack(pady=10)
        self.download_pdf_button.pack_forget()

        # Help Button (placed in the top right corner)
        help_button = ctk.CTkButton(self.master, text="Help", command=self.open_help_page)
        help_button.place(relx=1.0, rely=0.0, anchor='ne')

    def is_site_accessible(self, url):
        try:
            response = requests.head(url, timeout=5)  # Utiliser HEAD pour une requête rapide
            return response.status_code == 200
        except requests.RequestException:
            return False

    def open_help_page(self):
        webbrowser.open("https://sqlmap.org/usage.html")

    def run_sqlmap(self):
        url = self.url_entry.get()

        if not self.is_site_accessible(url):
            self.result_text.insert(ctk.END, f"Le site {url} n'est pas accessible.\n")
            return

        cmd = ['python', self.sqlmap_path, '-u', url, '--batch', '--level=1', '--risk=1', '--threads=5']

        if self.random_agent_var.get():
            cmd.append('--random-agent')
        if self.crawl_var.get():
            cmd.append('--crawl=2')
        if self.tamper_var.get():
            cmd.append('--tamper=between,randomcase')
        if self.dbs_var.get():
            cmd.append('--dbs')
        if self.tables_var.get():
            cmd.append('--tables')
        if self.columns_var.get():
            cmd.append('--columns')
        if self.dump_var.get():
            cmd.append('--dump')
        if self.os_shell_var.get():
            cmd.append('--os-shell')
        if self.banner_var.get():
            cmd.append('--banner')
        if self.flush_session_var.get():
            cmd.append('--flush-session')

        self.run_button.pack_forget()  # Hide the run button
        self.stop_button.pack()  # Show the stop button

        def execute():
            print(f"Executing command: {' '.join(cmd)}")  # Debugging: Print the command being executed
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            total_steps = 100
            progress_step = total_steps / 10  # Assuming we have 10 major steps to reflect

            progress = 0
            for line in iter(self.process.stdout.readline, ''):
                self.result_text.insert(ctk.END, line)
                self.result_text.see(ctk.END)
                
                # Update progress bar based on specific sqlmap output lines
                if re.search(r'testing (for|if|whether|the)', line):
                    progress += progress_step
                    self.progress_bar.set(progress / total_steps)
                
            self.process.stdout.close()
            stderr_output = self.process.stderr.read()
            if stderr_output:
                self.result_text.insert(ctk.END, "\n[ERROR OUTPUT]\n")
                self.result_text.insert(ctk.END, stderr_output)
            self.process.stderr.close()
            self.process.wait()
            self.progress_bar.set(1.0)  # Set to 100% completion at the end

            self.stop_button.pack_forget()
            self.run_button.pack()
            self.download_pdf_button.pack()  # Show download button after process completes

        self.execution_thread = Thread(target=execute)
        self.execution_thread.start()

    def stop_sqlmap(self):
        if self.process:
            self.process.terminate()
            self.result_text.insert(ctk.END, "\n[PROCESS TERMINATED]\n")
            self.process = None
            self.stop_button.pack_forget()
            self.run_button.pack()
            self.progress_bar.set(0)
            self.download_pdf_button.pack()  # Show download button even if process is terminated

    def download_pdf(self):
        now = datetime.now()
        timestamp = now.strftime("%d%m%Y_%H%M%S")
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        pdf_filename = f"sqlmap_results/sqlmap_{timestamp}_{random_str}.pdf"

        if not os.path.exists("sqlmap_results"):
            os.makedirs("sqlmap_results")

        # Create PDF using reportlab
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter
        text = c.beginText(40, height - 40)
        packets = self.result_text.get("1.0", ctk.END).strip().split("\n")

        for packet in packets:
            text.textLine(packet)
            if text.getY() < 40:
                c.drawText(text)
                c.showPage()
                text = c.beginText(40, height - 40)

        c.drawText(text)
        c.save()

        messagebox.showinfo("Succès", f"Le fichier PDF a été enregistré sous {pdf_filename}.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = SQLMapApp(root)
    root.mainloop()
