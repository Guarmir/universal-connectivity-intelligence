from core.decision_engine.intelligence_score import (
    calculate_intelligence_score,
)

from core.decision_engine.contextual_decision import (
    recommend_contextual_interface,
    calculate_contextual_score,
    build_decision_reason,
)

from core.decision_engine.interface_filter import (
    filter_operational_interfaces,
)

from core.security_engine.risk_analyzer import analyze_risk
from core.emergency_control.emergency_controller import emergency_check
from core.failover.failover_engine import evaluate_failover
from core.failover.adaptive_failover import evaluate_adaptive_failover

from core.monitor.stability_engine import calculate_stability_score
from core.monitor.intelligent_baseline import compare_with_intelligent_baseline
from core.monitor.anomaly_detector import detect_operational_anomalies
from core.monitor.degradation_engine import analyze_degradation
from core.monitor.predictive_engine import predict_operational_risk

from core.behavior.behavioral_engine import analyze_behavior
from core.behavior.profile_engine import generate_operational_profile

from core.autonomous.autonomous_engine import (
    make_autonomous_decision,
)

from core.prevention.preventive_engine import (
    generate_preventive_recommendation,
)

from core.quality.connectivity_quality import (
    measure_latency,
    classify_latency,
)


def enrich_interfaces_with_intelligence(interfaces):
    latency = measure_latency()
    latency_quality = classify_latency(latency)

    enriched = []

    for interface in interfaces:
        risk = analyze_risk(
            interface["trust_score"]
        )

        stability_score = calculate_stability_score(
            interface["name"]
        )

        intelligence_score = calculate_intelligence_score(
            interface["trust_score"],
            stability_score,
            latency_quality,
        )

        interface["risk_level"] = risk["risk_level"]
        interface["risk_action"] = risk["action"]
        interface["risk_message"] = risk["message"]
        interface["stability_score"] = stability_score
        interface["latency_ms"] = latency
        interface["quality"] = latency_quality
        interface["intelligence_score"] = intelligence_score

        contextual_score = calculate_contextual_score(
            interface
        )

        interface["contextual_score"] = contextual_score

        interface["decision_reason"] = build_decision_reason(
            interface,
            contextual_score
        )

        interface["anomalies"] = detect_operational_anomalies(
            interface
        )

        enriched.append(interface)

    enriched.sort(
        key=lambda item: item["contextual_score"],
        reverse=True
    )

    return enriched


def build_risk_payload(recommended):
    return {
        "risk_level": recommended["risk_level"],
        "action": recommended["risk_action"],
        "message": recommended["risk_message"],
    }


def execute_operational_analysis(interfaces):
    baseline_alerts = compare_with_intelligent_baseline(
        interfaces
    )

    operational_interfaces = filter_operational_interfaces(
        interfaces
    )

    enriched_interfaces = enrich_interfaces_with_intelligence(
        operational_interfaces
    )

    recommended = recommend_contextual_interface(
        enriched_interfaces
    )

    behavior_result = analyze_behavior(
        limit=100
    )

    operational_profile = generate_operational_profile()

    if not recommended:
        autonomous_decision = make_autonomous_decision(
            None,
            {},
            operational_profile,
            {},
        )

        preventive_recommendation = (
            generate_preventive_recommendation(
                autonomous_decision,
                {},
                {},
                operational_profile,
            )
        )

        return {
            "interfaces": interfaces,
            "baseline_alerts": baseline_alerts,
            "operational_interfaces": operational_interfaces,
            "enriched_interfaces": enriched_interfaces,
            "recommended": None,
            "risk": None,
            "emergency": None,
            "failover": None,
            "degradation_result": None,
            "prediction_result": None,
            "adaptive_failover": None,
            "behavior_result": behavior_result,
            "operational_profile": operational_profile,
            "autonomous_decision": autonomous_decision,
            "preventive_recommendation": preventive_recommendation,
        }

    degradation_result = analyze_degradation(
        limit=10
    )

    prediction_result = predict_operational_risk()

    adaptive_failover = evaluate_adaptive_failover(
        recommended,
        prediction_result,
        degradation_result,
    )

    autonomous_decision = make_autonomous_decision(
        recommended,
        prediction_result,
        operational_profile,
        adaptive_failover,
    )

    preventive_recommendation = generate_preventive_recommendation(
        autonomous_decision,
        prediction_result,
        adaptive_failover,
        operational_profile,
    )

    risk = build_risk_payload(
        recommended
    )

    emergency = emergency_check(
        risk["risk_level"]
    )

    failover = evaluate_failover(
        recommended,
        risk
    )

    return {
        "interfaces": interfaces,
        "baseline_alerts": baseline_alerts,
        "operational_interfaces": operational_interfaces,
        "enriched_interfaces": enriched_interfaces,
        "recommended": recommended,
        "risk": risk,
        "emergency": emergency,
        "failover": failover,
        "degradation_result": degradation_result,
        "prediction_result": prediction_result,
        "adaptive_failover": adaptive_failover,
        "behavior_result": behavior_result,
        "operational_profile": operational_profile,
        "autonomous_decision": autonomous_decision,
        "preventive_recommendation": preventive_recommendation,
    }