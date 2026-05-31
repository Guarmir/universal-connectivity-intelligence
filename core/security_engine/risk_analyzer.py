def analyze_risk(trust_score):
    if trust_score >= 80:
        return {
            "risk_level": "BAIXO",
            "action": "PERMITIR",
            "message": "Interface confiável para uso normal."
        }

    if trust_score >= 50:
        return {
            "risk_level": "MÉDIO",
            "action": "MONITORAR",
            "message": "Interface utilizável, mas deve ser monitorada."
        }

    if trust_score > 0:
        return {
            "risk_level": "ALTO",
            "action": "EVITAR",
            "message": "Interface de alto risco. Evite uso automático."
        }

    return {
        "risk_level": "BLOQUEADA",
        "action": "BLOQUEAR",
        "message": "Interface inválida ou insegura para uso."
    }