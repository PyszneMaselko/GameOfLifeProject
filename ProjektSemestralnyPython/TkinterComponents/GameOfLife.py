import tkinter as tk
import random

CELL_SIZE = 10
GRID_WIDTH = 160
GRID_HEIGHT = 80
DELAY = 100  # ms

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.running = False
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        self.canvas = tk.Canvas(master, width=CELL_SIZE*GRID_WIDTH, height=CELL_SIZE*GRID_HEIGHT, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.start_button = tk.Button(master, text="Start", command=self.toggle_running)
        self.start_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT)

        self.random_button = tk.Button(master, text="Losowo", command=self.randomize_grid)
        self.random_button.pack(side=tk.LEFT)

        self.draw_grid()
        self.update()

    def toggle_cell(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        self.grid[y][x] = 1 - self.grid[y][x]
        self.draw_grid()

    def toggle_running(self):
        self.running = not self.running
        self.start_button.config(text="Stop" if self.running else "Start")

    def reset_grid(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.draw_grid()

    def randomize_grid(self):
        self.grid = [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    x1 = x * CELL_SIZE
                    y1 = y * CELL_SIZE
                    x2 = x1 + CELL_SIZE
                    y2 = y1 + CELL_SIZE
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

    def next_generation(self):
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                alive = self.grid[y][x]
                neighbors = self.count_neighbors(x, y)
                if alive:
                    new_grid[y][x] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[y][x] = 1 if neighbors == 3 else 0
        self.grid = new_grid

    def count_neighbors(self, x, y):
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
        if self.running:
            self.next_generation()
            self.draw_grid()
        self.master.after(DELAY, self.update)