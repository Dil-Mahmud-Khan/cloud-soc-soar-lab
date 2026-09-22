# Architecture & Data Flow Breakdown

This document details how data, alerts, and API calls flow between each component of the **Cloud EDR & SOAR Pipeline**.

---

## 1. High-Level Architectural Flowchart

```
+-----------------------------------------------------------------------------------+
|                              1. ATTACK EXECUTION                                 |
|                                                                                   |
|  Target Machine: Windows 10/11 Enterprise                                        |
|  Execution: Atomic Red Team / PowerShell Script                                   |
|  Attacks:                                                                         |
|    - T1105: Ingress Tool Transfer (certutil.exe -urlcache -split -f)               |
|    - T1003.001: OS Credential Dumping (LSASS memory handle open)                  |
|    - T1059.001: Obfuscated PowerShell execution                                  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | Real-time Kernel & Process Telemetry
                                          v
+-----------------------------------------------------------------------------------+
|                        2. DETECTION & RESPONSE (EDR)                             |
|                                                                                   |
|  Platform: LimaCharlie Cloud EDR (Sensor Agent on Windows)                        |
|  Mechanism:                                                                       |
|    - Captures Process Tree (parent -> child), CLI arguments, and file hashes     |
|    - Evaluates events against custom D&R (Detection & Response) YAML rules        |
|    - Matches suspicious behavior and generates a Detection Event                  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | Webhook POST (JSON Event Payload)
                                          v
+-----------------------------------------------------------------------------------+
|                        3. SOAR AUTOMATION ENGINE                                 |
|                                                                                   |
|  Platform: Tines Cloud Community Edition                                         |
|  Actions Executed:                                                                |
|    1. Webhook Action: Ingests raw JSON payload from LimaCharlie                   |
|    2. Data Transformation: Extracts {hostname, ip, process, hash, command_line}   |
|    3. HTTP Request: Queries VirusTotal API v3 (GET /api/v3/files/{hash})          |
|    4. Decision Node: Evaluates VT reputation score & suspicious flags            |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | Webhook POST (Formatted Message Card)
                                          v
+-----------------------------------------------------------------------------------+
|                    4. SOC COMMUNICATION & TRIAGE                                  |
|                                                                                   |
|  Platform: Slack (Private #soc-alerts channel)                                   |
|  Output: Structured Incident Card displaying:                                    |
|    - Severity level & Timestamp                                                  |
|    - Affected Host & User account                                                |
|    - Malicious Process & Full Command Line                                       |
|    - VirusTotal Detections (e.g., "54/72 engines flagged as malicious")          |
|    - Interactive Buttons: [ Isolate Machine ]  [ Dismiss Alert ]                  |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | Analyst Clicks "Isolate Machine"
                                          v
+-----------------------------------------------------------------------------------+
|                    5. AUTOMATED CONTAINMENT EXECUTION                             |
|                                                                                   |
|  Action: Tines calls LimaCharlie API (POST /v1/sensor/{sensor_id}/isolation)      |
|  Result on Endpoint:                                                              |
|    - Network driver cuts off all external and internal TCP/UDP traffic            |
|    - Target machine cannot contact C2 server or move laterally                    |
|    - LimaCharlie agent remains alive over isolated channel for forensic triage    |
+-----------------------------------------------------------------------------------+
```

---

## 2. Telemetry Comparison: Why EDR Beats Traditional Syslog

During this project, I compared what a standard Syslog server sees versus what a modern EDR captures:

| Event Detail | Traditional Syslog / Event Viewer | LimaCharlie EDR |
| :--- | :--- | :--- |
| **Process Execution** | Only logs that `certutil.exe` started. | Captures full CLI arguments, parent process (`cmd.exe`), and PID. |
| **File Hashes** | Often requires separate Sysmon setup. | Real-time SHA-256 and MD5 hash generated automatically. |
| **Memory Access** | Almost invisible without advanced audit. | Alerts on unauthorized handles opened to `lsass.exe`. |
| **Containment** | Requires manual login or local scripts. | Instant 1-click network isolation over cloud C2 channel. |

---

## 3. Human-in-the-Loop: Why It Matters in Real SOC Operations

One of the most important design choices in this architecture is having a **Human-in-the-Loop** confirmation step in Slack instead of 100% blind automated isolation.

* **The Risk of Blind Automation:** If an automated rule incorrectly flags a mission-critical server (like a Domain Controller or SQL database) during business hours, instant automated isolation causes a costly operational outage.
* **The Benefit of Assisted Automation:** The SOAR does 90% of the manual labor (enriching the hash on VirusTotal, extracting logs, drafting the ticket). The human analyst only has to look at the evidence card and press the button. This reduces response time from **15 minutes to under 10 seconds** without risking business disruption.
