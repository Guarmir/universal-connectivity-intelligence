from core.monitor.degradation_engine import analyze_degradation


def calculate_prediction_level(degradation_result):
    """
    Calcula nível preditivo baseado na análise histórica.
    """

    if not degradation_result:
        return "INDEFINIDO"

    status = degradation_result.get("status")

    if status == "DEGRADACAO_DETECTADA":
        return "ALTO"

    averages = degradation_result.get("averages", {})

    avg_latency = averages.get("latency")
    avg_intelligence = averages.get("intelligence")
    avg_stability = averages.get("stability")

    if avg_latency is None:
        return "BAIXO"

    if avg_latency >= 180:
        return "ALTO"

    if avg_latency >= 120:
        return "MÉDIO"

    if avg_intelligence is not None and avg_intelligence < 70:
        return "MÉDIO"

    if avg_stability is not None and avg_stability < 80:
        return "MÉDIO"

    return "BAIXO"


def generate_prediction_message(prediction_level):
    """
    Gera mensagem de previsão operacional.
    """

    if prediction_level == "ALTO":
        return (
            "Alta probabilidade de instabilidade operacional. "
            "Recomenda-se monitorar a conexão e preparar failover."
        )

    if prediction_level == "MÉDIO":
        return (
            "Possível tendência de instabilidade. "
            "Recomenda-se acompanhar a evolução da conexão."
        )

    if prediction_level == "BAIXO":
        return (
            "Baixa probabilidade de instabilidade no momento."
        )

    return (
        "Não foi possível calcular previsão operacional."
    )


def predict_operational_risk():
    """
    Executa previsão operacional baseada no histórico.
    """

    degradation_result = analyze_degradation(
        limit=10
    )

    prediction_level = calculate_prediction_level(
        degradation_result
    )

    message = generate_prediction_message(
        prediction_level
    )

    return {
        "prediction_level": prediction_level,
        "message": message,
        "source": degradation_result,
    }


def summarize_prediction(prediction_result):
    """
    Resume previsão operacional em texto.
    """

    if not prediction_result:
        return "Previsão operacional indisponível."

    level = prediction_result.get(
        "prediction_level",
        "INDEFINIDO"
    )

    message = prediction_result.get(
        "message",
        "Sem mensagem preditiva."
    )

    return (
        f"Nível preditivo: {level}\n"
        f"{message}"
    )