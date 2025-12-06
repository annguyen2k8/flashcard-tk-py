import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

from app import App
from ui import Button, Entry, Frame, Label, LabelFrame


@App.register_frame
class QuizFrame(Frame):
    def __init__(self, master: App):
        super().__init__(master)
        
        Button(
            self, text="Quit", 
            command=self.__on_quit
        ).pack(
            padx=10, pady=10, anchor=tk.NW
        )
        
        self.lf = LabelFrame(
            self, text="Question 0", height=100
        )
        
        self.lf.columnconfigure(0, weight=1)
        
        self.label = Label(
            self.lf, text="Are you dumbass?"
        )
        
        self.label.grid(
            column=0, row=0,
            padx=10, pady=10,
            sticky=tk.EW
        )
        
        self.entry = Entry(
            self.lf, 
        )
        
        self.entry.grid(
            column=0, row=1,
            padx=10, pady=10,
            sticky=tk.EW
        )
        
        self.lf.pack(
            padx=10, pady=10, fill=tk.X, expand=True, anchor=tk.CENTER
        )
    
    def on_show(self):
        self.entry.focus()
    
    def __on_quit(self) -> None:
        from .menu import MenuFrame
        
        if askyesno(message="Are you sure to quit?"):
            self.container.show(MenuFrame)