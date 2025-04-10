import tkinter as tk
import customtkinter as ctk

class Buttons:
    def __init__(self, master):
        self.master = master
        self.buttons_list = []
        self.text_buttons = ["%", "CE", "C", "⌫",
                             "¹⁄ₓ", "x²", "√", "÷",
                             "7", "8", "9", "×",
                             "4", "5", "6", "-",
                             "1", "2", "3", "+",
                             "±", "0", ".", "="]
        self.clicked_button = ""
        self.create_buttons()

    def create_buttons(self):
        count = 0
        for i in range(6):
             for j in range(4):
                btn = ctk.CTkButton(
                     self.master,
                     text=self.text_buttons[count],
                     fg_color="#4a4c4c",
                     hover_color="#5b5b5b",
                     font=("Segoe UI Variable", 15),
                     text_color="white",
                     corner_radius=5,
                )

                btn.grid(row=i, column=j, sticky=tk.NSEW, padx=1, pady=1)

                if count in (8, 9, 10, 12, 13, 14, 16, 17, 18, 20, 21, 22):
                    btn.configure(fg_color="#5b5b5b", hover_color="#4a4c4c")
                elif count == 23:
                    btn.configure(fg_color="#4cc2ff", hover_color="#44afe6")

                #strech row and column
                self.master.grid_rowconfigure(i, weight=1)
                self.master.grid_columnconfigure(j, weight=1)
                self.buttons_list.append(btn)

                count += 1