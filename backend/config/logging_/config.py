import logging
import atexit
import logging.config
import tomli
from logging import Handler
from pathlib import Path
from typing import Any


def configure_django_logging() -> dict[str, Any]:
    config_file: Path = Path("./config/logging_/config.toml")
    with open(config_file, "rb") as file:
        config: dict[str, Any] = tomli.load(file)

    return config
