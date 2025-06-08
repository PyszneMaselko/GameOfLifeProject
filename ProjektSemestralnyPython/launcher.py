import customtkinter as ctk
from game_of_life import GameOfLife
from new_game_window import NewGameWindow
from config import *


def run_app():
    root = ctk.CTk()
    root.withdraw()  # ukrywa główne okno na początku
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT - 75}+{x}+{y}")

    def start_game(width, height, bg_color, draw_color):
        root.deiconify()  # pokazuje główne okno
        game = GameOfLife(root, grid_width=width, grid_height=height, bg_color=bg_color, draw_color=draw_color)
        game.update()
        #root.protocol("WM_DELETE_WINDOW", game.on_close)

    NewGameWindow(root, start_game)

    root.mainloop()
