from core.monitor.history_reader import (
    read_last_logs,
)


def detect_recurrent_patterns(
    limit=50
):
    """
    Detecta padrões recorrentes
    no histórico operacional.
    """

    logs = read_last_logs(limit=limit)

    if not logs:
        return {
            "patterns": [],
            "message": (
                "Histórico insuficiente."
            )
        }

    occurrences = {
        "PREVENTIVO": 0,
        "CRITICO": 0,
        "AUTONOMIA_NORMAL": 0,
        "INTERVENCAO_RECOMENDADA": 0,
        "FAILOVER": 0,
        "REDE_ESTAVEL": 0,
    }

    for line in logs:

        if "PREPARAR_FAILOVER" in line:
            occurrences["FAILOVER"] += 1

        if "Prevenção: CRITICO" in line:
            occurrences["CRITICO"] += 1

        if "Prevenção: BAIXO" in line:
            occurrences["PREVENTIVO"] += 1

        if "Autonomia: AUTONOMIA_NORMAL" in line:
            occurrences["AUTONOMIA_NORMAL"] += 1

        if "Autonomia: INTERVENCAO_RECOMENDADA" in line:
            occurrences["INTERVENCAO_RECOMENDADA"] += 1

        if "Perfil Operacional: REDE_ESTAVEL" in line:
            occurrences["REDE_ESTAVEL"] += 1

    patterns = []

    for key, value in occurrences.items():

        if value > 0:
            patterns.append({
                "pattern": key,
                "occurrences": value,
            })

    patterns.sort(
        key=lambda item: item["occurrences"],
        reverse=True
    )

    return {
        "patterns": patterns,
        "message": (
            "Padrões operacionais identificados."
        )
    }


def calculate_operational_learning(
    patterns_result
):
    """
    Calcula maturidade operacional
    baseada nos padrões históricos.
    """

    patterns = patterns_result.get(
        "patterns",
        []
    )

    if not patterns:
        return 0

    score = 0

    for pattern in patterns:

        pattern_name = pattern["pattern"]
        occurrences = pattern["occurrences"]

        if pattern_name == "AUTONOMIA_NORMAL":
            score += occurrences * 5

        elif pattern_name == "REDE_ESTAVEL":
            score += occurrences * 4

        elif pattern_name == "PREVENTIVO":
            score += occurrences * 3

        elif pattern_name == "FAILOVER":
            score += occurrences * 2

        elif pattern_name == "CRITICO":
            score -= occurrences * 4

        elif pattern_name == "INTERVENCAO_RECOMENDADA":
            score -= occurrences * 5

    if score < 0:
        score = 0

    if score > 100:
        score = 100

    return score


def generate_learning_status(
    learning_score
):
    """
    Define status de aprendizado.
    """

    if learning_score >= 80:
        return "ALTA_MATURIDADE_OPERACIONAL"

    if learning_score >= 60:
        return "BOA_MATURIDADE_OPERACIONAL"

    if learning_score >= 40:
        return "MATURIDADE_MODERADA"

    if learning_score >= 20:
        return "BAIXA_MATURIDADE_OPERACIONAL"

    return "APRENDIZADO_INICIAL"


def generate_learning_analysis(
    limit=50
):
    """
    Gera análise completa de aprendizado.
    """

    patterns_result = detect_recurrent_patterns(
        limit=limit
    )

    learning_score = calculate_operational_learning(
        patterns_result
    )

    learning_status = generate_learning_status(
        learning_score
    )

    return {
        "score": learning_score,
        "status": learning_status,
        "patterns": patterns_result.get(
            "patterns",
            []
        ),
        "message": patterns_result.get(
            "message"
        ),
    }


def summarize_learning(
    learning_result
):
    """
    Resume aprendizado operacional.
    """

    if not learning_result:
        return (
            "Sistema de aprendizado indisponível."
        )

    lines = [
        f"Status: "
        f"{learning_result.get('status')}",

        f"Learning Score: "
        f"{learning_result.get('score')}/100",

        learning_result.get(
            "message",
            ""
        )
    ]

    patterns = learning_result.get(
        "patterns",
        []
    )

    if patterns:

        lines.append(
            "\nPadrões identificados:"
        )

        for pattern in patterns[:5]:

            lines.append(
                f"- {pattern['pattern']}: "
                f"{pattern['occurrences']} ocorrência(s)"
            )

    return "\n".join(lines)