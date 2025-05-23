import tkinter as tk
import random

CELL_SIZE = 10
GRID_WIDTH = 160
GRID_HEIGHT = 80
DELAY = 50  # ms


class GameOfLife:
    def __init__(self, master):
        self.master = master

        self.is_running = False
        self.grid = [[0 for i in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

        main_frame = tk.Frame(master)
        main_frame.pack()

        self.screen = tk.Canvas(
            main_frame,
            bg="grey",
            width=CELL_SIZE * GRID_WIDTH,
            height=CELL_SIZE * GRID_HEIGHT,
            highlightthickness=2,
            highlightbackground="black"
        )
        self.screen.pack(side=tk.LEFT)

        self.bottom_panel = tk.Frame(master, bg="grey")
        self.bottom_panel.pack(side=tk.BOTTOM, fill=tk.X)

        self.sidebar = tk.Frame(main_frame, bg="grey")
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        self.start_button = tk.Button(self.bottom_panel, text="Start", command=self.toggle_running, bg="black",
                                      fg="white")
        self.start_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.bottom_panel, text="Reset", command=self.reset_grid, bg="black", fg="white")
        self.reset_button.pack(side=tk.LEFT)

        self.randomize_button = tk.Button(self.bottom_panel, text="Randomize", command=self.randomize_grid, bg="black",
                                          fg="white")
        self.randomize_button.pack(side=tk.LEFT)

        self.add_pattern_buttons()

        self.screen.bind("<Button-1>", self.draw_on_click)
        self.screen.bind("<B1-Motion>", self.draw_while_dragging)
        self.screen.bind("<Button-3>", self.clear_on_clik)
        self.screen.bind("<B3-Motion>", self.clear_while_dragging)

    def add_pattern_buttons(self):
        tk.Label(self.sidebar, text="Examples:", bg="black", fg="white").pack(pady=10)
        tk.Button(self.sidebar, text="Glider", command=self.place_glider, bg="black", fg="white").pack(pady=2)
        tk.Button(self.sidebar, text="LWSS", command=self.place_lwss, bg="black", fg="white").pack(pady=2)
        tk.Button(self.sidebar, text="Pulsar", command=self.place_pulsar, bg="black", fg="white").pack(pady=2)
        tk.Button(self.sidebar, text="xd", command=self.place_xd, bg="black", fg="white").pack(pady=2)

    def draw_on_click(self, click):
        x = click.x // CELL_SIZE
        y = click.y // CELL_SIZE
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.grid[y][x] = 1
            self.draw_grid()

    def draw_while_dragging(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.grid[y][x] = 1
            self.draw_grid()

    def clear_on_clik(self, click):
        x = click.x // CELL_SIZE
        y = click.y // CELL_SIZE
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.grid[y][x] = 0
            self.draw_grid()

    def clear_while_dragging(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            self.grid[y][x] = 0
            self.draw_grid()

    def draw_grid(self):
        self.screen.delete("all")
        margin = 0.5
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    top_left_x = x * CELL_SIZE + margin
                    top_left_y = y * CELL_SIZE + margin
                    bottom_right_x = (x + 1) * CELL_SIZE - margin
                    bottom_right_y = (y + 1) * CELL_SIZE - margin
                    # bottom_right_x = top_left_x + CELL_SIZE
                    # bottom_right_y = top_left_y + CELL_SIZE
                    self.screen.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill="black",
                                                 outline="")

    def toggle_running(self):
        self.is_running = not self.is_running
        self.start_button.config(text="Stop" if self.is_running else "Start")

    def reset_grid(self):
        self.grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.is_running = False
        self.draw_grid()
        self.start_button.config(text="Stop" if self.is_running else "Start")

    def randomize_grid(self):
        self.grid = [[random.choice([1, 0]) for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.is_running = False
        self.start_button.config(text="Stop" if self.is_running else "Start")
        self.draw_grid()

    def next_generation(self):
        new_grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
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
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                    count += self.grid[ny][nx]
        return count

    def update(self):
        if self.is_running:
            self.next_generation()
            self.draw_grid()
        self.master.after(DELAY, self.update)

    def insert_pattern(self, pattern):
        self.reset_grid()
        offset_x = GRID_WIDTH // 2
        offset_y = GRID_HEIGHT // 2
        for dx, dy in pattern:
            x = offset_x + dx
            y = offset_y + dy
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                self.grid[y][x] = 1
        self.is_running = False
        self.start_button.config(text="Stop" if self.is_running else "Start")
        self.draw_grid()

    def place_glider(self):
        pattern = [
            (1, 0), (2, 1), (0, 2), (1, 2), (2, 2)
        ]
        self.insert_pattern(pattern)

    def place_lwss(self):
        pattern = [
            (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (4, 1),
            (4, 2),
            (0, 3), (3, 2)
        ]
        self.insert_pattern(pattern)

    def place_pulsar(self):
        pattern = [
            (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
            (0, 2), (5, 2), (7, 2), (12, 2),
            (0, 3), (5, 3), (7, 3), (12, 3),
            (0, 4), (5, 4), (7, 4), (12, 4),
            (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
            (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
            (0, 8), (5, 8), (7, 8), (12, 8),
            (0, 9), (5, 9), (7, 9), (12, 9),
            (0, 10), (5, 10), (7, 10), (12, 10),
            (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)
        ]
        self.insert_pattern(pattern)


    def place_xd(self):
        pattern = [
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
            (1, 0), (2, 0), (0,6), (0, 7), (-1, 6),
            (-1, 7), (1, 6), (1, 7), (2, 6), (2, 7),
            (3, 6), (3, 7), (4, 6), (4, 7)
        ]
        self.insert_pattern(pattern)

root = tk.Tk()
root.title("Gra w życie - Conway's Game of Life")
game = GameOfLife(root)
game.update()
root.mainloop()
