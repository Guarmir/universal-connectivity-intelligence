ALLOWED_CLASSES = [
    "REAL",
    "VPN",
]


def is_operational_interface(interface_data):
    """
    Determina se a interface pode ser usada
    operacionalmente.
    """

    classification = interface_data.get(
        "classification",
        ""
    )

    return classification in ALLOWED_CLASSES


def filter_operational_interfaces(
    interfaces
):
    """
    Remove interfaces não operacionais.
    """

    return [
        interface
        for interface in interfaces
        if is_operational_interface(interface)
    ]