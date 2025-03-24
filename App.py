import tkinter as tk

from Display import Display
from MainButtons import Buttons
from Menu import Menu

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Calculator")
        self.master.iconphoto(False, tk.PhotoImage(file="png/icon.png"))
        self.master.geometry("355x500") #325
        self.master.config(bg="#12171f")

        #Configure row
        self.master.grid_rowconfigure(0, weight=150) #Numbers
        self.master.grid_rowconfigure(1, weight=30) #Top
        self.master.grid_rowconfigure(2, weight=190,) #Buttons
        self.master.grid_columnconfigure(0, weight=1)

        #Frame of numbers
        self.numbers_frame = tk.Frame(self.master)
        self.numbers_frame.grid(row=0, column=0, sticky="nsew")
        self.numbers_frame.grid_propagate(False)  #Const height
        #Frame old operation
        self.memory_buttons_frame = tk.Frame(self.master, bg="gray")
        self.memory_buttons_frame.grid(row=1, column=0, sticky="nsew")
        self.memory_buttons_frame.grid_propagate(False)  #Const height
        # Frame of buttons
        self.buttons_frame = tk.Frame(self.master, bg="black")
        self.buttons_frame.grid(row=2, column=0, sticky="nsew")

        buttons = Buttons(self.buttons_frame)
        display = Display(self.numbers_frame, buttons.buttons_list, buttons.text_buttons, self.memory_buttons_frame)
        menu = Menu(self.master)

root = tk.Tk()
myApp = App(root)
myApp.mainloop()
