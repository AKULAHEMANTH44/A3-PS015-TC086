import pytest

from app.core.fault_scenarios import (
    SCENARIOS,
    create_scenario_evidence
)
from app.core.decision_engine import diagnose


@pytest.mark.parametrize(
    "scenario, expected",
    [
        (
            "Normal Connection",
            "NO MAJOR LOCAL CONNECTIVITY FAULT DETECTED"
        ),
        (
            "Gateway Unreachable",
            "GATEWAY UNREACHABLE"
        ),
        (
            "DNS Failure",
            "DNS FAILURE"
        ),
        (
            "Induced Packet Loss",
            "PACKET LOSS DETECTED"
        ),
        (
            "Network Congestion",
            "ELEVATED LATENCY"
        ),
        (
            "Inconclusive",
            "INCONCLUSIVE"
        ),
    ]
)
def test_required_scenarios(scenario, expected):

    evidence = create_scenario_evidence(scenario)

    result = diagnose(evidence)

    assert result["diagnosis"] == expected


def test_all_required_scenarios_exist():

    required = {
        "Gateway Unreachable",
        "DNS Failure",
        "Induced Packet Loss",
        "Network Congestion"
    }

    assert required.issubset(set(SCENARIOS.keys()))


def test_gateway_failure_has_high_confidence():

    evidence = create_scenario_evidence(
        "Gateway Unreachable"
    )

    result = diagnose(evidence)

    assert result["diagnosis"] == "GATEWAY UNREACHABLE"
    assert result["confidence"] == "High"


def test_dns_failure_has_high_confidence():

    evidence = create_scenario_evidence(
        "DNS Failure"
    )

    result = diagnose(evidence)

    assert result["diagnosis"] == "DNS FAILURE"
    assert result["confidence"] == "High"


def test_packet_loss_detected():

    evidence = create_scenario_evidence(
        "Induced Packet Loss"
    )

    result = diagnose(evidence)

    assert result["diagnosis"] == "PACKET LOSS DETECTED"


def test_inconclusive_case():

    evidence = create_scenario_evidence(
        "Inconclusive"
    )

    result = diagnose(evidence)

    assert result["diagnosis"] == "INCONCLUSIVE"


def test_normal_connection():

    evidence = create_scenario_evidence(
        "Normal Connection"
    )

    result = diagnose(evidence)

    assert (
        result["diagnosis"]
        == "NO MAJOR LOCAL CONNECTIVITY FAULT DETECTED"
    )
