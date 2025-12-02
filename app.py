from __future__ import annotations

import tkinter as tk
import tkinter.filedialog as fd
from typing import Any, Callable, List, Optional, Tuple

from core.window import Window
from ui import Button, Entry, Frame, ScrollBar, TreeView
from utils import Appdata, report_callback_exception


class ManagerView(TreeView):
    def __init__(self, master: App):
        super().__init__(master, columns=("question", "answer"), show="headings")

        self.appdata = master.appdata
        self.set_items(self.appdata.load_save())

        # self.bind(
        #     "<Double-1>",
        #     lambda event: self.entry_at(event.x, event.y)
        # )

        # The problem:
        #   It is not triggered if you turn on Caps lock
        # self.bind("<Control-a>", lambda event: self.selection_set(self.get_children()))

        self.selected_col: Optional[int] = None

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

    def __on_click(self, event: tk.Event):
        column = self.identify_column(event.x)

        if not column:
            for item_id in self.selection():
                self.selection_remove(item_id)
                self.selected_col = None
            return

        self.selected_col = int(column[1:]) - 1
        self.entry.focus()

    def __on_delete(self, event: tk.Event):
        selected_items = self.selection()
        if not selected_items:
            return
        items = self.get_children()
        iitem = items.index(self.selected_item)

        for item_id in selected_items:
            self.delete_item(item_id)

        if len(self.items) > iitem:
            self.selection_add(self.get_children()[iitem])

        self.selected_col = None
        self.entry.clear()

    def __on_focus_entry(self, event: tk.Event):
        item_id = self.selected_item
        if not (self.selected_col and item_id):
            return

        value = self.get_item(item_id)[self.selected_col]

        self.entry.set(value)

    def __on_enter_entry(self, event: tk.Event):
        if not self.entry.get().replace(" ", ""):
            return

        if not (self.selected_col and self.selected_item):
            item_id = self.insert_item((self.entry.get(), ""))
            self.selection_set(item_id)
            self.selected_col = 1
            self.__on_focus_entry(event)
        else:
            self.selection_remove(self.selected_item)
            self.selected_col = None

        self.entry.clear()
        self.appdata.save(self.items)

    def __validate(self, new_value: str) -> bool:
        item_id = self.selected_item

        if not (self.selected_col and item_id):
            return True

        values = list(self.get_item(item_id))
        values[self.selected_col] = new_value

        self.item(item_id, values=tuple(values))

        return True

    @property
    def length(self) -> int:
        return len(self.get_children())

    @property
    def items(self) -> List[Tuple[str, ...]]:
        return [tuple(self.item(row, "values")) for row in self.get_children()]

    @property
    def selected_item(self) -> str:
        items = self.selection()
        if not items:
            return ""
        return items[-1]

    def set_item(self, item_id: str, values: Tuple[Any, ...]):
        self.item(item_id, values=values)

    def get_item(self, item_id: str) -> Tuple[Any, ...]:
        values = tuple(self.item(item_id, "values"))
        return values if values else ("", "")

    def insert_item(self, values: Tuple[Any, ...]) -> str:
        return self.insert("", tk.END, values=values)

    def delete_item(self, item_id: str):
        self.delete(item_id)

    def clear_items(self):
        for item_id in self.get_children():
            self.delete_item(item_id)

    def set_items(self, items: List[Tuple[str, ...]]) -> None:
        self.clear_items()
        for values in items:
            self.insert_item(values)


class RightFrame(Frame):
    buttons: List[Button]

    def __init__(self, master: App, *, width: int = 15):
        super().__init__(master, width=width)
        self.buttons = []

    def add_button(self, text: str, func: Callable):
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
    def add_button(self, text: str, func: Callable):
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
    def __init__(self, args: List[str]):
        super().__init__()
        self.report_callback_exception = report_callback_exception
        self.appdata = Appdata("jalt")

        self.set_icon("./assets/icon.png")
        self.title = "Flashcard - JALT"

        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=4)

        self.resizable = False

        self.manager = ManagerView(self)
        self.manager.grid(column=1, row=0, padx=10, pady=10)

        # NOTE: I will improve* this UI soon!

        # self.scrollbar = ScrollBar(self, orient=tk.VERTICAL, command=self.manager.yview)
        # self.manager.configure(yscrollcommand=self.scrollbar.set)
        # self.scrollbar.grid(column=0, row=0, padx=10, pady=50, ipady=50, sticky=tk.NS)

        # Right frame
        self.rframe = RightFrame(self)
        self.rframe.add_button("Start Now", lambda: print("Pressed!"))
        self.rframe.add_button("Import", self.__import_file)
        self.rframe.add_button("Export", self.__export_file)
        self.rframe.add_button("Help", lambda: print("Pressed!"))
        self.rframe.grid(column=2, row=0, padx=5, pady=10, ipadx=2.5, sticky=tk.N)

        # Bottom frame
        # self.bframe = BottomFrame(self)
        # self.bframe.add_button("Add", self.manager.on_add)
        # self.bframe.add_button("Delete", self.manager.on_delete)
        # self.bframe.add_button("Edit", self.manager.on_edit)
        # self.bframe.grid(column=1, row=2, columnspan=2, padx=7.5, pady=10, sticky=tk.EW)

    filetypes: Tuple[Tuple[str, str]] = (("JSON files", "*.jalt.json"),)
    defaultextension: str = "*.jalt.json"

    def __import_file(self):
        filename = fd.askopenfilename(
            title="Import a file",
            initialdir=self.appdata.save_path,
            filetypes=self.filetypes,
        )
        if not filename:
            return

        items = self.appdata.import_save(filename=filename)
        self.manager.set_items(items)

    def __export_file(self):
        filename = fd.asksaveasfilename(
            title="Export a file",
            initialdir=self.appdata.save_path,
            defaultextension=self.defaultextension,
            filetypes=self.filetypes,
        )
        if not filename:
            return

        self.appdata.export_save(
            self.manager.items,
            filename=filename,
        )

    def mainloop(self, n: int = 0):
        return super().mainloop(n)
