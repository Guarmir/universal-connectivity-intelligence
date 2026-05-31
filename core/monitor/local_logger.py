from datetime import datetime
from pathlib import Path


LOG_FILE = Path("logs/connectivity_log.txt")


def save_log(message):
    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:
        file.write(
            f"[{datetime.now()}] {message}\n"
        )