import subprocess
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

class PythonNmapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Nmap GUI")
        self.master.geometry("1000x900")  # Taille initiale de la fenêtre
        self.master.resizable(True, True)  # Permettre le redimensionnement de la fenêtre

        self.create_widgets()

    def create_widgets(self):
        # IP Entry
        ctk.CTkLabel(self.master, text="IP à scanner :").pack(padx=10, pady=5)
        self.ip_entry = ctk.CTkEntry(self.master, width=400)
        self.ip_entry.pack(padx=10, pady=5)

        # Options
        self.ping_scan_var = ctk.BooleanVar()
        self.service_scan_var = ctk.BooleanVar()
        self.os_detection_var = ctk.BooleanVar()
        self.aggressive_scan_var = ctk.BooleanVar()
        self.fast_scan_var = ctk.BooleanVar()

        frame = ctk.CTkFrame(self.master)
        frame.pack(padx=10, pady=5)

        ping_scan_check = ctk.CTkCheckBox(frame, text="Ping Scan (-sP)", variable=self.ping_scan_var)
        ping_scan_check.grid(row=0, column=0, sticky="w", padx=5)
        ToolTip(ping_scan_check, "Effectue un ping scan pour découvrir les hôtes actifs.")

        service_scan_check = ctk.CTkCheckBox(frame, text="Service Scan (-sV)", variable=self.service_scan_var)
        service_scan_check.grid(row=1, column=0, sticky="w", padx=5)
        ToolTip(service_scan_check, "Effectue une détection de version des services.")

        os_detection_check = ctk.CTkCheckBox(frame, text="OS Detection (-O)", variable=self.os_detection_var)
        os_detection_check.grid(row=2, column=0, sticky="w", padx=5)
        ToolTip(os_detection_check, "Détecte le système d'exploitation des hôtes.")

        aggressive_scan_check = ctk.CTkCheckBox(frame, text="Aggressive Scan (-A)", variable=self.aggressive_scan_var)
        aggressive_scan_check.grid(row=3, column=0, sticky="w", padx=5)
        ToolTip(aggressive_scan_check, "Effectue une analyse agressive incluant OS detection, version detection, script scanning, et traceroute.")

        fast_scan_check = ctk.CTkCheckBox(frame, text="Fast Scan (-T4)", variable=self.fast_scan_var)
        fast_scan_check.grid(row=4, column=0, sticky="w", padx=5)
        ToolTip(fast_scan_check, "Effectue une analyse rapide avec des temps d'attente plus courts.")

        # Run and Stop Buttons
        self.run_button = ctk.CTkButton(self.master, text="Run Nmap", command=self.run_nmap)
        self.run_button.pack(padx=10, pady=20)

        self.stop_button = ctk.CTkButton(self.master, text="Arrêter", command=self.stop_nmap)
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

    def open_help_page(self):
        webbrowser.open("https://nmap.org/book/man-briefoptions.html")

    def run_nmap(self):
        ip_range = self.ip_entry.get()
        
        global cmd
        nmap_path = r"C:\Users\Public\Documents\Master1\outils\Nmap\nmap.exe"
        cmd = [nmap_path]

        if self.ping_scan_var.get():
            cmd.append('-sP')
        if self.service_scan_var.get():
            cmd.append('-sV')
        if self.os_detection_var.get():
            cmd.append('-O')
        if self.aggressive_scan_var.get():
            cmd.append('-A')
        if self.fast_scan_var.get():
            cmd.append('-T4')

        cmd.append(ip_range)

        self.run_button.pack_forget()  # Hide the run button
        self.stop_button.pack()  # Show the stop button

        def execute():
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            total_steps = 100
            progress_step = total_steps / 10  # Assuming we have 10 major steps to reflect

            progress = 0
            for line in iter(process.stdout.readline, ''):
                self.result_text.insert(ctk.END, line)
                self.result_text.see(ctk.END)
                
                # Simulate progress update (nmap doesn't give progress updates, this is a placeholder)
                if re.search(r'Starting|Initiating|Completed', line):
                    progress += progress_step
                    self.progress_bar.set(progress / total_steps)
                
            process.stdout.close()
            stderr_output = process.stderr.read()
            if stderr_output:
                self.result_text.insert(ctk.END, "\n[ERROR OUTPUT]\n")
                self.result_text.insert(ctk.END, stderr_output)
            process.stderr.close()
            process.wait()
            self.progress_bar.set(1.0)  # Set to 100% completion at the end

            self.stop_button.pack_forget()
            self.run_button.pack()
            self.download_pdf_button.pack()  # Show download button after process completes

        self.execution_thread = Thread(target=execute)
        self.execution_thread.start()

    def stop_nmap(self):
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
        pdf_filename = f"nmap_results/nmap_{timestamp}_{random_str}.pdf"

        if not os.path.exists("nmap_results"):
            os.makedirs("nmap_results")

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
    app = PythonNmapApp(root)
    root.mainloop()
