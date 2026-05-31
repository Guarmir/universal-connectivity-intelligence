import socket
import psutil
from datetime import datetime

from core.decision_engine.interface_decision import (
    recommend_best_interface,
    explain_recommendation,
)

from core.security_engine.risk_analyzer import analyze_risk
from core.monitor.local_logger import save_log
from core.monitor.history_reader import read_last_logs


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

    elif "vpn" in name_lower:
        return "VPN"

    elif ip.startswith("169.254"):
        return "INVALIDA"

    elif "virtual" in name_lower:
        return "VIRTUAL"

    elif "wi-fi" in name_lower or "wifi" in name_lower:
        return "REAL"

    elif "ethernet" in name_lower:
        return "REAL"

    else:
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

    print("\nINTERFACES DETECTADAS")
    print("-" * 60)

    for interface in interfaces:

        print(f"\nInterface: {interface['name']}")
        print(f"IPv4: {interface['ip']}")
        print(f"Classificação: {interface['classification']}")
        print(f"Trust Score: {interface['trust_score']}/100")

    print("\nRECOMENDAÇÃO DO SISTEMA")
    print("-" * 60)

    recommended = recommend_best_interface(
        interfaces
    )

    print(
        explain_recommendation(
            recommended
        )
    )

    if recommended:

        risk = analyze_risk(
            recommended["trust_score"]
        )

        print("\nANÁLISE DE SEGURANÇA")
        print("-" * 60)
        print(
            f"Nível de risco: {risk['risk_level']}"
        )
        print(
            f"Ação recomendada: {risk['action']}"
        )
        print(
            f"Mensagem: {risk['message']}"
        )
    if recommended:
        save_log(
        f"Recomendação: {recommended['name']} | "
        f"IP: {recommended['ip']} | "
        f"Trust Score: {recommended['trust_score']}/100 | "
        f"Risco: {risk['risk_level']} | "
        f"Ação: {risk['action']}"
    )
        print("\nHISTÓRICO RECENTE")
    print("-" * 60)

    history = read_last_logs(limit=5)

    if history:
        for line in history:
            print(line.strip())
    else:
        print("Nenhum histórico encontrado.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_scan()