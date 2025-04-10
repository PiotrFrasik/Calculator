import tkinter as tk
import customtkinter as ctk
from sympy import sympify
import uuid #generate unique ID for each frame

from AnimatedDownPanel import AnimatedDownPanel
from Tools import on_click, delete_zeros, round_number


def hover_label(color, widget1, widget2):
    widget1.configure(fg_color=color)
    widget2.configure(fg_color=color)


class MemoryButtons:
    def __init__(self, master, update_operation_from_memory, buttons_frame, main_window):
        self.master = master
        self.buttons_list = []
        self.text_buttons = ["MC", "MR", "M+", "M-", "MS", "ML"]
        self.memory_value = {} #with uuid
        self.create_buttons()
        self.buttons_frame = buttons_frame
        self.main_window = main_window

        # update operation_now when we click "MR"
        self.update_operation_from_memory = update_operation_from_memory

        self.operation_show = "0" #from class Display
        self.value_button = ""
        self.disable_buttons_value = True #at the start some buttons are off
        self.disable_all = False #when calculator is overflowing

        on_click(self.buttons_list, self.buttons_function)

        self.animated_panel = AnimatedDownPanel(buttons_frame,
                                                1, 0,
                                                self.disable_button, self.enable_button)
        self.animated_panel.grid_rowconfigure(0, weight=1)
        self.animated_panel.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = ctk.CTkScrollableFrame(self.animated_panel, fg_color="#282828")
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")


        self.down_frame = ctk.CTkFrame(self.animated_panel, fg_color="#282828")
        self.down_frame.grid(column=0, row=0, sticky="sew", pady=2)
        self.down_frame.columnconfigure(0, weight=1)
        self.down_frame.rowconfigure(0, weight=1)

        #listeninig if there is new size of window
        self.master.bind("<Configure>", self.on_resize)


    def on_resize(self, event):
        """Update scroll_frame width"""
        new_width = self.master.winfo_width() - 20
        self.scrollable_frame.configure(width=new_width)

    def update_operation_show(self, new_value):
        """Update operation_show in this class"""
        self.operation_show = new_value

    def get_memory_value(self):
        """Update operation_now on display"""
        if self.memory_value:
            self.update_operation_from_memory(list(self.memory_value.values())[-1])
        return "0"

    def calculation(self, sign):
        if self.memory_value:
            try:
                last_key = list(self.memory_value.keys())[-1]
                last_value = self.memory_value[last_key]
                expression = str(last_value) + sign + self.operation_show
                self.memory_value[last_key] = delete_zeros(round_number(sympify(expression.replace(" ", ""))))
            except Exception as e:
                print(f"Memory error: {e}")

    def add_new_element(self, element):
        """add new element to memory_value with unique id"""
        new_id = str(uuid.uuid4())
        self.memory_value[new_id] = str(element)

    def buttons_function(self, i):
        if not self.disable_all:

            self.value_button = self.text_buttons[i]  #txt from on_click

            if self.value_button == "MS":
                if not self.memory_value:
                    self.enable_button()
                    self.disable_buttons_value = False
                self.add_new_element(str(self.operation_show))
                #update operation_now from Display
                self.update_operation_from_memory("0", False)

            elif self.value_button in ["M+", "M-"]:
                if not self.memory_value:
                    if self.value_button == "M-":
                        self.add_new_element(str("-" + self.operation_show))
                    else:
                        self.add_new_element(str(self.operation_show))
                    self.enable_button()
                    self.disable_buttons_value = False
                else:
                    self.calculation(self.value_button[-1])
                #update operation_now from Display
                self.update_operation_from_memory("0", False)

            elif self.value_button == "ML":
                if not self.disable_buttons_value:
                    #delete frame and create new
                    for widget in self.scrollable_frame.winfo_children():
                        widget.destroy()

                    self.animated_panel.animate()
                    self.created_animated_numbers()
                    self.down_frame_function(self.animated_panel.animate)

            elif self.value_button == "MC":
                if not self.disable_buttons_value:
                    self.memory_value = {}
                    self.disable_button()
                    self.disable_buttons_value = True

            elif self.value_button == "MR":
                if not self.disable_buttons_value:
                    self.get_memory_value()

    def create_buttons(self):
        count = 0
        for i in range(6):
            btn = ctk.CTkButton(
                self.master,
                text=self.text_buttons[count],
                fg_color="#282828",
                hover_color="#4d4d4d",
                font=("Segoe UI Variable", 12),
                text_color="white",
                corner_radius=5,
            )

            btn.grid(row=1, column=i,
                     sticky=tk.NSEW, padx=1, pady=1)

            #strech column
            self.master.grid_columnconfigure(i, weight=1)
            self.buttons_list.append(btn)

            count += 1

        if not self.memory_value:
            self.disable_button()

    def disable_button(self, all_buttons = False):
        buttons_disable = []
        if not all_buttons:
            buttons_disable = [0, 1, 5]
        elif all_buttons:
            buttons_disable = [0, 1, 2, 3, 4, 5]
            self.disable_all = True
        for i in range(len(buttons_disable)):
            self.buttons_list[buttons_disable[i]].configure(state="disabled")

    def enable_button(self, all_buttons = False):
        buttons_disable = []
        if not all_buttons:
            buttons_disable = [0, 1, 5]
        elif all_buttons:
            buttons_disable = [0, 1, 2, 3, 4, 5]
            self.disable_all = False
        for i in range(len(buttons_disable)):
            self.buttons_list[buttons_disable[i]].configure(state="normal")

    def down_frame_function(self, animate):
        """Frame with exit and delete all buttons"""
        if self.down_frame is None or not self.down_frame.winfo_exists():
            self.down_frame = ctk.CTkFrame(self.animated_panel, fg_color="#282828")
            self.down_frame.grid(column=0, row=0, sticky="sew", pady=2)

        def delete_memory():
            self.memory_value = {}
            animate()
            self.down_frame.destroy()
            self.enable_button(True)
            self.disable_button()

        def exit_frame():
            animate()
            self.down_frame.destroy()

        btn_exit = ctk.CTkButton(self.down_frame, text="Exit",
                               command=exit_frame,
                               corner_radius=5, fg_color="#282828", width=30)

        btn_delete_memory = ctk.CTkButton(self.down_frame, text="Delete All",
                                 command=delete_memory,
                                 corner_radius=5, fg_color="#282828", width=30)

        btn_exit.pack(side="right", padx=3, pady=3)
        btn_delete_memory.pack(side="left", padx=3, pady=3)

    def operation_for_animated(self, value_button, key, label_frame, main_frame):
        """calculator operation only for animation"""
        value_memory = self.memory_value[key]

        if value_button == "M+" or value_button == "M-":
            expression = str(value_memory) + value_button[-1] + self.operation_show

            self.memory_value[key] = delete_zeros(round_number(sympify(
                expression.replace(" ", ""))))
            #update number in label_frame
            for widget in self.scrollable_frame.winfo_children():
                if hasattr(widget, 'key') and widget.key == key:
                    label_frame.configure(text=self.memory_value[key])

        elif value_button == "MC":

            if key in self.memory_value:
                del self.memory_value[key]
                main_frame.destroy()
                self.enable_button(all_buttons=True)
            #if it is last frame in animation
            if not self.memory_value:
                self.animated_panel.animate_backwards()
                self.down_frame.destroy()
                self.disable_button()
                self.disable_buttons_value = True

    def created_animated_numbers(self):
        for uuid_key, value in self.memory_value.items():

            self.scrollable_frame.configure(width=self.master.winfo_width() - 20)

            #Background each other frame
            main_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            main_frame.pack(side="bottom", anchor="e", expand=True, fill="both")
            main_frame.key = uuid_key #it is the same key which number have in memory


            #There are numbers from memory
            label_frame = ctk.CTkLabel(main_frame, text=value, font=("Segoe UI Variable", 19, "bold"),
                                       anchor="e", width=100)
            label_frame.pack(side="top", fill="x", padx=5, pady=2)
            label_frame.key = uuid_key #it is the same key which number have in memory

            #Hover frames
            main_frame.bind("<Enter>", lambda e, mf=main_frame, lf=label_frame:
                            hover_label("#4d4d4d", mf, lf))
            main_frame.bind("<Leave>", lambda e, mf=main_frame, lf=label_frame:
                            hover_label("#282828", mf, lf))
            label_frame.bind("<Enter>", lambda e, lf=label_frame, mf=main_frame:
                            hover_label("#4d4d4d", lf, mf))
            label_frame.bind("<Leave>", lambda e, lf=label_frame, mf=main_frame:
                            hover_label("#282828", lf, mf))

            #Frame for buttons Exit and Delete All
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(side="top", anchor="e")

            #Buttons for each frame
            btn_mc = ctk.CTkButton(button_frame, text="MC",
                                   command=lambda key=uuid_key, lb = label_frame, mf = main_frame:
                                   self.operation_for_animated("MC", key, lb, mf),
                                   corner_radius=5, fg_color="#282828", width=30)

            btn_plus = ctk.CTkButton(button_frame, text="M+",
                                      command=lambda key = uuid_key, lb = label_frame, mf = main_frame:
                                      self.operation_for_animated("M+", key, lb, mf),
                                      corner_radius=5, fg_color="#282828", width=30)
            btn_minus = ctk.CTkButton(button_frame, text="M-",
                                       command=lambda key=uuid_key, lb = label_frame, mf = main_frame:
                                       self.operation_for_animated("M-", key, lb, mf),
                                       corner_radius=5, fg_color="#282828", width=30)

            btn_minus.pack(side="right", padx=2, pady=2)
            btn_plus.pack(side="right", padx=2, pady=2)
            btn_mc.pack(side="right", padx=2, pady=2)
