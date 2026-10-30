let lastReport = "";
const HISTORY_KEY = "netnexus_diagnosis_history";

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch {
        return [];
    }
}

function saveHistory(data, type) {
    const history = getHistory();

    history.unshift({
        id: Date.now(),
        type,
        timestamp: new Date().toISOString(),
        diagnosis: data.diagnosis || "Unknown",
        confidence: data.confidence || "Not available",
        report: data
    });

    localStorage.setItem(
        HISTORY_KEY,
        JSON.stringify(history.slice(0, 100))
    );

    renderHistory();
}

function displayResult(container, data, labels) {
    container.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = data.diagnosis || "Diagnosis completed";
    container.appendChild(heading);

    labels.forEach(([label, value]) => {
        const paragraph = document.createElement("p");
        paragraph.textContent = label + ": " + value;
        container.appendChild(paragraph);
    });
}



function displayEvidenceTables(container, evidence) {
    if (!evidence || typeof evidence !== "object") return;

    function createTable(title, rows) {
        const section = document.createElement("section");
        section.className = "scenario-evidence";

        const heading = document.createElement("h3");
        heading.textContent = title;
        section.appendChild(heading);

        const table = document.createElement("table");
        table.className = "evidence-table";

        const thead = document.createElement("thead");
        const headerRow = document.createElement("tr");

        ["Measurement", "Value", "Status"].forEach(label => {
            const th = document.createElement("th");
            th.textContent = label;
            headerRow.appendChild(th);
        });

        thead.appendChild(headerRow);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");

        rows.forEach(([measurement, value, status]) => {
            const row = document.createElement("tr");

            [measurement, value, status].forEach((text, index) => {
                const cell = document.createElement("td");
                cell.textContent = text == null ? "Not available" : String(text);

                if (index === 2) {
                    cell.className = String(status).toLowerCase().includes("pass")
                        ? "evidence-pass"
                        : String(status).toLowerCase().includes("fail")
                            ? "evidence-fail"
                            : "evidence-neutral";
                }

                row.appendChild(cell);
            });

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        section.appendChild(table);
        container.appendChild(section);
    }

    const gateway = evidence.gateway_test || {};
    const dns = evidence.dns_test || {};
    const internet = evidence.internet_test || {};
    const throughput = evidence.throughput_test || {};

    createTable("SCENARIO EVIDENCE", [
        [
            "Gateway",
            gateway.host || evidence.gateway || "Not available",
            gateway.reachable === true ? "PASS" :
                gateway.reachable === false ? "FAIL" : "NOT AVAILABLE"
        ],
        [
            "Gateway latency",
            gateway.latency_ms == null ? "Not available" : gateway.latency_ms + " ms",
            "SIMULATED"
        ],
        [
            "DNS",
            dns.hostname || "Not available",
            dns.success === true ? "PASS" :
                dns.success === false ? "FAIL" : "NOT AVAILABLE"
        ],
        [
            "Resolved IP",
            dns.resolved_ip || "Not available",
            dns.success === true ? "RESOLVED" : "NOT AVAILABLE"
        ],
        [
            "DNS resolution time",
            dns.resolution_ms == null ? "Not available" : dns.resolution_ms + " ms",
            "SIMULATED"
        ],
        [
            "External reachability",
            internet.host || "Not available",
            internet.reachable === true ? "PASS" :
                internet.reachable === false ? "FAIL" : "NOT AVAILABLE"
        ],
        [
            "Packet loss",
            internet.packet_loss_percent == null
                ? "Not available"
                : internet.packet_loss_percent + "%",
            "SIMULATED"
        ],
        [
            "Latency",
            internet.latency_ms == null
                ? "Not available"
                : internet.latency_ms + " ms",
            "SIMULATED"
        ]
    ]);

    createTable("THROUGHPUT EVIDENCE", [
        [
            "Throughput",
            throughput.throughput_mbps == null
                ? "Not available"
                : throughput.throughput_mbps + " Mbps",
            throughput.success ? "SIMULATED PASS" : "NOT AVAILABLE"
        ],
        [
            "Loaded condition",
            throughput.loaded_condition ? "YES" : "NO",
            "SIMULATED"
        ],
        [
            "Source",
            throughput.source || "Not available",
            "REFERENCE"
        ]
    ]);

    const note = document.createElement("p");
    note.className = "simulation-note";
    note.textContent =
        "NOTE: These are controlled scenario simulation values, not live measurements from the visitor's device.";

    container.appendChild(note);
}



function displayLiveEvidenceTables(container, data) {
    const server = data.server_checks || {};
    const external = data.external_checks || {};
    const connection = data.connection || {};

    function createEvidenceTable(title, rows, note) {
        const section = document.createElement("section");
        section.className = "scenario-evidence";

        const heading = document.createElement("h3");
        heading.textContent = title;
        section.appendChild(heading);

        const table = document.createElement("table");
        table.className = "evidence-table";

        const thead = document.createElement("thead");
        const header = document.createElement("tr");

        ["Measurement", "Value", "Status"].forEach(label => {
            const th = document.createElement("th");
            th.textContent = label;
            header.appendChild(th);
        });

        thead.appendChild(header);
        table.appendChild(thead);

        const tbody = document.createElement("tbody");

        rows.forEach(([label, value, status]) => {
            const row = document.createElement("tr");

            [label, value, status].forEach((text, index) => {
                const cell = document.createElement("td");
                cell.textContent = String(text);

                if (index === 2) {
                    cell.className = String(status).includes("PASS")
                        ? "evidence-pass"
                        : String(status).includes("FAIL")
                            ? "evidence-fail"
                            : "evidence-neutral";
                }

                row.appendChild(cell);
            });

            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        section.appendChild(table);

        const message = document.createElement("p");
        message.className = "simulation-note";
        message.textContent = note;
        section.appendChild(message);

        container.appendChild(section);
    }

    createEvidenceTable("LIVE NETWORK EVIDENCE", [
        [
            "Gateway",
            "Not accessible from ordinary browser",
            "NOT AVAILABLE"
        ],
        [
            "Gateway latency",
            "Not measured",
            "NOT AVAILABLE"
        ],
        [
            "DNS",
            "Checked indirectly through browser resource requests",
            "LIMITED CHECK"
        ],
        [
            "Resolved IP",
            "Not exposed to ordinary browser",
            "NOT AVAILABLE"
        ],
        [
            "DNS resolution time",
            "Not measured separately",
            "NOT AVAILABLE"
        ],
        [
            "External reachability",
            `${external.successful ?? 0} / ${external.total ?? 0} successful checks`,
            (external.successful ?? 0) > 0 ? "PASS" : "CHECK"
        ],
        [
            "Packet loss",
            "Not directly measurable by ordinary browser",
            "NOT AVAILABLE"
        ],
        [
            "NETNEXUS server latency",
            server.average_latency_ms == null
                ? "Not available"
                : server.average_latency_ms + " ms",
            server.average_latency_ms == null ? "NOT AVAILABLE" : "LIVE MEASUREMENT"
        ],
        [
            "Connection type",
            connection.effectiveType || connection.type || "Not provided",
            "BROWSER INFORMATION"
        ]
    ], "Measurements are collected from the visitor's browser. Browser resource loading checks are not equivalent to direct DNS queries or ICMP ping.");

    createEvidenceTable("THROUGHPUT EVIDENCE", [
        ["Throughput", "Not measured yet", "NOT AVAILABLE"],
        ["Loaded condition", "Not measured yet", "NOT AVAILABLE"],
        ["Source", "Visitor's browser", "REFERENCE"]
    ], "A live download measurement will be added separately. No sample throughput value is being presented as a real measurement.");
}
async function testExternalResource(url) {
    return new Promise(resolve => {
        const image = new Image();
        const started = performance.now();
        let finished = false;

        const timeout = setTimeout(() => {
            if (finished) return;
            finished = true;
            image.src = "";
            resolve({ success: false, latency_ms: null });
        }, 8000);

        image.onload = () => {
            if (finished) return;
            finished = true;
            clearTimeout(timeout);
            resolve({
                success: true,
                latency_ms: Number((performance.now() - started).toFixed(2))
            });
        };

        image.onerror = () => {
            if (finished) return;
            finished = true;
            clearTimeout(timeout);
            resolve({ success: false, latency_ms: null });
        };

        image.src = url + "?netnexus=" + Date.now() + Math.random();
    });
}

async function runBrowserProbes() {
    const serverProbes = [];

    for (let i = 0; i < 5; i++) {
        const controller = new AbortController();
        const started = performance.now();
        const timeout = setTimeout(() => controller.abort(), 5000);

        try {
            const response = await fetch(
                "/api/client-probe?test=" + Date.now() + "-" + i,
                {
                    method: "GET",
                    cache: "no-store",
                    signal: controller.signal
                }
            );

            if (!response.ok) {
                throw new Error("HTTP " + response.status);
            }

            serverProbes.push({
                success: true,
                latency_ms: Number((performance.now() - started).toFixed(2))
            });
        } catch (error) {
            serverProbes.push({
                success: false,
                error: error.message
            });
        } finally {
            clearTimeout(timeout);
        }
    }

    const externalProbes = await Promise.all([
        testExternalResource("https://www.google.com/favicon.ico"),
        testExternalResource("https://www.cloudflare.com/favicon.ico")
    ]);

    return {
        server: serverProbes,
        external: externalProbes
    };
}

async function diagnose() {
    const output = document.getElementById("liveResult");
    output.textContent =
        "Testing this device's connection to NETNEXUS and external services...";

    try {
        const probes = await runBrowserProbes();

        const network =
            navigator.connection ||
            navigator.mozConnection ||
            navigator.webkitConnection;

        const connection = network ? {
            effectiveType: network.effectiveType || null,
            type: network.type || null,
            downlink: network.downlink ?? null,
            rtt: network.rtt ?? null
        } : {};

        const response = await fetch("/api/client-diagnose", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                browser_online: navigator.onLine,
                device_type: /Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ? "Mobile / Tablet" : "Desktop / Laptop",
                server_probes: probes.server,
                external_probes: probes.external,
                connection
            })
        });

        if (!response.ok) {
            throw new Error("Server returned HTTP " + response.status);
        }

        const data = await response.json();

        lastReport = data.report_text ||
            JSON.stringify(data, null, 4);

        displayResult(output, data, [
            ["Confidence", data.confidence],
            ["Browser online", data.browser_online ? "Yes" : "No"],
            ["NETNEXUS successful requests",
                data.server_checks?.successful + " / " + data.server_checks?.total],
            ["NETNEXUS failed requests",
                data.server_checks?.failed],
            ["NETNEXUS average response time",
                data.server_checks?.average_latency_ms == null
                    ? "Unavailable"
                    : data.server_checks.average_latency_ms + " ms"],
            ["External successful checks",
                data.external_checks?.successful + " / " + data.external_checks?.total],
            ["External failed checks",
                data.external_checks?.failed],
            ["External average resource response time",
                data.external_checks?.average_latency_ms == null
                    ? "Unavailable"
                    : data.external_checks.average_latency_ms + " ms"],
            ["Connection type",
                data.connection?.effectiveType || "Not provided"],
            ["Diagnostic scope", data.scope],
            ["Gateway test", data.gateway_test],
            ["Explanation", data.reason]
        ]);

        displayLiveEvidenceTables(output, data);

        displayTimeline(output, [
            "Browser online status: " + (data.browser_online ? "Online" : "Offline"),
            "NETNEXUS server checks passed: " + data.server_checks?.successful,
            "External service checks passed: " + data.external_checks?.successful,
            "NETNEXUS average response time: " +
                (data.server_checks?.average_latency_ms ?? "Unavailable") + " ms",
            "External average resource response time: " +
                (data.external_checks?.average_latency_ms ?? "Unavailable") + " ms",
            "Final result: " + data.diagnosis
        ]);

        saveHistory(data, "Computer / Mobile Browser Live Diagnosis");

    } catch (error) {
        output.textContent = "Diagnosis failed: " + error.message;
    }
}

async function runScenario() {
    const scenario = document.getElementById("scenario").value;
    const output = document.getElementById("scenarioResult");

    output.textContent = "Running controlled fault simulation...";

    try {
        const response = await fetch(
            "/api/scenario/" + encodeURIComponent(scenario),
            { method: "POST" }
        );

        if (!response.ok) {
            throw new Error("Server returned HTTP " + response.status);
        }

        const data = await response.json();

        lastReport = data.report_text ||
            JSON.stringify(data, null, 4);

        displayResult(output, data, [
            ["Scenario", data.scenario],
            ["Confidence", data.confidence],
            ["Simulation", data.simulated ? "Yes" : "No"],
            ["Explanation", data.reason || "See report for details"]
        ]);

        displayEvidenceTables(output, data.evidence);
        displayTimeline(output, data.timeline);

        saveHistory(data, "Fault Scenario");

    } catch (error) {
        output.textContent = "Scenario failed: " + error.message;
    }
}

function renderHistory() {
    const container = document.getElementById("historyList");
    if (!container) return;

    const history = getHistory();
    container.replaceChildren();

    if (history.length === 0) {
        const message = document.createElement("p");
        message.textContent = "No diagnosis history yet.";
        container.appendChild(message);
        return;
    }

    history.forEach((entry, index) => {
        const item = document.createElement("div");
        item.className = "history-item";

        const title = document.createElement("h3");
        title.textContent = entry.diagnosis;

        const type = document.createElement("p");
        type.textContent = entry.type;

        const date = document.createElement("p");
        date.textContent = new Date(entry.timestamp).toLocaleString();

        const confidence = document.createElement("p");
        confidence.textContent = "Confidence: " + entry.confidence;

        const viewButton = document.createElement("button");
        viewButton.textContent = "VIEW REPORT";
        viewButton.addEventListener("click", () => viewHistory(index));

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "DELETE";
        deleteButton.addEventListener("click", () => deleteHistory(index));

        item.append(
            title, type, date, confidence, viewButton, deleteButton
        );

        container.appendChild(item);
    });
}

function viewHistory(index) {
    const entry = getHistory()[index];
    if (!entry) return;

    lastReport = entry.report.report_text ||
        JSON.stringify(entry.report, null, 4);

    const details = document.getElementById("historyDetails");
    details.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = "Previous Diagnosis";

    const result = document.createElement("pre");
    result.textContent = lastReport;

    const downloadButton = document.createElement("button");
    downloadButton.textContent = "DOWNLOAD THIS REPORT";
    downloadButton.addEventListener("click", downloadReport);

    details.append(heading, result, downloadButton);
    details.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function deleteHistory(index) {
    const history = getHistory();
    history.splice(index, 1);

    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));

    document.getElementById("historyDetails").replaceChildren();
    renderHistory();
}

function clearHistory() {
    if (!confirm("Delete all diagnosis history from this browser?")) {
        return;
    }

    localStorage.removeItem(HISTORY_KEY);
    document.getElementById("historyDetails").replaceChildren();
    renderHistory();
}

function downloadReport() {
    if (!lastReport) {
        alert("Run a diagnosis or select a previous report first.");
        return;
    }

    const blob = new Blob(
        [lastReport],
        { type: "text/plain;charset=utf-8" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "NETNEXUS-Report.txt";
    link.click();

    setTimeout(() => URL.revokeObjectURL(url), 1000);
}

document.addEventListener("DOMContentLoaded", renderHistory);

function displayTimeline(container, events) {
    const section = document.createElement("div");
    section.className = "evidence-timeline";

    const heading = document.createElement("h3");
    heading.textContent = "DIAGNOSTIC EVIDENCE TIMELINE";
    section.appendChild(heading);

    if (!Array.isArray(events) || events.length === 0) {
        const message = document.createElement("p");
        message.textContent = "No additional timeline evidence available.";
        section.appendChild(message);
    } else {
        const list = document.createElement("ol");

        events.forEach(event => {
            const item = document.createElement("li");
            item.textContent = typeof event === "string"
                ? event
                : JSON.stringify(event);
            list.appendChild(item);
        });

        section.appendChild(list);
    }

    container.appendChild(section);
}




// ======================================================
// COMPUTER-BASED NETWORK CHECK
// Browser-accessible device information only
// ======================================================

async function runComputerCheck() {
    const output = document.getElementById("computerResult");
    output.textContent = "Collecting browser-accessible device information...";

    try {
        const network =
            navigator.connection ||
            navigator.mozConnection ||
            navigator.webkitConnection;

        const deviceType =
            /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)
                ? "Mobile / Tablet"
                : "Desktop / Laptop";

        const details = {
            "Device category": deviceType,
            "Browser online status": navigator.onLine ? "Online" : "Offline",
            "Browser language": navigator.language || "Unavailable",
            "Platform information": navigator.userAgentData?.platform ||
                navigator.platform || "Not provided",
            "Screen resolution": screen.width + " x " + screen.height,
            "Browser connection type": network?.effectiveType || "Not supported",
            "Reported downlink": network?.downlink != null
                ? network.downlink + " Mbps"
                : "Not provided",
            "Reported browser RTT": network?.rtt != null
                ? network.rtt + " ms"
                : "Not provided"
        };

        const result = {
            diagnosis: "DEVICE INFORMATION CHECK COMPLETED",
            confidence: "Browser-reported information",
            reason: "These details are limited to information exposed by the visitor's browser.",
            details,
            report_text: [
                "NETNEXUS - COMPUTER-BASED NETWORK CHECK",
                "Generated: " + new Date().toISOString(),
                "",
                ...Object.entries(details).map(([key, value]) => key + ": " + value),
                "",
                "LIMITATIONS:",
                "This is not direct operating-system inspection.",
                "Gateway discovery and raw ping are unavailable to ordinary browsers."
            ].join("\n"),
            timestamp: new Date().toISOString()
        };

        displayResult(output, result, [
            ...Object.entries(details),
            ["Scope", "Information available to this browser"],
            ["Gateway discovery", "Not available in ordinary browsers"],
            ["Raw ping", "Not available in ordinary browsers"]
        ]);

        lastReport = result.report_text;
        saveHistory(result, "Computer-Based Network Check");

    } catch (error) {
        output.textContent = "Device check failed: " + error.message;
    }
}


// ======================================================
// NETWORK PERFORMANCE TEST
// Measures browser <-> NETNEXUS server transfer speed
// ======================================================

async function runPerformanceTest() {
    const output = document.getElementById("performanceResult");
    const button = document.getElementById("performanceButton");

    button.disabled = true;
    output.textContent = "Running download and upload measurements...";

    try {
        const downloadSize = 2 * 1024 * 1024;
        const uploadSize = 1 * 1024 * 1024;

        // DOWNLOAD TEST
        const downloadStart = performance.now();

        const downloadResponse = await fetch(
            "/api/performance-download?size=" + downloadSize + "&t=" + Date.now(),
            { cache: "no-store" }
        );

        if (!downloadResponse.ok) {
            throw new Error("Download test returned HTTP " + downloadResponse.status);
        }

        const downloadedData = await downloadResponse.arrayBuffer();
        const downloadSeconds = (performance.now() - downloadStart) / 1000;

        if (downloadSeconds <= 0 || downloadedData.byteLength === 0) {
            throw new Error("Download measurement was incomplete.");
        }

        const downloadMbps =
            (downloadedData.byteLength * 8) / downloadSeconds / 1000000;

        // UPLOAD TEST
        const uploadData = new Uint8Array(uploadSize);
        const uploadStart = performance.now();

        const uploadResponse = await fetch("/api/performance-upload", {
            method: "POST",
            headers: { "Content-Type": "application/octet-stream" },
            body: uploadData
        });

        if (!uploadResponse.ok) {
            throw new Error("Upload test returned HTTP " + uploadResponse.status);
        }

        const uploadResult = await uploadResponse.json();
        const uploadSeconds = (performance.now() - uploadStart) / 1000;

        if (uploadSeconds <= 0 || uploadResult.bytes_received !== uploadSize) {
            throw new Error("Upload measurement was incomplete.");
        }

        const uploadMbps =
            (uploadResult.bytes_received * 8) / uploadSeconds / 1000000;

        const result = {
            diagnosis: "NETWORK PERFORMANCE TEST COMPLETED",
            confidence: "Measured browser-to-server transfer",
            reason: "The measurements represent data transfer between this browser and the NETNEXUS server.",
            download_mbps: Number(downloadMbps.toFixed(2)),
            upload_mbps: Number(uploadMbps.toFixed(2)),
            download_bytes: downloadedData.byteLength,
            upload_bytes: uploadResult.bytes_received,
            download_seconds: Number(downloadSeconds.toFixed(3)),
            upload_seconds: Number(uploadSeconds.toFixed(3)),
            report_text: [
                "NETNEXUS - NETWORK PERFORMANCE REPORT",
                "Generated: " + new Date().toISOString(),
                "",
                "Download speed: " + downloadMbps.toFixed(2) + " Mbps",
                "Upload speed: " + uploadMbps.toFixed(2) + " Mbps",
                "Download data: " + downloadedData.byteLength + " bytes",
                "Upload data: " + uploadResult.bytes_received + " bytes",
                "Download duration: " + downloadSeconds.toFixed(3) + " seconds",
                "Upload duration: " + uploadSeconds.toFixed(3) + " seconds",
                "",
                "SCOPE: Browser to NETNEXUS server.",
                "These results are not a measurement of total internet speed."
            ].join("\n"),
            timestamp: new Date().toISOString()
        };

        displayResult(output, result, [
            ["Download speed", result.download_mbps + " Mbps"],
            ["Upload speed", result.upload_mbps + " Mbps"],
            ["Download data", result.download_bytes + " bytes"],
            ["Upload data", result.upload_bytes + " bytes"],
            ["Download duration", result.download_seconds + " seconds"],
            ["Upload duration", result.upload_seconds + " seconds"],
            ["Measurement scope", "Browser to NETNEXUS server"]
        ]);

        lastReport = result.report_text;
        saveHistory(result, "Network Performance Test");

    } catch (error) {
        output.textContent = "Performance test failed: " + error.message;
    } finally {
        button.disabled = false;
    }
}
