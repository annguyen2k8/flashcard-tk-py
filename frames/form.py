import tkinter as tk
from tkinter import ttk

from ui import Frame
from app import App


@App.register_frame
class FormFrame(Frame):
    def __init__(self, app: App):
        super().__init__(app)
        
        from .menu import MenuFrame
        
        ttk.Button(
            self, text="Coming soon;)", 
            command=lambda: app.show(MenuFrame)).pack(
                padx=10, pady=10, anchor=tk.NW
            )