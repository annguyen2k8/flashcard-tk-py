from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from ui.widgets import Frame


class ScrolledText(Frame):
    def __init__(
        self, master: Optional[tk.Misc] = None, *,
        wrap: Literal["none", "char", "word"] = "none",
        **kwargs
    ) -> None:
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.text = tk.Text(self, wrap=wrap)
        
        self.scrollbar = ttk.Scrollbar(
            self,
            command=self.text.yview, 
            orient=tk.VERTICAL
            )
        
        self.text.configure(
            yscrollcommand=self.scrollbar.set
        )
        
        self.text.grid(
            row=0, column=0, sticky=tk.NSEW
        )
        
        self.scrollbar.grid(
            row=0, column=1, sticky=tk.NS
        )
        