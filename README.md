# NETNEXUS – NetExplain
### Explainable Connectivity Diagnostic System | AIORI-3 Hackathon

**Team Name:** NETNEXUS  
**Team Code:** A3-PS015-TC086  
**Problem Statement:** PS-015  
**Project:** NetExplain – Explainable Connectivity Diagnostic System

## Team Introduction Video

**YouTube Video:** [Watch our team introduction video](https://youtu.be/Uk20ocYenkc?feature=shared)

---

## 1. Project Overview

NETNEXUS – NetExplain is a browser-based network connectivity diagnostic system designed to help users understand network problems through simple, evidence-based checks.

The system examines browser-accessible connectivity information, measures communication performance with the NETNEXUS server, demonstrates common network faults through controlled simulations, and generates understandable diagnostic reports.

Our goal is to make network troubleshooting easier for users without requiring advanced technical knowledge or additional software installation.

## 2. Problem Statement

Network connectivity issues can be difficult for ordinary users to identify and understand. Problems involving connection availability, external service reachability, response delays and network performance often require technical knowledge and diagnostic tools.

NetExplain addresses this challenge by providing a simple web platform that performs accessible checks and explains the evidence behind its results.

## 3. Proposed Solution

The project provides the following features:

### A. Live Network Diagnosis
- Checks browser online status.
- Tests connectivity to the NETNEXUS server.
- Checks selected external web resources.
- Measures server response times.
- Displays diagnostic results, explanations and evidence timelines.

### B. Computer-Based Network Check
- Identifies device category.
- Displays browser online status.
- Reports available platform and browser information.
- Displays screen resolution.
- Shows browser-reported connection information when supported.

### C. Network Performance Test
- Measures download performance.
- Measures upload performance.
- Calculates data transfer speeds in Mbps.
- Displays transfer size and duration.

*Performance measurements represent communication between the visitor's browser and the NETNEXUS server.*

### D. Controlled Fault Scenarios

The system demonstrates six network conditions:

1. Normal Connection
2. Gateway Unreachable
3. DNS Failure
4. Induced Packet Loss
5. Network Congestion
6. Inconclusive

These scenarios use controlled simulated evidence and do not create actual faults on the visitor's device.

## 4. Reports and Diagnosis History

- Generates downloadable diagnostic reports.
- Displays supporting evidence and explanations.
- Maintains diagnosis history in browser local storage.
- Allows users to view, download and delete previous results.

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | Backend web framework |
| HTML | Website structure |
| CSS | Website styling |
| JavaScript | Browser-side functionality |
| Uvicorn | Application server |
| Jinja2 | HTML template rendering |
| Render | Cloud deployment |

## 6. System Architecture

The application follows a client-server architecture.

1. The frontend provides the user interface.
2. JavaScript performs browser-accessible checks and performance measurements.
3. FastAPI receives requests and processes diagnostic evidence.
4. Python generates diagnostic results and reports.
5. Render hosts the application for public access.

## 7. Key Advantages

- Simple browser-based interface.
- No API keys required.
- No central database required.
- No additional software installation for visitors.
- Desktop and mobile browser accessibility.
- Explainable diagnostic results.
- Evidence-based reporting.
- Controlled network fault simulations.

## 8. Technical Limitations

Ordinary browsers restrict direct access to certain operating-system and network functions. Therefore, this system does not claim to perform direct gateway discovery, raw ICMP ping or actual packet-loss measurements on the visitor's network.

Browser-reported connection information may also vary depending on browser support.

## 9. Future Scope

- Additional browser-compatible network checks.
- Improved diagnostic explanations.
- More detailed performance analysis.
- Expanded fault simulation scenarios.
- Enhanced report visualizations.

## 10. Conclusion

NETNEXUS – NetExplain aims to make network connectivity diagnosis more accessible and understandable. By combining browser-based connectivity checks, device information, performance measurements, controlled fault simulations and downloadable reports, the system helps users understand observable network conditions through a simple web application.
## 🌐 Live Website

**NETNEXUS – NetExplain is live!**

Visit our deployed application:

🔗 **[Open NETNEXUS Live Website](https://a3-ps015-tc086.onrender.com/)**


---

**NETNEXUS | NetExplain**  
*Making Network Diagnostics Understandable.*  
**AIORI-3 Hackathon | PS-015**
