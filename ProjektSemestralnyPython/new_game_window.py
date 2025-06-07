import tkinter.colorchooser as colorchooser
import customtkinter as ctk
from CTkColorPicker import *
from config import *

class NewGameWindow(ctk.CTkToplevel):
    def __init__(self, master, start_game_callback):
        super().__init__(master)
        self.title("Nowa gra")

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        self.callback = start_game_callback

        self.bg_color = "#A0A0A0"  # domyślny kolor tła
        self.draw_color = "#000000"  # domyślny kolor rysowania
        self.configure(fg_color="#2b2b2b")  # kolor okna

        frame = ctk.CTkFrame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        frame.configure(fg_color="#2b2b2b") # kolor buttonFrame

        self.start_button = ctk.CTkButton(frame, text="Start", command=self.start)
        self.start_button.pack(pady=(0, 10))

        self.bg_color_button = ctk.CTkButton(frame, text="Wybierz kolor tła", command=self.choose_bg_color)
        self.bg_color_button.pack(pady=(0, 10))

        self.draw_color_button = ctk.CTkButton(frame, text="Wybierz kolor rysowania", command=self.choose_draw_color)
        self.draw_color_button.pack()
        # self.color_picker = ColorPicker(self, initial_color=self.draw_color, callback=self.set_draw_color)
        # self.color_picker.pack(pady=10)


    # wybor uzywajac CTkColorPicker
    def choose_draw_color(self):
        picker = AskColor(
            width=400,
            title="Wybierz kolor tła",
            initial_color="#2b2b2b",
            fg_color="black",
            bg_color="#2b2b2b",
            button_color="#2b2b2b",
            button_hover_color="#555555"
        )
        color = picker.get()
        if color:
            self.draw_color = color
            self.draw_color_button.configure(fg_color=color)

    def choose_bg_color(self):
        picker = AskColor(
            width=400,
            title="Wybierz kolor rysowania",
            initial_color="#2b2b2b",
            fg_color="black",
            bg_color="#2b2b2b",
            button_color="#2b2b2b",
            button_hover_color="#555555"
        )
        color = picker.get()
        if color:
            self.bg_color = color
            self.bg_color_button.configure(fg_color=color)


    # domyslny wybór kolory
    #==========================================
    # def choose_bg_color(self):
    #     color = colorchooser.askcolor(title="Wybierz kolor tła", initialcolor=self.bg_color)
    #     if color[1] is not None:
    #         self.bg_color = color[1]
    #         self.bg_color_button.configure(text=f"Kolor tła", fg_color=self.bg_color)

    # def choose_draw_color(self):
    #     color = colorchooser.askcolor(title="Wybierz kolor rysowania")
    #     if color[1] is not None:
    #         self.draw_color = color[1]
    #         self.draw_color_button.configure(text=f"Kolor rysowania", fg_color=self.draw_color)

    # def set_draw_color(self, new_color):
    #     self.draw_color = new_color
    #     print(f"New draw color: {self.draw_color}")
    #===========================================

    def start(self):
        try:
            print(f"[NewGameWindow] Selected draw_color: {self.draw_color}")
            self.destroy()
            self.callback(DEFAULT_GRID_WIDTH, DEFAULT_GRID_HEIGHT, self.bg_color, self.draw_color)
        except ValueError:
            print("Niepoprawne dane.")
