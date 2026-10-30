from pathlib import Path
import socket

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.diagnostics import run_basic_diagnostics
from app.core.decision_engine import diagnose as run_decision_engine
from app.core.fault_scenarios import SCENARIOS, create_scenario_evidence
from app.core.evidence_timeline import build_evidence_timeline
from app.core.report_generator import create_report


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="NETNEXUS NetExplain")

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/health")
def health():
    return {"status": "online"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/api/diagnose")
def diagnose():
    try:
        evidence = run_basic_diagnostics()

        diagnosis_result = run_decision_engine(evidence)

        timeline = build_evidence_timeline(
            evidence,
            diagnosis_result
        )

        report_text = create_report(
            evidence,
            diagnosis_result
        )

        dns_test = evidence.get("dns_test") or {}
        internet_test = evidence.get("internet_test") or {}

        return {
            "hostname": socket.gethostname(),
            "timestamp": evidence.get("timestamp"),
            "gateway": evidence.get("gateway"),
            "dns": "PASS" if dns_test.get("success") else "FAIL",
            "internet": (
                "PASS" if internet_test.get("reachable") else "FAIL"
            ),
            "latency_ms": internet_test.get("latency_ms"),
            "diagnosis": diagnosis_result["diagnosis"],
            "confidence": diagnosis_result["confidence"],
            "reason": diagnosis_result["reason"],
            "decision_evidence": diagnosis_result.get("evidence", []),
            "evidence": evidence,
            "timeline": timeline,
            "report_text": report_text,
            "execution_context": (
                "Measurements are collected by the machine hosting this app."
            )
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Diagnostic error: {str(error)}"
        )


@app.post("/api/scenario/{scenario}")
def scenario(scenario: str):
    if scenario not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail="Unknown scenario"
        )

    try:
        evidence = create_scenario_evidence(scenario)

        diagnosis_result = run_decision_engine(evidence)

        timeline = build_evidence_timeline(
            evidence,
            diagnosis_result
        )

        report_text = create_report(
            evidence,
            diagnosis_result
        )

        return {
            "scenario": scenario,
            "simulated": True,
            "timestamp": evidence.get("timestamp"),
            "diagnosis": diagnosis_result["diagnosis"],
            "confidence": diagnosis_result["confidence"],
            "reason": diagnosis_result["reason"],
            "decision_evidence": diagnosis_result.get("evidence", []),
            "evidence": evidence,
            "timeline": timeline,
            "report_text": report_text
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Scenario error: {str(error)}"
        )


@app.post("/api/report")
async def report(data: dict):
    content = data.get("content", "")

    if not isinstance(content, str) or not content:
        raise HTTPException(
            status_code=400,
            detail="Report is empty"
        )

    return PlainTextResponse(
        content,
        headers={
            "Content-Disposition":
            'attachment; filename="NETEXPLAIN-Report.txt"'
        }
    )

@app.get("/api/client-probe")
def client_probe():
    from datetime import datetime, timezone
    return {
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }



@app.post("/api/client-diagnose")
async def client_diagnose(request: Request):
    from datetime import datetime, timezone
    import statistics

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid diagnostic data")

    server_probes = data.get("server_probes", [])
    external_probes = data.get("external_probes", [])

    if not isinstance(server_probes, list) or not isinstance(external_probes, list):
        raise HTTPException(status_code=400, detail="Invalid probe results")

    if len(server_probes) > 10 or len(external_probes) > 10:
        raise HTTPException(status_code=400, detail="Too many probe results")

    def summarize(probes):
        valid = [
            item for item in probes
            if isinstance(item, dict)
        ]
        successful = [item for item in valid if item.get("success") is True]
        failed = len(valid) - len(successful)

        times = [
            float(item["latency_ms"])
            for item in successful
            if isinstance(item.get("latency_ms"), (int, float))
            and item["latency_ms"] >= 0
        ]

        average = round(statistics.mean(times), 2) if times else None

        return {
            "total": len(valid),
            "successful": len(successful),
            "failed": failed,
            "average_latency_ms": average
        }

    server = summarize(server_probes)
    external = summarize(external_probes)

    browser_online = data.get("browser_online") is True
    connection = data.get("connection") or {}

    if not isinstance(connection, dict):
        connection = {}

    if not browser_online:
        diagnosis = "BROWSER REPORTS OFFLINE"
        confidence = "Limited"
        reason = "The browser reports that this device is offline."

    elif server["successful"] == 0:
        diagnosis = "UNABLE TO REACH NETNEXUS SERVER"
        confidence = "Medium"
        reason = "The browser could not complete requests to the NETNEXUS server."

    elif server["average_latency_ms"] is not None and server["average_latency_ms"] >= 150:
        diagnosis = "ELEVATED LATENCY TO NETNEXUS SERVER"
        confidence = "Medium"
        reason = f"The average response time to NETNEXUS was {server['average_latency_ms']} ms."

    elif external["total"] > 0 and external["successful"] == 0:
        diagnosis = "EXTERNAL CHECKS UNAVAILABLE"
        confidence = "Limited"
        reason = "External resources could not be loaded. This does not establish that the internet connection has failed."

    elif external["failed"] > 0:
        diagnosis = "SOME EXTERNAL CHECKS UNAVAILABLE"
        confidence = "Limited"
        reason = "Some external resource checks did not complete. This may be due to service restrictions or network conditions."

    else:
        diagnosis = "BROWSER CONNECTIVITY CHECKS PASSED"
        confidence = "Medium"
        reason = "NETNEXUS and the tested external services were reachable. External resource loading time is informational and is not used as a pure latency measurement."

    device_type = data.get("device_type", "Computer / Mobile browser")

    def probe_lines(title, probes, names=None):
        lines = [title]

        for index, probe in enumerate(probes):
            name = names[index] if names and index < len(names) else f"Check {index + 1}"

            if probe.get("success") is True:
                latency = probe.get("latency_ms", "Unavailable")
                lines.append(f"  {name}: PASS | Response time: {latency} ms")
            else:
                lines.append(f"  {name}: FAILED")

        if not probes:
            lines.append("  No measurements available")

        return lines

    report_lines = [
        "=" * 65,
        "          NETNEXUS - NETEXPLAIN CONNECTIVITY REPORT",
        "=" * 65,
        "",
        "PROJECT INFORMATION",
        "Team: NETNEXUS",
        "Problem Statement: PS-015",
        "System: Explainable Connectivity Diagnostic System",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "-" * 65,
        "1. DEVICE INFORMATION",
        "-" * 65,
        f"Device category: {device_type}",
        f"Browser online status: {'ONLINE' if browser_online else 'OFFLINE'}",
        f"Connection type: {connection.get('effectiveType') or 'Not provided'}",
        f"Reported downlink: {connection.get('downlink') or 'Not provided'}",
        f"Reported browser RTT: {connection.get('rtt') or 'Not provided'}",
        "",
        "Diagnostic scope: Visitor browser to NETNEXUS and selected external services",
        "",
        "-" * 65,
        "2. NETNEXUS SERVER CONNECTIVITY",
        "-" * 65,
        f"Successful requests: {server['successful']} / {server['total']}",
        f"Failed requests: {server['failed']}",
        f"Average response time: {server['average_latency_ms'] if server['average_latency_ms'] is not None else 'Unavailable'} ms",
        "",
    ]

    report_lines.extend(
        probe_lines("INDIVIDUAL SERVER REQUESTS", server_probes)
    )

    report_lines.extend([
        "",
        "-" * 65,
        "3. EXTERNAL SERVICE CONNECTIVITY",
        "-" * 65,
        f"Successful checks: {external['successful']} / {external['total']}",
        f"Failed checks: {external['failed']}",
        f"Average resource response time: {external['average_latency_ms'] if external['average_latency_ms'] is not None else 'Unavailable'} ms",
        "",
    ])

    report_lines.extend(
        probe_lines(
            "INDIVIDUAL EXTERNAL RESOURCE CHECKS",
            external_probes,
            ["Google resource", "Cloudflare resource"]
        )
    )

    report_lines.extend([
        "",
        "-" * 65,
        "4. DIAGNOSTIC RESULT",
        "-" * 65,
        f"Diagnosis: {diagnosis}",
        f"Confidence: {confidence}",
        f"Explanation: {reason}",
        "",
        "-" * 65,
        "5. EVIDENCE TIMELINE",
        "-" * 65,
        "1. Browser online status checked.",
        f"2. NETNEXUS server requests completed: {server['successful']} successful.",
        f"3. External resource checks completed: {external['successful']} successful.",
        f"4. NETNEXUS average response time: {server['average_latency_ms'] if server['average_latency_ms'] is not None else 'Unavailable'} ms.",
        f"5. External resource average response time: {external['average_latency_ms'] if external['average_latency_ms'] is not None else 'Unavailable'} ms.",
        f"6. Final diagnosis: {diagnosis}.",
        "",
        "-" * 65,
        "6. TECHNICAL LIMITATIONS",
        "-" * 65,
        "- Browser resource loading time is not pure network ping.",
        "- External services may block or restrict browser requests.",
        "- Ordinary browsers cannot perform raw ICMP ping.",
        "- Direct local gateway discovery is unavailable to ordinary browsers.",
        "- These results do not represent a complete internet speed test.",
        "- Browser connection information is not supported by every browser.",
        "",
        "-" * 65,
        "END OF REPORT",
        "NETNEXUS | NetExplain | AIORI PS-015",
        "=" * 65
    ])

    report_text = "\n".join(report_lines)

    return {
        "diagnosis": diagnosis,
        "confidence": confidence,
        "reason": reason,
        "browser_online": browser_online,
        "server_checks": server,
        "external_checks": external,
        "connection": connection,
        "scope": "Visitor browser to NETNEXUS and selected external services",
        "gateway_test": "Not available in ordinary browser",
        "raw_ping": "Not available in ordinary browser",
        "report_text": "\n".join(report_lines),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ======================================================
# TEMPORARY BROWSER PERFORMANCE TEST ENDPOINTS
# No database and no permanent file storage
# ======================================================

@app.get("/api/performance-download")
def performance_download(size: int = 2097152):
    from fastapi.responses import StreamingResponse

    if size < 1 or size > 5242880:
        raise HTTPException(
            status_code=400,
            detail="Download size must be between 1 byte and 5 MB."
        )

    chunk = b"0" * 65536
    remaining = size

    def generate_data():
        nonlocal remaining
        while remaining > 0:
            amount = min(len(chunk), remaining)
            yield chunk[:amount]
            remaining -= amount

    return StreamingResponse(
        generate_data(),
        media_type="application/octet-stream",
        headers={
            "Content-Length": str(size),
            "Cache-Control": "no-store, no-cache, must-revalidate"
        }
    )


@app.post("/api/performance-upload")
async def performance_upload(request: Request):
    content_length = request.headers.get("content-length")

    if content_length:
        try:
            if int(content_length) > 2097152:
                raise HTTPException(
                    status_code=413,
                    detail="Upload is larger than the allowed limit."
                )
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid content length."
            )

    body = await request.body()

    if len(body) > 2097152:
        raise HTTPException(
            status_code=413,
            detail="Upload is larger than the allowed limit."
        )

    return {
        "status": "received",
        "bytes_received": len(body),
        "scope": "Browser to NETNEXUS server"
    }
