from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from app import App

class Frame(ttk.Frame):
    def __init__(
        self, master: Optional[Union[tk.Misc, App]] = None, *,
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
        
        self.container = master
    
    def on_show(self): pass