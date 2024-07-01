import argparse
import sys
from .chunker import Chunker, get_chunking_strategy
from .config import Config
from .input_handlers import get_input_handler
from .output_handlers import get_output_handler

def main():
    config = Config()
    args = parse_arguments()

    try:
        input_handler = get_input_handler(args.input)
        text = input_handler.read()

        encoder = config.get_encoder(args.model) if args.strategy == 'token' else None
        chunking_strategy = get_chunking_strategy(args.strategy, encoder)
        chunker = Chunker(chunking_strategy)

        chunks = chunker.chunk_text(text, args.chunk_size)

        output_handler = get_output_handler(args.format)
        output_handler.write(chunks, args.output)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Chunk a document based on various strategies")
    parser.add_argument("input", nargs='?', help="Path to the input text file. If not provided, reads from stdin.")
    parser.add_argument("-o", "--output", help="Output file. If not provided, writes to stdout.")
    parser.add_argument("-s", "--chunk-size", type=int, default=500, help="Target chunk size (default: 500)")
    parser.add_argument("-m", "--model", default="gpt-3.5-turbo", help="Model to use for tokenization (default: gpt-3.5-turbo)")
    parser.add_argument("-f", "--format", choices=['json', 'csv', 'xml', 'line-xml'], 
                        default='json', help="Output format (default: json)")
    parser.add_argument("--strategy", choices=['token', 'line', 'paragraph'], 
                        default='token', help="Chunking strategy (default: token)")
    parser.add_argument("-c", "--config", help="Path to configuration file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    return parser.parse_args()

if __name__ == "__main__":
    main()