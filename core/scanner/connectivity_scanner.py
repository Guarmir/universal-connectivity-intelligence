import socket
import psutil
from datetime import datetime

from core.decision_engine.intelligence_score import (
    calculate_intelligence_score,
)

from core.decision_engine.contextual_decision import (
    recommend_contextual_interface,
    calculate_contextual_score,
    build_decision_reason,
)

from core.decision_engine.interface_filter import (
    filter_operational_interfaces,
)

from core.security_engine.risk_analyzer import analyze_risk
from core.emergency_control.emergency_controller import emergency_check
from core.failover.failover_engine import evaluate_failover

from core.monitor.local_logger import save_log
from core.monitor.history_reader import read_last_logs
from core.monitor.stability_engine import calculate_stability_score

from core.monitor.intelligent_baseline import (
    compare_with_intelligent_baseline,
)

from core.monitor.anomaly_detector import (
    detect_operational_anomalies,
    summarize_anomalies,
)

from core.monitor.degradation_engine import (
    analyze_degradation,
    summarize_degradation,
)

from core.monitor.predictive_engine import (
    predict_operational_risk,
    summarize_prediction,
)

from core.quality.connectivity_quality import (
    measure_latency,
    classify_latency,
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


def enrich_interfaces_with_intelligence(interfaces):
    latency = measure_latency()
    latency_quality = classify_latency(latency)

    enriched = []

    for interface in interfaces:
        risk = analyze_risk(
            interface["trust_score"]
        )

        stability_score = calculate_stability_score(
            interface["name"]
        )

        intelligence_score = calculate_intelligence_score(
            interface["trust_score"],
            stability_score,
            latency_quality,
        )

        interface["risk_level"] = risk["risk_level"]
        interface["risk_action"] = risk["action"]
        interface["risk_message"] = risk["message"]
        interface["stability_score"] = stability_score
        interface["latency_ms"] = latency
        interface["quality"] = latency_quality
        interface["intelligence_score"] = intelligence_score

        contextual_score = calculate_contextual_score(
            interface
        )

        interface["contextual_score"] = contextual_score

        interface["decision_reason"] = build_decision_reason(
            interface,
            contextual_score
        )

        interface["anomalies"] = detect_operational_anomalies(
            interface
        )

        enriched.append(interface)

    enriched.sort(
        key=lambda item: item["contextual_score"],
        reverse=True
    )

    return enriched


def print_detected_interfaces(interfaces):
    print("\nINTERFACES DETECTADAS")
    print("-" * 60)

    for interface in interfaces:
        print(f"\nInterface: {interface['name']}")
        print(f"IPv4: {interface['ip']}")
        print(f"Classificação: {interface['classification']}")
        print(f"Trust Score: {interface['trust_score']}/100")


def print_baseline_status(baseline_alerts):
    print("\nBASELINE INTELIGENTE")
    print("-" * 60)

    if baseline_alerts:
        for alert in baseline_alerts:
            print(
                f"[{alert['severity']}] "
                f"{alert['message']}"
            )
    else:
        print("Ambiente compatível com o baseline.")


def print_operational_ranking(enriched_interfaces):
    print("\nRANKING OPERACIONAL")
    print("-" * 60)

    for position, interface in enumerate(
        enriched_interfaces,
        start=1
    ):
        print(
            f"{position}. "
            f"{interface['name']} | "
            f"Score: {interface['contextual_score']}/100 | "
            f"Risco: {interface['risk_level']}"
        )


def print_recommendation(recommended):
    print("\nRECOMENDAÇÃO CONTEXTUAL")
    print("-" * 60)

    print(f"Interface: {recommended['name']}")
    print(f"IP: {recommended['ip']}")
    print(
        f"Contextual Score: "
        f"{recommended['contextual_score']}/100"
    )
    print(f"Motivos: {recommended['decision_reason']}")


def print_anomaly_status(recommended):
    print("\nANOMALIAS OPERACIONAIS")
    print("-" * 60)

    anomalies = recommended.get("anomalies", [])

    print(
        summarize_anomalies(
            anomalies
        )
    )


def print_degradation_status():
    print("\nDEGRADAÇÃO HISTÓRICA")
    print("-" * 60)

    degradation_result = analyze_degradation(
        limit=10
    )

    print(
        summarize_degradation(
            degradation_result
        )
    )


def print_prediction_status():
    print("\nPREVISÃO OPERACIONAL")
    print("-" * 60)

    prediction_result = predict_operational_risk()

    print(
        summarize_prediction(
            prediction_result
        )
    )


def print_security_status(risk):
    print("\nANÁLISE DE SEGURANÇA")
    print("-" * 60)
    print(f"Risco: {risk['risk_level']}")
    print(f"Ação: {risk['action']}")
    print(f"Mensagem: {risk['message']}")


def print_quality_status(recommended):
    print("\nESTABILIDADE")
    print("-" * 60)
    print(f"{recommended['stability_score']}/100")

    print("\nQUALIDADE")
    print("-" * 60)
    print(
        f"Latência: "
        f"{recommended['latency_ms']} ms"
    )
    print(f"Qualidade: {recommended['quality']}")

    print("\nINTELLIGENCE SCORE")
    print("-" * 60)
    print(f"{recommended['intelligence_score']}/100")


def print_emergency_status(emergency):
    print("\nCONTROLE DE EMERGÊNCIA")
    print("-" * 60)
    print(f"Status: {emergency['status']}")
    print(f"Ação: {emergency['action']}")


def print_failover_status(failover):
    print("\nFAILOVER")
    print("-" * 60)
    print(f"Status: {failover['status']}")
    print(f"Ação: {failover['action']}")
    print(f"Mensagem: {failover['message']}")


def print_history():
    print("\nHISTÓRICO RECENTE")
    print("-" * 60)

    history = read_last_logs(
        limit=5
    )

    if history:
        for line in history:
            print(line.strip())
    else:
        print("Nenhum histórico encontrado.")


def save_recommendation_log(recommended, risk):
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
        f"Ação: {risk['action']}"
    )


def run_scan():
    print("=" * 60)
    print("INTELIGÊNCIA UNIVERSAL DE CONECTIVIDADE")
    print("=" * 60)

    print(f"Data/Hora: {datetime.now()}")

    if check_internet():
        print("Status: INTERNET DISPONÍVEL")
    else:
        print("Status: SEM INTERNET")

    interfaces = collect_interfaces()

    print_detected_interfaces(
        interfaces
    )

    baseline_alerts = compare_with_intelligent_baseline(
        interfaces
    )

    operational_interfaces = filter_operational_interfaces(
        interfaces
    )

    enriched_interfaces = enrich_interfaces_with_intelligence(
        operational_interfaces
    )

    recommended = recommend_contextual_interface(
        enriched_interfaces
    )

    print_baseline_status(
        baseline_alerts
    )

    print_operational_ranking(
        enriched_interfaces
    )

    if not recommended:
        print("\nRECOMENDAÇÃO CONTEXTUAL")
        print("-" * 60)
        print("Nenhuma interface operacional disponível.")

        print_history()
        print("\n" + "=" * 60)
        return

    risk = {
        "risk_level": recommended["risk_level"],
        "action": recommended["risk_action"],
        "message": recommended["risk_message"],
    }

    emergency = emergency_check(
        risk["risk_level"]
    )

    failover = evaluate_failover(
        recommended,
        risk
    )

    print_recommendation(
        recommended
    )

    print_anomaly_status(
        recommended
    )

    print_degradation_status()

    print_prediction_status()

    print_security_status(
        risk
    )

    print_quality_status(
        recommended
    )

    print_emergency_status(
        emergency
    )

    print_failover_status(
        failover
    )

    save_recommendation_log(
        recommended,
        risk
    )

    print_history()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_scan()