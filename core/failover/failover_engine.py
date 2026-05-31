def evaluate_failover(recommended_interface, risk):
    if recommended_interface is None:
        return {
            "status": "SEM INTERFACE",
            "action": "AGUARDAR NOVA CONEXÃO",
            "message": "Nenhuma interface disponível para failover."
        }

    trust_score = recommended_interface["trust_score"]
    risk_level = risk["risk_level"]

    if risk_level == "BLOQUEADA":
        return {
            "status": "BLOQUEADO",
            "action": "NÃO TROCAR",
            "message": "A interface recomendada foi bloqueada por segurança."
        }

    if trust_score >= 80:
        return {
            "status": "ESTÁVEL",
            "action": "MANTER CONEXÃO",
            "message": "A conexão atual parece estável e confiável."
        }

    if trust_score >= 50:
        return {
            "status": "MONITORAR",
            "action": "PREPARAR TROCA",
            "message": "A conexão pode ser usada, mas exige monitoramento."
        }

    return {
        "status": "INSTÁVEL",
        "action": "TROCA RECOMENDADA",
        "message": "A conexão não parece confiável. Recomenda-se buscar alternativa."
    }