def calculate_autonomous_confidence(
    recommended,
    prediction_result,
    operational_profile,
    adaptive_failover,
):
    """
    Calcula confiança operacional autônoma.
    """

    confidence = 100

    contextual_score = recommended.get(
        "contextual_score",
        0
    )

    prediction_level = prediction_result.get(
        "prediction_level",
        "BAIXO"
    )

    profile_name = operational_profile.get(
        "profile_name",
        "DESCONHECIDO"
    )

    adaptive_action = adaptive_failover.get(
        "action",
        "MANTER_CONEXAO"
    )

    if contextual_score < 80:
        confidence -= 15

    if contextual_score < 60:
        confidence -= 25

    if prediction_level == "MÉDIO":
        confidence -= 20

    if prediction_level == "ALTO":
        confidence -= 40

    if profile_name == "REDE_MODERADA":
        confidence -= 15

    if profile_name == "REDE_INSTAVEL":
        confidence -= 35

    if adaptive_action in [
        "PREPARAR_FAILOVER",
        "FAILOVER_IMEDIATO",
    ]:
        confidence -= 30

    if confidence < 0:
        confidence = 0

    return confidence


def classify_autonomous_mode(confidence):
    """
    Classifica modo operacional autônomo.
    """

    if confidence >= 85:
        return "AUTONOMIA_NORMAL"

    if confidence >= 65:
        return "AUTONOMIA_ASSISTIDA"

    if confidence >= 40:
        return "AUTONOMIA_RESTRITA"

    return "INTERVENCAO_RECOMENDADA"


def generate_autonomous_action(mode):
    """
    Define ação autônoma recomendada.
    """

    if mode == "AUTONOMIA_NORMAL":
        return "MANTER_OPERACAO"

    if mode == "AUTONOMIA_ASSISTIDA":
        return "MONITORAR_COM_ATENCAO"

    if mode == "AUTONOMIA_RESTRITA":
        return "REDUZIR_CONFIANCA_OPERACIONAL"

    return "SOLICITAR_INTERVENCAO"


def generate_autonomous_message(
    mode,
    confidence,
):
    """
    Gera mensagem operacional.
    """

    if mode == "AUTONOMIA_NORMAL":
        return (
            f"Operação saudável. "
            f"Confiança autônoma: {confidence}/100."
        )

    if mode == "AUTONOMIA_ASSISTIDA":
        return (
            f"Operação aceitável, mas requer atenção. "
            f"Confiança autônoma: {confidence}/100."
        )

    if mode == "AUTONOMIA_RESTRITA":
        return (
            f"Condições operacionais limitadas. "
            f"Confiança autônoma: {confidence}/100."
        )

    return (
        f"Intervenção recomendada. "
        f"Confiança autônoma: {confidence}/100."
    )


def make_autonomous_decision(
    recommended,
    prediction_result,
    operational_profile,
    adaptive_failover,
):
    """
    Cria decisão operacional autônoma.
    """

    if not recommended:
        return {
            "status": "SEM_INTERFACE",
            "confidence": 0,
            "mode": "INTERVENCAO_RECOMENDADA",
            "action": "SEM_INTERFACE_OPERACIONAL",
            "message": (
                "Nenhuma interface operacional disponível."
            ),
        }

    confidence = calculate_autonomous_confidence(
        recommended,
        prediction_result,
        operational_profile,
        adaptive_failover,
    )

    mode = classify_autonomous_mode(
        confidence
    )

    action = generate_autonomous_action(
        mode
    )

    message = generate_autonomous_message(
        mode,
        confidence,
    )

    return {
        "status": "OK",
        "confidence": confidence,
        "mode": mode,
        "action": action,
        "message": message,
    }


def summarize_autonomous_decision(
    autonomous_decision
):
    """
    Resume decisão autônoma.
    """

    if not autonomous_decision:
        return (
            "Decisão autônoma indisponível."
        )

    return (
        f"Modo: "
        f"{autonomous_decision.get('mode')}\n"
        f"Confiança: "
        f"{autonomous_decision.get('confidence')}/100\n"
        f"Ação: "
        f"{autonomous_decision.get('action')}\n"
        f"Mensagem: "
        f"{autonomous_decision.get('message')}"
    )