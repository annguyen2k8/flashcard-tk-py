import tkinter as tk
from tkinter import ttk
from typing import Literal, Optional, Tuple

from ui.widgets import Frame, TreeView


class ScrolledTreeView(Frame):
    def __init__(
        self, master: Optional[tk.Misc] = None, *,
        columns: Tuple[str, ...] = ("", ),
        height: int = 10,
        show: Literal["tree", "headings", "tree headings", ""] = "",
        **kwargs
    ) -> None:
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        
        self.treeview = TreeView(
            self,
            columns=columns, 
            height=height,
            show=show,
            **kwargs
        )
        
        self.scrollbar = ttk.Scrollbar(
            self,
            command=self.treeview.yview, 
            orient=tk.VERTICAL
            )
        
        self.treeview.configure(
            yscrollcommand=self.scrollbar.set
        )
        
        self.treeview.grid(
            row=0, column=0, sticky=tk.NSEW
        )
        
        self.scrollbar.grid(
            row=0, column=1, sticky=tk.NS
        )
        