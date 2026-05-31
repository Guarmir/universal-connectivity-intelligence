from pathlib import Path


LOG_FILE = Path("logs/connectivity_log.txt")


def read_last_logs(limit=5):
    if not LOG_FILE.exists():
        return []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return lines[-limit:]