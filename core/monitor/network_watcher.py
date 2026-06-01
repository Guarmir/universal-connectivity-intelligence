import time
from datetime import datetime

from core.scanner.connectivity_scanner import (
    run_scan,
    collect_interfaces,
)

from core.monitor.change_detector import (
    detect_changes,
)

from core.monitor.local_logger import (
    save_log,
)

from core.monitor.baseline_engine import (
    load_baseline,
)

from core.monitor.baseline_comparator import (
    compare_with_baseline,
)

from core.monitor import runtime_state


def start_monitor(interval=30):

    print("=" * 60)
    print("NETWORK WATCHER INICIADO")
    print("=" * 60)

    baseline_interfaces = load_baseline()

    if baseline_interfaces:
        print("Baseline carregada com sucesso.")
    else:
        print("Nenhuma baseline encontrada.")

    while True:

        print(
            f"\nNova verificação: "
            f"{datetime.now()}"
        )

        current_interfaces = collect_interfaces()

        changes = detect_changes(
            current_interfaces,
            runtime_state.previous_interfaces
        )

        baseline_alerts = compare_with_baseline(
            current_interfaces,
            baseline_interfaces
        )

        if changes:

            print("\nMUDANÇAS DETECTADAS")
            print("-" * 60)

            for change in changes:

                print(change)

                save_log(
                    f"MUDANÇA DETECTADA: {change}"
                )

        else:

            print(
                "\nNenhuma mudança detectada."
            )

        if baseline_alerts:

            print("\nALERTAS DE BASELINE")
            print("-" * 60)

            for alert in baseline_alerts:

                print(alert)

                save_log(
                    f"ALERTA DE BASELINE: {alert}"
                )

        else:

            print(
                "\nAmbiente dentro da baseline."
            )

        runtime_state.previous_interfaces = (
            current_interfaces
        )

        run_scan()

        print(
            f"\nPróxima verificação em "
            f"{interval} segundos..."
        )

        time.sleep(interval)


if __name__ == "__main__":
    start_monitor()