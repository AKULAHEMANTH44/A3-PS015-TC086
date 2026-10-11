from datetime import datetime


def build_evidence_timeline(evidence, diagnosis):

    timeline = []

    timestamp = evidence.get(
        "timestamp",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    gateway = evidence.get("gateway_test")
    dns = evidence.get("dns_test")
    internet = evidence.get("internet_test")
    throughput = evidence.get("throughput_test")

    timeline.append({
        "step": 1,
        "test": "Gateway Discovery",
        "status": "PASS" if evidence.get("gateway") else "FAIL",
        "evidence": evidence.get("gateway") or "No gateway detected",
        "timestamp": timestamp
    })

    if gateway:
        timeline.append({
            "step": 2,
            "test": "Gateway Reachability",
            "status": (
                "PASS"
                if gateway.get("reachable")
                else "FAIL"
            ),
            "evidence": (
                f"Latency: {gateway.get('latency_ms')} ms | "
                f"Packet loss: {gateway.get('packet_loss_percent')}%"
            ),
            "timestamp": timestamp
        })

    if dns:
        timeline.append({
            "step": 3,
            "test": "DNS Resolution",
            "status": (
                "PASS"
                if dns.get("success")
                else "FAIL"
            ),
            "evidence": (
                f"Host: {dns.get('hostname')} | "
                f"Resolution: {dns.get('resolution_ms')} ms"
            ),
            "timestamp": timestamp
        })

    if internet:
        timeline.append({
            "step": 4,
            "test": "External Reachability",
            "status": (
                "PASS"
                if internet.get("reachable")
                else "FAIL"
            ),
            "evidence": (
                f"Latency: {internet.get('latency_ms')} ms | "
                f"Packet loss: {internet.get('packet_loss_percent')}%"
            ),
            "timestamp": timestamp
        })

    if throughput:
        throughput_value = throughput.get("throughput_mbps")

        timeline.append({
            "step": 5,
            "test": "Throughput Measurement",
            "status": (
                "PASS"
                if throughput.get("success")
                else "UNAVAILABLE"
            ),
            "evidence": (
                f"Throughput: "
                f"{throughput_value} Mbps"
                if throughput_value is not None
                else "Throughput unavailable"
            ),
            "timestamp": timestamp
        })

    timeline.append({
        "step": 6,
        "test": "Explainable Decision",
        "status": "COMPLETE",
        "evidence": (
            f"{diagnosis.get('diagnosis')} "
            f"({diagnosis.get('confidence')} confidence)"
        ),
        "timestamp": timestamp
    })

    return timeline
