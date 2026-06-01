from core.scanner.connectivity_scanner import collect_interfaces
from core.monitor.baseline_engine import save_baseline


def main():
    interfaces = collect_interfaces()

    save_baseline(interfaces)

    print("=" * 60)
    print("BASELINE CRIADA COM SUCESSO")
    print("=" * 60)

    for interface in interfaces:
        print(
            f"{interface['name']} | "
            f"{interface['ip']} | "
            f"{interface['classification']} | "
            f"{interface['trust_score']}/100"
        )


if __name__ == "__main__":
    main()