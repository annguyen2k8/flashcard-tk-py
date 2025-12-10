from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno, showinfo
from typing import Callable, Dict, List, Optional, Tuple

from managers import FrameManager
from ui import Button, Entry, Frame, Label, LabelFrame


class QuizFrame(FrameManager.Frame):
    __questions: List[Tuple[str, ...]]
    __index: int
    __results: Dict[int, Optional[str]]
    
    def __init__(self, manager: FrameManager, *args, **kwargs):
        super().__init__(manager, *args, **kwargs)
        
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
    
    @property
    def mistakes(self) -> Dict[int, bool]:
        return self.filter_results(self.__is_wrong)
    
    def __is_wrong(self, index: int, answer: str) -> bool:
        return not self.questions[index][1].lower() == answer.lower()
    
    @property
    def total_mistakes(self) -> int:
        return len(self.mistakes)
    
    def filter_results(self, func: Callable[[int, bool], bool]) -> Dict[int, bool]:
        results = {}
        for index, answer in self.results.items():
            if func(index, answer):
                results[index] = self.results[index]
        return results
    
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
    
    def __on_return(self, event: tk.Event):
        answer = self.entry.get()
        
        if not answer.replace(" ", ""):
            return
        
        self.results[self.index] = answer
        
        if not self.remaining:
            return self.__on_result(event)

        self.__next_question(event)
    
    def __next_question(self, event: tk.Event):
        self.__index += 1
        self.__update()
        self.entry.clear()
    
    def __on_result(self, event: tk.Event):
        ...
        
    def __on_quit(self):
        from frames.menu import MenuFrame
        
        if askyesno(message="Are you sure to quit?"):
            self.manager.show(MenuFrame)