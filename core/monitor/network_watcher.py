import time
from datetime import datetime

from core.scanner.connectivity_scanner import run_scan


def start_monitor(interval=30):

    print("=" * 60)
    print("NETWORK WATCHER INICIADO")
    print("=" * 60)

    while True:

        print(
            f"\nNova verificação: "
            f"{datetime.now()}"
        )

        run_scan()

        print(
            f"\nPróxima verificação em "
            f"{interval} segundos..."
        )

        time.sleep(interval)


if __name__ == "__main__":
    start_monitor()