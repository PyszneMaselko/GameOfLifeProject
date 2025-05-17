import tkinter as tk
from TkinterComponents import GameOfLife

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gra w życie - Conway's Game of Life")
    game = GameOfLife(root)
    root.mainloop()
