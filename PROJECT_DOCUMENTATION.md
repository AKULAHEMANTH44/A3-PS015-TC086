# NETNEXUS
## NetExplain – Explainable Connectivity Diagnostic System

**Problem Statement:** PS-015  
**Team Name:** NETNEXUS  
**Team Code:** A3-PS015-TC086  
**Project Category:** Network Diagnostics and Connectivity Monitoring

---

# 1. Introduction

In our everyday lives, the internet has become an important part of almost everything we do. We depend on it for online classes, communication, office work, entertainment, and many other activities.

However, internet connectivity problems can occur at any time. Sometimes a website takes too long to load, a connection becomes unstable, or network performance suddenly decreases. Although users experience these problems, they often do not know what is causing them or how to understand the issue.

To address this problem, our team developed **NETNEXUS – NetExplain**, an Explainable Connectivity Diagnostic System.

NETNEXUS is a web-based application that helps users examine network connectivity, understand possible performance issues, run controlled fault simulations, and view diagnostic reports. Instead of presenting only technical results, the system aims to explain the findings in a simple and understandable manner.

# 2. Problem Statement

Network connectivity problems are common, but identifying their actual cause is not always easy for ordinary users.

Many existing diagnostic approaches display technical information such as latency, packet loss, DNS errors, and connection failures. Users without networking knowledge may find these results difficult to understand.

There is a need for a simple and accessible system that can examine available network information, identify possible connectivity issues, and explain the results in a user-friendly way.

# 3. Proposed Solution

We propose NETNEXUS, a browser-based connectivity diagnostic platform that brings multiple network-checking features together in one place.

The application provides different diagnostic options so users can examine their connectivity, check browser-accessible device and network information, perform a browser-to-server performance test, and understand simulated network faults.

The main focus of our project is not just detecting an issue, but also helping users understand what the result means.

The application runs through a website, so users do not need to install a separate desktop application or configure an external database or API key.

# 4. Main Objectives

The major objectives of NETNEXUS are:

1. To provide an easy-to-use network diagnostic interface.
2. To examine available network connectivity information.
3. To identify and explain possible network-related problems.
4. To provide a browser-based computer and network check.
5. To measure data transfer performance between the browser and the hosted server.
6. To demonstrate different network fault conditions through controlled simulations.
7. To generate useful diagnostic reports and maintain diagnosis history.
8. To make network diagnostic information understandable to non-technical users.

# 5. Key Features

## 5.1 Live Network Diagnosis

This feature allows users to perform a connectivity diagnosis using the diagnostic capabilities available in the application.

The system examines the available diagnostic information and presents the result with an explanation. It helps users understand whether a possible connectivity issue has been identified.

## 5.2 Computer-Based Network Check

This feature collects information that the user's web browser makes available.

It can examine information such as:

- Browser connectivity status.
- Available network connection information.
- Device and browser details.
- Screen and system-related information supported by the browser.

This provides users with a basic overview of their browsing environment.

## 5.3 Network Performance Test

The Network Performance Test checks the data transfer performance between the user's browser and the NETNEXUS hosted server.

It performs download and upload operations and calculates the time taken for the data transfer.

The results help users understand the responsiveness and transfer performance of the connection to our application server.

**Note:** This is a browser-to-server performance measurement. It should not be treated as a certified measurement of the user's complete internet or ISP speed.

## 5.4 Controlled Fault Scenarios

This feature demonstrates different network fault conditions in a controlled environment.

The system includes scenarios such as:

- Normal Connection
- Gateway Unreachable
- DNS Failure
- Induced Packet Loss
- Network Congestion
- Inconclusive Diagnosis

These scenarios help demonstrate how different connectivity conditions can affect diagnostic results.

The scenarios are simulations and are not necessarily real faults occurring on the user's device.

## 5.5 Reports and Evidence

NETNEXUS provides a reports section where diagnostic findings and supporting evidence can be presented in an organized format.

This helps users review the results rather than depending only on temporary messages displayed during a diagnosis.

## 5.6 Diagnosis History

The diagnosis history feature helps users revisit previous diagnostic results available in the application.

It makes it easier to compare previous checks and understand the results of different diagnostic activities.

# 6. System Architecture

NETNEXUS follows a simple web-based architecture with three main parts.

### A. Frontend

The frontend is developed using:

- HTML – Defines the structure of the website.
- CSS – Handles the visual appearance and dashboard design.
- JavaScript – Manages user interactions and communicates with the backend.

### B. Backend

The backend is developed using Python and FastAPI.

It handles application requests, processes diagnostic operations, performs server-side functions, and returns results to the frontend.

### C. Diagnostic Engine

The diagnostic engine contains the logic used to process diagnostic information and classify possible network conditions.

It helps organize the available evidence and present understandable diagnostic results.

### Overall Workflow

1. The user opens the NETNEXUS website.
2. The user selects a diagnostic feature.
3. The frontend sends the required request to the backend.
4. The backend processes the request using the relevant application logic.
5. The system prepares the diagnostic result.
6. The result is displayed through the dashboard.
7. The user can review the available reports and diagnosis history.

# 7. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development and diagnostic logic |
| FastAPI | Backend web framework |
| HTML | Website structure |
| CSS | Website styling |
| JavaScript | Frontend interaction |
| Uvicorn | Running the FastAPI application |
| Jinja2 | Rendering HTML templates |
| Git and GitHub | Source code management |
| Render | Website hosting and deployment |

The project uses a Python-based backend with standard web technologies for the frontend.

# 8. Working Methodology

The working process of NETNEXUS can be divided into the following stages.

**Stage 1 – User Interaction**

The user accesses the website and chooses the required diagnostic operation.

**Stage 2 – Information Collection**

The application collects the information required for the selected operation. Depending on the feature, this may include browser information, connectivity status, server responses, or simulated test conditions.

**Stage 3 – Processing**

The backend processes the received information using the relevant diagnostic functions.

**Stage 4 – Result Classification**

The diagnostic engine evaluates the available evidence and prepares an appropriate result.

**Stage 5 – Explanation**

The application presents the findings in a simple format so users can understand the possible problem.

**Stage 6 – Report and History**

The user can review the available diagnostic evidence and previous results.

# 9. Deployment

NETNEXUS is deployed as a live web application using Render.

The application is connected to its GitHub repository, allowing the deployment to be updated when new code is pushed.

The deployment uses Python dependencies from the requirements file and starts the FastAPI application through Uvicorn.

Users can access the hosted application through a web browser without installing the project on their computers.

**Live Website:**  
[Insert your actual Render website URL]

**GitHub Repository:**  
https://github.com/AKULAHEMANTH44/A3-PS015-TC086

# 10. Testing and Verification

After development and deployment, the team tested the major features of the application.

The following features were verified on the live website:

1. Live Network Diagnosis.
2. Computer-Based Network Check.
3. Network Performance Test.
4. Controlled Fault Scenarios.
5. Reports and Evidence.
6. Diagnosis History.

The team also checked the website's dashboard styling and general functionality after deployment.

All six major features were verified successfully on the deployed application.

# 11. Advantages

- Easy-to-use web interface.
- No separate desktop installation required.
- Multiple diagnostic features in one platform.
- Human-readable diagnostic explanations.
- Controlled network fault demonstrations.
- Organized diagnostic reports.
- Accessible through a hosted website.
- Python-based backend architecture.
- No external API key or database required for the current implementation.

# 12. Limitations

Although NETNEXUS provides several useful diagnostic features, certain limitations should be considered.

- Web browsers restrict direct access to some low-level network information.
- Actual gateway discovery and raw ICMP testing are not generally available to ordinary browser applications.
- Some network information depends on browser and device support.
- The performance test measures transfers between the browser and the NETNEXUS server, not the complete ISP connection.
- Controlled fault scenarios demonstrate simulated conditions rather than necessarily detecting real faults on the user's network.
- Results depend on the information and diagnostic capabilities available during testing.

These limitations are important because the application aims to provide understandable and honest diagnostic results.

# 13. Future Enhancements

In the future, NETNEXUS can be improved by introducing additional capabilities, such as:

1. More advanced network diagnostic techniques.
2. Improved connectivity analysis.
3. Better historical comparison of diagnostic results.
4. Additional network fault scenarios.
5. More detailed evidence visualization.
6. Improved report generation.
7. Support for additional devices and browsers.
8. Enhanced performance analysis.

These improvements can make the system more useful for users who want to understand network connectivity issues in greater detail.

# 14. Conclusion

NETNEXUS – NetExplain was developed with the goal of making network diagnostics easier to understand and access.

During development, our team focused on combining different diagnostic features into a single web application. We worked on connectivity diagnosis, browser-based computer checks, network performance testing, controlled fault simulations, reports, and diagnosis history.

One of the important aspects of this project is its focus on explainability. We believe that identifying a possible network issue is useful, but explaining the result in a way that ordinary users can understand is equally important.

The application has been deployed successfully on Render, and all six major features have been verified on the live website.

Through NETNEXUS, our team aims to make network troubleshooting more accessible, understandable, and user-friendly.

---

# 15. Team Information

**Team Name:** NETNEXUS  
**Problem Statement:** PS-015  
**Team Code:** A3-PS015-TC086

**Project:** NetExplain – Explainable Connectivity Diagnostic System

**Repository:**  
https://github.com/AKULAHEMANTH44/A3-PS015-TC086

**Deployment:**  
[https://a3-ps015-tc086.onrender.com/]

**Developed as part of:** AIORI Hackathon

