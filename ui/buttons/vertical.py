import tkinter as tk
from typing import Callable, List, Optional

from ui import Button, Frame


class VerticalButtons(Frame):
    buttons: List[Button]

    def __init__(self, master: Optional[tk.Misc], *, width: int = 15, padx: int = 2.5):
        super().__init__(master, width=width)
        self.buttons = []
        self.padx = padx
    
    def add_button(self, text: str, func: Callable):
        button = Button(
            self,
            text=text,
            command=func,
            width=int(self["width"] * 0.8),
        )
        self.buttons.append(button)

        for column, button in enumerate(self.buttons):
            button.grid(column=column, row=0, padx=self.padx)
