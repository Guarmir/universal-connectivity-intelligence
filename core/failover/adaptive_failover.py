def evaluate_adaptive_failover(
    recommended_interface,
    prediction_result,
    degradation_result,
):
    """
    Motor adaptativo de failover.

    Usa:
    - score contextual
    - previsão operacional
    - degradação histórica
    """

    contextual_score = recommended_interface.get(
        "contextual_score",
        0
    )

    prediction_level = prediction_result.get(
        "prediction_level",
        "BAIXO"
    )

    degradation_status = degradation_result.get(
        "status",
        "NORMAL"
    )

    if contextual_score < 40:
        return {
            "status": "CRÍTICO",
            "action": "FAILOVER_IMEDIATO",
            "message": (
                "Score contextual crítico."
            )
        }

    if prediction_level == "ALTO":
        return {
            "status": "PREVENTIVO",
            "action": "PREPARAR_FAILOVER",
            "message": (
                "Alta probabilidade de instabilidade."
            )
        }

    if degradation_status == "DEGRADACAO_DETECTADA":
        return {
            "status": "ATENÇÃO",
            "action": "MONITORAR",
            "message": (
                "Degradação histórica detectada."
            )
        }

    return {
        "status": "ESTÁVEL",
        "action": "MANTER_CONEXAO",
        "message": (
            "Conectividade saudável."
        )
    }