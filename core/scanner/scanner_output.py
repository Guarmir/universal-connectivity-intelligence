from core.monitor.history_reader import read_last_logs

from core.monitor.anomaly_detector import (
    summarize_anomalies,
)

from core.monitor.degradation_engine import (
    summarize_degradation,
)

from core.monitor.predictive_engine import (
    summarize_prediction,
)

from core.behavior.behavioral_engine import (
    summarize_behavior,
)

from core.behavior.profile_engine import (
    summarize_operational_profile,
)

from core.autonomous.autonomous_engine import (
    summarize_autonomous_decision,
)

from core.prevention.preventive_engine import (
    summarize_preventive_recommendation,
)

from core.self_healing.self_healing_engine import (
    summarize_self_healing,
)

from core.learning.learning_engine import (
    summarize_learning,
)

from core.context.context_engine import (
    summarize_context_awareness,
)

from core.evolution.evolution_engine import (
    summarize_evolution,
)


def print_header():
    print("=" * 60)
    print("INTELIGÊNCIA UNIVERSAL DE CONECTIVIDADE")
    print("=" * 60)


def print_section(title):
    print(f"\n{title}")
    print("-" * 60)


def print_detected_interfaces(interfaces):
    print_section("INTERFACES DETECTADAS")

    for interface in interfaces:
        print(f"\nInterface: {interface['name']}")
        print(f"IPv4: {interface['ip']}")
        print(f"Classificação: {interface['classification']}")
        print(f"Trust Score: {interface['trust_score']}/100")


def print_baseline_status(baseline_alerts):
    print_section("BASELINE INTELIGENTE")

    if baseline_alerts:
        for alert in baseline_alerts:
            print(f"[{alert['severity']}] {alert['message']}")
    else:
        print("Ambiente compatível com o baseline.")


def print_operational_ranking(enriched_interfaces):
    print_section("RANKING OPERACIONAL")

    for position, interface in enumerate(
        enriched_interfaces,
        start=1
    ):
        print(
            f"{position}. {interface['name']} | "
            f"Score: {interface['contextual_score']}/100 | "
            f"Risco: {interface['risk_level']}"
        )


def print_recommendation(recommended):
    print_section("RECOMENDAÇÃO CONTEXTUAL")

    print(f"Interface: {recommended['name']}")
    print(f"IP: {recommended['ip']}")
    print(
        f"Contextual Score: "
        f"{recommended['contextual_score']}/100"
    )
    print(
        f"Motivos: "
        f"{recommended['decision_reason']}"
    )


def print_no_recommendation():
    print_section("RECOMENDAÇÃO CONTEXTUAL")
    print(
        "Nenhuma interface operacional disponível."
    )


def print_anomaly_status(recommended):
    print_section("ANOMALIAS OPERACIONAIS")

    anomalies = recommended.get(
        "anomalies",
        []
    )

    print(
        summarize_anomalies(
            anomalies
        )
    )


def print_degradation_status(
    degradation_result
):
    print_section("DEGRADAÇÃO HISTÓRICA")

    print(
        summarize_degradation(
            degradation_result
        )
    )


def print_prediction_status(
    prediction_result
):
    print_section("PREVISÃO OPERACIONAL")

    print(
        summarize_prediction(
            prediction_result
        )
    )


def print_behavior_status(
    behavior_result
):
    print_section("COMPORTAMENTO OPERACIONAL")

    print(
        summarize_behavior(
            behavior_result
        )
    )


def print_operational_profile_status(
    operational_profile
):
    print_section("PERFIL OPERACIONAL")

    print(
        summarize_operational_profile(
            operational_profile
        )
    )


def print_autonomous_status(
    autonomous_decision
):
    print_section("DECISÃO AUTÔNOMA")

    print(
        summarize_autonomous_decision(
            autonomous_decision
        )
    )


def print_preventive_status(
    preventive_recommendation
):
    print_section("AÇÃO PREVENTIVA")

    print(
        summarize_preventive_recommendation(
            preventive_recommendation
        )
    )


def print_self_healing_status(
    self_healing_result
):
    print_section("SELF-HEALING")

    print(
        summarize_self_healing(
            self_healing_result
        )
    )


def print_learning_status(
    learning_result
):
    print_section("APRENDIZADO OPERACIONAL")

    print(
        summarize_learning(
            learning_result
        )
    )


def print_context_status(
    context_result
):
    print_section(
        "CONSCIÊNCIA CONTEXTUAL"
    )

    print(
        summarize_context_awareness(
            context_result
        )
    )


def print_evolution_status(
    evolution_result
):
    print_section(
        "EVOLUÇÃO DECISIONAL"
    )

    print(
        summarize_evolution(
            evolution_result
        )
    )


def print_security_status(risk):
    print_section("ANÁLISE DE SEGURANÇA")

    print(
        f"Risco: "
        f"{risk['risk_level']}"
    )

    print(
        f"Ação: "
        f"{risk['action']}"
    )

    print(
        f"Mensagem: "
        f"{risk['message']}"
    )


def print_quality_status(
    recommended
):
    print_section("ESTABILIDADE")

    print(
        f"{recommended['stability_score']}/100"
    )

    print_section("QUALIDADE")

    print(
        f"Latência: "
        f"{recommended['latency_ms']} ms"
    )

    print(
        f"Qualidade: "
        f"{recommended['quality']}"
    )

    print_section(
        "INTELLIGENCE SCORE"
    )

    print(
        f"{recommended['intelligence_score']}/100"
    )


def print_emergency_status(
    emergency
):
    print_section(
        "CONTROLE DE EMERGÊNCIA"
    )

    print(
        f"Status: "
        f"{emergency['status']}"
    )

    print(
        f"Ação: "
        f"{emergency['action']}"
    )


def print_failover_status(
    failover
):
    print_section("FAILOVER")

    print(
        f"Status: "
        f"{failover['status']}"
    )

    print(
        f"Ação: "
        f"{failover['action']}"
    )

    print(
        f"Mensagem: "
        f"{failover['message']}"
    )


def print_adaptive_failover_status(
    adaptive_failover
):
    print_section(
        "ADAPTIVE FAILOVER"
    )

    print(
        f"Status: "
        f"{adaptive_failover['status']}"
    )

    print(
        f"Ação: "
        f"{adaptive_failover['action']}"
    )

    print(
        f"Mensagem: "
        f"{adaptive_failover['message']}"
    )


def print_history():
    print_section(
        "HISTÓRICO RECENTE"
    )

    history = read_last_logs(limit=5)

    if history:
        for line in history:
            print(line.strip())
    else:
        print(
            "Nenhum histórico encontrado."
        )


def print_footer():
    print("\n" + "=" * 60)