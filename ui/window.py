import sys
import threading
import tkinter as tk

import darkdetect
import sv_ttk

from ui.wwm import WWm

if sys.platform == "win32":
    import pywinstyles

class Window(tk.Tk, WWm):
    def __init__(self) -> None:
        super().__init__()
        
        self.set_icon("assets/icon")

    def set_theme(self, theme: str):
        theme = theme.lower()
        sv_ttk.set_theme(theme, self)

        if sys.platform == "win32":
            version = sys.getwindowsversion()
            if version.major == 10 and version.build >= 22000:
                pywinstyles.change_header_color(
                    self, "#1c1c1c" if theme == "dark" else "#fafafa"
                )
            elif version.major == 10:
                pywinstyles.apply_style(self, "dark" if theme == "dark" else "normal")

                self.wm_attributes("-alpha", 0.99)
                self.wm_attributes("-alpha", 1)

        self.update()

    def get_theme(self) -> str:
        return sv_ttk.get_theme()

    def mainloop(self, n: int = 0) -> None:
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except ImportError:
            pass
        finally:
            self.set_theme(darkdetect.theme())  # type: ignore

            threading.Thread(
                target=darkdetect.listener, args=(self.set_theme,), daemon=True
            ).start()
            
            super().mainloop(n)


if __name__ == "__main__":
    window = Window()

    window.title = "Hello world!"
    window.size = (300, 100)
    window.position = (
        int((window.display_w - window.width) / 2),
        int((window.display_h - window.height) / 2),
    )

    window.set_theme("dark")

    window.mainloop()
