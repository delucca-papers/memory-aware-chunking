import os
import uuid

DEFAULT_CONFIG_FILE = os.environ.get("DOWSER_CONFIG_FILE", "dowser.toml")
DEFAULT_CONFIG = {
    "dowser": {
        "execution_id": uuid.uuid4(),
        "output_dir": "./",
        "metrics": {
            "input_metadata": "",
            "memory_usage": {
                "backend": "kernel",
                "precision": "4",
                "output_dir": "memory_usage",
                "filename_prefix": "",
                "filename_suffix": "",
                "unit": "kb",
            },
        },
        "logging": {
            "level": "info",
            "filename": "dowser.log",
        },
    }
}
