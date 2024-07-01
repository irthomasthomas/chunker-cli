import os
import json
import tiktoken
from typing import Dict, Any

class Config:
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_STRATEGY = "token"
    DEFAULT_FORMAT = "json"

    def __init__(self, config_file: str = None):
        self.config: Dict[str, Any] = {
            "chunk_size": self.DEFAULT_CHUNK_SIZE,
            "model": self.DEFAULT_MODEL,
            "strategy": self.DEFAULT_STRATEGY,
            "format": self.DEFAULT_FORMAT
        }
        self.load_config(config_file)

    def load_config(self, config_file: str = None):
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self.config.update(file_config)

        # Load from environment variables
        env_config = {
            "chunk_size": os.environ.get("CHUNKDOC_CHUNK_SIZE"),
            "model": os.environ.get("CHUNKDOC_MODEL"),
            "strategy": os.environ.get("CHUNKDOC_STRATEGY"),
            "format": os.environ.get("CHUNKDOC_FORMAT")
        }
        
        # Update config with non-None environment variables
        self.config.update({k: v for k, v in env_config.items() if v is not None})

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def get_encoder(self, model: str = None) -> tiktoken.Encoding:
        model = model or self.get("model")
        return tiktoken.encoding_for_model(model)

    @property
    def chunk_size(self) -> int:
        return int(self.get("chunk_size"))

    @property
    def model(self) -> str:
        return self.get("model")

    @property
    def strategy(self) -> str:
        return self.get("strategy")

    @property
    def format(self) -> str:
        return self.get("format")

def get_config_path() -> str:
    """
    Get the path to the config file based on XDG Base Directory Specification.
    """
    config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(config_home, "chunkdoc", "config.json")

def load_config(config_file: str = None) -> Config:
    if not config_file:
        config_file = get_config_path()
    return Config(config_file)
