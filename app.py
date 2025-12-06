from __future__ import annotations

import tkinter as tk
from typing import List, Type, Dict

from core.window import Window
from ui import Frame
from utils import report_callback_exception

import functools

class App(Window):
    frames: Dict[str, Frame] = {}
    
    def __init__(self, args: List[str]):
        super().__init__()
        self.report_callback_exception = report_callback_exception

        self.title = "Flashcard - JALT"
        
        self.resizable = False
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        import frames # Don't delete this line!
        
        for frame in self.__frames:
            _frame = frame(self)
            _frame.grid(
                row=0, column=0,
                sticky="nsew"
                )
            
            self.frames[frame.__name__] = _frame
        
        
        # Menu should show first
        self.show(frames.MenuFrame)

    def mainloop(self, n: int = 0):
        return super().mainloop(n)
    
    __frames: List[Type[Frame]] = []
    @classmethod
    def register_frame(cls, method: Type[Frame]) -> Type[Frame]:
        cls.__frames.append(method)
        
        return method
        
    
    def show(self, frame_cls: str) -> Frame:
        try:
            frame = self.frames[frame_cls.__name__]
            
            frame.tkraise()
            frame.on_show()
            
            return frame
        except KeyError:
            pass