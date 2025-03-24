import tkinter as tk

from sympy import sympify

from Tools import check_cursor, on_click, delete_zeros, round_number


class MemoryButtons:
    def __init__(self, master, update_operation_from_memory):
        self.master = master
        self.buttons_list = []
        self.text_buttons = ["MC", "MR", "M+", "M-", "MS", "ML"]
        self.memory = []
        self.create_buttons()
        # update operation_now when we click "MR"
        self.update_operation_from_memory = update_operation_from_memory

        self.operation_show = "0" #from class Display
        self.value_button = ""
        self.disable_buttons = True #at the start some buttons are off

        check_cursor(self.master, self.buttons_list)
        on_click(self.buttons_list, self.buttons_function)

    def update_operation_show(self, new_value):
        self.operation_show = new_value

    def get_memory_value(self):
        if self.memory:
            self.update_operation_from_memory(self.memory[-1])
        return "0"

    def calculation(self, sign):
        if self.memory:
            try:
                expression = str(self.memory[-1]) + sign + self.operation_show
                self.memory[-1] = delete_zeros(round_number(sympify(expression)))
            except Exception as e:
                print(f"Memory error: {e}")

    def buttons_function(self, i):
        self.value_button = self.text_buttons[i]  #txt from on_click

        if self.value_button == "MS":
            if not self.memory:
                self.enable_button()
                self.disable_buttons = False
            self.memory.append(str(self.operation_show))

        elif self.value_button in ["M+", "M-"]:
            if not self.memory:
                self.memory.append(str(self.operation_show))
                self.enable_button()
                self.disable_buttons = False
            else:
                self.calculation(self.value_button[-1])

        elif self.value_button == "ML":
            if not self.disable_buttons:
                print("List: ", self.memory)

        elif self.value_button == "MC":
            if not self.disable_buttons:
                self.memory = []
                self.disable_button()
                self.disable_buttons = True

        elif self.value_button == "MR":
            if not self.disable_buttons:
                self.get_memory_value()


    def create_buttons(self):
        count = 0
        for i in range(6):
            btn = tk.Button(self.master, fg="white", text=self.text_buttons[count],
                                bg="#77767a", activebackground="#49484a",
                                activeforeground="#959396", highlightbackground="blue",
                                justify="center", borderwidth=3)

            btn.grid(row=1, column=i, sticky=tk.NSEW, padx=1, pady=1)

            #strech column
            self.master.grid_columnconfigure(i, weight=1)
            self.buttons_list.append(btn)

            count += 1

        if not self.memory:
            self.disable_button()


    def disable_button(self):
        buttons_disable = [0, 1, 5]
        for i in range(3):
            self.buttons_list[buttons_disable[i]].config(state="disabled")

    def enable_button(self):
        button_enable = [0, 1, 5]
        for i in range(3):
            self.buttons_list[button_enable[i]].config(state="normal")