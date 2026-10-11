from typing import Dict, Any


def diagnose(evidence: Dict[str, Any]) -> Dict[str, Any]:

    gateway = evidence.get("gateway_test")
    dns = evidence.get("dns_test")
    internet = evidence.get("internet_test")

    # RULE 1 — Missing gateway evidence
    if gateway is None:
        return {
            "diagnosis": "INCONCLUSIVE",
            "confidence": "Low",
            "reason": "Gateway measurement is unavailable.",
            "evidence": []
        }

    # RULE 2 — Gateway unreachable
    if not gateway.get("reachable", False):
        return {
            "diagnosis": "GATEWAY UNREACHABLE",
            "confidence": "High",
            "reason": "The default gateway did not respond to the controlled reachability test.",
            "evidence": [
                f"Gateway: {gateway.get('host')}",
                f"Packet loss: {gateway.get('packet_loss_percent')}%"
            ]
        }

    # RULE 3 — Missing DNS evidence
    if dns is None:
        return {
            "diagnosis": "INCONCLUSIVE",
            "confidence": "Low",
            "reason": "DNS measurement is unavailable.",
            "evidence": [
                "Gateway reachability: PASS"
            ]
        }

    # RULE 4 — DNS failure
    if not dns.get("success", False):
        return {
            "diagnosis": "DNS FAILURE",
            "confidence": "High",
            "reason": "The gateway is reachable, but hostname resolution failed.",
            "evidence": [
                "Gateway reachability: PASS",
                "DNS resolution: FAIL"
            ]
        }

    # RULE 5 — Missing internet evidence
    if internet is None:
        return {
            "diagnosis": "INCONCLUSIVE",
            "confidence": "Low",
            "reason": "External connectivity evidence is unavailable.",
            "evidence": [
                "Gateway reachability: PASS",
                "DNS resolution: PASS"
            ]
        }

    loss = internet.get("packet_loss_percent")
    latency = internet.get("latency_ms")

    # RULE 6 — Incomplete measurements
    if loss is None or latency is None:
        return {
            "diagnosis": "INCONCLUSIVE",
            "confidence": "Low",
            "reason": "Available measurements are insufficient to isolate a specific connectivity fault.",
            "evidence": [
                "Gateway reachability: PASS",
                "DNS resolution: PASS",
                "External latency or packet-loss measurement unavailable"
            ]
        }

    # RULE 7 — Packet loss
    if loss >= 20:
        return {
            "diagnosis": "PACKET LOSS DETECTED",
            "confidence": "Medium",
            "reason": "The controlled external test measured substantial packet loss.",
            "evidence": [
                f"Packet loss: {loss}%",
                f"Latency: {latency} ms"
            ]
        }

    # RULE 8 — Elevated latency
    if latency >= 150:
        return {
            "diagnosis": "ELEVATED LATENCY",
            "confidence": "Medium",
            "reason": "Reachability succeeds, but measured round-trip latency is elevated. Additional loaded-network evidence is required before attributing this specifically to congestion.",
            "evidence": [
                f"Internet latency: {latency} ms",
                f"Packet loss: {loss}%"
            ]
        }

    # RULE 9 — Healthy
    if (
        gateway.get("reachable")
        and dns.get("success")
        and internet.get("reachable")
    ):
        return {
            "diagnosis": "NO MAJOR LOCAL CONNECTIVITY FAULT DETECTED",
            "confidence": "Medium",
            "reason": "Gateway reachability, DNS resolution and external reachability all succeeded.",
            "evidence": [
                "Gateway: PASS",
                "DNS: PASS",
                "External reachability: PASS"
            ]
        }

    # RULE 10 — Fallback
    return {
        "diagnosis": "INCONCLUSIVE",
        "confidence": "Low",
        "reason": "Available measurements do not isolate a single fault.",
        "evidence": []
    }
