from collections import defaultdict


def analyze_multi_network(enriched_interfaces):
    if not enriched_interfaces:
        return {
            "status": "SEM_INTERFACES",
            "best_interface": None,
            "interface_count": 0,
            "network_diversity": "BAIXA",
            "message": (
                "Nenhuma interface operacional disponível."
            )
        }

    interface_count = len(enriched_interfaces)

    interface_scores = {}

    for interface in enriched_interfaces:

        interface_scores[
            interface["name"]
        ] = interface.get(
            "contextual_score",
            0
        )

    best_interface = max(
        interface_scores,
        key=interface_scores.get
    )

    diversity_map = defaultdict(int)

    for interface in enriched_interfaces:

        diversity_map[
            interface["classification"]
        ] += 1

    diversity_count = len(
        diversity_map
    )

    if diversity_count >= 3:
        network_diversity = "ALTA"

    elif diversity_count == 2:
        network_diversity = "MEDIA"

    else:
        network_diversity = "BAIXA"

    return {
        "status": "MULTI_NETWORK_ATIVO",
        "best_interface": best_interface,
        "interface_count": interface_count,
        "network_diversity": network_diversity,
        "message": (
            "Motor multi-rede ativo."
        )
    }


def summarize_multi_network(
    result
):
    return (
        f"Status: "
        f"{result['status']}\n"
        f"Melhor Interface: "
        f"{result['best_interface']}\n"
        f"Interfaces Detectadas: "
        f"{result['interface_count']}\n"
        f"Diversidade de Rede: "
        f"{result['network_diversity']}\n"
        f"Mensagem: "
        f"{result['message']}"
    )