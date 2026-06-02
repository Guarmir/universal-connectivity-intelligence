def calculate_intelligence_score(
    trust_score,
    stability_score,
    latency_quality
):

    latency_points = {
        "EXCELENTE": 100,
        "BOA": 80,
        "RUIM": 50,
        "CRÍTICA": 20,
        "SEM RESPOSTA": 0,
    }

    latency_score = latency_points.get(
        latency_quality,
        0
    )

    final_score = int(
        (
            trust_score * 0.4
            +
            stability_score * 0.4
            +
            latency_score * 0.2
        )
    )

    return final_score