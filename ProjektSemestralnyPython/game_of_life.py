from config import *
from components import *
from patterns import *
import random
import customtkinter as ctk
import tkinter as tk


class GameOfLife:
    def __init__(self, parent, grid_width, grid_height, bg_color, draw_color):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.bg_color = bg_color
        self.draw_color = draw_color
        self.master = parent
        self._after_id = None
        self.is_running = False
        self.delay = DEFAULT_DELAY
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill=ctk.BOTH, expand=True)

        self.screen = tk.Canvas(
            main_frame,
            bg=bg_color,
            width=CELL_SIZE * self.grid_width,
            height=CELL_SIZE * self.grid_height,
            highlightthickness=2,
            highlightbackground="black"
        )

        self.screen.pack(side=ctk.LEFT)

        self.bottom_panel = ctk.CTkFrame(parent)
        self.bottom_panel.pack(side=ctk.BOTTOM, fill=ctk.X)

        self.sidebar = sidebar(main_frame, self.insert_pattern)

        self.start_button = ctk.CTkButton(self.bottom_panel, text="Start", command=self.toggle_running)
        self.start_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.reset_button = ctk.CTkButton(self.bottom_panel, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.randomize_button = ctk.CTkButton(self.bottom_panel, text="Randomize", command=self.randomize_grid)
        self.randomize_button.pack(side=ctk.LEFT, padx=5, pady=5)

        self.speed_slider = speed_slider(self.bottom_panel, self.delay, self.change_speed)

        self.screen.bind("<Button-1>", self.draw_on_click)
        self.screen.bind("<B1-Motion>", self.draw_while_dragging)
        self.screen.bind("<Button-3>", self.clear_on_click)
        self.screen.bind("<B3-Motion>", self.clear_while_dragging)

    def add_pattern_buttons(self):
        label = ctk.CTkLabel(self.sidebar, text="Examples:", font=("Arial", 14))
        label.pack(pady=10)

        ctk.CTkButton(self.sidebar, text="Glider", command=place_glider).pack(pady=2)
        ctk.CTkButton(self.sidebar, text="LWSS", command=place_lwss).pack(pady=2)
        ctk.CTkButton(self.sidebar, text="Pulsar", command=place_pulsar).pack(pady=2)
        ctk.CTkButton(self.sidebar, text="xd", command=place_xd).pack(pady=2)
        ctk.CTkButton(self.sidebar, text="Gosper glider gun", command=place_gosper_glider_gun_pattern).pack(pady=2)

    def draw_on_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.grid[y][x] = 1
            self.draw_grid()

    def draw_while_dragging(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.grid[y][x] = 1
            self.draw_grid()

    def clear_on_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.grid[y][x] = 0
            self.draw_grid()

    def clear_while_dragging(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
            self.grid[y][x] = 0
            self.draw_grid()

    def draw_grid(self):
        self.screen.delete("all")
        margin = 0.5
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] == 1:
                    self.screen.create_rectangle(
                        x * CELL_SIZE + margin,
                        y * CELL_SIZE + margin,
                        (x + 1) * CELL_SIZE - margin,
                        (y + 1) * CELL_SIZE - margin,
                        fill=self.draw_color,
                        outline=""
                    )

    def toggle_running(self):
        self.is_running = not self.is_running
        self.start_button.configure(text="Stop" if self.is_running else "Start")

    def reset_grid(self):
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.is_running = False
        self.start_button.configure(text="Start")
        self.draw_grid()

    def randomize_grid(self):
        self.grid = [[random.choice([0, 1]) for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.is_running = False
        self.start_button.configure(text="Start")
        self.draw_grid()

    def change_speed(self, value):
        self.delay = int(float(value))

    def next_generation(self):
        new_grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                alive = self.grid[y][x]
                neighbours = self.count_neighbours(x, y)
                if alive:
                    new_grid[y][x] = 1 if neighbours in [2, 3] else 0
                else:
                    new_grid[y][x] = 1 if neighbours == 3 else 0
        self.grid = new_grid

    def count_neighbours(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    count += self.grid[ny][nx]
        return count

    def update(self):
        if self.is_running:
            self.next_generation()
            self.draw_grid()
        self._after_id = self.master.after(self.delay, self.update)

    def insert_pattern(self, pattern):
        self.reset_grid()
        offset_x = self.grid_width // 2
        offset_y = self.grid_height // 2
        for dx, dy in pattern:
            x = offset_x + dx
            y = offset_y + dy
            if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                self.grid[y][x] = 1
        self.draw_grid()
