from typing import Optional, Callable, List, Tuple, Any

from pathlib import Path
import json


def filename(*, is_file: bool = True, ext: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                filename: Path = kwargs.pop("filename")
            except KeyError:
                pass
            else:
                if not filename.is_file == is_file:
                    raise OSError(f"File {filename.absolute()} must be a file")
                if not ext and filename.suffix != ext:
                    raise OSError(f"File {filename.absolute()} must end with {ext}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

class Appdata:
    def __init__(self, name: str) -> None:
        self.path = Path("~", f".{name}")
    
    def save(self, items: List[Tuple[str, ...]],) -> None:
        return self.export_save(self.path / "save.txt", items)

    def load_save(self) -> List[Tuple[str, ...]]:
        return self.import_save(self.path / "save.txt")

    @filename(is_file=True, ext=".json")
    def import_save(self, filename: Path) -> List[Tuple[str, ...]]:
        if not filename.exists():
            return []
        
        items = []
        with open(filename, "r") as fp:
            _items = json.load(fp)
            for item in _items:
                items.append((item["q"], item["a"]))
        return items
        
    @filename(is_file=True, ext=".json")
    def export_save(self, filename: Path, items: List[Tuple[str, ...]]) -> None:
        _items = []
        for question, answer in items:
            _items.append({
                "q": question,
                "a": answer
            })
        
        with open(filename, "w") as fp:
            json.dump(_items, fp)