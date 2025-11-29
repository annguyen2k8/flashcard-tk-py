from __future__ import annotations

import tkinter as tk
from typing import Any, Callable, List, Optional, Tuple

from core.window import Window
from ui import Button, Entry, Frame, ScrollBar, TreeView


class ManagerView(TreeView):
    def __init__(self, master: App) -> None:
        super().__init__(master, columns=("question", "answer"), show="headings")

        # self.bind(
        #     "<Double-1>",
        #     lambda event: self.entry_at(event.x, event.y)
        # )

        self.bind("<ButtonPress-1>", self.on_press_at)

        self.bind("<Delete>", lambda event: self.on_delete())

        # The problem:
        #   It is not triggered if you turn on Caps lock
        # self.bind("<Control-a>", lambda event: self.selection_set(self.get_children()))

        self.selected_pos: Optional[Tuple[str, int]] = None

        self.entry = Entry(
            self.master,
            validate="key",
            validatecommand=(self.register(self.__validate), "%P"),
        )
        self.entry.insert(0, "")
        self.entry.grid(column=1, row=1, sticky=tk.EW, padx=10, pady=10)
        self.entry.focus_set()

        self.entry.bind("<FocusIn>", self.__on_focus)
        self.entry.bind("<Return>", self.__on_enter)
    
    def __on_focus(self, event: tk.Event) -> None:
        if not self.selected_pos:
            return

        item_id, col_index = self.selected_pos

        values = self.get_values(item_id)

        self.entry.set(values[col_index])

    def __on_enter(self, event: tk.Event) -> None:
        if not self.entry.get().replace(" ", ""):
            return

        if self.selected_pos is None:
            item_id = self.insert_values((self.entry.get(), ""))
            self.selection_set(item_id)
            self.selected_pos = (item_id, 1)
            self.__on_focus(event)
        else:
            item_id, col_index = self.selected_pos

            self.selection_remove(item_id)
            self.selected_pos = None
        self.entry.clear()

    def __validate(self, new_value: str) -> bool:
        if self.selected_pos is None:
            return True

        item_id, col_index = self.selected_pos

        values = list(self.get_values(item_id))
        values[col_index] = new_value

        self.item(item_id, values=tuple(values))

        return True

    @property
    def length(self) -> int:
        return len(self.get_children())

    @property
    def items(self) -> List[Tuple[str, ...]]:
        return [tuple(self.item(row, "values")) for row in self.get_children()]

    def set_values(self, item_id: str, values: Tuple[Any, ...]):
        self.item(item_id, values=values)

    def get_values(self, item_id: str) -> Tuple[Any, ...]:
        return tuple(self.item(item_id, "values"))

    def insert_values(self, values: Tuple[Any, ...]) -> str:
        return self.insert("", tk.END, values=values)

    def on_delete(self) -> None:
        selected_items = self.selection()
        if selected_items:
            for item in selected_items:
                self.delete(item)

    def on_press_at(self, event: tk.Event) -> None:
        self.selected_pos = (
            self.identify_row(event.y),
            int(self.identify_column(event.x)[1:]) - 1,
        )
        if self.selected_pos[0] == "":
            return
        self.entry.focus()

    def add(self, values: Tuple[Any, ...]) -> str:
        return self.insert("", tk.END, values=values)


class RightFrame(Frame):
    buttons: List[Button]

    def __init__(self, master: App, *, width: int = 15):
        super().__init__(master, width=width)
        self.buttons = []

    def add_button(self, text: str, func: Callable) -> None:
        button = Button(
            self,
            text=text,
            command=func,
            width=int(self["width"] * 0.8),
        )
        self.buttons.append(button)

        for i, button in enumerate(self.buttons):
            button.grid(column=0, row=i, pady=2.5)


class BottomFrame(RightFrame):
    def add_button(self, text: str, func: Callable) -> None:
        button = Button(
            self,
            text=text,
            command=func,
            width=int(self["width"] * 0.8),
        )
        self.buttons.append(button)

        for i, button in enumerate(self.buttons):
            button.grid(column=i, row=0, padx=2.5)


class App(Window):
    def __init__(self, args: List[str]) -> None:
        super().__init__()
        self.set_icon("assets/icon.ico")
        self.title = "Flashcard - JALT"

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=4)

        self.resizable = False

        self.manager = ManagerView(self)
        self.manager.grid(column=1, row=0, padx=10, pady=10)

        # ------- NOTE: I will make this UI to be better soon!

        # self.scrollbar = ScrollBar(self, orient=tk.VERTICAL, command=self.manager.yview)
        # self.manager.configure(yscrollcommand=self.scrollbar.set)
        # self.scrollbar.grid(column=0, row=0, padx=10, pady=50, ipady=50, sticky=tk.NS)

        # Right frame
        self.rframe = RightFrame(self)
        self.rframe.add_button("Start Now", lambda: print("Pressed!"))
        self.rframe.add_button("Import", lambda: print("Pressed!"))
        self.rframe.add_button("Export", lambda: print("Pressed!"))
        self.rframe.add_button("Help", lambda: print("Pressed!"))
        self.rframe.grid(column=2, row=0, padx=5, pady=10, ipadx=2.5, sticky=tk.N)

        # Bottom frame
        # self.bframe = BottomFrame(self)
        # self.bframe.add_button("Add", self.manager.on_add)
        # self.bframe.add_button("Delete", self.manager.on_delete)
        # self.bframe.add_button("Edit", self.manager.on_edit)
        # self.bframe.grid(column=1, row=2, columnspan=2, padx=7.5, pady=10, sticky=tk.EW)

    def mainloop(self, n: int = 0) -> None:
        return super().mainloop(n)