from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    LOG_DIR = BASE_DIR / "logs"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

    # Anti brute force
    MAX_FAILED_ATTEMPTS = 3
    WINDOW_SECONDS = 60

    # Maximum length of a user value written in a log
    MAX_LOG_FIELD_LENGTH = 100