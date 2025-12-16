import sys
import tkinter
import tkinter as tk
from typing import Callable, Literal, Optional, Tuple, overload

from PIL import Image, ImageTk


class WWm(tk.Wm):
    @property
    def title(self) -> str:
        return self.wm_title()

    @title.setter
    def title(self, title: str):
        self.wm_title(title)

    @property
    def resizable(self) -> Tuple[bool, bool]:
        return self.wm_resizable()

    @resizable.setter
    def resizable(self, value: Tuple[bool, bool] | bool):
        if isinstance(value, bool):
            self.wm_resizable(value, value)
        else:
            self.wm_resizable(value[0], value[1])

    def set_icon(self, name: str):
        try:
            if sys.platform == "win32":
                self.wm_iconbitmap(name + ".ico")
            else:
                image = Image.open(name  + ".png")
                photo = ImageTk.PhotoImage(image)
                self.wm_iconphoto(True, photo)
        except FileNotFoundError:
            print("Icon file not found. Using default icon.")

    @property
    def geometry(self) -> Tuple[int, int, int, int]:
        parts = self.winfo_geometry().replace("+", "x").split("x")
        w, h, x, y = map(int, parts)
        return (w, h, x, y)

    @overload
    def set_geometry(self, size: Tuple[int, int]):
        pass

    @overload
    def set_geometry(self, size: Tuple[int, int], position: Tuple[int, int]):
        pass

    def set_geometry(
        self, size: Tuple[int, int], position: Optional[Tuple[int, int]] = None
    ):
        geometry = f"{size[0]}x{size[1]}"
        if position:
            geometry += f"+{position[0]}+{position[1]}"
        self.wm_geometry(geometry)
        self.update()

    @property
    def size(self) -> tuple[int, int]:
        return self.geometry[:2]

    @size.setter
    def size(self, value: Tuple[int, int]):
        self.set_geometry(value)

    @property
    def width(self) -> int:
        return self.size[0]

    @width.setter
    def width(self, value: int):
        self.size = (value, self.height)

    @property
    def height(self) -> int:
        return self.size[1]

    @height.setter
    def height(self, value: int):
        self.size = (self.width, value)

    @property
    def position(self) -> Tuple[int, int]:
        return self.geometry[2:]

    @position.setter
    def position(self, value: Tuple[int, int]):
        self.set_geometry(self.size, value)

    @property
    def x(self) -> int:
        return self.position[0]

    @x.setter
    def x(self, value: int):
        self.position = (value, self.y)

    @property
    def y(self) -> int:
        return self.position[1]

    @y.setter
    def y(self, value: int):
        self.position = (self.x, value)

    @property
    def display_wh(self) -> Tuple[int, int]:
        return (self.display_h, self.display_w)

    @property
    def display_w(self) -> int:
        return self.winfo_screenwidth()

    @property
    def display_h(self) -> int:
        return self.winfo_screenheight()