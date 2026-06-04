from core.decision_engine.decision_weights import (
    INTELLIGENCE_WEIGHT,
    STABILITY_WEIGHT,
    LATENCY_WEIGHT,
    QUALITY_WEIGHT,
    TRUST_WEIGHT,
)


def normalize_latency(latency_ms):
    if latency_ms is None:
        return 0

    try:
        latency_ms = float(latency_ms)
    except (ValueError, TypeError):
        return 0

    if latency_ms <= 50:
        return 100
    elif latency_ms <= 100:
        return 85
    elif latency_ms <= 150:
        return 70
    elif latency_ms <= 250:
        return 50
    elif latency_ms <= 400:
        return 30
    else:
        return 10


def normalize_quality(quality):
    if not quality:
        return 0

    quality = str(quality).upper()

    if quality == "EXCELENTE":
        return 100
    elif quality == "BOA":
        return 80
    elif quality == "REGULAR":
        return 55
    elif quality == "RUIM":
        return 30
    else:
        return 40


def calculate_contextual_score(interface_data):
    intelligence_score = interface_data.get(
        "intelligence_score",
        0
    ) or 0

    stability_score = interface_data.get(
        "stability_score",
        0
    ) or 0

    latency_score = normalize_latency(
        interface_data.get("latency_ms")
    )

    quality_score = normalize_quality(
        interface_data.get("quality")
    )

    trust_score = interface_data.get(
        "trust_score",
        0
    ) or 0

    final_score = (
        intelligence_score * INTELLIGENCE_WEIGHT
        + stability_score * STABILITY_WEIGHT
        + latency_score * LATENCY_WEIGHT
        + quality_score * QUALITY_WEIGHT
        + trust_score * TRUST_WEIGHT
    )

    return round(final_score, 2)


def build_decision_reason(interface_data, final_score):
    reasons = []

    if interface_data.get("intelligence_score", 0) >= 80:
        reasons.append("alto intelligence score")

    if interface_data.get("stability_score", 0) >= 80:
        reasons.append("boa estabilidade histórica")

    latency_ms = interface_data.get("latency_ms")

    if latency_ms is not None:
        try:
            if float(latency_ms) <= 150:
                reasons.append("latência aceitável")
            else:
                reasons.append("latência elevada")
        except (ValueError, TypeError):
            reasons.append("latência indisponível")

    quality = str(
        interface_data.get("quality", "")
    ).upper()

    if quality in ["EXCELENTE", "BOA"]:
        reasons.append("boa qualidade de conexão")
    elif quality:
        reasons.append("qualidade de conexão limitada")

    if interface_data.get("trust_score", 0) >= 70:
        reasons.append("trust score confiável")

    risk = str(
        interface_data.get("risk_level", "")
    ).upper()

    if risk == "ALTO":
        reasons.append("atenção: risco alto detectado")
    elif risk == "MÉDIO":
        reasons.append("risco moderado detectado")
    elif risk == "BAIXO":
        reasons.append("baixo risco operacional")

    if not reasons:
        reasons.append("dados suficientes para decisão operacional")

    return ", ".join(reasons)


def recommend_contextual_interface(interfaces):
    if not interfaces:
        return None

    ranked_interfaces = []

    for interface in interfaces:
        final_score = calculate_contextual_score(interface)
        interface["contextual_score"] = final_score
        interface["decision_reason"] = build_decision_reason(
            interface,
            final_score
        )
        ranked_interfaces.append(interface)

    ranked_interfaces.sort(
        key=lambda item: item.get("contextual_score", 0),
        reverse=True
    )

    return ranked_interfaces[0]