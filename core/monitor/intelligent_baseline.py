from core.monitor.baseline_engine import load_baseline


def compare_with_intelligent_baseline(current_interfaces):
    """
    Compara as interfaces atuais com o baseline salvo
    e detecta mudanças operacionais relevantes.
    """

    baseline = load_baseline()
    alerts = []

    if not baseline:
        alerts.append({
            "type": "BASELINE_AUSENTE",
            "severity": "MÉDIA",
            "message": "Nenhum baseline encontrado para comparação."
        })
        return alerts

    baseline_map = {}

    for item in baseline:
        name = item.get("name")
        if name:
            baseline_map[name] = item

    current_map = {}

    for item in current_interfaces:
        name = item.get("name")
        if name:
            current_map[name] = item

    for name, current in current_map.items():
        if name not in baseline_map:
            alerts.append({
                "type": "NOVA_INTERFACE",
                "severity": "MÉDIA",
                "interface": name,
                "message": f"Nova interface detectada: {name}"
            })
            continue

        baseline_item = baseline_map[name]

        if current.get("ip") != baseline_item.get("ip"):
            alerts.append({
                "type": "IP_ALTERADO",
                "severity": "MÉDIA",
                "interface": name,
                "message": (
                    f"IP alterado na interface {name}: "
                    f"{baseline_item.get('ip')} -> {current.get('ip')}"
                )
            })

        if current.get("classification") != baseline_item.get("classification"):
            alerts.append({
                "type": "CLASSIFICACAO_ALTERADA",
                "severity": "ALTA",
                "interface": name,
                "message": (
                    f"Classificação alterada na interface {name}: "
                    f"{baseline_item.get('classification')} -> "
                    f"{current.get('classification')}"
                )
            })

        if current.get("trust_score") != baseline_item.get("trust_score"):
            alerts.append({
                "type": "TRUST_SCORE_ALTERADO",
                "severity": "BAIXA",
                "interface": name,
                "message": (
                    f"Trust Score alterado na interface {name}: "
                    f"{baseline_item.get('trust_score')} -> "
                    f"{current.get('trust_score')}"
                )
            })

    for name in baseline_map:
        if name not in current_map:
            alerts.append({
                "type": "INTERFACE_REMOVIDA",
                "severity": "ALTA",
                "interface": name,
                "message": f"Interface do baseline não encontrada agora: {name}"
            })

    return alerts


def summarize_baseline_alerts(alerts):
    """
    Gera resumo textual dos alertas de baseline.
    """

    if not alerts:
        return "Ambiente compatível com o baseline."

    summary = []

    for alert in alerts:
        severity = alert.get("severity", "INDEFINIDA")
        message = alert.get("message", "Alerta sem mensagem.")
        summary.append(f"[{severity}] {message}")

    return "\n".join(summary)