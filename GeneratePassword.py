import customtkinter as ctk
import random
import string
import webbrowser

class GeneratePasswordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Générateur de Mot de Passe")
        self.master.geometry("600x500")

        self.create_widgets()

    def create_widgets(self):
        # Définir les cadres pour l'organisation
        frame_top = ctk.CTkFrame(master=self.master)
        frame_top.pack(pady=20, padx=20, fill="x")

        frame_middle = ctk.CTkFrame(master=self.master)
        frame_middle.pack(pady=20, padx=20, fill="x")

        frame_bottom = ctk.CTkFrame(master=self.master)
        frame_bottom.pack(pady=20, padx=20, fill="both", expand=True)

        # Ajouter des widgets
        label = ctk.CTkLabel(master=frame_top, text="Générateur de Mot de Passe", font=("Arial", 24))
        label.pack(pady=10)

        # Slider pour sélectionner le niveau de sécurité
        label_slider = ctk.CTkLabel(master=frame_middle, text="Robustesse du mot de passe")
        label_slider.pack(pady=5)
        self.slider = ctk.CTkSlider(master=frame_middle, from_=1, to=10, number_of_steps=10)
        self.slider.pack(pady=5)

        # Bouton pour générer le mot de passe
        button_generate = ctk.CTkButton(master=frame_middle, text="Générer Mot de Passe", command=self.generate)
        button_generate.pack(pady=20)

        # Bouton pour ouvrir une page web
        button_info = ctk.CTkButton(master=frame_middle, text="En savoir plus", command=self.open_webpage)
        button_info.pack(pady=5)

        # Zone de texte pour afficher le mot de passe généré et le temps de brut force
        self.text_results = ctk.CTkTextbox(master=frame_bottom)
        self.text_results.pack(pady=20, padx=20, fill="both", expand=True)

    def estimate_crack_time(self, password):
        charset_size = len(set(password))
        possible_combinations = charset_size ** len(password)
        attempts_per_second = 1e9  # Hypothèse : 1 milliard d'essais par seconde
        seconds = possible_combinations / attempts_per_second

        if seconds < 60:
            return f"{seconds:.2f} secondes"
        elif seconds < 3600:
            return f"{seconds / 60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.2f} heures"
        elif seconds < 31536000:
            return f"{seconds / 86400:.2f} jours"
        elif seconds < 315360000:
            return f"{seconds / 31536000:.2f} ans"
        else:
            return f"{seconds / 315360000:.2f} siècles"

    def generate_password(self, strength_level):
        if strength_level == 1:
            characters = string.ascii_lowercase
            length = 4
        elif strength_level == 2:
            characters = string.ascii_lowercase + string.digits
            length = 6
        elif strength_level == 3:
            characters = string.ascii_letters + string.digits
            length = 8
        elif strength_level == 4:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 10
        elif strength_level == 5:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 12
        elif strength_level == 6:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 14
        elif strength_level == 7:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 16
        elif strength_level == 8:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 18
        elif strength_level == 9:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 20
        elif strength_level == 10:
            characters = string.ascii_letters + string.digits + string.punctuation
            length = 24
        else:
            return "", ""

        password = ''.join(random.choice(characters) for i in range(length))
        crack_time = self.estimate_crack_time(password)
        return password, crack_time

    def generate(self):
        strength_level = int(self.slider.get())
        password, crack_time = self.generate_password(strength_level)
        
        self.text_results.delete(1.0, ctk.END)
        self.text_results.insert(ctk.END, f"Mot de passe généré : {password}\n")
        self.text_results.insert(ctk.END, f"Temps estimé pour le brut force : {crack_time}")

    def open_webpage(self):
        webbrowser.open("https://fr.wikipedia.org/wiki/Mot_de_passe")

if __name__ == "__main__":
    root = ctk.CTk()
    app = GeneratePasswordApp(root)
    root.mainloop()
