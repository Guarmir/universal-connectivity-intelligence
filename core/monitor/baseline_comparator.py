def compare_with_baseline(
    current_interfaces,
    baseline_interfaces
):

    alerts = []

    baseline_names = {
        item["name"]
        for item in baseline_interfaces
    }

    current_names = {
        item["name"]
        for item in current_interfaces
    }

    new_interfaces = (
        current_names - baseline_names
    )

    missing_interfaces = (
        baseline_names - current_names
    )

    for interface in new_interfaces:
        alerts.append(
            f"NOVA INTERFACE FORA DO BASELINE: "
            f"{interface}"
        )

    for interface in missing_interfaces:
        alerts.append(
            f"INTERFACE AUSENTE DO BASELINE: "
            f"{interface}"
        )

    return alerts