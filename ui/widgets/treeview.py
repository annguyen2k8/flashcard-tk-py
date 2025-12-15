import tkinter as tk
from tkinter import ttk
from typing import Literal, Optional, Tuple


class TreeView(ttk.Treeview):
    def __init__(
        self, master: Optional[tk.Misc] = None, *,
        columns: Tuple[str, ...] = ("", ),
        height: int = 10,
        show: Literal["tree", "headings", "tree headings", ""] = "",
        **kwargs
    ) -> None:
        super().__init__(
            master,
            columns=columns, 
            height=height,
            show=show,
            **kwargs
        )
        
        for column in columns:
            self.heading(column, text=column.title())