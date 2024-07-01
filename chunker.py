import tiktoken
from abc import ABC, abstractmethod
from typing import List, Tuple

class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text: str, chunk_size: int) -> List[Tuple[str, int]]:
        pass

class TokenBasedChunking(ChunkingStrategy):
    def __init__(self, encoder: tiktoken.Encoding):
        self.encoder = encoder

    def chunk(self, text: str, chunk_size: int) -> List[Tuple[str, int]]:
        tokens = self.encoder.encode(text)
        chunks = []
        current_chunk = []
        current_chunk_size = 0

        for token in tokens:
            if current_chunk_size >= chunk_size:
                chunk_text = self.encoder.decode(current_chunk)
                chunks.append((chunk_text, len(current_chunk)))
                current_chunk = []
                current_chunk_size = 0
            
            current_chunk.append(token)
            current_chunk_size += 1

        if current_chunk:
            chunk_text = self.encoder.decode(current_chunk)
            chunks.append((chunk_text, len(current_chunk)))

        return chunks

class LineBasedChunking(ChunkingStrategy):
    def chunk(self, text: str, chunk_size: int) -> List[Tuple[str, int]]:
        lines = text.splitlines()
        chunks = []
        current_chunk = []
        current_chunk_size = 0

        for line in lines:
            line_size = len(line.split())
            if current_chunk_size + line_size > chunk_size and current_chunk:
                chunks.append((' '.join(current_chunk), current_chunk_size))
                current_chunk = []
                current_chunk_size = 0
            
            current_chunk.append(line)
            current_chunk_size += line_size

        if current_chunk:
            chunks.append((' '.join(current_chunk), current_chunk_size))

        return chunks

class ParagraphBasedChunking(ChunkingStrategy):
    def chunk(self, text: str, chunk_size: int) -> List[Tuple[str, int]]:
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_chunk_size = 0

        for paragraph in paragraphs:
            paragraph_size = len(paragraph.split())
            if current_chunk_size + paragraph_size > chunk_size and current_chunk:
                chunks.append(('\n\n'.join(current_chunk), current_chunk_size))
                current_chunk = []
                current_chunk_size = 0
            
            current_chunk.append(paragraph)
            current_chunk_size += paragraph_size

        if current_chunk:
            chunks.append(('\n\n'.join(current_chunk), current_chunk_size))

        return chunks

class Chunker:
    def __init__(self, strategy: ChunkingStrategy):
        self.strategy = strategy

    def chunk_text(self, text: str, chunk_size: int) -> List[Tuple[str, int]]:
        return self.strategy.chunk(text, chunk_size)

def get_chunking_strategy(strategy_name: str, encoder: tiktoken.Encoding = None) -> ChunkingStrategy:
    if strategy_name == 'token':
        if encoder is None:
            raise ValueError("Encoder is required for token-based chunking")
        return TokenBasedChunking(encoder)
    elif strategy_name == 'line':
        return LineBasedChunking()
    elif strategy_name == 'paragraph':
        return ParagraphBasedChunking()
    else:
        raise ValueError(f"Unknown chunking strategy: {strategy_name}")