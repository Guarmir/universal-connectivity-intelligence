import socket
import time


def measure_latency(
    host="8.8.8.8",
    port=53,
    timeout=3
):

    try:

        start = time.time()

        socket.create_connection(
            (host, port),
            timeout=timeout
        )

        latency = (
            time.time() - start
        ) * 1000

        return round(latency, 2)

    except Exception:
        return None


def classify_latency(latency):

    if latency is None:
        return "SEM RESPOSTA"

    if latency <= 50:
        return "EXCELENTE"

    if latency <= 100:
        return "BOA"

    if latency <= 200:
        return "RUIM"

    return "CRÍTICA"