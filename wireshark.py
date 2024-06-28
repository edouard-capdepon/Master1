import customtkinter as ctk
from scapy.all import AsyncSniffer
import threading
import psutil
import queue
import webbrowser
import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import messagebox
import random
import string

class NetworkPacketCaptureApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Network Packet Capture")
        self.master.geometry("1000x800")

        self.packet_queue = queue.Queue()
        self.sniffer = None  # Garder une référence au sniffer pour pouvoir l'arrêter

        self.create_widgets()
        self.update_output_box()

        self.db_conn = sqlite3.connect('packet_capture.db')
        self.create_table()

    def create_widgets(self):
        self.help_button = ctk.CTkButton(self.master, text="Help", command=self.open_help)
        self.help_button.pack(pady=10, padx=10, anchor='ne')

        self.interface_label = ctk.CTkLabel(self.master, text="Network Interface:")
        self.interface_label.pack(pady=10)

        self.interfaces = self.get_network_interfaces()
        self.interface_combobox = ctk.CTkComboBox(self.master, values=self.interfaces)
        self.interface_combobox.pack(pady=10)

        self.packet_count_label = ctk.CTkLabel(self.master, text="Number of Packets:")
        self.packet_count_label.pack(pady=10)

        self.packet_count_entry = ctk.CTkEntry(self.master)
        self.packet_count_entry.pack(pady=10)

        self.start_button = ctk.CTkButton(self.master, text="Start Capture", command=self.on_start_capture)
        self.start_button.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self.master, width=780, height=400)
        self.output_box.pack(pady=10)

        self.save_pdf_button = None  # Bouton générer PDF, initialement nul

    def get_network_interfaces(self):
        interfaces = psutil.net_if_addrs().keys()
        print(f"Available interfaces: {interfaces}")
        return list(interfaces)

    def validate_packet_count(self):
        try:
            max_packets = int(self.packet_count_entry.get())
            if max_packets <= 0:
                raise ValueError
            return max_packets
        except ValueError:
            self.output_box.insert(ctk.END, "Please enter a valid positive number for packet count.\n")
            self.output_box.yview(ctk.END)
            return None

    def on_start_capture(self):
        if self.sniffer and self.sniffer.running:
            self.sniffer.stop()
            self.sniffer = None

        interface = self.interface_combobox.get()
        max_packets = self.validate_packet_count()
        if max_packets is None:
            return

        self.output_box.delete('1.0', ctk.END)  # Clear output box
        print(f"Starting capture on interface: {interface} for {max_packets} packets")
        self.output_box.insert(ctk.END, f"Starting packet capture on interface: {interface} for {max_packets} packets\n")
        self.output_box.yview(ctk.END)
        capture_thread = threading.Thread(target=self.start_capture, args=(interface, max_packets))
        capture_thread.start()

    def start_capture(self, interface, max_packets):
        print(f"Starting packet capture on interface: {interface}")
        packet_count = 0

        def packet_handler(packet):
            nonlocal packet_count
            self.packet_queue.put(str(packet))
            packet_count += 1
            if packet_count >= max_packets:
                self.stop_sniffer()
                self.packet_queue.put("Packet capture finished.")
                print("Packet capture finished.")
                self.master.after(100, self.show_save_pdf_button)  # Affiche le bouton "Générer PDF" après un léger délai

        try:
            self.sniffer = AsyncSniffer(iface=interface, prn=packet_handler)
            self.sniffer.start()
            self.sniffer.join()
        except PermissionError:
            error_message = f"Permission denied: Unable to capture packets on interface {interface}. Please run as administrator."
            print(error_message)
            self.packet_queue.put(error_message)
        except Exception as e:
            error_message = f"Error capturing packets on interface {interface}: {e}"
            print(error_message)
            self.packet_queue.put(error_message)

    def stop_sniffer(self):
        if self.sniffer and self.sniffer.running:
            try:
                self.sniffer.stop()
                print("Sniffer stopped successfully.")
            except Exception as e:
                print(f"Error stopping sniffer: {e}")

    def update_output_box(self):
        while not self.packet_queue.empty():
            packet = self.packet_queue.get()
            print(f"Displaying packet: {packet[:50]}...")  # Afficher le début du paquet pour confirmation
            self.output_box.insert(ctk.END, packet + "\n")
            self.output_box.yview(ctk.END)
        self.master.after(100, self.update_output_box)

    def show_save_pdf_button(self):
        if self.save_pdf_button is None:
            self.save_pdf_button = ctk.CTkButton(self.master, text="Générer PDF", command=self.save_as_pdf)
            self.save_pdf_button.pack(pady=10)
            print("Générer PDF button displayed.")
        else:
            print("Générer PDF button already displayed.")

    def save_as_pdf(self):
        try:
            directory = "wireshark_results"
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            
            timestamp = datetime.now().strftime("%d_%m_%Y")
            random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            pdf_filename = os.path.join(directory, f"wireshar_{timestamp}_{random_id}.pdf")
            print(f"Saving PDF as: {pdf_filename}")
            
            packets = self.output_box.get("1.0", ctk.END).strip().split("\n")
            print(f"Packets to save: {len(packets)}")

            c = canvas.Canvas(pdf_filename, pagesize=letter)
            width, height = letter
            text = c.beginText(40, height - 40)

            for packet in packets:
                text.textLine(packet)
                if text.getY() < 40:
                    c.drawText(text)
                    c.showPage()
                    text = c.beginText(40, height - 40)

            c.drawText(text)
            c.save()
            print(f"PDF generation complete: {pdf_filename}")

            self.save_pdf_to_db(pdf_filename)
            self.output_box.insert(ctk.END, f"\nPDF saved as {pdf_filename}\n")
            messagebox.showinfo("PDF Saved", f"PDF saved as {pdf_filename}")
            print(f"PDF saved as {pdf_filename}")
        except Exception as e:
            error_message = f"Error saving PDF: {e}"
            print(error_message)
            self.output_box.insert(ctk.END, f"\n{error_message}\n")

    def save_pdf_to_db(self, pdf_filename):
        try:
            with open(pdf_filename, 'rb') as file:
                pdf_data = file.read()
            self.db_conn.execute("INSERT INTO captures (pdf_data) VALUES (?)", (pdf_data,))
            self.db_conn.commit()
            print(f"PDF saved to database: {pdf_filename}")
        except Exception as e:
            print(f"Error saving PDF to database: {e}")

    def create_table(self):
        self.db_conn.execute("""
            CREATE TABLE IF NOT EXISTS captures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_data BLOB
            )
        """)
        self.db_conn.commit()

    def open_help(self):
        webbrowser.open("https://www.wireshark.org/docs/")

if __name__ == "__main__":
    if os.name == 'nt':
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:
        is_admin = os.geteuid() == 0

    if not is_admin:
        raise PermissionError("This script must be run as an administrator/root.")
    
    root = ctk.CTk()
    app = NetworkPacketCaptureApp(root)
    root.mainloop()
