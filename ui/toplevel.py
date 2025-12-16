import tkinter as tk
from typing import Any, Dict, Optional

from ui.wwm import WWm


class TopLevel(tk.BaseWidget, WWm):
    def __init__(
        self, master: Optional[tk.Misc] = None, *,
        title: Optional[str] = None,
        cnf: Dict[str, Any] = {}, 
        **kw
        ):
        if kw:
            cnf = tk._cnfmerge((cnf, kw))
        extra = ()
        for wmkey in ["screen", "class_", "class", "visual", "colormap"]:
            if wmkey in cnf:
                print(wmkey)
                val = cnf[wmkey]
                if wmkey[-1] == "_": 
                    opt = "-" + wmkey[:-1]
                else: 
                    opt = "-" + wmkey
                extra = extra + (opt, val)
                del cnf[wmkey]
        
        super().__init__(master, "toplevel", cnf, {}, extra)
        
        root: Window = self._root()
        
        self.iconname(root.iconname)
        self.title = title or root.title
        self.resizable = False
        
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        self.transient(master)
        self.grab_set()
        self.focus_force()