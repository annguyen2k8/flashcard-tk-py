from __future__ import annotations

import tkinter as tk
from typing import Any, Callable, List, Optional, Tuple

from core.window import Window
from ui import Button, Entry, Frame, ScrollBar, TreeView
from utils import Appdata, report_callback_exception


class ManagerView(TreeView):
    def __init__(self, master: App) -> None:
        super().__init__(master, columns=("question", "answer"), show="headings")
        
        self.appdata = master.appdata

        items = self.appdata.load_save()
        for values in items:
            self.insert_values(values)
        
        # self.bind(
        #     "<Double-1>",
        #     lambda event: self.entry_at(event.x, event.y)
        # )

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

        self.entry.bind("<FocusIn>", self.__on_focus_entry)
        self.entry.bind("<Return>", self.__on_enter_entry)

        self.master.bind("<ButtonPress-1>", self.__on_click)
        self.master.bind("<Delete>", self.__on_delete)
        
    
    def __on_click(self, event: tk.Event) -> None:
        row = self.identify_row(event.y)
        column = self.identify_column(event.x)
        
        if row == "" or column == "":
            for row in self.selection():
                self.selection_remove(row)
                self.selected_pos = None
            return
        
        self.selected_pos = (row, int(column[1:]) - 1)
        self.entry.focus()
    
    
    def __on_delete(self, event: tk.Event) -> None:
        selected_items = self.selection()
        if selected_items:
            for item in selected_items:
                self.delete(item)
        self.selected_pos = None
        self.entry.clear()
    
    def __on_focus_entry(self, event: tk.Event) -> None:
        if not self.selected_pos:
            return

        item_id, col_index = self.selected_pos
        value = self.get_values(item_id)[col_index]

        self.entry.set(value)
    
    def __on_enter_entry(self, event: tk.Event) -> None:
        if not self.entry.get().replace(" ", ""):
            return

        if self.selected_pos is None:
            item_id = self.insert_values((self.entry.get(), ""))
            self.selection_set(item_id)
            self.selected_pos = (item_id, 1)
            self.__on_focus_entry(event)
        else:
            item_id, col_index = self.selected_pos
            if col_index == 1:
                self.appdata.save(self.items)

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
        values = tuple(self.item(item_id, "values"))
        return values if values else ("", "")

    def insert_values(self, values: Tuple[Any, ...]) -> str:
        return self.insert("", tk.END, values=values)

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
        self.report_callback_exception = report_callback_exception
        self.appdata = Appdata("jalt")
        
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