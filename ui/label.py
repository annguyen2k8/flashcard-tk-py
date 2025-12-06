from typing import Optional

import tkinter as tk
from tkinter import ttk


class Label(ttk.Label):
    def __init__(
        self, master: Optional[tk.Misc] = None, *,
        text: str
    ) -> None:
        super().__init__(
            master,
            text=text
        )