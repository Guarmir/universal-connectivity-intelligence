import socket
from datetime import datetime


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False


def get_local_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "IP não encontrado"


def run_scan():
    print("=" * 50)
    print("INTELIGÊNCIA UNIVERSAL DE CONECTIVIDADE")
    print("=" * 50)

    print(f"Data/Hora: {datetime.now()}")
    print(f"IP Local: {get_local_ip()}")

    if check_internet():
        print("Status: INTERNET DISPONÍVEL")
    else:
        print("Status: SEM INTERNET")

    print("=" * 50)


if __name__ == "__main__":
    run_scan()