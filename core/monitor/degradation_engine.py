from core.monitor.history_reader import read_last_logs


def extract_metric_from_log(line, metric_name):
    """
    Extrai um valor numérico simples de uma linha de log.
    Exemplo:
    Latência: 58.96 ms
    Intelligence Score: 88/100
    Estabilidade: 100/100
    """

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


def analyze_degradation(limit=10):
    """
    Analisa os últimos logs e identifica sinais
    de degradação histórica.
    """

    logs = read_last_logs(limit=limit)

    if not logs:
        return {
            "status": "SEM_HISTORICO",
            "message": "Histórico insuficiente para análise de degradação.",
            "details": []
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

    avg_latency = calculate_average(
        latency_values
    )

    avg_intelligence = calculate_average(
        intelligence_values
    )

    avg_stability = calculate_average(
        stability_values
    )

    alerts = []

    latest_latency = latency_values[-1] if latency_values else None
    latest_intelligence = (
        intelligence_values[-1]
        if intelligence_values
        else None
    )
    latest_stability = (
        stability_values[-1]
        if stability_values
        else None
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
        and latest_intelligence < avg_intelligence * 0.85
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
        and latest_stability < avg_stability * 0.85
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
    """
    Gera resumo textual da análise de degradação.
    """

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