import tkinter as tk

from managers import FrameManager, FrameType
from ui.widgets import Button


class LicenseFrame(FrameManager.Frame):
    def __init__(self, manager: FrameManager, *args, **kwargs):
        super().__init__(manager, FrameType.LICENSE,*args, **kwargs)
        Button(
            self, text="Quit", 
            command=self.__on_quit
        ).pack(
            padx=10, pady=10, anchor=tk.NW
        )
        
    def __on_quit(self):
        self.manager.show(FrameType.MENU)