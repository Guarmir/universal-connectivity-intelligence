from datetime import datetime

from core.monitor.history_reader import (
    read_last_logs,
)


def determine_period(hour):
    """
    Classifica período do dia.
    """

    if 0 <= hour < 6:
        return "MADRUGADA"

    if 6 <= hour < 12:
        return "MANHÃ"

    if 12 <= hour < 18:
        return "TARDE"

    return "NOITE"


def extract_latency(line):
    try:

        if "Latência:" not in line:
            return None

        latency_part = (
            line.split("Latência:")[1]
            .split("|")[0]
            .replace("ms", "")
            .strip()
        )

        return float(latency_part)

    except Exception:
        return None


def extract_timestamp(line):
    try:

        start = line.find("[")
        end = line.find("]")

        if start == -1 or end == -1:
            return None

        timestamp_text = line[start + 1:end]

        return datetime.strptime(
            timestamp_text,
            "%Y-%m-%d %H:%M:%S.%f"
        )

    except Exception:
        return None


def analyze_behavior(limit=100):
    """
    Analisa comportamento histórico.
    """

    logs = read_last_logs(limit)

    if not logs:
        return {
            "status": "SEM_DADOS",
            "message": (
                "Histórico insuficiente."
            )
        }

    periods = {
        "MADRUGADA": [],
        "MANHÃ": [],
        "TARDE": [],
        "NOITE": [],
    }

    for line in logs:

        timestamp = extract_timestamp(
            line
        )

        latency = extract_latency(
            line
        )

        if (
            timestamp is None
            or latency is None
        ):
            continue

        period = determine_period(
            timestamp.hour
        )

        periods[period].append(
            latency
        )

    profile = {}

    for period, values in periods.items():

        if values:

            avg = round(
                sum(values) / len(values),
                2
            )

            profile[period] = {
                "samples": len(values),
                "average_latency": avg,
            }

    return {
        "status": "OK",
        "message": (
            "Perfil comportamental calculado."
        ),
        "profile": profile,
    }


def summarize_behavior(
    behavior_result
):
    """
    Resumo textual.
    """

    if not behavior_result:
        return (
            "Análise comportamental indisponível."
        )

    if (
        behavior_result["status"]
        != "OK"
    ):
        return behavior_result[
            "message"
        ]

    lines = [
        behavior_result[
            "message"
        ]
    ]

    profile = behavior_result.get(
        "profile",
        {}
    )

    for period, data in profile.items():

        lines.append(
            f"{period}: "
            f"{data['average_latency']} ms "
            f"({data['samples']} amostras)"
        )

    return "\n".join(lines)