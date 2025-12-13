from __future__ import annotations

import functools
import tkinter as tk
from typing import Dict, List, Type

from managers import FrameManager, FrameType
from ui.window import Window
from utils import report_callback_exception


class App(Window):
    def __init__(self, args: List[str]):
        super().__init__()
        self.report_callback_exception = report_callback_exception
        self.title = "Flashcard - JALT"
        self.resizable = False

        self.frame_manager = FrameManager(self)
        
        self.frame_manager.show(FrameType.MENU)
        
    def mainloop(self, n: int = 0):
        return super().mainloop(n)