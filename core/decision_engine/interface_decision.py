def recommend_best_interface(interfaces):
    if not interfaces:
        return None

    sorted_interfaces = sorted(
        interfaces,
        key=lambda item: item["trust_score"],
        reverse=True
    )

    return sorted_interfaces[0]


def explain_recommendation(interface):
    if interface is None:
        return "Nenhuma interface disponível para recomendação."

    return (
        f"Interface recomendada: {interface['name']} | "
        f"IP: {interface['ip']} | "
        f"Classificação: {interface['classification']} | "
        f"Trust Score: {interface['trust_score']}/100"
    )