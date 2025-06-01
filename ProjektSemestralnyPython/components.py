import customtkinter as ctk


def create_speed_slider(parent, initial_value, callback):
    slider = ctk.CTkSlider(parent, from_=1000, to=10, number_of_steps=40, command=callback)
    slider.set(initial_value)
    slider.pack(side=ctk.LEFT, padx=10)

    label = ctk.CTkLabel(parent, text="Speed")
    label.pack(side=ctk.LEFT)

    return slider
