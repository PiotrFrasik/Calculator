import customtkinter as ctk

import MemoryButtons


class AnimatedDownPanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos, disable_button, enable_button):
        super().__init__(master = parent)

        self.disable_button = disable_button
        self.enable_button = enable_button

        #general attributes
        self.start_pos = start_pos + 1
        self.end_pos = end_pos
        self.height = abs(start_pos - end_pos)

        #animation logic
        self.pos = self.start_pos
        self.in_start_pos = True

        #layout
        self.place(relx = 0, rely = self.start_pos, relwidth = 1, relheight = self.height)

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
            self.disable_button(all_buttons = True)
        else:
            self.animate_backwards()
            self.enable_button(all_buttons = True)

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.05
            self.place(relx = 0, rely = self.pos, relwidth = 1, relheight = self.height)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.05
            self.place(relx = 0, rely = self.pos, relwidth = 1, relheight = self.height)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True

