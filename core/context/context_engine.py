from datetime import datetime

from core.monitor.history_reader import (
    read_last_logs,
)


def detect_operational_context():
    """
    Detecta contexto operacional atual.
    """

    current_hour = datetime.now().hour

    if 0 <= current_hour < 6:
        return {
            "context": "MADRUGADA",
            "risk_modifier": -5,
            "description": (
                "Ambiente normalmente menos congestionado."
            )
        }

    if 6 <= current_hour < 12:
        return {
            "context": "MANHA",
            "risk_modifier": -10,
            "description": (
                "Horário operacional mais saudável."
            )
        }

    if 12 <= current_hour < 18:
        return {
            "context": "TARDE",
            "risk_modifier": 0,
            "description": (
                "Ambiente operacional moderado."
            )
        }

    return {
        "context": "NOITE",
        "risk_modifier": 10,
        "description": (
            "Horário com maior tendência de degradação."
        )
    }


def analyze_contextual_history(
    limit=50
):
    """
    Analisa histórico baseado em contexto.
    """

    logs = read_last_logs(limit=limit)

    if not logs:
        return {
            "healthy_contexts": [],
            "critical_contexts": [],
        }

    healthy = {
        "MADRUGADA": 0,
        "MANHA": 0,
        "TARDE": 0,
        "NOITE": 0,
    }

    critical = {
        "MADRUGADA": 0,
        "MANHA": 0,
        "TARDE": 0,
        "NOITE": 0,
    }

    for line in logs:

        for context in healthy.keys():

            if context in line:

                if (
                    "Qualidade: EXCELENTE" in line
                    or "AUTONOMIA_NORMAL" in line
                ):
                    healthy[context] += 1

                if (
                    "INTERVENCAO_RECOMENDADA" in line
                    or "CRITICO" in line
                ):
                    critical[context] += 1

    return {
        "healthy_contexts": healthy,
        "critical_contexts": critical,
    }


def generate_context_awareness(
    limit=50
):
    """
    Gera consciência contextual.
    """

    current_context = detect_operational_context()

    contextual_history = analyze_contextual_history(
        limit=limit
    )

    current_name = current_context["context"]

    healthy_count = contextual_history[
        "healthy_contexts"
    ].get(current_name, 0)

    critical_count = contextual_history[
        "critical_contexts"
    ].get(current_name, 0)

    awareness_score = 50

    awareness_score += healthy_count * 5
    awareness_score -= critical_count * 10

    if awareness_score > 100:
        awareness_score = 100

    if awareness_score < 0:
        awareness_score = 0

    if awareness_score >= 80:
        status = "CONTEXTO_ALTAMENTE_CONFIAVEL"

    elif awareness_score >= 60:
        status = "CONTEXTO_ESTAVEL"

    elif awareness_score >= 40:
        status = "CONTEXTO_MODERADO"

    else:
        status = "CONTEXTO_INSTAVEL"

    return {
        "current_context": current_name,
        "description": current_context[
            "description"
        ],
        "risk_modifier": current_context[
            "risk_modifier"
        ],
        "awareness_score": awareness_score,
        "status": status,
        "healthy_occurrences": healthy_count,
        "critical_occurrences": critical_count,
    }


def summarize_context_awareness(
    context_result
):
    """
    Resume consciência contextual.
    """

    if not context_result:
        return (
            "Sistema contextual indisponível."
        )

    return (
        f"Contexto Atual: "
        f"{context_result.get('current_context')}\n"

        f"Status: "
        f"{context_result.get('status')}\n"

        f"Awareness Score: "
        f"{context_result.get('awareness_score')}/100\n"

        f"Ocorrências Saudáveis: "
        f"{context_result.get('healthy_occurrences')}\n"

        f"Ocorrências Críticas: "
        f"{context_result.get('critical_occurrences')}\n"

        f"Descrição: "
        f"{context_result.get('description')}"
    )