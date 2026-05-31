import socket
import psutil
from datetime import datetime


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def list_interfaces():
    interfaces = psutil.net_if_addrs()

    print("\nINTERFACES DETECTADAS")
    print("-" * 50)

    for interface_name, interface_addresses in interfaces.items():

        print(f"\nInterface: {interface_name}")

        for address in interface_addresses:

            if address.family == socket.AF_INET:
                print(f"IPv4: {address.address}")


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