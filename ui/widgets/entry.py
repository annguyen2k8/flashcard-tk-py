import tkinter as tk
from tkinter import ttk


class Entry(ttk.Entry):    
    def clear(self) -> None:
        self.delete(0, tk.END)
    
    def set(self, string: str):
        self.clear()
        self.insert(0, string)