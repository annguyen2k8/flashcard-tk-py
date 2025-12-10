import json
import sys
import traceback
from pathlib import Path
from tkinter.messagebox import showerror
from types import TracebackType
from typing import Any, Callable, List, Optional, Tuple, Union


def filename(*, is_file: bool = True, ext: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                filename: Path = Path(kwargs["filename"])
                
                if not filename.is_file != is_file:
                    raise OSError(f"File {filename.absolute()} must be a file")
                if ext != None and filename.suffix != ext:
                    raise OSError(f"File {filename.absolute()} must end with {ext}")
            except (AttributeError, KeyError):
                pass
            return func(*args, **kwargs)

        return wrapper

    return decorator


class Appdata:
    def __init__(self, name: str):
        self.path = Path.home() / f".{name}"
        self.path.mkdir(exist_ok=True)
    
        self.save_file = self.path / ".temp.json"
        if not self.save_file.exists():
            self.save()
        
        self.save_path = Path.home() / "Documents"
        if not self.save_path.exists():
            self.save_path = self.path / "saves"
        self.save_path.mkdir(exist_ok=True)
    
    # def save(
    #     self,
    #     items: List[Tuple[str, ...]] = [],
    # ):
    #     return self.export_save(items, filename=self.save_file)

    # def load_save(self) -> List[Tuple[str, ...]]:
    #     return self.import_save(filename=self.save_file)

    # @filename(is_file=True, ext=".json")
    # def import_save(
    #     self, *, 
    #     filename: Union[str, Path]
    #     ) -> List[Tuple[str, ...]]:
    #     items = []
    #     with open(filename, "r") as fp:
    #         _items = json.load(fp)
    #         for item in _items:
    #             items.append((item["q"], item["a"]))
    #     return items

    # @filename(is_file=True, ext=".json")
    # def export_save(
    #     self, items: List[Tuple[str, ...]] = [], *,
    #     filename: Union[str, Path]
    #     ):
    #     _items = []
    #     for question, answer in items:
    #         _items.append({"q": question, "a": answer})

    #     with open(filename, "w") as fp:
    #         json.dump(_items, fp)

def report_callback_exception(
    exc_type: type[BaseException], 
    exc_value: BaseException, 
    exc_traceback: Optional[TracebackType] = None
    ):
    message = "".join(traceback.format_exception(type(exc_value), exc_value, exc_value.__traceback__))
    
    sys.stdout.write(message)
    
    showerror(
        title=exc_type.__name__,
        message=message
        )

def ignore_keyerror(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except KeyError:
            pass
    return wrapper