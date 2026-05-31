def emergency_check(risk_level):
    if risk_level == "ALTO":
        return {
            "status": "EMERGÊNCIA",
            "action": "ATIVAR PROTOCOLO DE SEGURANÇA"
        }

    return {
        "status": "NORMAL",
        "action": "CONTINUAR OPERAÇÃO"
    }