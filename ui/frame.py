import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Union


class Frame(ttk.Frame):
    def __init__(
        self, master: Optional[tk.Misc] = None, *,
        height: float = 0,
        padding: Union[float, Tuple[float, float], Tuple[float, float, float, float]] = 0,
        width: float = 0,
        **kwargs
        ) -> None:
        super().__init__(
            master,
            height=height,
            padding=padding,
            width=width,
            **kwargs
        )