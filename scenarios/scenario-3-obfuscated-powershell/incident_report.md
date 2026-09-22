# Incident Investigation Report: INC-2026-003

* **Incident ID:** INC-2026-003
* **Date / Time Detected:** 2026-09-22 16:50:30 UTC
* **Severity Level:** Medium (P3)
* **Assigned Analyst:** Dil Mahmud Khan (SOC Tier 1 Analyst)
* **Status:** Resolved & Closed
* **Incident Classification:** Obfuscated Script Execution (MITRE ATT&CK: T1059.001)

---

## 1. Executive Summary

At 16:50:30 UTC, LimaCharlie EDR generated an alert detecting `powershell.exe` spawned with an encoded command string (`-EncodedCommand`) and execution policy bypass parameters. The analyst extracted the base64-encoded string from the telemetry, decoded it using CyberChef, and confirmed it was a simulated test command. The incident was documented and resolved without requiring host isolation.

---

## 2. Telemetry & Artifacts

* **Target Host:** `WIN10-ENT-LAB`
* **Parent Process:** `cmd.exe` (PID: 3812)
* **Command Line:** `powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand VwByAGkAdABlAC0ASABvAHMAdAAgACc...`
* **Decoded Payload:** `Write-Host 'Adversary Emulation: Simulated Malicious Script Execution'; Start-Sleep -Seconds 2`

---

## 3. Findings & Resolution

* No malicious outbound network sockets or persistence mechanisms were detected.
* Classified as an adversary emulation / testing event. Closed with status: Benign Test.
