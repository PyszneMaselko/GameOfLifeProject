import customtkinter as ctk
from CTkColorPicker import *
from config import *


class NewGameWindow(ctk.CTkToplevel):
    def __init__(self, master, start_game_callback):
        super().__init__(master)
        self.title("Game of Life")

        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        self.callback = start_game_callback

        self.bg_color = DEFAULT_BG_COLOR  # domyślny kolor tła
        self.draw_color = DEFAULT_DRAW_COLOR  # domyślny kolor rysowania
        self.configure(fg_color=DEFAULT_FRAME_COLOR)  # kolor okna

        button_frame = ctk.CTkFrame(self)
        button_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_frame.configure(fg_color=DEFAULT_FRAME_COLOR)  # kolor button_frame

        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start)
        self.start_button.pack(pady=(0, 10))

        self.bg_color_button = ctk.CTkButton(button_frame, text="Background color", fg_color="#A0A0A0",
                                             command=self.choose_bg_color)
        self.bg_color_button.pack(pady=(0, 10))

        self.draw_color_button = ctk.CTkButton(button_frame, text="Draw color", fg_color="#000000",
                                               command=self.choose_draw_color)
        self.draw_color_button.pack()

    # wybor uzywajac CTkColorPicker
    def choose_draw_color(self):
        picker = AskColor(
            width=400,
            title="Color Picker",
            initial_color=DEFAULT_FRAME_COLOR,
            fg_color="black",
            bg_color=DEFAULT_FRAME_COLOR,
            button_color=DEFAULT_FRAME_COLOR,
            button_hover_color="#555555"
        )
        color = picker.get()
        if color:
            self.draw_color = color
            self.draw_color_button.configure(fg_color=color)

    def choose_bg_color(self):
        picker = AskColor(
            width=400,
            title="Color Picker",
            initial_color=DEFAULT_FRAME_COLOR,
            fg_color="black",
            bg_color=DEFAULT_FRAME_COLOR,
            button_color=DEFAULT_FRAME_COLOR,
            button_hover_color="#555555"
        )
        color = picker.get()
        if color:
            self.bg_color = color
            self.bg_color_button.configure(fg_color=color)

    # domyslny wybór koloru
    # ==========================================
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
    # ===========================================

    def start(self):
        try:
            self.destroy()
            self.callback(DEFAULT_GRID_WIDTH, DEFAULT_GRID_HEIGHT, self.bg_color, self.draw_color)
        except ValueError:
            print("Niepoprawne dane.")
