from pathlib import Path
from datetime import datetime


def _display(value, suffix=""):
    if value is None:
        return "Not measured"
    return f"{value}{suffix}"


def create_report(evidence, diagnosis):

    timestamp = evidence.get(
        "timestamp",
        "SIMULATED CONTROLLED LAB SCENARIO"
    )

    gateway_test = evidence.get("gateway_test") or {}
    dns_test = evidence.get("dns_test") or {}
    internet_test = evidence.get("internet_test") or {}
    throughput_test = evidence.get("throughput_test") or {}

    report = f"""
NETEXPLAIN CONNECTIVITY DIAGNOSTIC REPORT
=========================================

Team: NETNEXUS
Problem Statement: PS-015
System: Explainable Connectivity Diagnostic System

TIMESTAMP
---------
{timestamp}


DIAGNOSIS
---------
Result: {diagnosis["diagnosis"]}
Confidence: {diagnosis["confidence"]}

Reason:
{diagnosis["reason"]}


MEASURED EVIDENCE
-----------------

Gateway:
{evidence.get("gateway", "Not available")}

Gateway Reachability:
{gateway_test.get("reachable", "Not measured")}

Gateway Latency:
{_display(gateway_test.get("latency_ms"), " ms")}

Gateway Packet Loss:
{_display(gateway_test.get("packet_loss_percent"), " %")}


DNS Resolution:
{dns_test.get("success", "Not measured")}

DNS Hostname:
{dns_test.get("hostname", "Not measured")}

Resolved Address:
{dns_test.get("resolved_ip", "Not measured")}

DNS Resolution Time:
{_display(dns_test.get("resolution_ms"), " ms")}


External Reachability:
{internet_test.get("reachable", "Not measured")}

External Test Host:
{internet_test.get("host", "Not measured")}

External Latency:
{_display(internet_test.get("latency_ms"), " ms")}

External Packet Loss:
{_display(internet_test.get("packet_loss_percent"), " %")}


THROUGHPUT EVIDENCE
-------------------

Throughput:
{_display(throughput_test.get("throughput_mbps"), " Mbps")}

Measurement Status:
{
    "PASS"
    if throughput_test.get("success")
    else "Not measured"
}

Loaded Condition:
{
    "YES"
    if throughput_test.get("loaded_condition")
    else "NO"
}

Measurement Source:
{throughput_test.get("source", "Not specified")}


DECISION EVIDENCE
-----------------
- Gateway reachability: {
    "PASS"
    if gateway_test.get("reachable")
    else "FAIL"
}
- DNS resolution: {
    "PASS"
    if dns_test.get("success")
    else "FAIL"
}
- External latency: {_display(internet_test.get("latency_ms"), " ms")}
- External packet loss: {_display(internet_test.get("packet_loss_percent"), " %")}
- Throughput: {_display(throughput_test.get("throughput_mbps"), " Mbps")}


DECISION RULE
-------------

The diagnosis was generated using deterministic,
explainable network decision rules.

For the controlled congestion scenario, elevated
latency is evaluated together with simulated
throughput evidence under a loaded condition.

The system does not claim:
- Physical cable damage
- ISP-internal root cause
- Wi-Fi interference without radio telemetry

An INCONCLUSIVE result is produced when available
measurements cannot isolate a specific fault.


END OF REPORT
=============
"""

    return report.strip()


def save_report(report_text):

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    filename = (
        reports_dir
        / f"netexplain_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    filename.write_text(report_text, encoding="utf-8")

    return filename


