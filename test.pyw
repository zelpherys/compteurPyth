import tkinter as tk
import os
import ctypes
import threading
import keyboard  # Importer le module keyboard

class DeathCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("Compteur de Morts")
        self.root.geometry("170x140")  # Définir la taille de la fenêtre
        self.root.configure(bg="black")  # Définir le fond noir

        # Supprimer l'icône par défaut
        self.root.iconbitmap(default='')

        # Utiliser ctypes pour rendre la barre de titre noire
        hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int(1)))

        self.count = self.read_count_from_file()
        
        self.label = tk.Label(root, text=f"Nombre de Morts: {self.count}", font=("Helvetica", 10), fg="white", bg="black")
        self.label.pack(pady=5)
        
        self.increment_button = tk.Button(root, text="Ajouter une Mort", command=self.increment_count, font=("Helvetica", 8), fg="white", bg="black")
        self.increment_button.pack(pady=2)
        
        self.decrement_button = tk.Button(root, text="Enlever une Mort", command=self.decrement_count, font=("Helvetica", 8), fg="white", bg="black")
        self.decrement_button.pack(pady=2)

        # Lier plusieurs variantes de la touche + du pavé numérique à la fonction increment_count
        self.root.bind('<KP_Add>', lambda event: self.increment_count())
        self.root.bind('<plus>', lambda event: self.increment_count())
        self.root.bind('<+>', lambda event: self.increment_count())

        # Démarrer un thread séparé pour écouter les pressions de touches globales
        threading.Thread(target=self.listen_for_keypress, daemon=True).start()
        
    def increment_count(self):
        self.count += 1
        self.label.config(text=f"Nombre de Morts: {self.count}")
        self.write_count_to_file()
        
    def decrement_count(self):
        if self.count > 0:
            self.count -= 1
            self.label.config(text=f"Nombre de Morts: {self.count}")
            self.write_count_to_file()
        
    def read_count_from_file(self):
        if os.path.exists("count.txt"):
            with open("count.txt", "r") as file:
                return int(file.read())
        return 0
    
    def write_count_to_file(self):
        with open("count.txt", "w") as file:
            file.write(str(self.count))

    def listen_for_keypress(self):
        keyboard.add_hotkey('num 9', self.increment_count)  # Remplacer 'num +' par 'num 9'

if __name__ == "__main__":
    root = tk.Tk()
    app = DeathCounter(root)
    root.mainloop()
