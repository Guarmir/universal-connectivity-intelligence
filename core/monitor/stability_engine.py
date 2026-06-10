from pathlib import Path


LOG_FILE = Path(
    "logs/connectivity_log.txt"
)


def calculate_stability_score(
    interface_name,
    limit=20
):
    """
    Calcula estabilidade operacional
    baseada no histórico recente.
    """

    if not LOG_FILE.exists():
        return 100

    with LOG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:

        lines = file.readlines()

    recent_lines = lines[-limit:]

    if not recent_lines:
        return 100

    total_recommendations = 0
    interface_recommendations = 0

    for line in recent_lines:

        if (
            "Recomendação:" in line
            or
            "Recomendação Contextual:" in line
        ):

            total_recommendations += 1

            if (
                f"Recomendação: {interface_name}"
                in line
                or
                f"Recomendação Contextual: {interface_name}"
                in line
            ):

                interface_recommendations += 1

    if total_recommendations == 0:
        return 100

    stability = int(
        (
            interface_recommendations
            / total_recommendations
        ) * 100
    )

    if stability < 0:
        stability = 0

    if stability > 100:
        stability = 100

    return stability