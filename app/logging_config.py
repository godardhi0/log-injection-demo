import logging
from pathlib import Path


def _build_logger(name: str, file_path: Path, log_format: str) -> None:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # avoids duplicated lines

    if not logger.handlers:  # avoids adding the handler twice
        handler = logging.FileHandler(file_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)


def setup_logging(log_dir: Path, log_format: str) -> None:
    log_dir.mkdir(exist_ok=True)
    _build_logger("demo.vulnerable", log_dir / "vulnerable.log", log_format)
    _build_logger("demo.secure", log_dir / "secure.log", log_format)