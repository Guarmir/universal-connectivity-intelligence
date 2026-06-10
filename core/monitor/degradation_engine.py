from core.monitor.history_reader import read_last_logs


def extract_metric_from_log(line, metric_name):
    try:
        if metric_name not in line:
            return None

        part = line.split(metric_name + ":")[1]
        value_text = part.split("|")[0].strip()

        value_text = (
            value_text
            .replace("ms", "")
            .replace("/100", "")
            .strip()
        )

        return float(value_text)

    except Exception:
        return None


def calculate_average(values):
    valid_values = [
        value for value in values
        if value is not None
    ]

    if not valid_values:
        return None

    return round(
        sum(valid_values) / len(valid_values),
        2
    )


def filter_invalid_stability_values(values):
    """
    Remove quedas artificiais de estabilidade 0
    quando houver valores saudáveis recentes.
    """

    valid_values = [
        value for value in values
        if value is not None
    ]

    if not valid_values:
        return []

    healthy_values = [
        value for value in valid_values
        if value >= 80
    ]

    if healthy_values:
        return [
            value for value in valid_values
            if value > 0
        ]

    return valid_values


def analyze_degradation(limit=10):
    logs = read_last_logs(limit=limit)

    if not logs:
        return {
            "status": "SEM_HISTORICO",
            "message": "Histórico insuficiente para análise de degradação.",
            "details": [],
            "averages": {}
        }

    latency_values = []
    intelligence_values = []
    stability_values = []

    for line in logs:
        latency_values.append(
            extract_metric_from_log(
                line,
                "Latência"
            )
        )

        intelligence_values.append(
            extract_metric_from_log(
                line,
                "Intelligence Score"
            )
        )

        stability_values.append(
            extract_metric_from_log(
                line,
                "Estabilidade"
            )
        )

    filtered_stability_values = filter_invalid_stability_values(
        stability_values
    )

    avg_latency = calculate_average(
        latency_values
    )

    avg_intelligence = calculate_average(
        intelligence_values
    )

    avg_stability = calculate_average(
        filtered_stability_values
    )

    alerts = []

    latest_latency = next(
        (
            value for value in reversed(latency_values)
            if value is not None
        ),
        None
    )

    latest_intelligence = next(
        (
            value for value in reversed(intelligence_values)
            if value is not None
        ),
        None
    )

    latest_stability = next(
        (
            value for value in reversed(filtered_stability_values)
            if value is not None
        ),
        None
    )

    if (
        avg_latency is not None
        and latest_latency is not None
        and latest_latency > avg_latency * 1.5
    ):
        alerts.append({
            "type": "LATENCIA_EM_DEGRADACAO",
            "severity": "ALTA",
            "message": (
                f"Latência atual ({latest_latency} ms) "
                f"está acima da média histórica ({avg_latency} ms)."
            )
        })

    if (
        avg_intelligence is not None
        and latest_intelligence is not None
        and latest_intelligence < avg_intelligence * 0.70
    ):
        alerts.append({
            "type": "INTELLIGENCE_EM_QUEDA",
            "severity": "MÉDIA",
            "message": (
                f"Intelligence Score atual ({latest_intelligence}/100) "
                f"está abaixo da média histórica ({avg_intelligence}/100)."
            )
        })

    if (
        avg_stability is not None
        and latest_stability is not None
        and latest_stability < avg_stability * 0.70
    ):
        alerts.append({
            "type": "ESTABILIDADE_EM_QUEDA",
            "severity": "ALTA",
            "message": (
                f"Estabilidade atual ({latest_stability}/100) "
                f"está abaixo da média histórica ({avg_stability}/100)."
            )
        })

    if alerts:
        return {
            "status": "DEGRADACAO_DETECTADA",
            "message": "Sinais de degradação histórica detectados.",
            "details": alerts,
            "averages": {
                "latency": avg_latency,
                "intelligence": avg_intelligence,
                "stability": avg_stability,
            }
        }

    return {
        "status": "NORMAL",
        "message": "Nenhuma degradação histórica relevante detectada.",
        "details": [],
        "averages": {
            "latency": avg_latency,
            "intelligence": avg_intelligence,
            "stability": avg_stability,
        }
    }


def summarize_degradation(degradation_result):
    if not degradation_result:
        return "Análise de degradação indisponível."

    lines = [
        degradation_result.get(
            "message",
            "Sem mensagem de degradação."
        )
    ]

    averages = degradation_result.get(
        "averages",
        {}
    )

    if averages:
        lines.append(
            f"Média histórica de latência: "
            f"{averages.get('latency')} ms"
        )
        lines.append(
            f"Média histórica de intelligence score: "
            f"{averages.get('intelligence')}/100"
        )
        lines.append(
            f"Média histórica de estabilidade: "
            f"{averages.get('stability')}/100"
        )

    details = degradation_result.get(
        "details",
        []
    )

    for item in details:
        lines.append(
            f"[{item['severity']}] "
            f"{item['message']}"
        )

    return "\n".join(lines)