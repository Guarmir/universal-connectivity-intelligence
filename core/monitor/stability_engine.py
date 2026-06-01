from pathlib import Path


LOG_FILE = Path("logs/connectivity_log.txt")


def calculate_stability_score(interface_name, limit=20):
    if not LOG_FILE.exists():
        return 0

    with LOG_FILE.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    recent_lines = lines[-limit:]

    if not recent_lines:
        return 0

    total_recommendations = 0
    interface_recommendations = 0

    for line in recent_lines:
        if "Recomendação:" in line:
            total_recommendations += 1

            if f"Recomendação: {interface_name}" in line:
                interface_recommendations += 1

    if total_recommendations == 0:
        return 0

    stability = int(
        (interface_recommendations / total_recommendations) * 100
    )

    return stability