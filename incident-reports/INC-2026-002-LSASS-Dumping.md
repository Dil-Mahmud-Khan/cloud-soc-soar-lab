# Incident Investigation Report: INC-2026-002

* **Incident ID:** INC-2026-002
* **Date / Time Detected:** 2026-09-22 16:15:45 UTC
* **Severity Level:** Critical (P1)
* **Assigned Analyst:** Dil Mahmud Khan (SOC Tier 1 Analyst)
* **Status:** Resolved & Closed
* **Incident Classification:** Credential Access / LSASS Memory Dumping (MITRE ATT&CK: T1003.001)

---

## 1. Executive Summary

At 16:15:45 UTC, a critical P1 alert fired in the SOC queue. LimaCharlie EDR identified `rundll32.exe` invoking `comsvcs.dll` with the `MiniDump` export function targeting the Local Security Authority Subsystem Service (`lsass.exe`). This technique is frequently used by adversaries to extract password hashes, plaintext credentials, and Kerberos tickets directly from system memory. The analyst confirmed the attack in Slack and initiated network isolation within 20 seconds of detection. The generated memory dump file was isolated and deleted, preventing credential compromise.

---

## 2. Alert & Telemetry Evidence

| Telemetry Attribute | Observed Value |
| :--- | :--- |
| **Affected Endpoint** | `WIN10-ENT-LAB` (IP: `192.168.56.105`) |
| **Logged User** | `DESKTOP-TEST\DilMahmud` (Elevated Admin) |
| **Target Process** | `C:\Windows\System32\lsass.exe` (PID: `748`) |
| **Executing Process** | `C:\Windows\System32\rundll32.exe` (PID: `5840`) |
| **Parent Process** | `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe` |
| **Full Command Line** | `rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump 748 C:\LabAttacks\lsass_simulated.dmp full` |

---

## 3. Threat Assessment & Attack Technique

* **Technique Overview:**  
  `comsvcs.dll` contains a built-in function called `MiniDump` designed for application crash analysis. However, threat actors abuse this legitimate binary to dump the process memory of `lsass.exe` without dropping third-party tools like Mimikatz onto the disk.
* **Impact of Execution:**  
  If the attacker exfiltrates `lsass_simulated.dmp`, they can parse it offline using tools like `pypykatz` to obtain domain credentials, hash values (NTLM), and active session tickets.

---

## 4. Triage & Containment Timeline

* **16:15:45 UTC:** EDR detects `rundll32.exe` executing with `MiniDump` command-line parameter.
* **16:15:47 UTC:** Tines SOAR receives webhook and generates high-priority card in Slack `#soc-alerts`.
* **16:16:05 UTC:** Analyst investigates command line, recognizes LSASS PID matching target, and executes **[ Isolate Machine ]** action.
* **16:16:07 UTC:** LimaCharlie applies endpoint network isolation rule.
* **16:18:20 UTC:** Analyst opens remote forensic shell, locates `C:\LabAttacks\lsass_simulated.dmp`, calculates file hash for chain of custody, and securely removes the file.
* **16:21:00 UTC:** Password reset request initiated for affected user account `DilMahmud`.

---

## 5. Defensive Hardening Recommendations

1. **Enable LSA Protection:** Configure RunAsPPL registry key (`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa` -> `RunAsPPL=1`) to prevent non-protected processes from reading LSASS memory.
2. **Credential Guard:** Enable Windows Defender Credential Guard to isolate LSASS secrets in virtualized memory.
3. **Attack Surface Reduction (ASR):** Enable the ASR rule: *"Block credential stealing from the Windows local security authority subsystem (lsass.exe)"* (GUID: `9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2`).
