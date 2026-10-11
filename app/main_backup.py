import streamlit as st
import pandas as pd

from app.core.diagnostics import run_basic_diagnostics
from app.core.decision_engine import diagnose
from app.core.fault_scenarios import SCENARIOS, create_scenario_evidence
from app.core.report_generator import create_report, save_report
from app.core.evidence_timeline import build_evidence_timeline


st.set_page_config(
    page_title="NetExplain - NETNEXUS",
    page_icon="🌐",
    layout="wide"
)

st.title("NetExplain")
st.caption("NETNEXUS - Explainable Connectivity Diagnostic System | PS-015")


tab_live, tab_lab, tab_reports = st.tabs([
    "Live Network Diagnosis",
    "Controlled Fault Scenarios",
    "Reports & Evidence"
])


with tab_live:
    st.header("Live Network Diagnosis")

    st.info(
        "Runs non-destructive local connectivity tests for gateway "
        "reachability, DNS resolution, Internet reachability and latency."
    )

    if st.button("Run Live Diagnosis", type="primary"):
        with st.spinner("Collecting network evidence..."):
            evidence = run_basic_diagnostics()
            diagnosis = diagnose(evidence)
            report = create_report(evidence, diagnosis)
            timeline = build_evidence_timeline(evidence, diagnosis)

        st.session_state["live_evidence"] = evidence
        st.session_state["live_diagnosis"] = diagnosis
        st.session_state["live_report"] = report
        st.session_state["live_timeline"] = timeline

    if "live_diagnosis" in st.session_state:
        evidence = st.session_state["live_evidence"]
        diagnosis = st.session_state["live_diagnosis"]
        timeline = st.session_state["live_timeline"]

        st.subheader("Diagnosis")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Diagnosis",
            diagnosis.get("label", "Unknown")
        )

        c2.metric(
            "Confidence",
            diagnosis.get("confidence", "Unknown")
        )

        c3.metric(
            "Gateway",
            "Reachable"
            if evidence.get("gateway_test", {}).get("reachable")
            else "Unreachable"
        )

        st.write(
            diagnosis.get(
                "reason",
                "No explanation available."
            )
        )

        st.subheader("Measured Evidence")

        gateway = evidence.get("gateway_test", {})
        dns = evidence.get("dns_test", {})
        internet = evidence.get("internet_test", {})

        rows = [
            {
                "Test": "Gateway Reachability",
                "Result": (
                    "Reachable"
                    if gateway.get("reachable")
                    else "Unreachable"
                ),
                "Latency (ms)": gateway.get("latency_ms"),
                "Packet Loss (%)": gateway.get("packet_loss_pct")
            },
            {
                "Test": "DNS Resolution",
                "Result": (
                    "Success"
                    if dns.get("success")
                    else "Failure"
                ),
                "Latency (ms)": dns.get("latency_ms"),
                "Packet Loss (%)": None
            },
            {
                "Test": "External Connectivity",
                "Result": (
                    "Reachable"
                    if internet.get("reachable")
                    else "Unreachable"
                ),
                "Latency (ms)": internet.get("latency_ms"),
                "Packet Loss (%)": internet.get("packet_loss_pct")
            }
        ]

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Evidence Timeline")

        for item in timeline:
            st.write(
                f"Step {item.get('step', '?')} - {item.get('name', item.get('test', item.get('title', 'Evidence')))}\n"
                f"{item.get('status', 'Recorded')} - {item.get('details', item.get('evidence', item.get('message', item.get('description', 'Evidence recorded.'))))}"
            )


with tab_lab:
    st.header("Controlled Fault Scenario Lab")

    st.write(
        "Controlled scenarios reproduce known connectivity conditions "
        "for repeatable evaluation of the decision engine."
    )

    scenario_names = list(SCENARIOS.keys())

    selected = st.selectbox(
        "Select Fault Scenario",
        scenario_names
    )

    if st.button("Run Controlled Scenario", type="primary"):
        evidence = create_scenario_evidence(selected)
        diagnosis = diagnose(evidence)
        report = create_report(evidence, diagnosis)
        timeline = build_evidence_timeline(evidence, diagnosis)

        st.session_state["lab_evidence"] = evidence
        st.session_state["lab_diagnosis"] = diagnosis
        st.session_state["lab_report"] = report
        st.session_state["lab_timeline"] = timeline
        st.session_state["lab_selected"] = selected

    if "lab_diagnosis" in st.session_state:
        evidence = st.session_state["lab_evidence"]
        diagnosis = st.session_state["lab_diagnosis"]
        timeline = st.session_state["lab_timeline"]
        selected = st.session_state.get("lab_selected", selected)

        st.divider()

        st.subheader("Scenario Result")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Diagnosis",
            diagnosis.get("label", "Unknown")
        )

        c2.metric(
            "Confidence",
            diagnosis.get("confidence", "Unknown")
        )

        c3.metric(
            "Scenario",
            selected
        )

        st.write(
            diagnosis.get(
                "reason",
                "No explanation available."
            )
        )

        st.subheader("Measured / Simulated Evidence")

        gateway = evidence.get("gateway_test", {})
        dns = evidence.get("dns_test", {})
        internet = evidence.get("internet_test", {})
        throughput = evidence.get("throughput_test", {})

        rows = [
            {
                "Evidence": "Gateway",
                "Result": (
                    "Reachable"
                    if gateway.get("reachable")
                    else "Unreachable"
                ),
                "Value": gateway.get("latency_ms")
            },
            {
                "Evidence": "DNS",
                "Result": (
                    "Success"
                    if dns.get("success")
                    else "Failure"
                ),
                "Value": dns.get("latency_ms")
            },
            {
                "Evidence": "External Connectivity",
                "Result": (
                    "Reachable"
                    if internet.get("reachable")
                    else "Unreachable"
                ),
                "Value": internet.get("latency_ms")
            },
            {
                "Evidence": "Packet Loss",
                "Result": "Measured / Simulated",
                "Value": internet.get("packet_loss_pct")
            },
            {
                "Evidence": "Throughput",
                "Result": (
                    "Available"
                    if throughput.get("success")
                    else "Not measured"
                ),
                "Value": (
                    f"{throughput.get('throughput_mbps')} Mbps"
                    if throughput.get("throughput_mbps") is not None
                    else "Not measured"
                )
            }
        ]

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        if throughput:
            st.subheader("Throughput Evidence")

            tc1, tc2, tc3 = st.columns(3)

            tc1.metric(
                "Throughput",
                (
                    f"{throughput.get('throughput_mbps')} Mbps"
                    if throughput.get("throughput_mbps") is not None
                    else "Not measured"
                )
            )

            tc2.metric(
                "Loaded Condition",
                "Yes"
                if throughput.get("loaded_condition")
                else "No"
            )

            tc3.metric(
                "Evidence Source",
                "Controlled Simulation"
                if throughput.get("source")
                else "Unavailable"
            )

            st.caption(
                "Scenario throughput values are controlled laboratory "
                "simulation evidence and are not Internet/WAN measurements."
            )

        st.subheader("Evidence Timeline")

        for item in timeline:
            st.write(
                f"Step {item.get('step', '?')} - {item.get('name', item.get('test', item.get('title', 'Evidence')))}\n"
                f"{item.get('status', 'Recorded')} - {item.get('details', item.get('evidence', item.get('message', item.get('description', 'Evidence recorded.'))))}"
            )


with tab_reports:
    st.header("Reports & Evidence")

    report_source = st.radio(
        "Select report",
        ["Live Diagnosis", "Controlled Scenario"]
    )

    if report_source == "Live Diagnosis":
        report = st.session_state.get("live_report")
    else:
        report = st.session_state.get("lab_report")

    if report:
        st.text_area(
            "Evidence-Based Report",
            report,
            height=500
        )

        st.download_button(
            "Download Report",
            data=report,
            file_name="netnexus_diagnostic_report.txt",
            mime="text/plain"
        )

        if st.button("Save Report to reports"):
            path = save_report(report)
            st.success(f"Report saved: {path}")

    else:
        st.info(
            "Run a live diagnosis or controlled scenario first."
        )


st.divider()

st.caption(
    "NETNEXUS / NetExplain - PS-015 prototype. "
    "The system does not claim physical cable damage, ISP-internal "
    "root causes, or Wi-Fi interference without appropriate telemetry."
)



