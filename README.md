# Cloud EDR & SOAR Incident Response Lab

An automated detection and response project connecting LimaCharlie EDR, Tines SOAR, VirusTotal API, and Slack to detect Windows attacks, enrich threat data, and test automated endpoint containment.

* **Author:** Dil Mahmud Khan (Cybersecurity Master's Student, Erasmus Mundus CyberMACS)
* **Target Role:** SOC Analyst Level 1 / Blue Team Intern
* **Live SecOps Console:** [Interactive Dashboard Demo](https://dil-mahmud-khan.github.io/cloud-soc-soar-lab/dashboard/)
* **GitHub Actions:** [![Validate Detections, Playbooks & Tools](https://github.com/Dil-Mahmud-Khan/cloud-soc-soar-lab/actions/workflows/validate-rules.yml/badge.svg)](https://github.com/Dil-Mahmud-Khan/cloud-soc-soar-lab/actions/workflows/validate-rules.yml)

---

## Why I Built This Project

After setting up my [Wazuh SOC Home Lab](https://github.com/Dil-Mahmud-Khan/SOC-Home-Lab) on Ubuntu Linux, I started reviewing real job postings for Tier 1 SOC Analyst and Working Student roles across Germany and the EU. 

I noticed three recurring requirements that my previous Linux lab did not cover:
1. **Windows Telemetry:** Most enterprise intrusions (credential dumping, living-off-the-land attacks, phishing droppers) happen on Windows endpoints. I needed hands-on experience with Windows process trees, command-line arguments, and memory events.
2. **True EDR vs. Syslog:** In real incident response, analysts don't just read passive log files; they interact with an EDR agent that can inspect parent-child process relationships and isolate machines from the network.
3. **Alert Fatigue & Automation:** A recurring complaint among SOC analysts is the time spent manually copying hashes into VirusTotal and writing routine tickets. I wanted to see how much of that triage workflow could be safely automated using modern SOAR tools (Tines) and APIs.

I built this project to answer a simple question: **Can I build an automated pipeline that detects a real Windows attack, checks if the artifact is malicious via VirusTotal, alerts me in Slack, and lets me isolate the machine with one click?**

---

## System Architecture

```
[ Adversary Emulation ]
(Atomic Red Team: Certutil LOLBAS / LSASS Dump / Obfuscated PowerShell)
           │
           ▼
[ Windows 10/11 Endpoint ]
(LimaCharlie EDR Kernel Sensor)
           │
           ▼ (Detection Webhook)
[ Tines Cloud SOAR ]
     │               │
     ▼               ▼
[ VirusTotal API ]   [ Data Parser ]
(Check File Hash)    (Host, User, CLI, Parent PID)
     │               │
     └───────┬───────┘
             │
             ▼
[ Slack #soc-alerts Channel ]
"Incident Card: Malicious Artifact Detected"
Action: [ Isolate Endpoint ] or [ Dismiss ]
             │
             ▼ (Analyst clicks "Isolate")
[ LimaCharlie Cloud API ]
(Windows host network traffic blocked in real time)
```

---

## Tools Used & Why

* **Windows 10/11 Enterprise (VM):** The target workstation where simulated attacks are run.
* **LimaCharlie EDR:** Cloud-managed EDR (free for up to 2 sensors). I chose this because it gives raw process lineage, network sockets, and an open API for network isolation without needing expensive enterprise licenses.
* **Atomic Red Team:** Open-source testing library by Red Canary to safely run MITRE ATT&CK techniques instead of downloading random untrusted malware.
* **Tines SOAR (Community Edition):** Cloud automation platform to parse incoming EDR webhooks, query APIs, and dispatch Slack cards.
* **VirusTotal v3 API:** To enrich file hashes automatically during triage.
* **Slack (Private Workspace):** Simulates the internal SOC operations channel where analysts receive and triage alerts.
* **Python 3:** Standalone automation scripts for phishing analysis, incident metrics, case management, sandbox detonation, and offline SOAR testing.

---

## Attack Scenarios Tested

I created three dedicated test modules. Each has its own folder containing the attack script, detection rule, and incident report:

### 1. Ingress Tool Transfer via LOLBAS ([scenarios/scenario-1-certutil-lolbas/](scenarios/scenario-1-certutil-lolbas/))
* **Technique:** MITRE ATT&CK T1105
* **What I did:** Used `certutil.exe` with `-urlcache -split -f` to download a file from an external URL into `C:\LabAttacks\`.
* **Why:** Attackers abuse built-in Windows utilities so perimeter firewalls and basic antivirus don't flag the download.
* **Detection:** Wrote a LimaCharlie rule monitoring `certutil.exe` execution when combined with cache/split download parameters.

### 2. Credential Access: LSASS Memory Dump ([scenarios/scenario-2-lsass-dumping/](scenarios/scenario-2-lsass-dumping/))
* **Technique:** MITRE ATT&CK T1003.001
* **What I did:** Tested native DLL execution using `rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump` targeting the `lsass.exe` process ID.
* **Why:** This simulates extracting credentials from memory without dropping third-party tools like Mimikatz to disk.
* **Detection:** Rule flags `rundll32.exe` whenever its command line references `comsvcs.dll` and `MiniDump`.

### 3. Obfuscated PowerShell Execution ([scenarios/scenario-3-obfuscated-powershell/](scenarios/scenario-3-obfuscated-powershell/))
* **Technique:** MITRE ATT&CK T1059.001
* **What I did:** Launched PowerShell with `-EncodedCommand` (Base64) and `-ExecutionPolicy Bypass`.
* **Why:** Attackers frequently hide command strings inside encoded arguments to evade basic keyword filters.
* **Detection:** Flagged on process creation for `powershell.exe` containing `-enc` or `-EncodedCommand`.

---

## Operational Blue Team Modules Built for This Lab

To make this project reflect actual daily enterprise SOC work, I built ten practical modules:

1. **Phishing Email Analysis ([phishing-analysis/](phishing-analysis/)):**  
   Built `phishing_analyzer.py` to parse raw `.eml` files, extract routing hops, check SPF/DKIM/DMARC authentication, defang URLs (`hxxps://`), and calculate attachment SHA-256 hashes.

2. **Live Incident Triage Script ([digital-forensics-triage/](digital-forensics-triage/)):**  
   Created a PowerShell collector (`collect_triage.ps1`) based on RFC 3227 order of volatility. Captures network sockets, active processes with command lines, logged-in sessions, registry Run keys, and temp staging folders from an isolated host.

3. **Purple Team Verification Scorecard ([purple-team/](purple-team/)):**  
   Built `purple_team_runner.py` to systematically execute each attack, verify whether EDR detection and SOAR enrichment triggered, and output an automated Pass/Fail coverage matrix.

4. **Incident Case Management & Ticketing ([case-management/](case-management/)):**  
   Built `create_case.py` to automatically transform raw EDR alerts into structured TheHive 5 / Jira REST API cases with tagged observables, TLP:AMBER ratings, and standard PICERL response tasks.

5. **Automated Malware Sandbox Detonation ([malware-sandbox/](malware-sandbox/)):**  
   Built `detonate_sample.py` simulating automated dynamic sandbox execution (CAPEv2 / Any.Run), tracking spawned processes, C2 callbacks, and registry persistence hooks.

6. **Network Forensics & Packet Triage ([network-forensics/](network-forensics/)):**  
   Built `analyze_network.py` to correlate endpoint EDR telemetry with network connection logs, verifying DNS requests, TLS SNI, and HTTP user-agents.

7. **SLA & Performance Metrics ([soc-metrics/](soc-metrics/)):**  
   Modeled enterprise SLAs (P1: MTTR < 15 min). Built `calculate_metrics.py` to evaluate incident logs, demonstrating how SOAR reduced Mean Time to Respond from ~24 minutes down to 2.3 minutes.

8. **Alert Suppression & Tuning ([tuning-and-suppression/](tuning-and-suppression/)):**  
   Authored `suppression_rules.yaml` to whitelist legitimate Windows Update certificate updates from Task Scheduler without blinding detections for external download attacks.

9. **Threat Intelligence Feed Ingest ([threat-intelligence/](threat-intelligence/)):**  
   Created a Python normalizer (`ingest_ioc_feed.py`) converting external C2 IP and hash feeds into normalized JSON lookup lists for real-time EDR correlation.

10. **Interactive SOC Dashboard ([Live Console Demo](https://dil-mahmud-khan.github.io/cloud-soc-soar-lab/dashboard/) | [dashboard/index.html](dashboard/index.html)):**  
    Built a standalone enterprise SecOps console featuring a 7-incident triage queue, MITRE ATT&CK mapping, process lineage inspection, VirusTotal enrichment, and real-time host containment actions.

---

## Real Challenges I Faced & What I Learned

Building this lab wasn't plug-and-play. Here are three real problems I encountered:

1. **Windows Defender Quarantining Test Payloads:**  
   When testing the certutil download with the EICAR test string, Windows Defender immediately blocked the file before LimaCharlie finished recording the event. I had to configure specific lab directory exclusions (`C:\LabAttacks\`) so I could observe how the EDR sensor and detection rules behave independently of signature AV.

2. **Parsing Nested JSON in Tines:**  
   LimaCharlie webhooks package event data in deeply nested structures (`body.routing.hostname`, `body.event.COMMAND_LINE`). My initial Tines story failed because fields were missing when process events didn't have parent hashes. I had to add an Event Transformation node with fallback values to ensure Slack cards didn't break on partial telemetry.

3. **Why Human-in-the-Loop is Safer than 100% Automation:**  
   At first, I considered making host isolation completely automatic when VirusTotal score > 0. But during testing, I realized that if a benign administrative script triggers a rule on a production machine, automatic isolation would cause an outage. Having Tines send an interactive button to Slack gives the speed of automated data gathering while keeping the final decision in human hands.

---

## Repository Structure

```
cloud-soc-soar-lab/
├── README.md                      <- Master project guide and overview
├── dashboard/                     <- Standalone interactive SOC dashboard console
│   └── index.html
├── .github/workflows/             <- Automated Detection-as-Code CI/CD
│   └── validate-rules.yml
├── docs/                          <- Technical guides, SOPs, and Interview Prep
│   ├── 01-environment-setup.md
│   ├── 02-architecture-design.md
│   ├── 03-soar-workflow-guide.md
│   ├── 04-incident-response-sop.md (NIST SP 800-61 SOP)
│   ├── 05-interview-master-guide.md (STAR pitch and technical Q&A)
│   ├── mitre-attack-coverage.json (Official ATT&CK Navigator layer)
│   └── SCREENSHOT_GUIDE.md
├── scenarios/                     <- Dedicated folders for EACH attack test
│   ├── scenario-1-certutil-lolbas/
│   ├── scenario-2-lsass-dumping/
│   └── scenario-3-obfuscated-powershell/
├── purple-team/                   <- Automated Purple Team coverage verification
├── case-management/               <- TheHive 5 / Jira case generation & observable tagging
├── malware-sandbox/               <- Automated dynamic sandbox execution pipeline
├── network-forensics/             <- Deep packet inspection & connection session analyzer
├── sigma/                         <- Universal Sigma HQ detection rules
├── edr-rules/                     <- LimaCharlie D&R detection rules
├── threat-hunting/                <- Hypothesis-driven threat hunting playbook (HUNT-001)
├── soar-playbooks/                <- Tines workflow JSON & tested Python automation
├── phishing-analysis/             <- Email header analysis tool & suspicious .eml samples
├── digital-forensics-triage/      <- RFC 3227 live endpoint volatile evidence collector
├── soc-metrics/                   <- SLA framework & MTTR/MTTD calculator
├── tuning-and-suppression/        <- False positive suppression rules & tuning policies
├── threat-intelligence/           <- CTI feed ingestion and normalization engine
└── scripts/                       <- Endpoint initialization, mock server, and cleanup utilities
```

---

## Interview Defense Summary

If asked about this project in an interview, here is the short summary of what I accomplished:

* **What problem does it solve?** It eliminates manual alert triage delays by using SOAR (Tines) and the VirusTotal API to automatically enrich Windows EDR detections, allowing an analyst to verify and isolate a compromised machine in under 2 minutes.
* **What did I personally write?** I wrote the PowerShell attack scripts, the custom LimaCharlie D&R rules, the Sigma rules, the Python phishing parser (`phishing_analyzer.py`), the live triage script (`collect_triage.ps1`), the case generator (`create_case.py`), the purple team runner (`purple_team_runner.py`), the KPI calculator, and the Tines workflow.
* **How does it complement my previous work?** My Wazuh lab taught me Linux logging, decoders, and network IDS with Suricata. This project gave me practical experience with Windows endpoint telemetry, EDR process trees, memory dumping techniques, and API-driven SOAR automation.

For full technical answers and behavioral STAR responses, see [docs/05-interview-master-guide.md](docs/05-interview-master-guide.md).

---

## License
MIT License - Created for educational and cybersecurity portfolio purposes.
