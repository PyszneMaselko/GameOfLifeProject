import tkinter as tk
import random

CELL_SIZE = 10
GRID_WIDTH = 160
GRID_HEIGHT = 80
DELAY = 100 # ms

class GameOfLife:
    def __init__(self, master):
        self.master = master
        self.is_running = False
        self.grid = [[0 for i in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

        self.screen = tk.Canvas(master, bg="white", width=CELL_SIZE*GRID_WIDTH, height=CELL_SIZE*GRID_HEIGHT)
        self.screen.pack()

        self.screen.bind("<Button>", self.toggle_cell)

        self.start_button = tk.Button(master, text="Start", command=self.toggle_running)
        self.start_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT)


    def toggle_cell(self, click):
        x = click.x // CELL_SIZE
        y = click.y // CELL_SIZE
        self.grid[y][x] = 1 - self.grid[y][x]
        self.draw_grid()

    def draw_grid(self):
        self.screen.delete("all")
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 1:
                    top_left_x = x * CELL_SIZE
                    top_left_y = y * CELL_SIZE
                    bottom_right_x = top_left_x + CELL_SIZE
                    bottom_right_y = top_left_y + CELL_SIZE
                    self.screen.create_rectangle(top_left_x, top_left_y, bottom_right_x, bottom_right_y, fill="black")

    def toggle_running(self):
        self.running = not self.running
        self.start_button.config(text="Stop" if self.running else "Start")

    def reset_grid(self):
        self.grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
        self.running = False
        self.draw_grid()




root = tk.Tk()
root.title("Gra w życie - Conway's Game of Life")
game = GameOfLife(root)
root.mainloop()