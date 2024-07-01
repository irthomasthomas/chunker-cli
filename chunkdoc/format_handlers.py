"""
format_handlers.py

This module provides input and output handlers for processing text chunks.
It includes classes and functions for reading input from various sources
and writing output in different formats such as JSON, CSV, and XML.
"""

import sys
import json
import csv
from abc import ABC, abstractmethod
from typing import List, Tuple, Union, IO, Optional
from xml.sax.saxutils import escape as xml_escape

# Input Handlers

class InputHandler(ABC):
    @abstractmethod
    def read(self) -> str:
        """Read and return the input as a string."""
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

def get_input_handler(source: Optional[str]) -> InputHandler:
    """
    Factory function to get the appropriate input handler.
    
    Args:
        source (Optional[str]): The input source. If None, uses stdin.
                                If it's a string, it's treated as a filename.

    Returns:
        InputHandler: An instance of the appropriate InputHandler subclass.

    Raises:
        ValueError: If an invalid input source is provided.
    """
    if source is None or source == '-':
        return StdinInputHandler()
    elif isinstance(source, str):
        return FileInputHandler(source)
    else:
        raise ValueError(f"Invalid input source: {source}")

def read_input(source: Union[str, None, IO]) -> str:
    """
    Convenience function to read input from various sources.

    Args:
        source (Union[str, None, IO]): The input source.
                                       If None, reads from stdin.
                                       If str, treats as filename (or stdin if '-').
                                       If file-like object, reads directly.

    Returns:
        str: The input text.

    Raises:
        ValueError: If an invalid input source is provided.
    """
    if isinstance(source, str) or source is None:
        handler = get_input_handler(source)
        return handler.read()
    elif hasattr(source, 'read'):
        return source.read()
    else:
        raise ValueError(f"Invalid input source: {source}")

# Output Handlers

class OutputHandler(ABC):
    @abstractmethod
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]) -> None:
        """Write the chunks to the specified output."""
        pass

class JsonOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]) -> None:
        data = [{"text": chunk, "tokens": token_count} for chunk, token_count in chunks]
        if isinstance(output, str):
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif output is None or output == sys.stdout:
            json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        else:
            json.dump(data, output, ensure_ascii=False, indent=2)

class CsvOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]) -> None:
        if isinstance(output, str):
            with open(output, 'w', newline='', encoding='utf-8') as f:
                self._write_csv(chunks, f)
        elif output is None or output == sys.stdout:
            self._write_csv(chunks, sys.stdout)
        else:
            self._write_csv(chunks, output)

    def _write_csv(self, chunks: List[Tuple[str, int]], output_file: IO) -> None:
        writer = csv.writer(output_file)
        writer.writerow(["text", "tokens"])
        writer.writerows(chunks)

class XmlOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]) -> None:
        xml_content = self._generate_xml(chunks)
        if isinstance(output, str):
            with open(output, 'w', encoding='utf-8') as f:
                f.write(xml_content)
        elif output is None or output == sys.stdout:
            sys.stdout.write(xml_content)
        else:
            output.write(xml_content)

    def _generate_xml(self, chunks: List[Tuple[str, int]]) -> str:
        lines = ['<chunks>']
        for chunk, token_count in chunks:
            lines.append(f'  <chunk tokens="{token_count}">')
            lines.append(f'    {xml_escape(chunk)}')
            lines.append('  </chunk>')
        lines.append('</chunks>')
        return ''.join(lines)

class LineXmlOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]) -> None:
        if isinstance(output, str):
            with open(output, 'w', encoding='utf-8') as f:
                self._write_line_xml(chunks, f)
        elif output is None or output == sys.stdout:
            self._write_line_xml(chunks, sys.stdout)
        else:
            self._write_line_xml(chunks, output)

    def _write_line_xml(self, chunks: List[Tuple[str, int]], output_file: IO) -> None:
        for chunk, token_count in chunks:
            output_file.write(f'<chunk tokens="{token_count}">{xml_escape(chunk)}</chunk>')

def get_output_handler(format: str) -> OutputHandler:
    """
    Factory function to get the appropriate output handler.
    
    Args:
        format (str): The desired output format.

    Returns:
        OutputHandler: An instance of the appropriate OutputHandler subclass.

    Raises:
        ValueError: If an unsupported output format is provided.
    """
    handlers = {
        'json': JsonOutputHandler,
        'csv': CsvOutputHandler,
        'xml': XmlOutputHandler,
        'line-xml': LineXmlOutputHandler
    }
    handler_class = handlers.get(format.lower())
    if handler_class is None:
        raise ValueError(f"Unsupported output format: {format}")
    return handler_class()
