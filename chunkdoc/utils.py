import os
import sys
from typing import Iterator, Any

def chunk_iterable(iterable: Iterator[Any], chunk_size: int) -> Iterator[list]:
    """
    Yield successive n-sized chunks from an iterable.
    
    Args:
    iterable: The iterable to chunk.
    chunk_size: The size of each chunk.

    Yields:
    Iterator[list]: Chunks of the iterable.
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
    file_path (str): Path to the file.

    Returns:
    int: Size of the file in bytes.
    """
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        print(f"Error getting file size: {e}", file=sys.stderr)
        return 0

def human_readable_size(size_bytes: int) -> str:
    """
    Convert a size in bytes to a human-readable string.
    
    Args:
    size_bytes (int): Size in bytes.

    Returns:
    str: Human-readable size string.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def is_valid_file(parser, arg):
    """
    Check if a file exists and is readable.
    
    Args:
    parser: The argument parser.
    arg: The file path to check.

    Returns:
    str: The file path if valid.

    Raises:
    parser.error: If the file is not valid.
    """
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    elif not os.path.isfile(arg):
        parser.error(f"{arg} is not a file!")
    elif not os.access(arg, os.R_OK):
        parser.error(f"The file {arg} is not readable!")
    else:
        return arg

def create_progress_bar(total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 50, fill: str = '█', print_end: str = ""):
    """
    Create a progress bar for console output.
    
    Args:
    total (int): Total iterations.
    prefix (str): Prefix string.
    suffix (str): Suffix string.
    decimals (int): Positive number of decimals in percent complete.
    length (int): Character length of bar.
    fill (str): Bar fill character.
    print_end (str): End character (e.g. "", "
").

    Returns:
    callable: A function that updates and prints the progress bar.
    """
    def print_progress_bar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'{prefix} |{bar}| {percent}% {suffix}', end=print_end)
        if iteration == total:
            print()

    return print_progress_bar

def setup_logging(verbose: bool = False):
    """
    Set up logging for the application.
    
    Args:
    verbose (bool): If True, set log level to DEBUG. Otherwise, set to INFO.
    """
    import logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
