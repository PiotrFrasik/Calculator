import tkinter as tk
from sympy import sympify
import math

from MemoryButtons import MemoryButtons
from Tools import on_click, delete_zeros, round_number

class Display:

    def __init__(self, master, buttons_list, text_buttons, memory_buttons_frame, buttons_frame, main_window):
        #create memory_buttons
        self.memory_buttons = MemoryButtons(memory_buttons_frame,
                                            self.update_operation_from_memory,
                                            buttons_frame, main_window)
        #master.bind("<Configure>", self.memory_buttons.on_resize(master.winfo_width()))

        self.update_operation_show = self.memory_buttons.update_operation_show #for class MemoryButtons

        self.get_memory_value = self.memory_buttons.get_memory_value() #from class MemoryButtons

        self.master = master
        self.buttons_list = buttons_list
        self.text_buttons = text_buttons
        self.operation = "" #operation in operation_old
        self.operation_now = "0" #new number
        self.operation_now_delete = ""
        self.operation_old = ""
        self.result = "" #result operation_old before display
        self.value_button = ""
        self.fg_show_now = 39 #size font show_now
        self.number_operation_old = "" #only number from operation_old
        self.twice_click_plus_minus = False
        self.sqrt = False #information that we use √
        self.second_number = False

        on_click(self.buttons_list, self.buttons_function)

        self.show_old = tk.Label(self.master,
                                 text=self.operation_old,
                                 justify=tk.RIGHT,
                                 bg="#282828",
                                 fg="#939393",
                                 font=("Segoe UI Variable", 12),
                                 pady=5,
                                 anchor="e"
                                 )
        self.show_old.grid(row=0, column=0, sticky="nse")

        self.show_now = tk.Label(self.master,
                                 text=self.operation_now,
                                 justify=tk.RIGHT,
                                 bg="#282828",
                                 fg="white",
                                 font=("Segoe UI Variable",
                                       self.fg_show_now,
                                       "bold"),
                                 anchor="e"
                                 )
        self.show_now.grid(row=1, column=0, sticky="nes")

        self.master.grid_rowconfigure(0, weight=10)
        self.master.grid_rowconfigure(1, weight=60)
        self.master.grid_columnconfigure(0, weight=1)

        self.display()

    def buttons_function(self, i):

        self.value_button = self.text_buttons[i]  # txt from on_click

        # security in situation if disable_button don't work
        if self.operation_now == "Overflow" and self.value_button in "%¹⁄ₓx²√÷×-+.":
            return

        elif self.operation_now == "Overflow" and self.value_button in "CE⌫0123456789=":
            self.enable_button()
            self.clear_display_result()

        #security from crash application
        if self.operation_now != "" and self.operation_now != "Overflow":
            if self.operation_now in "+-÷×":
                self.operation_now = self.operation_now[:-2]

            if (math.isinf(float(self.operation_now.replace(" ", "")))
                    or (float(self.operation_now.replace(" ", "")) == 0.0
                        and "e-" in self.operation_now)):
                self.change_size_font(25)
                self.operation_now = "Overflow"
                self.disable_button()
                self.display()
                self.value_button = ""
                return

        if self.operation == "0" and self.fg_show_now != 39:
            self.fg_show_now = 39
            self.change_size_font(self.fg_show_now)

        if self.value_button in "+-÷×":
            if self.operation_now.replace(" ", "") == "":
                for char in "+-÷× ":
                    self.operation_now = self.operation_now.replace(char, "")

            if self.value_button in self.operation_old and self.next_number():
                self.twice_click_plus_minus = True
                self.equal()
            else:
                #situacion if clicked twice "=" and next clicked "-" or "+"
                if self.result and self.value_button in "+-÷×":
                    self.number_operation_old = ""
                    self.operation_old = str(
                        delete_zeros(round_number(sympify(self.result).evalf()))) + " " + self.value_button + " "
                    self.operation_now = self.operation_old.split()[0]

                elif self.value_button in "+-÷×":
                    if self.sqrt:
                        self.operation_old = self.operation_now + " " + self.value_button + " "
                    else:
                        if len(self.operation_old) > 2:
                            if self.operation_old[-2] not in self.value_button:
                                self.operation_old = self.operation_old[:-2] + self.value_button + " "
                        else:
                            #display when click "+-÷×", the same number in operation_old and operation_now
                            self.operation_old = self.operation_now + " " + self.value_button + " " + self.operation_old
                            self.operation_now = self.operation_old[:-3]

                self.second_number = True
                self.operation = self.value_button
                self.display()

        elif self.value_button == "C":
            #clean everything
            self.clear_display_result()
            self.change_size_font(self.fg_show_now)

        elif self.value_button == "CE":
            #clean everything
            if self.result:
                self.clear_display_result()
            else: #clean self.operation_now
                self.operation_now = "0"
                self.display()

            self.change_size_font(self.fg_show_now)

        elif self.value_button == "⌫":
            if "e" in self.operation_now:
                return

            if not self.operation_now or self.operation_now == "0":
                return
            else:
                try:
                    if self.operation_now[-2] == " " and len(self.operation_now) > 2 : #when oper.now like "555 555"
                        self.operation_now = self.operation_now[:-2]
                    else:
                        self.operation_now = self.operation_now[:-1]

                except IndexError:
                    self.operation_now = "0"

            self.max_numbers_show(self.operation_now)
            self.display()

        elif self.value_button in "%√":
            result = 0
            #number = self.operation_now #operation_now in the form √(x) in operation_old
            self.operation_now = self.operation_now.replace(" ", "")

            if self.operation_now == "":
                self.operation_now = self.result

            if self.value_button == "%":
                result = delete_zeros(sympify(f"{self.operation_now} / 100").evalf())
            elif self.value_button == "√":
                result = delete_zeros(sympify(f"sqrt({self.operation_now})").evalf())
                self.sqrt = True

            if len(str(result)) > 15:
                result = round_number(result)

            self.max_numbers_show(result)  #if len(number) is bigger than 14

            self.operation_now = str(result)

            self.display()

        elif self.value_button == "¹⁄ₓ":
            self.operation_now = self.operation_now.replace(" ", "")
            if self.operation_now == "0":
                self.change_size_font(17)
                self.operation_now = "Nie można dzielić przez zero"
                self.operation_old = "1/(0)"
            else:
                result = delete_zeros(sympify(f"1 / {self.operation_now}").evalf())
                length = len(str(result))

                if length > 15:
                    result = round_number(result)
                self.max_numbers_show(result) #if len(number) is bigger than 14

                self.operation_now = str(result)

            self.operation = self.value_button
            self.display()
            if self.operation_now == "Nie można dzielić przez zero" and self.operation_old == "1/(0)":
                self.operation_now = "0"
                self.operation_old = ""

        elif self.value_button == "x²":
            if self.operation_now == "":
                self.operation_now = self.result
            self.operation_now = self.operation_now.replace(" ", "")
            result = delete_zeros(sympify(f"{self.operation_now} * {self.operation_now}").evalf())

            length = len(str(result))

            if length > 15:
                result = round_number(result)

            self.max_numbers_show(result)  # if len(number) is bigger than 14
            self.operation_now = str(result)

            self.operation = self.value_button
            self.display()

        elif self.value_button == ".":
            if len(str(self.operation_now)) < 17:
                if self.operation_now[-1] == " ":
                    self.operation_now = self.operation_now[:-1]
                self.operation_now = self.operation_now + "."
            self.display()

        elif self.value_button == "±":
            self.operation_now = delete_zeros(sympify(f"{self.operation_now} * -1").evalf())
            self.display()

        elif self.value_button in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            if self.second_number:
                self.operation_now = "0"
                self.second_number = False

            max_numbers = 16 if "." in self.operation_now else 14
            #max 12 numbers on the screen
            if len(self.operation_now.replace(" ", "")) <= max_numbers:

                #show more numbers on the screen minimizing size of them
                if len(self.operation_now.replace(" ", "")) > 8:
                    if self.fg_show_now != 27:
                        self.fg_show_now = self.fg_show_now - 3
                        self.change_size_font(self.fg_show_now)
                else:
                    self.fg_show_now = 39
                    self.change_size_font(self.fg_show_now)

                if self.operation_now == "0": #for example first try application
                    self.operation_now = self.value_button
                #space after three numbers
                elif len(self.operation_now.replace(" ", "")) % 3 == 0 and self.operation_now.find(".") == -1:
                    self.operation_now = str(self.operation_now) + " " + self.value_button
                else:
                    self.operation_now = (self.operation_now + self.value_button)

            self.display()

        elif self.value_button == "=":
            self.equal()

    def equal(self):

        if self.operation_now == "0" and self.operation_old == "":
            return

        self.result = 0 #If click "CE" and before you wasn't clicked "="

        #if we use twice_click_plus_minus and click "=" and operation_now = ""
        if self.next_number() and self.operation_now.replace(" ", "") == "":
            self.operation_now = self.operation_old.split()[0]
            self.operation_old = self.operation_old + " "
            self.display()

        try:
            self.result = sympify(((self.operation_old.replace("÷", "/").replace("×", "*") + self.operation_now).replace(" ", "")).replace("=", "")).evalf()
        except ValueError:
            return

        sign = self.operation #operation sign

        sign2 = "error_sign"

        #if after basic operation clicked special operation
        if any(sgn in self.operation_old for sgn in "+-÷×"):
            sign2 = self.operation_old.split()[1]

        if self.number_operation_old == "":
            self.number_operation_old = self.operation_now

        self.result = str(self.result)

        #full operation on the screen and result on the screen
        if self.twice_click_plus_minus:
            try:
                self.operation_now = delete_zeros(round_number(self.result))
                if sign in "+-÷×":
                    self.operation_old = delete_zeros(round_number(self.result)) + " " + sign
                else:
                    self.operation_old = delete_zeros(round_number(self.result)) + " " + sign2
            except Exception:
                self.operation_now = self.operation_old[:-2]
                self.value_button = sign
                return
        else:
            #assignment to value of the screen
            self.operation_old = self.operation_old + self.operation_now + " " + self.value_button

            if self.result.find("e") == -1:
                self.operation_now = delete_zeros(round_number(self.result))
            else:
                self.operation_now = round_number(self.result)

        #floating-point numbers
        if len(str(self.operation_now)) > 15:
            self.operation_now = str(round_number(self.operation_now))

        self.max_numbers_show(self.operation_now)  #if len(number) is bigger than 14

        self.display()

        self.operation_now_delete = self.operation_now  #for button "⌫"

        if self.number_operation_old not in self.operation_old:
            self.number_operation_old = self.find_sign_operation()

        if self.twice_click_plus_minus:
            self.twice_click_plus_minus = False
            #self.operation_now = ""
        else:
            #if click "=" twice - you need operation with the same number
            if sign in "+-/*":
                self.operation_old = self.operation_now + " " + sign + " " + self.number_operation_old
            else:
                self.operation_old = self.operation_now + " " + sign2 + " " + self.number_operation_old

        self.operation_now = ""  # information that we clicked twice "="
        self.second_number = False

    #Click "MR" and get memory[-1] value
    def update_operation_from_memory(self, new_value, display = True):
        self.operation_now = new_value
        if display:
            self.display()

    def display(self):
        if self.get_memory_value:
            self.show_now.config(text=self.operation_now)
        else:
            self.show_now.config(text=self.operation_now)
        self.show_old.config(text=self.operation_old)
        # change operation_show from class MemoryButtons
        self.update_operation_show(self.operation_now)


    def clear_display_result(self):
        self.result = ""
        self.operation_now = "0"
        self.operation_old = ""
        self.operation_now_delete = ""
        self.number_operation_old = ""
        self.fg_show_now = 39
        self.change_size_font(self.fg_show_now)
        self.display()

    def change_size_font(self, size):
        self.show_now.config(font=("Segoe UI Variable", size, "bold"))

    def max_numbers_show(self, number):
        if type(number) != str:
            number = str(number)

        # max thirteen number on the screen in time fg = 39
        # max sixteen number on the screen in time fg = 27
        length = len(number)
        if 14 <= length <= 16:
            self.fg_show_now = 39 - ((length * 3) - 39) - 3
            self.change_size_font(self.fg_show_now)

    def disable_button(self):
        #"%","¹⁄ₓ","x²","√","÷","×", "-","+",".","±"
        buttons_disable = [0, 4, 5, 6, 7, 11, 15, 19, 20, 22]
        for i in range(10):
            self.buttons_list[buttons_disable[i]].configure(state="disabled")
        #for memory buttons
        for i in range(6):
            self.memory_buttons.buttons_list[i].configure(state="disabled")
        self.memory_buttons.disable_all  = True

    def enable_button(self):
        #"%","¹⁄ₓ","x²","√","÷","×", "-","+",".","±"
        buttons_enable = [0, 4, 5, 6, 7, 11, 15, 19, 20, 22]
        for i in range(10):
            self.buttons_list[buttons_enable[i]].configure(state="normal")
        #for memory buttons
        for i in range(6):
            self.memory_buttons.buttons_list[i].configure(state="normal")
        self.memory_buttons.disable_all = False

        #check if all memory_buttons should work
        if not self.memory_buttons.memory_value:
            self.memory_buttons.disable_button()
            self.memory_buttons.disable_buttons_value = True

    def find_sign_operation(self):
        #find second number after operation in operation_old
        excluded_chars = "+-÷×="

        operation_old = self.operation_old
        if operation_old[0] == "-":
            self.operation_old = self.operation_old[1:]
        elif "e" in operation_old:
            index_e = operation_old.find("e")
            operation_old = (operation_old[:index_e]
                             + operation_old[index_e + 2:])  # Delete "e" oraz "+" or "-" after "e"

        indeks_operation = min(
            (self.operation_old.replace(" ", "").find(op) for op in "+-÷×" if op in self.operation_old), default=-1)

        number_operation_now = self.operation_old[indeks_operation+2:]

        #if excluded_chars in number_operation_now:
        number_operation_now = "".join(char for char in number_operation_now if char not in excluded_chars)
        number_operation_now = number_operation_now[1:-1] #delete first and last space character

        self.operation_old = operation_old

        return number_operation_now

    def next_number(self):
        operation_old = self.operation_old

        if operation_old[0] == "-":
            operation_old = operation_old[1:]
        elif "e" in operation_old:
            index_e = operation_old.find("e")
            operation_old = operation_old[:index_e] + operation_old[
                                                      index_e + 2:]  # Delete "e" oraz "+" or "-" after "e"

        operation_old = operation_old.replace(" ", "")

        indeks_operation = min(
            (operation_old.find(op) for op in "+-÷×" if op in operation_old), default=-1)

        if len(operation_old) == indeks_operation + 1:
            return True
        else:
            return False