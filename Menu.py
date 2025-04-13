import customtkinter as ctk
from PIL import Image

class Menu:
    def __init__(self, master):
        self.master = master
        self.history_operation()

    def history_operation(self):
        #image_history = ctk.CTkImage("png\\history.png")

        image_history = ctk.CTkImage(light_image=Image.open('png/history.png'))

        btn_history = ctk.CTkButton(self.master, image=image_history, text="",
                             #command=exit_frame,
                             corner_radius=5, fg_color="#282828",
                             hover_color="#4d4d4d", width=30)

        btn_history.pack(side="right", padx=3, pady=3)


