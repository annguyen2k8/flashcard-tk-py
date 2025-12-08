import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo

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
        
        self.entry.bind("<Return>", self.__on_return)
    
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
    def total(self) -> int:
        return len(self.results.keys())
    
    @property
    def answered(self) -> int:
        count = 0
        for val in self.results.values():
            if val is None:
               continue
            count += 1
        return count
    
    @property
    def remaining(self) -> int:
        return self.total - self.answered
    
    @property
    def question(self) -> str:
        return self.questions[self.index][0]
    
    @property
    def answer(self) -> str:
        return self.questions[self.index][1]
    
    def start(self, items: List[Tuple[str, ...]]):
        self.__questions = items
        self.__index = 0
        self.__results = {}
        
        for i in range(len(items)):
            self.results[i] = None
        
        self.__update()
    
    def __update(self):
        self.lf.text = f"Question {self.index + 1}"
        self.label.text = self.question
    
    def __next_question(self):
        self.__index += 1
        self.__update()
        self.entry.clear()
    
    def __on_return(self, event: tk.Event):
        answer = self.entry.get()
        
        if not answer.replace(" ", ""):
            return
        
        
        result = answer.lower() == self.answer.lower()
        
        self.results[self.index] = result
        
        print(self.results, self.answered, self.remaining)
        
        if self.remaining != 0:
            return self.__next_question()
        
        showinfo(message="Done!")
        
        
    def __on_quit(self) -> None:
        from .menu import MenuFrame
        
        if askyesno(message="Are you sure to quit?"):
            self.container.show(MenuFrame)