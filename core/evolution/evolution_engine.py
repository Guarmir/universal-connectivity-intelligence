from core.monitor.history_reader import (
    read_last_logs,
)


def analyze_decision_evolution(
    limit=50
):
    """
    Analisa evolução das decisões
    operacionais.
    """

    logs = read_last_logs(limit=limit)

    if not logs:
        return {
            "evolution_score": 0,
            "status": "SEM_HISTORICO",
            "adaptation_level": "DESCONHECIDO",
            "message": (
                "Histórico insuficiente."
            )
        }

    autonomy_normal = 0
    intervention = 0
    preventive_low = 0
    preventive_critical = 0
    stable_operations = 0

    for line in logs:

        if "AUTONOMIA_NORMAL" in line:
            autonomy_normal += 1

        if "INTERVENCAO_RECOMENDADA" in line:
            intervention += 1

        if "Prevenção: BAIXO" in line:
            preventive_low += 1

        if "Prevenção: CRITICO" in line:
            preventive_critical += 1

        if (
            "Qualidade: EXCELENTE" in line
            or "Qualidade: BOA" in line
        ):
            stable_operations += 1

    evolution_score = 50

    evolution_score += autonomy_normal * 5
    evolution_score += preventive_low * 3
    evolution_score += stable_operations * 2

    evolution_score -= intervention * 8
    evolution_score -= preventive_critical * 10

    if evolution_score > 100:
        evolution_score = 100

    if evolution_score < 0:
        evolution_score = 0

    if evolution_score >= 80:
        status = "EVOLUCAO_AVANCADA"
        adaptation_level = "ALTAMENTE_ADAPTATIVO"

    elif evolution_score >= 60:
        status = "EVOLUCAO_ESTAVEL"
        adaptation_level = "ADAPTATIVO"

    elif evolution_score >= 40:
        status = "EVOLUCAO_MODERADA"
        adaptation_level = "PARCIALMENTE_ADAPTATIVO"

    else:
        status = "EVOLUCAO_LIMITADA"
        adaptation_level = "BAIXA_ADAPTACAO"

    return {
        "evolution_score": evolution_score,
        "status": status,
        "adaptation_level": adaptation_level,
        "autonomy_normal": autonomy_normal,
        "intervention": intervention,
        "preventive_low": preventive_low,
        "preventive_critical": preventive_critical,
        "stable_operations": stable_operations,
        "message": (
            "Sistema de evolução decisional ativo."
        )
    }


def summarize_evolution(
    evolution_result
):
    """
    Resume evolução operacional.
    """

    if not evolution_result:
        return (
            "Sistema evolutivo indisponível."
        )

    return (
        f"Status: "
        f"{evolution_result.get('status')}\n"

        f"Nível Adaptativo: "
        f"{evolution_result.get('adaptation_level')}\n"

        f"Evolution Score: "
        f"{evolution_result.get('evolution_score')}/100\n"

        f"Autonomia Normal: "
        f"{evolution_result.get('autonomy_normal')}\n"

        f"Intervenções: "
        f"{evolution_result.get('intervention')}\n"

        f"Operações Estáveis: "
        f"{evolution_result.get('stable_operations')}\n"

        f"Mensagem: "
        f"{evolution_result.get('message')}"
    )