import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno

from app import App
from ui import Button, Entry, Frame, Label, LabelFrame
from typing import List, Tuple, Dict


@App.register_frame
class QuizFrame(Frame):
    __questions: List[Tuple[str, ...]]
    __index: int
    __results: Dict[int, bool]
    
    
    def __init__(self, master: App):
        super().__init__(master)
        
        Button(
            self, text="Quit", 
            command=self.__on_quit
        ).pack(
            padx=10, pady=10, anchor=tk.NW
        )
        
        self.lf = LabelFrame(self, height=100)
        
        self.lf.columnconfigure(0, weight=1)
        
        self.label = Label(self.lf, text=" ")
        
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
    
    @property
    def questions(self) -> List[Tuple[str, ...]]:
        return self.__questions
    
    @property
    def index(self) -> int:
        return self.__index
    
    @property
    def results(self) -> Dict[int, bool]:
        return self.__results
    
    @property
    def answered(self) -> int:
       return sum(status is not None for status in self.results.values())
    
    @property
    def remaining(self) -> int:
        return self.answered - self.answered
    
    
    def start(self, items: List[Tuple[str, ...]]):
        self.__questions = items
        self.__index = 0
        self.__results = {}
        
        for i in range(len(items)):
            self.results[i] = None
        
        self.__update()
    
    def __update(self):
        self.lf.text = f"Question {self.index + 1}"
        self.label.text = self.questions[self.index][0]
    
    def __next_question(self):
        ...
    
    def __on_return(self):
        if not self.entry.get().replace(" ", ""):
            return
        
        ...

    def __on_quit(self) -> None:
        from .menu import MenuFrame
        
        if askyesno(message="Are you sure to quit?"):
            self.container.show(MenuFrame)