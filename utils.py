import sys
import traceback
from pathlib import Path
from tkinter.messagebox import showerror
from types import TracebackType
from typing import Any, Callable, Optional


def filename(*, is_file: bool = True, ext: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            try:
                filename: Path = Path(kwargs["filename"])
                
                if is_file and not filename.is_file():
                    raise OSError(f"File {filename.absolute()} must be a file")

                if not is_file and not filename.is_dir():
                    raise OSError(f"{filename.absolute()} must be a directory")
            
                if ext != None and filename.suffix != ext:
                    raise OSError(f"File {filename.absolute()} must end with {ext}")
            except (AttributeError, KeyError):
                pass
            return func(*args, **kwargs)

        return wrapper

    return decorator

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