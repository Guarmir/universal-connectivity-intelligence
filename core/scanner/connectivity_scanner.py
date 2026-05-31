import socket
import psutil
from datetime import datetime


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


def list_interfaces():
    interfaces = psutil.net_if_addrs()

    print("\nINTERFACES DETECTADAS")
    print("-" * 60)

    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                classification = classify_interface(
                    interface_name,
                    address.address
                )

                trust_score = calculate_trust_score(classification)

                print(f"\nInterface: {interface_name}")
                print(f"IPv4: {address.address}")
                print(f"Classificação: {classification}")
                print(f"Trust Score: {trust_score}/100")


def run_scan():
    print("=" * 60)
    print("INTELIGÊNCIA UNIVERSAL DE CONECTIVIDADE")
    print("=" * 60)

    print(f"Data/Hora: {datetime.now()}")

    if check_internet():
        print("Status: INTERNET DISPONÍVEL")
    else:
        print("Status: SEM INTERNET")

    list_interfaces()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_scan()