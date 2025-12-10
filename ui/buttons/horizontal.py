import tkinter as tk
from typing import Callable, List, Optional

from ui import Button, Frame


class HorizontalButtons(Frame):
    buttons: List[Button]

    def __init__(self, master: Optional[tk.Misc], *, width: int = 15, pady: int = 2.5):
        super().__init__(master, width=width)
        self.buttons = []
        self.pady = pady

    def add_button(self, text: str, func: Callable):
        button = Button(
            self,
            text=text,
            command=func,
            width=int(self["width"] * 0.8),
        )
        self.buttons.append(button)

        for row, button in enumerate(self.buttons):
            button.grid(column=0, row=row, pady=self.pady)
