from __future__ import annotations

import tkinter as tk
from enum import Enum, auto
from typing import Dict, List, Optional, Type, overload

from ui.widgets import Frame
from utils import ignore_keyerror


class FrameType(Enum):
    MENU = auto()
    VIEW = auto()

class FrameManager:
    class Frame(Frame):
        __manager: FrameManager        
        def __init__(self, manager: FrameManager, frame_type: FrameType, *arg, **kwargs):
            super().__init__(manager.master, *arg, **kwargs)
            self.__manager = manager
            self.__frame_type = frame_type

        @property
        def manager(self) -> FrameManager:
            return self.__manager
    
        @property
        def frame_type(self) -> auto:
            return self.__frame_type
    
    master: Optional[tk.Misc]
    frames: Dict[FrameType, _Frame] = {}
    
    def __init__(self, master: Optional[tk.Misc]):
        self.master = master
        
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        self.load_frames()
        
    def load_frames(self):
        import frames
        for obj_name in frames.__all__:
            obj = eval(f"frames.{obj_name}")
            if isinstance(obj, Type):
                self.add(obj)
    
    def add(self, frame_cls: Type[Frame]):
        frame = frame_cls(self)
        
        frame.grid(
            row=0, column=0,
            sticky="nsew"
        )
        
        self.frames[frame.frame_type] = frame
    
    @ignore_keyerror
    def remove(self, frame_type: FrameType):
        self.frames.pop(frame_type).destroy()
    
    @ignore_keyerror
    def show(self, frame_type: FrameType):
        self.frames[frame_type].tkraise()