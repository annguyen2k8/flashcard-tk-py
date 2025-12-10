from __future__ import annotations

import tkinter as tk
from typing import Dict, Optional, Type, overload

from ui import Frame
from utils import ignore_keyerror


class FrameManager:
    class Frame(Frame):
        __manager: FrameManager
        
        def __init__(self, manager: FrameManager, *arg, **kwargs):
            super().__init__(manager.master, *arg, **kwargs)
            
            self.__manager = manager

        @property
        def manager(self) -> FrameManager:
            return self.__manager
    
    master: Optional[tk.Misc]
    frames: Dict[str, _Frame] = {}
    
    def __init__(self, master: Optional[tk.Misc]):
        self.master = master
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
    
    def add(self, frame_cls: Type[_Frame]):
        frame = frame_cls(self)
        
        frame.grid(
            row=0, column=0,
            sticky="nsew"
        )
        
        self.frames[frame_cls.__name__] = frame
    
    def remove(self, frame_cls: _Frame):
        self.frames.pop(frame_cls.__name__).destroy()
    
    def show(self, frame_cls: _Frame):
        self.frames[frame_cls.__name__].tkraise()