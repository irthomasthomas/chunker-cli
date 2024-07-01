import sys
import json
import csv
from abc import ABC, abstractmethod
from typing import List, Tuple, Union, IO
from xml.sax.saxutils import escape as xml_escape

class OutputHandler(ABC):
    @abstractmethod
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]):
        pass

class JsonOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]):
        data = [{"text": chunk, "tokens": token_count} for chunk, token_count in chunks]
        if isinstance(output, str):
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif output is None or output == sys.stdout:
            json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
        else:
            json.dump(data, output, ensure_ascii=False, indent=2)

class CsvOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]):
        if isinstance(output, str):
            with open(output, 'w', newline='', encoding='utf-8') as f:
                self._write_csv(chunks, f)
        elif output is None or output == sys.stdout:
            self._write_csv(chunks, sys.stdout)
        else:
            self._write_csv(chunks, output)

    def _write_csv(self, chunks: List[Tuple[str, int]], output_file: IO):
        writer = csv.writer(output_file)
        writer.writerow(["text", "tokens"])
        writer.writerows(chunks)

class XmlOutputHandler(OutputHandler):
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]):
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
    def write(self, chunks: List[Tuple[str, int]], output: Union[str, None, IO]):
        if isinstance(output, str):
            with open(output, 'w', encoding='utf-8') as f:
                self._write_line_xml(chunks, f)
        elif output is None or output == sys.stdout:
            self._write_line_xml(chunks, sys.stdout)
        else:
            self._write_line_xml(chunks, output)

    def _write_line_xml(self, chunks: List[Tuple[str, int]], output_file: IO):
        for chunk, token_count in chunks:
            output_file.write(f'<chunk tokens="{token_count}">{xml_escape(chunk)}</chunk>')

def get_output_handler(format: str) -> OutputHandler:
    """
    Factory function to get the appropriate output handler.
    
    Args:
    format (str): The desired output format.

    Returns:
    OutputHandler: An instance of the appropriate OutputHandler subclass.
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
