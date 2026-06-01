def detect_changes(current_interfaces, previous_interfaces):

    changes = []

    current_names = {
        item["name"]
        for item in current_interfaces
    }

    previous_names = {
        item["name"]
        for item in previous_interfaces
    }

    added = current_names - previous_names
    removed = previous_names - current_names

    for interface in added:
        changes.append(
            f"Nova interface detectada: {interface}"
        )

    for interface in removed:
        changes.append(
            f"Interface removida: {interface}"
        )

    return changes