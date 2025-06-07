import customtkinter as ctk
import colorsys

class ColorPicker(ctk.CTkFrame):
    def __init__(self, parent, initial_color="#FF0000", callback=None):
        super().__init__(parent)
        self.callback = callback  # funkcja do wywołania przy zmianie koloru

        self.hue_slider = ctk.CTkSlider(self, from_=0, to=360, command=self.on_hue_change)
        self.hue_slider.pack(fill="x", padx=10, pady=10)

        self.color_preview = ctk.CTkLabel(self, text=" ", width=100, height=40, corner_radius=8)
        self.color_preview.pack(pady=10)

        # ustaw początkowy kolor
        self.hue_slider.set(0)
        self.current_color = initial_color
        self.update_preview_color(initial_color)

    def on_hue_change(self, value):
        # value jest float, od 0 do 360
        h = float(value) / 360
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        r, g, b = int(r*255), int(g*255), int(b*255)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.current_color = hex_color
        self.update_preview_color(hex_color)
        if self.callback:
            self.callback(hex_color)

    def update_preview_color(self, color):
        self.color_preview.configure(bg_color=color)