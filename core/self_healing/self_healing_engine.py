def evaluate_self_healing(
    preventive_recommendation,
    autonomous_decision,
    adaptive_failover,
    risk,
):
    """
    Avalia necessidade de auto-recuperação.
    """

    preventive_level = preventive_recommendation.get(
        "level",
        "BAIXO"
    )

    autonomous_mode = autonomous_decision.get(
        "mode",
        "AUTONOMIA_NORMAL"
    )

    failover_action = adaptive_failover.get(
        "action",
        "MANTER_CONEXAO"
    )

    risk_level = risk.get(
        "risk_level",
        "BAIXO"
    )

    if (
        preventive_level == "CRITICO"
        or autonomous_mode == "INTERVENCAO_RECOMENDADA"
    ):
        return {
            "status": "AUTO_RECUPERACAO_CRITICA",
            "action": "EXECUTAR_RECUPERACAO_IMEDIATA",
            "message": (
                "Condição crítica detectada. "
                "Executando resposta de auto-recuperação."
            )
        }

    if failover_action == "PREPARAR_FAILOVER":
        return {
            "status": "AUTO_RECUPERACAO_PREVENTIVA",
            "action": "PREPARAR_RESTAURACAO",
            "message": (
                "Preparando recuperação preventiva "
                "de conectividade."
            )
        }

    if risk_level == "MÉDIO":
        return {
            "status": "AUTO_RECUPERACAO_MODERADA",
            "action": "AUMENTAR_RESILIENCIA",
            "message": (
                "Aplicando mecanismos moderados "
                "de resiliência operacional."
            )
        }

    return {
        "status": "SISTEMA_ESTAVEL",
        "action": "MANTER_OPERACAO",
        "message": (
            "Nenhuma ação de auto-recuperação necessária."
        )
    }


def summarize_self_healing(
    self_healing_result
):
    """
    Resume estado de auto-recuperação.
    """

    if not self_healing_result:
        return (
            "Sistema de auto-recuperação indisponível."
        )

    return (
        f"Status: "
        f"{self_healing_result.get('status')}\n"
        f"Ação: "
        f"{self_healing_result.get('action')}\n"
        f"Mensagem: "
        f"{self_healing_result.get('message')}"
    )