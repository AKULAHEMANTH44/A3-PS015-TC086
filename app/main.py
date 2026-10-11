import json
import os
import urllib.request
import urllib.error

import streamlit as st
import pandas as pd

from app.ui import apply_styles

from app.core.diagnostics import run_basic_diagnostics
from app.core.decision_engine import diagnose

from app.core.fault_scenarios import (
    SCENARIOS,
    create_scenario_evidence
)

from app.core.report_generator import (
    create_report,
    save_report
)

from app.core.evidence_timeline import (
    build_evidence_timeline
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NetExplain",
    page_icon="??",
    layout="wide"
)

apply_styles()


# ============================================================
# LOCAL AGENT CONFIGURATION
# ============================================================

LOCAL_AGENT_URL = "http://127.0.0.1:8765"


def is_render_environment():
    return os.getenv("RENDER", "").lower() == "true"


def get_local_agent_health():
    """
    Check whether the NETNEXUS Local Agent is running
    on the current computer.
    """

    if is_render_environment():
        return False

    try:
        with urllib.request.urlopen(
            f"{LOCAL_AGENT_URL}/health",
            timeout=3
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

            return data.get("status") == "ONLINE"

    except Exception:
        return False


def get_local_diagnosis():
    """
    Request real network evidence from the
    NETNEXUS Local Agent.
    """

    try:
        with urllib.request.urlopen(
            f"{LOCAL_AGENT_URL}/diagnose",
            timeout=20
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

            if data.get("status") != "ONLINE":
                return None, "Local Agent returned an error."

            evidence = data.get("evidence")

            if not evidence:
                return None, "Local Agent returned no evidence."

            return evidence, None

    except urllib.error.URLError:
        return (
            None,
            "NETNEXUS Local Agent is not running on this computer."
        )

    except Exception as exc:
        return (
            None,
            f"Unable to connect to Local Agent: {exc}"
        )


# ============================================================
# HEADER
# ============================================================

st.title("?? NetExplain")

st.subheader(
    "Explainable Connectivity Diagnostic System"
)

st.caption(
    "TEAM NETNEXUS  |  SIH PS-015  |  SMART CITIES"
)

st.divider()


# ============================================================
# TABS
# ============================================================

live_tab, lab_tab, reports_tab = st.tabs(
    [
        "Live Network Diagnosis",
        "Controlled Fault Scenarios",
        "Reports & Evidence"
    ]
)


# ============================================================
# LIVE NETWORK DIAGNOSIS
# ============================================================

with live_tab:

    st.header("Live Network Diagnosis")

    # --------------------------------------------------------
    # RENDER / LOCAL DIAGNOSIS MODE
    # --------------------------------------------------------

    if is_render_environment():

        st.info(
            "☁️ NETNEXUS Cloud Demo Mode"
        )

        st.write(
            "Run a live connectivity diagnosis from the "
            "NETNEXUS cloud environment."
        )

        if st.button(
            "🔍 Run Live Diagnosis",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Collecting cloud network evidence..."
            ):

                try:
                    evidence = run_basic_diagnostics()
                    error = None

                except Exception as exc:
                    evidence = None
                    error = str(exc)

            if error:

                st.error(
                    f"Live diagnosis failed: {error}"
                )

            elif not evidence:

                st.error(
                    "Live diagnosis returned no network evidence."
                )

            else:

                result = diagnose(evidence)

                timeline = build_evidence_timeline(
                    evidence,
                    result
                )

                report = create_report(
                    evidence,
                    result
                )

                st.session_state.live_data = {
                    "evidence": evidence,
                    "result": result,
                    "timeline": timeline,
                    "report": report
                }

                st.rerun()

    else:

        st.write(
            "Run a real connectivity diagnosis using the "
            "NETNEXUS Local Agent on this computer."
        )

        # ----------------------------------------------------
        # LOCAL AGENT STATUS
        # ----------------------------------------------------

        agent_online = get_local_agent_health()

        if agent_online:

            st.success(
                "🟢 NETNEXUS Local Agent ONLINE"
            )

            st.caption(
                "Real diagnostics can be collected from this computer."
            )

        else:

            st.warning(
                "🟠 NETNEXUS Local Agent OFFLINE"
            )

            st.caption(
                "Start agent.py on this computer to enable real "
                "local network diagnosis."
            )

        st.divider()

        # ----------------------------------------------------
        # RUN REAL DIAGNOSIS
        # ----------------------------------------------------

        if st.button(
            "🔍 Run Real Live Diagnosis",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "Collecting real network evidence..."
            ):

                evidence, error = get_local_diagnosis()

            if error:

                st.error(error)

                st.info(
                    "Start the Local Agent with: "
                    "python .\agent.py"
                )

            else:

                result = diagnose(evidence)

                timeline = build_evidence_timeline(
                    evidence,
                    result
                )

                report = create_report(
                    evidence,
                    result
                )

                st.session_state.live_data = {
                    "evidence": evidence,
                    "result": result,
                    "timeline": timeline,
                    "report": report
                }

                st.rerun()

    # LIVE RESULTS
    # --------------------------------------------------------

    if "live_data" in st.session_state:

        evidence = st.session_state.live_data["evidence"]
        result = st.session_state.live_data["result"]
        timeline = st.session_state.live_data["timeline"]

        st.divider()

        st.subheader("Diagnosis")

        diagnosis_text = result.get(
            "diagnosis",
            "INCONCLUSIVE"
        )

        confidence = result.get(
            "confidence",
            "Low"
        )

        reason = result.get(
            "reason",
            "Available evidence is insufficient."
        )

        if diagnosis_text == "INCONCLUSIVE":

            st.warning(
                f"?? {diagnosis_text}"
            )

        elif diagnosis_text == "GATEWAY UNREACHABLE":

            st.error(
                f"?? {diagnosis_text}"
            )

        elif diagnosis_text == "DNS FAILURE":

            st.error(
                f"?? {diagnosis_text}"
            )

        elif diagnosis_text == "PACKET LOSS DETECTED":

            st.warning(
                f"?? {diagnosis_text}"
            )

        elif diagnosis_text == "ELEVATED LATENCY":

            st.warning(
                f"?? {diagnosis_text}"
            )

        else:

            st.success(
                f"?? {diagnosis_text}"
            )

        st.write(
            f"**Confidence:** {confidence}"
        )

        st.write(
            f"**Reason:** {reason}"
        )

        # ----------------------------------------------------
        # REAL NETWORK SUMMARY
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "Real Network Evidence"
        )

        gateway_test = (
            evidence.get("gateway_test")
            or {}
        )

        dns_test = (
            evidence.get("dns_test")
            or {}
        )

        internet_test = (
            evidence.get("internet_test")
            or {}
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Gateway",
                evidence.get(
                    "gateway",
                    "Not detected"
                )
            )

        with col2:

            st.metric(
                "Gateway Latency",
                (
                    f"{gateway_test.get('latency_ms')} ms"
                    if gateway_test.get("latency_ms")
                    is not None
                    else "N/A"
                )
            )

        with col3:

            st.metric(
                "DNS",
                (
                    "PASS"
                    if dns_test.get("success")
                    else "FAIL"
                )
            )

        with col4:

            st.metric(
                "Internet",
                (
                    "PASS"
                    if internet_test.get("reachable")
                    else "FAIL"
                )
            )

        # ----------------------------------------------------
        # DETAILED EVIDENCE
        # ----------------------------------------------------

        st.subheader(
            "Measurement Evidence"
        )

        evidence_rows = [
            {
                "Measurement": "Gateway",
                "Value": evidence.get(
                    "gateway",
                    "Not detected"
                ),
                "Status": (
                    "PASS"
                    if gateway_test.get("reachable")
                    else "FAIL"
                )
            },
            {
                "Measurement": "Gateway Latency",
                "Value": (
                    f"{gateway_test.get('latency_ms')} ms"
                    if gateway_test.get("latency_ms")
                    is not None
                    else "Not measured"
                ),
                "Status": (
                    "MEASURED"
                    if gateway_test.get("latency_ms")
                    is not None
                    else "UNAVAILABLE"
                )
            },
            {
                "Measurement": "Gateway Packet Loss",
                "Value": (
                    f"{gateway_test.get('packet_loss_percent')}%"
                    if gateway_test.get(
                        "packet_loss_percent"
                    ) is not None
                    else "Not measured"
                ),
                "Status": (
                    "MEASURED"
                    if gateway_test.get(
                        "packet_loss_percent"
                    ) is not None
                    else "UNAVAILABLE"
                )
            },
            {
                "Measurement": "DNS Resolution",
                "Value": dns_test.get(
                    "hostname",
                    "example.com"
                ),
                "Status": (
                    "PASS"
                    if dns_test.get("success")
                    else "FAIL"
                )
            },
            {
                "Measurement": "DNS Response",
                "Value": (
                    f"{dns_test.get('resolution_ms')} ms"
                    if dns_test.get("resolution_ms")
                    is not None
                    else "Not measured"
                ),
                "Status": (
                    "MEASURED"
                    if dns_test.get("resolution_ms")
                    is not None
                    else "UNAVAILABLE"
                )
            },
            {
                "Measurement": "External Connectivity",
                "Value": internet_test.get(
                    "host",
                    "8.8.8.8"
                ),
                "Status": (
                    "PASS"
                    if internet_test.get("reachable")
                    else "FAIL"
                )
            },
            {
                "Measurement": "Internet Latency",
                "Value": (
                    f"{internet_test.get('latency_ms')} ms"
                    if internet_test.get("latency_ms")
                    is not None
                    else "Not measured"
                ),
                "Status": (
                    "MEASURED"
                    if internet_test.get("latency_ms")
                    is not None
                    else "UNAVAILABLE"
                )
            },
            {
                "Measurement": "Internet Packet Loss",
                "Value": (
                    f"{internet_test.get('packet_loss_percent')}%"
                    if internet_test.get(
                        "packet_loss_percent"
                    ) is not None
                    else "Not measured"
                ),
                "Status": (
                    "MEASURED"
                    if internet_test.get(
                        "packet_loss_percent"
                    ) is not None
                    else "UNAVAILABLE"
                )
            }
        ]

        st.dataframe(
            pd.DataFrame(evidence_rows),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # EVIDENCE TIMELINE
        # ----------------------------------------------------

        st.subheader(
            "Evidence Timeline"
        )

        st.dataframe(
            pd.DataFrame(timeline),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # AGENT INFORMATION
        # ----------------------------------------------------

        st.caption(
            "Source: NETNEXUS Local Agent running on the "
            "diagnosing computer."
        )

    else:

        st.info(
            "Click 'Run Real Live Diagnosis' to collect "
            "real network evidence."
        )


# ============================================================
# CONTROLLED FAULT SCENARIOS
# ============================================================

with lab_tab:

    st.header(
        "Controlled Fault Scenarios"
    )

    st.write(
        "Use the controlled laboratory scenarios to "
        "validate NetExplain's explainable decision rules."
    )

    scenario_name = st.selectbox(
        "Select Fault Scenario",
        list(SCENARIOS.keys())
    )

    scenario_description = SCENARIOS[
        scenario_name
    ].get(
        "description",
        ""
    )

    st.info(
        scenario_description
    )

    if st.button(
        "?? Run Controlled Scenario",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Running controlled scenario..."
        ):

            evidence = create_scenario_evidence(
                scenario_name
            )

            result = diagnose(
                evidence
            )

            timeline = build_evidence_timeline(
                evidence,
                result
            )

            report = create_report(
                evidence,
                result
            )

        st.session_state.scenario_data = {
            "scenario": scenario_name,
            "evidence": evidence,
            "result": result,
            "timeline": timeline,
            "report": report
        }

        st.rerun()

    # --------------------------------------------------------
    # SCENARIO RESULTS
    # --------------------------------------------------------

    if "scenario_data" in st.session_state:

        data = st.session_state.scenario_data

        evidence = data["evidence"]
        result = data["result"]
        timeline = data["timeline"]

        st.divider()

        st.subheader(
            f"Scenario Diagnosis — {data['scenario']}"
        )

        diagnosis_text = result.get(
            "diagnosis",
            "INCONCLUSIVE"
        )

        if diagnosis_text == "INCONCLUSIVE":

            st.warning(
                diagnosis_text
            )

        elif diagnosis_text == "GATEWAY UNREACHABLE":

            st.error(
                diagnosis_text
            )

        elif diagnosis_text == "DNS FAILURE":

            st.error(
                diagnosis_text
            )

        elif diagnosis_text == "PACKET LOSS DETECTED":

            st.warning(
                diagnosis_text
            )

        else:

            st.success(
                diagnosis_text
            )

        st.write(
            f"**Confidence:** "
            f"{result.get('confidence', 'Low')}"
        )

        st.write(
            f"**Reason:** "
            f"{result.get('reason', '')}"
        )

        # ----------------------------------------------------
        # SCENARIO EVIDENCE
        # ----------------------------------------------------

        st.subheader(
            "Scenario Evidence"
        )

        gateway_test = (
            evidence.get("gateway_test")
            or {}
        )

        dns_test = (
            evidence.get("dns_test")
            or {}
        )

        internet_test = (
            evidence.get("internet_test")
            or {}
        )

        scenario_rows = [
            {
                "Measurement": "Gateway",
                "Value": evidence.get(
                    "gateway",
                    "Not detected"
                ),
                "Status": (
                    "PASS"
                    if gateway_test.get("reachable")
                    else "FAIL"
                )
            },
            {
                "Measurement": "DNS",
                "Value": dns_test.get(
                    "hostname",
                    "example.com"
                ),
                "Status": (
                    "PASS"
                    if dns_test.get("success")
                    else "FAIL"
                )
            },
            {
                "Measurement": "Packet Loss",
                "Value": (
                    f"{internet_test.get('packet_loss_percent')}%"
                    if internet_test.get(
                        "packet_loss_percent"
                    ) is not None
                    else "Unavailable"
                ),
                "Status": "MEASURED"
            },
            {
                "Measurement": "Latency",
                "Value": (
                    f"{internet_test.get('latency_ms')} ms"
                    if internet_test.get("latency_ms")
                    is not None
                    else "Unavailable"
                ),
                "Status": "MEASURED"
            }
        ]

        st.dataframe(
            pd.DataFrame(scenario_rows),
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # THROUGHPUT EVIDENCE
        # ----------------------------------------------------

        throughput_test = (
            evidence.get("throughput_test")
            or {}
        )

        if throughput_test:

            st.subheader(
                "Throughput Evidence"
            )

            throughput_value = (
                throughput_test.get(
                    "throughput_mbps"
                )
            )

            loaded_condition = (
                throughput_test.get(
                    "loaded_condition"
                )
            )

            throughput_rows = [
                {
                    "Measurement": "Throughput",
                    "Value": (
                        f"{throughput_value} Mbps"
                        if throughput_value
                        is not None
                        else "Not measured"
                    ),
                    "Status": (
                        "PASS"
                        if throughput_test.get(
                            "success"
                        )
                        else "UNAVAILABLE"
                    )
                },
                {
                    "Measurement": "Loaded Condition",
                    "Value": (
                        "YES"
                        if loaded_condition
                        else "NO"
                    ),
                    "Status": "SIMULATED"
                },
                {
                    "Measurement": "Source",
                    "Value": throughput_test.get(
                        "source",
                        "Controlled laboratory simulation"
                    ),
                    "Status": "REFERENCE"
                }
            ]

            st.dataframe(
                pd.DataFrame(throughput_rows),
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # TIMELINE
        # ----------------------------------------------------

        st.subheader(
            "Evidence Timeline"
        )

        st.dataframe(
            pd.DataFrame(timeline),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# REPORTS & EVIDENCE
# ============================================================

with reports_tab:

    st.header(
        "Reports & Evidence"
    )

    report = None

    if "live_data" in st.session_state:

        report = st.session_state.live_data.get(
            "report"
        )

        st.subheader(
            "Latest Live Diagnostic Report"
        )

    elif "scenario_data" in st.session_state:

        report = st.session_state.scenario_data.get(
            "report"
        )

        st.subheader(
            "Latest Controlled Scenario Report"
        )

    if report:

        st.code(
            report,
            language="text"
        )

        st.download_button(
            "? Download Report",
            data=report,
            file_name="NetExplain_Diagnostic_Report.txt",
            mime="text/plain"
        )

        if st.button(
            "?? Save Report to reports/"
        ):

            saved_path = save_report(
                report
            )

            st.success(
                f"Report saved: {saved_path}"
            )

    else:

        st.info(
            "Run a live diagnosis or controlled "
            "scenario to generate a report."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "NETNEXUS • NetExplain • PS-015 | "
    "Measure. Understand. Explain. Escalate."
)

st.caption(
    "NetExplain uses measurable network evidence and "
    "transparent decision rules. It does not claim "
    "physical cable damage, ISP-internal root causes, "
    "or Wi-Fi interference without supporting telemetry."
)
