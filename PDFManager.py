import customtkinter as ctk
import sqlite3
import webbrowser
import os
from tkinter import messagebox

class PDFManager:
    def __init__(self, master, db_conn):
        self.master = master
        self.db_conn = db_conn
        self.top = ctk.CTkToplevel(master)
        self.top.title("Available PDFs")
        self.top.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.pdf_listbox = ctk.CTkListbox(self.top)
        self.pdf_listbox.pack(pady=10, padx=10, fill=ctk.BOTH, expand=True)

        self.view_button = ctk.CTkButton(self.top, text="View PDF", command=self.view_pdf)
        self.view_button.pack(pady=10, padx=10)

        self.load_pdfs()

    def load_pdfs(self):
        cursor = self.db_conn.execute("SELECT id FROM captures")
        for row in cursor:
            self.pdf_listbox.insert(ctk.END, f"PDF Capture ID: {row[0]}")

    def view_pdf(self):
        selected_item = self.pdf_listbox.curselection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a PDF to view.")
            return

        pdf_id = int(self.pdf_listbox.get(selected_item).split(": ")[1])
        cursor = self.db_conn.execute("SELECT pdf_data FROM captures WHERE id=?", (pdf_id,))
        pdf_data = cursor.fetchone()[0]

        pdf_filename = f"capture_{pdf_id}.pdf"
        with open(pdf_filename, 'wb') as file:
            file.write(pdf_data)

        webbrowser.open(f"file://{os.path.abspath(pdf_filename)}")


# Example usage:
if __name__ == "__main__":
    root = ctk.CTk()  # Main application window
    db_conn = sqlite3.connect('packet_capture.db')  # Ensure this path is correct
    pdf_manager = PDFManager(root, db_conn)
    root.mainloop()
