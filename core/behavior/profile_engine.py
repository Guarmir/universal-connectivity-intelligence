from core.behavior.behavioral_engine import (
    analyze_behavior,
)


def classify_network_profile(
    averages
):
    """
    Classifica perfil geral da rede.
    """

    if not averages:
        return "DESCONHECIDO"

    values = list(
        averages.values()
    )

    overall_average = (
        sum(values) / len(values)
    )

    if overall_average <= 60:
        return "REDE_ESTAVEL"

    if overall_average <= 120:
        return "REDE_MODERADA"

    return "REDE_INSTAVEL"


def detect_best_period(
    averages
):
    """
    Detecta período mais saudável.
    """

    if not averages:
        return None

    return min(
        averages,
        key=averages.get
    )


def detect_worst_period(
    averages
):
    """
    Detecta período crítico.
    """

    if not averages:
        return None

    return max(
        averages,
        key=averages.get
    )


def build_operational_summary(
    profile_name,
    best_period,
    worst_period,
):
    """
    Monta resumo operacional.
    """

    lines = []

    lines.append(
        f"Perfil operacional: {profile_name}"
    )

    if best_period:
        lines.append(
            f"Horário mais saudável: "
            f"{best_period}"
        )

    if worst_period:
        lines.append(
            f"Horário crítico: "
            f"{worst_period}"
        )

    if (
        best_period
        and worst_period
        and best_period != worst_period
    ):
        lines.append(
            f"Tendência operacional: "
            f"degradação em "
            f"{worst_period}"
        )

    return "\n".join(lines)


def generate_operational_profile():
    """
    Gera perfil operacional inteligente.
    """

    behavior_result = analyze_behavior(
        limit=100
    )

    if (
        not behavior_result
        or behavior_result.get("status")
        != "OK"
    ):
        return {
            "status": "SEM_DADOS",
            "message": (
                "Dados insuficientes "
                "para perfil operacional."
            )
        }

    profile = behavior_result.get(
        "profile",
        {}
    )

    averages = {}

    for period, data in profile.items():

        averages[period] = data.get(
            "average_latency",
            0
        )

    network_profile = (
        classify_network_profile(
            averages
        )
    )

    best_period = detect_best_period(
        averages
    )

    worst_period = detect_worst_period(
        averages
    )

    summary = build_operational_summary(
        network_profile,
        best_period,
        worst_period,
    )

    return {
        "status": "OK",
        "profile_name": network_profile,
        "best_period": best_period,
        "worst_period": worst_period,
        "summary": summary,
        "behavior_data": behavior_result,
    }


def summarize_operational_profile(
    profile_result
):
    """
    Resume perfil operacional.
    """

    if not profile_result:
        return (
            "Perfil operacional indisponível."
        )

    if (
        profile_result.get("status")
        != "OK"
    ):
        return profile_result.get(
            "message",
            "Sem dados operacionais."
        )

    return profile_result.get(
        "summary",
        "Resumo indisponível."
    )