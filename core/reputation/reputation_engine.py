from pathlib import Path

LOG_FILE = Path("logs/connectivity_log.txt")


def calculate_interface_reputation(
    interface_name,
    limit=100
):
    if not LOG_FILE.exists():
        return {
            "score": 50,
            "classification": "DESCONHECIDA",
            "failures": 0,
            "successes": 0,
        }

    with LOG_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        lines = file.readlines()

    recent_lines = lines[-limit:]

    successes = 0
    failures = 0

    for line in recent_lines:

        if interface_name not in line:
            continue

        if (
            "Risco: BAIXO" in line
            and "PERMITIR" in line
        ):
            successes += 1

        if (
            "CRITICO" in line
            or "INTERVENCAO_RECOMENDADA" in line
            or "PREPARAR_FAILOVER" in line
        ):
            failures += 1

    total = successes + failures

    if total == 0:
        reputation = 50
    else:
        reputation = int(
            (successes / total) * 100
        )

    if reputation >= 90:
        classification = "ALTAMENTE_CONFIAVEL"

    elif reputation >= 70:
        classification = "CONFIAVEL"

    elif reputation >= 50:
        classification = "MODERADA"

    else:
        classification = "INSTAVEL"

    return {
        "score": reputation,
        "classification": classification,
        "failures": failures,
        "successes": successes,
    }