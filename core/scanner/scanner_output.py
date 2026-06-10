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


def print_header():

    print("=" * 60)

    print(
        "INTELIGÊNCIA UNIVERSAL DE CONECTIVIDADE"
    )

    print("=" * 60)


def print_section(title):

    print(f"\n{title}")

    print("-" * 60)


def print_detected_interfaces(
    interfaces
):

    print_section(
        "INTERFACES DETECTADAS"
    )

    for interface in interfaces:

        print(
            f"\nInterface: "
            f"{interface['name']}"
        )

        print(
            f"IPv4: "
            f"{interface['ip']}"
        )

        print(
            f"Classificação: "
            f"{interface['classification']}"
        )

        print(
            f"Trust Score: "
            f"{interface['trust_score']}/100"
        )


def print_baseline_status(
    baseline_alerts
):

    print_section(
        "BASELINE INTELIGENTE"
    )

    if baseline_alerts:

        for alert in baseline_alerts:

            print(
                f"[{alert['severity']}] "
                f"{alert['message']}"
            )

    else:

        print(
            "Ambiente compatível "
            "com o baseline."
        )


def print_operational_ranking(
    enriched_interfaces
):

    print_section(
        "RANKING OPERACIONAL"
    )

    for position, interface in enumerate(
        enriched_interfaces,
        start=1
    ):

        print(
            f"{position}. "
            f"{interface['name']} | "
            f"Score: "
            f"{interface['contextual_score']}/100 | "
            f"Risco: "
            f"{interface['risk_level']}"
        )


def print_recommendation(
    recommended
):

    print_section(
        "RECOMENDAÇÃO CONTEXTUAL"
    )

    print(
        f"Interface: "
        f"{recommended['name']}"
    )

    print(
        f"IP: "
        f"{recommended['ip']}"
    )

    print(
        f"Contextual Score: "
        f"{recommended['contextual_score']}/100"
    )

    print(
        f"Motivos: "
        f"{recommended['decision_reason']}"
    )


def print_no_recommendation():

    print_section(
        "RECOMENDAÇÃO CONTEXTUAL"
    )

    print(
        "Nenhuma interface "
        "operacional disponível."
    )


def print_anomaly_status(
    recommended
):

    print_section(
        "ANOMALIAS OPERACIONAIS"
    )

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

    print_section(
        "DEGRADAÇÃO HISTÓRICA"
    )

    print(
        summarize_degradation(
            degradation_result
        )
    )


def print_prediction_status(
    prediction_result
):

    print_section(
        "PREVISÃO OPERACIONAL"
    )

    print(
        summarize_prediction(
            prediction_result
        )
    )


def print_behavior_status(
    behavior_result
):

    print_section(
        "COMPORTAMENTO OPERACIONAL"
    )

    print(
        summarize_behavior(
            behavior_result
        )
    )


def print_operational_profile_status(
    operational_profile
):

    print_section(
        "PERFIL OPERACIONAL"
    )

    print(
        summarize_operational_profile(
            operational_profile
        )
    )


def print_autonomous_status(
    autonomous_decision
):

    print_section(
        "DECISÃO AUTÔNOMA"
    )

    print(
        summarize_autonomous_decision(
            autonomous_decision
        )
    )


def print_security_status(
    risk
):

    print_section(
        "ANÁLISE DE SEGURANÇA"
    )

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

    print_section(
        "ESTABILIDADE"
    )

    print(
        f"{recommended['stability_score']}/100"
    )

    print_section(
        "QUALIDADE"
    )

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

    print_section(
        "FAILOVER"
    )

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

    history = read_last_logs(
        limit=5
    )

    if history:

        for line in history:

            print(
                line.strip()
            )

    else:

        print(
            "Nenhum histórico encontrado."
        )


def print_footer():

    print(
        "\n" + "=" * 60
    )