import tkinter as tk
import customtkinter as ctk

from Display import Display
from MainButtons import Buttons
from Menu import Menu


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Calculator")
        self.master.iconphoto(False, tk.PhotoImage(file="png/icon.png"))
        self.master.geometry("365x500") #325, 355
        self.master.config(bg="#282828")

        #Configure row
        self.master.grid_rowconfigure(0, weight=5)  #Menu
        self.master.grid_rowconfigure(1, weight=120) #Numbers
        self.master.grid_rowconfigure(2, weight=30) #Top
        self.master.grid_rowconfigure(3, weight=150) #Buttons

        self.master.grid_columnconfigure(0, weight=1)

        self.menu_frame = ctk.CTkFrame(self.master, fg_color="#282828",
                                       height=25, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")

        self.menu_frame.grid_propagate(False)  # Const height

        #Frame of numbers
        self.numbers_frame = tk.Frame(self.master, bg="#282828")
        self.numbers_frame.grid(row=1, column=0, sticky="nsew")
        self.numbers_frame.grid_propagate(False)  #Const height
        #Frame old operation
        self.memory_buttons_frame = tk.Frame(self.master, bg="#282828")
        self.memory_buttons_frame.grid(row=2, column=0, sticky="nsew")
        self.memory_buttons_frame.grid_propagate(False)  #Const height
        # Frame of buttons
        self.buttons_frame = tk.Frame(self.master, bg="#282828")
        self.buttons_frame.grid(row=3, column=0, sticky="nsew")

        buttons = Buttons(self.buttons_frame)
        Display(self.numbers_frame, buttons.buttons_list,
                buttons.text_buttons, self.memory_buttons_frame,
                self.buttons_frame, self.master)
        Menu(self.menu_frame)


root = tk.Tk()
myApp = App(root)
myApp.mainloop()
