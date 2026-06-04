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
    print_recommendation,
    print_no_recommendation,
    print_anomaly_status,
    print_degradation_status,
    print_prediction_status,
    print_security_status,
    print_quality_status,
    print_emergency_status,
    print_failover_status,
    print_adaptive_failover_status,
    print_history,
    print_footer,
)


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
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

    if "wi-fi" in name_lower or "wifi" in name_lower:
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

    return scores.get(classification, 0)


def collect_interfaces():
    interfaces = psutil.net_if_addrs()
    collected = []

    for interface_name, interface_addresses in interfaces.items():
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
    recommended = analysis.get("recommended")
    risk = analysis.get("risk")
    adaptive_failover = analysis.get("adaptive_failover")

    if not recommended or not risk or not adaptive_failover:
        return

    save_log(
        f"Recomendação Contextual: "
        f"{recommended['name']} | "
        f"IP: {recommended['ip']} | "
        f"Score: {recommended['contextual_score']}/100 | "
        f"Intelligence Score: "
        f"{recommended['intelligence_score']}/100 | "
        f"Estabilidade: "
        f"{recommended['stability_score']}/100 | "
        f"Latência: {recommended['latency_ms']} ms | "
        f"Qualidade: {recommended['quality']} | "
        f"Risco: {risk['risk_level']} | "
        f"Ação: {risk['action']} | "
        f"Adaptive Failover: {adaptive_failover['action']}"
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

    recommended = analysis.get("recommended")

    if not recommended:
        print_no_recommendation()
        print_history()
        print_footer()
        return

    print_recommendation(
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
    print(f"Data/Hora: {datetime.now()}")

    if check_internet():
        print("Status: INTERNET DISPONÍVEL")
    else:
        print("Status: SEM INTERNET")

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