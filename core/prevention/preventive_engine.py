def calculate_preventive_level(
    autonomous_decision,
    prediction_result,
    adaptive_failover,
    operational_profile,
):
    """
    Calcula nível preventivo operacional.
    """

    autonomous_mode = autonomous_decision.get(
        "mode",
        "AUTONOMIA_NORMAL"
    )

    prediction_level = prediction_result.get(
        "prediction_level",
        "BAIXO"
    )

    adaptive_action = adaptive_failover.get(
        "action",
        "MANTER_CONEXAO"
    )

    profile_name = operational_profile.get(
        "profile_name",
        "DESCONHECIDO"
    )

    if autonomous_mode == "INTERVENCAO_RECOMENDADA":
        return "CRITICO"

    if adaptive_action == "FAILOVER_IMEDIATO":
        return "CRITICO"

    if prediction_level == "ALTO":
        return "ALTO"

    if adaptive_action == "PREPARAR_FAILOVER":
        return "ALTO"

    if autonomous_mode == "AUTONOMIA_RESTRITA":
        return "MEDIO"

    if prediction_level == "MÉDIO":
        return "MEDIO"

    if profile_name == "REDE_INSTAVEL":
        return "MEDIO"

    return "BAIXO"


def generate_preventive_action(
    preventive_level
):
    """
    Define ação preventiva.
    """

    if preventive_level == "CRITICO":
        return "EXECUTAR_RESPOSTA_CRITICA"

    if preventive_level == "ALTO":
        return "PREPARAR_FAILOVER_PREVENTIVO"

    if preventive_level == "MEDIO":
        return "AUMENTAR_MONITORAMENTO"

    return "MANTER_OPERACAO_NORMAL"


def generate_preventive_message(
    preventive_level
):
    """
    Gera mensagem preventiva.
    """

    if preventive_level == "CRITICO":
        return (
            "Condição crítica detectada. "
            "Recomenda-se ação imediata."
        )

    if preventive_level == "ALTO":
        return (
            "Risco elevado previsto. "
            "Preparar failover preventivo."
        )

    if preventive_level == "MEDIO":
        return (
            "Sinais moderados de atenção. "
            "Aumentar monitoramento operacional."
        )

    return (
        "Nenhuma ação preventiva necessária no momento."
    )


def generate_preventive_recommendation(
    autonomous_decision,
    prediction_result,
    adaptive_failover,
    operational_profile,
):
    """
    Gera recomendação preventiva operacional.
    """

    preventive_level = calculate_preventive_level(
        autonomous_decision,
        prediction_result,
        adaptive_failover,
        operational_profile,
    )

    preventive_action = generate_preventive_action(
        preventive_level
    )

    preventive_message = generate_preventive_message(
        preventive_level
    )

    return {
        "level": preventive_level,
        "action": preventive_action,
        "message": preventive_message,
    }


def summarize_preventive_recommendation(
    preventive_recommendation
):
    """
    Resume recomendação preventiva.
    """

    if not preventive_recommendation:
        return (
            "Prevenção operacional indisponível."
        )

    return (
        f"Nível preventivo: "
        f"{preventive_recommendation.get('level')}\n"
        f"Ação preventiva: "
        f"{preventive_recommendation.get('action')}\n"
        f"Mensagem: "
        f"{preventive_recommendation.get('message')}"
    )