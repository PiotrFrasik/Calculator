import tkinter as tk

class Menu:
    def __init__(self, master):
        self.master = master
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)  # Teraz przypisujemy menu do głównego okna

        main_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Motives", menu=main_menu)
        self.menu_bar.add_cascade(label="About", menu=main_menu)