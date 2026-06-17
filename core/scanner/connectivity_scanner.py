import socket
import psutil
from datetime import datetime

from core.monitor.local_logger import save_log

from core.scanner.scanner_analysis import (
    execute_operational_analysis,
)

from core.scanner.scanner_output import (
    print_header,
    print_detected_interfaces,
    print_baseline_status,
    print_operational_ranking,
    print_multi_network_status,
    print_recommendation,
    print_no_recommendation,
    print_anomaly_status,
    print_degradation_status,
    print_prediction_status,
    print_behavior_status,
    print_operational_profile_status,
    print_autonomous_status,
    print_preventive_status,
    print_self_healing_status,
    print_learning_status,
    print_context_status,
    print_evolution_status,
    print_security_status,
    print_quality_status,
    print_emergency_status,
    print_failover_status,
    print_adaptive_failover_status,
    print_history,
    print_footer,
    print_reputation_status,
)


def check_internet():
    try:
        socket.create_connection(
            ("8.8.8.8", 53),
            timeout=3
        )
        return True

    except OSError:
        return False


def classify_interface(name, ip):
    name_lower = name.lower()

    if "loopback" in name_lower:
        return "LOOPBACK"

    if "vpn" in name_lower:
        return "VPN"

    if ip.startswith("169.254"):
        return "INVALIDA"

    if "virtual" in name_lower:
        return "VIRTUAL"

    if (
        "wi-fi" in name_lower
        or "wifi" in name_lower
    ):
        return "REAL"

    if "ethernet" in name_lower:
        return "REAL"

    return "DESCONHECIDA"


def calculate_trust_score(classification):
    scores = {
        "REAL": 80,
        "VPN": 60,
        "VIRTUAL": 40,
        "DESCONHECIDA": 30,
        "LOOPBACK": 10,
        "INVALIDA": 0,
    }

    return scores.get(
        classification,
        0
    )


def collect_interfaces():
    interfaces = psutil.net_if_addrs()

    collected = []

    for (
        interface_name,
        interface_addresses
    ) in interfaces.items():

        for address in interface_addresses:

            if address.family == socket.AF_INET:

                classification = classify_interface(
                    interface_name,
                    address.address
                )

                trust_score = calculate_trust_score(
                    classification
                )

                collected.append({
                    "name": interface_name,
                    "ip": address.address,
                    "classification": classification,
                    "trust_score": trust_score,
                })

    return collected


def save_recommendation_log(analysis):
    recommended = analysis.get(
        "recommended"
    )

    risk = analysis.get(
        "risk"
    )

    adaptive_failover = analysis.get(
        "adaptive_failover"
    )

    operational_profile = analysis.get(
        "operational_profile"
    )

    autonomous_decision = analysis.get(
        "autonomous_decision"
    )

    preventive_recommendation = analysis.get(
        "preventive_recommendation"
    )

    self_healing_result = analysis.get(
        "self_healing_result"
    )

    learning_result = analysis.get(
        "learning_result"
    )

    context_result = analysis.get(
        "context_result"
    )

    evolution_result = analysis.get(
        "evolution_result"
    )

    if (
        not recommended
        or not risk
        or not adaptive_failover
    ):
        return

    profile_name = "DESCONHECIDO"
    autonomous_mode = "DESCONHECIDO"
    autonomous_confidence = 0
    preventive_level = "DESCONHECIDO"
    preventive_action = "DESCONHECIDO"
    self_healing_status = "DESCONHECIDO"
    self_healing_action = "DESCONHECIDO"
    learning_status = "DESCONHECIDO"
    learning_score = 0
    context_status = "DESCONHECIDO"
    context_score = 0
    evolution_status = "DESCONHECIDO"
    evolution_score = 0

    if operational_profile:
        profile_name = operational_profile.get(
            "profile_name",
            "DESCONHECIDO"
        )

    if autonomous_decision:
        autonomous_mode = autonomous_decision.get(
            "mode",
            "DESCONHECIDO"
        )

        autonomous_confidence = autonomous_decision.get(
            "confidence",
            0
        )

    if preventive_recommendation:
        preventive_level = preventive_recommendation.get(
            "level",
            "DESCONHECIDO"
        )

        preventive_action = preventive_recommendation.get(
            "action",
            "DESCONHECIDO"
        )

    if self_healing_result:
        self_healing_status = self_healing_result.get(
            "status",
            "DESCONHECIDO"
        )

        self_healing_action = self_healing_result.get(
            "action",
            "DESCONHECIDO"
        )

    if learning_result:
        learning_status = learning_result.get(
            "status",
            "DESCONHECIDO"
        )

        learning_score = learning_result.get(
            "score",
            0
        )

    if context_result:
        context_status = context_result.get(
            "status",
            "DESCONHECIDO"
        )

        context_score = context_result.get(
            "awareness_score",
            0
        )

    if evolution_result:
        evolution_status = evolution_result.get(
            "status",
            "DESCONHECIDO"
        )

        evolution_score = evolution_result.get(
            "evolution_score",
            0
        )

    save_log(
        f"Recomendação Contextual: "
        f"{recommended['name']} | "
        f"IP: {recommended['ip']} | "
        f"Score: "
        f"{recommended['contextual_score']}/100 | "
        f"Intelligence Score: "
        f"{recommended['intelligence_score']}/100 | "
        f"Estabilidade: "
        f"{recommended['stability_score']}/100 | "
        f"Latência: "
        f"{recommended['latency_ms']} ms | "
        f"Qualidade: "
        f"{recommended['quality']} | "
        f"Perfil Operacional: "
        f"{profile_name} | "
        f"Autonomia: "
        f"{autonomous_mode} | "
        f"Confiança Autônoma: "
        f"{autonomous_confidence}/100 | "
        f"Prevenção: "
        f"{preventive_level} | "
        f"Ação Preventiva: "
        f"{preventive_action} | "
        f"Self-Healing: "
        f"{self_healing_status} | "
        f"Ação Self-Healing: "
        f"{self_healing_action} | "
        f"Learning: "
        f"{learning_status} | "
        f"Learning Score: "
        f"{learning_score}/100 | "
        f"Contexto: "
        f"{context_status} | "
        f"Awareness Score: "
        f"{context_score}/100 | "
        f"Evolução: "
        f"{evolution_status} | "
        f"Evolution Score: "
        f"{evolution_score}/100 | "
        f"Risco: "
        f"{risk['risk_level']} | "
        f"Ação: "
        f"{risk['action']} | "
        f"Adaptive Failover: "
        f"{adaptive_failover['action']}"
    )


def render_scan_output(analysis):
    print_detected_interfaces(
        analysis["interfaces"]
    )

    print_baseline_status(
        analysis["baseline_alerts"]
    )

    print_operational_ranking(
        analysis["enriched_interfaces"]
    )

    print_multi_network_status(
    analysis["multi_network_result"]
    )

    recommended = analysis.get(
        "recommended"
    )

    if not recommended:
        print_no_recommendation()

        print_autonomous_status(
            analysis["autonomous_decision"]
        )

        print_preventive_status(
            analysis["preventive_recommendation"]
        )

        print_self_healing_status(
            analysis["self_healing_result"]
        )

        print_learning_status(
            analysis["learning_result"]
        )

        print_context_status(
            analysis["context_result"]
        )

        print_evolution_status(
            analysis["evolution_result"]
        )

        print_history()

        print_footer()

        return

    print_recommendation(
    recommended
    )

    print_reputation_status(
    recommended
    )

    print_anomaly_status(
    recommended
    )

    print_degradation_status(
        analysis["degradation_result"]
    )

    print_prediction_status(
        analysis["prediction_result"]
    )

    print_behavior_status(
        analysis["behavior_result"]
    )

    print_operational_profile_status(
        analysis["operational_profile"]
    )

    print_autonomous_status(
        analysis["autonomous_decision"]
    )

    print_preventive_status(
        analysis["preventive_recommendation"]
    )

    print_self_healing_status(
        analysis["self_healing_result"]
    )

    print_learning_status(
        analysis["learning_result"]
    )

    print_context_status(
        analysis["context_result"]
    )

    print_evolution_status(
        analysis["evolution_result"]
    )

    print_security_status(
        analysis["risk"]
    )

    print_quality_status(
        recommended
    )

    print_emergency_status(
        analysis["emergency"]
    )

    print_failover_status(
        analysis["failover"]
    )

    print_adaptive_failover_status(
        analysis["adaptive_failover"]
    )

    print_history()

    print_footer()


def run_scan():
    print_header()

    print(
        f"Data/Hora: "
        f"{datetime.now()}"
    )

    if check_internet():
        print(
            "Status: INTERNET DISPONÍVEL"
        )

    else:
        print(
            "Status: SEM INTERNET"
        )

    interfaces = collect_interfaces()

    analysis = execute_operational_analysis(
        interfaces
    )

    render_scan_output(
        analysis
    )

    save_recommendation_log(
        analysis
    )


if __name__ == "__main__":
    run_scan()