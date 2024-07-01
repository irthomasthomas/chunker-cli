import sys
from abc import ABC, abstractmethod
from typing import Union, IO

class InputHandler(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

class FileInputHandler(InputHandler):
    def __init__(self, filename: str):
        self.filename = filename

    def read(self) -> str:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Error reading file {self.filename}: {str(e)}")

class StdinInputHandler(InputHandler):
    def read(self) -> str:
        return sys.stdin.read()

class StringInputHandler(InputHandler):
    def __init__(self, text: str):
        self.text = text

    def read(self) -> str:
        return self.text

def get_input_handler(source: Union[str, None]) -> InputHandler:
    """
    Factory function to get the appropriate input handler.
    
    Args:
    source (str or None): The input source. If None, uses stdin.
                          If it's a string, it's treated as a filename.

    Returns:
    InputHandler: An instance of the appropriate InputHandler subclass.
    """
    if source is None:
        return StdinInputHandler()
    elif isinstance(source, str):
        if source == '-':
            return StdinInputHandler()
        else:
            return FileInputHandler(source)
    else:
        raise ValueError(f"Invalid input source: {source}")

def read_input(source: Union[str, None, IO]) -> str:
    """
    Convenience function to read input from various sources.

    Args:
    source (str, None, or file-like object): The input source.
                                             If None, reads from stdin.
                                             If str, treats as filename (or stdin if '-').
                                             If file-like object, reads directly.

    Returns:
    str: The input text.
    """
    if isinstance(source, str) or source is None:
        handler = get_input_handler(source)
        return handler.read()
    elif hasattr(source, 'read'):
        return source.read()
    else:
        raise ValueError(f"Invalid input source: {source}")
