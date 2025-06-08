import customtkinter as ctk
from patterns import *


def speed_slider(parent, initial_value, function):
    slider = ctk.CTkSlider(parent, from_=1000, to=1, number_of_steps=40, command=function)
    slider.set(initial_value)
    slider.pack(side=ctk.LEFT, padx=10)

    label = ctk.CTkLabel(parent, text="Speed")
    label.pack(side=ctk.LEFT)

    return slider


class Accordion(ctk.CTkFrame):
    def __init__(self, parent, categories, insert_pattern_func):
        super().__init__(parent, fg_color="#333")

        self.insert_pattern_func = insert_pattern_func
        self.category_frames = {}
        self.expanded_category = None

        for cat_name, patterns in categories.items():
            self.add_category(cat_name, patterns)

    def add_category(self, cat_name, patterns):
        category_container = ctk.CTkFrame(self)
        category_container.pack(fill=ctk.X, pady=(10, 5))

        header = ctk.CTkButton(category_container, text=cat_name, command=lambda c=cat_name: self.pick_category(c))
        header.pack(fill=ctk.X)

        frame = ctk.CTkFrame(category_container, fg_color="#333", corner_radius=8)
        frame.pack(fill=ctk.X, padx=10, pady=(5, 10))
        frame.pack_forget()

        for title, pattern in patterns:
            panel = ctk.CTkFrame(frame)
            panel.pack(padx=10, pady=2, fill=ctk.X)

            ctk.CTkLabel(panel, text=title, font=("Arial", 12, "bold")).pack(anchor="w")
            ctk.CTkButton(panel, text="Add", command=lambda p=pattern: self.insert_pattern_func(p)).pack(anchor="e",
                                                                                                           pady=2)

        self.category_frames[cat_name] = frame

    def pick_category(self, cat_name):
        if self.expanded_category == cat_name:
            self.category_frames[cat_name].pack_forget()
            self.expanded_category = None
        else:
            if self.expanded_category:
                self.category_frames[self.expanded_category].pack_forget()
            self.category_frames[cat_name].pack(fill=ctk.X)
            self.expanded_category = cat_name


def sidebar(parent, insert_pattern_func):
    sidebar = ctk.CTkFrame(parent, width=500)
    sidebar.pack(side=ctk.RIGHT, fill=ctk.Y)

    label = ctk.CTkLabel(sidebar, text="Examples:", font=("Arial", 14))
    label.pack(pady=10)

    categories = {
        "Stateczniki": [
            ("Glider", glider_pattern),
            ("LWSS", lwss_pattern)
        ],
        "Oscylatory": [
            ("Pulsar", pulsar_pattern),
        ],
        "Breedery": [
            ("gosper glider gun pattern", gosper_glider_gun_pattern)
        ],
        "Eksperymentalne": [
            ("XD", xd_pattern)
        ]
    }

    accordion = Accordion(sidebar, categories, insert_pattern_func)
    accordion.pack(fill=ctk.X, pady=5, padx=5)

    return sidebar
