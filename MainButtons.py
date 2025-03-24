import tkinter as tk

from Tools import check_cursor

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
        check_cursor(self.master, self.buttons_list)

    def create_buttons(self):
        count = 0
        for i in range(6):
             for j in range(4):
                btn = tk.Button(self.master, fg="white", text=self.text_buttons[count],
                              bg="#77767a", activebackground="#49484a",
                              activeforeground="#959396", highlightbackground="blue",
                              justify="center", borderwidth=3)

                btn.grid(row=i, column=j, sticky=tk.NSEW, padx=1, pady=1)

                #strech row and column
                self.master.grid_rowconfigure(i, weight=1)
                self.master.grid_columnconfigure(j, weight=1)
                self.buttons_list.append(btn)

                count += 1