from pathlib import Path


BASELINE_FILE = Path("logs/baseline.txt")


def save_baseline(interfaces):
    BASELINE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with BASELINE_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        for interface in interfaces:
            file.write(
                f"{interface['name']}|"
                f"{interface['ip']}|"
                f"{interface['classification']}|"
                f"{interface['trust_score']}\n"
            )


def load_baseline():
    if not BASELINE_FILE.exists():
        return []

    baseline = []

    with BASELINE_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        for line in file:
            parts = line.strip().split("|")

            if len(parts) == 4:
                baseline.append({
                    "name": parts[0],
                    "ip": parts[1],
                    "classification": parts[2],
                    "trust_score": int(parts[3]),
                })

    return baseline