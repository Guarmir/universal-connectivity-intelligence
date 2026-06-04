HIGH_LATENCY_THRESHOLD = 180
LOW_STABILITY_THRESHOLD = 50
LOW_INTELLIGENCE_THRESHOLD = 40


def detect_operational_anomalies(interface_data):
    """
    Detecta anomalias operacionais
    na conectividade.
    """

    anomalies = []

    latency = interface_data.get(
        "latency_ms",
        0
    )

    stability = interface_data.get(
        "stability_score",
        0
    )

    intelligence = interface_data.get(
        "intelligence_score",
        0
    )

    risk_level = interface_data.get(
        "risk_level",
        ""
    )

    if latency >= HIGH_LATENCY_THRESHOLD:

        anomalies.append({
            "type": "LATENCIA_ALTA",
            "severity": "ALTA",
            "message": (
                f"Latência elevada detectada: "
                f"{latency} ms"
            )
        })

    if stability <= LOW_STABILITY_THRESHOLD:

        anomalies.append({
            "type": "ESTABILIDADE_BAIXA",
            "severity": "ALTA",
            "message": (
                f"Estabilidade baixa detectada: "
                f"{stability}/100"
            )
        })

    if intelligence <= LOW_INTELLIGENCE_THRESHOLD:

        anomalies.append({
            "type": "INTELLIGENCE_BAIXO",
            "severity": "MÉDIA",
            "message": (
                f"Intelligence Score baixo: "
                f"{intelligence}/100"
            )
        })

    if risk_level == "ALTO":

        anomalies.append({
            "type": "RISCO_OPERACIONAL",
            "severity": "ALTA",
            "message": (
                "Risco operacional elevado detectado."
            )
        })

    return anomalies


def summarize_anomalies(anomalies):

    if not anomalies:
        return (
            "Nenhuma anomalia operacional detectada."
        )

    summary = []

    for anomaly in anomalies:

        summary.append(
            f"[{anomaly['severity']}] "
            f"{anomaly['message']}"
        )

    return "\n".join(summary)