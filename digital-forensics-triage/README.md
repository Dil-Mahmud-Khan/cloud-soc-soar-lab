# Live Endpoint Forensic Triage Collection

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*  
*Standard: RFC 3227 Guidelines for Evidence Collection and Archiving*

When an endpoint is compromised and isolated, standard operating procedure requires capturing **volatile forensic artifacts** before rebooting or reimaging the machine.

---

## 1. RFC 3227 Order of Volatility

Volatile data disappears when the machine loses power. The collection order prioritizes the most fragile artifacts first:

```
[ 1. Network Sockets & Established C2 Connections ]
                        │
                        ▼
[ 2. Process Tree & Memory Command Lines ]
                        │
                        ▼
[ 3. Logged-in User Sessions & Tokens ]
                        │
                        ▼
[ 4. Persistence Mechanisms (Registry Run Keys, Scheduled Tasks) ]
                        │
                        ▼
[ 5. Execution Cache (Prefetch, Temp directory artifacts) ]
```

---

## 2. Automated Triage Script (`collect_triage.ps1`)

I authored a lightweight PowerShell triage script designed to run remotely via LimaCharlie's shell or locally by an analyst.

### Artifacts Collected:
* `network_sockets.txt`: Active TCP/UDP connections mapped to PIDs.
* `process_list.csv`: All running processes with full CLI paths and parent PIDs.
* `active_sessions.txt`: Currently logged-in interactive and RDP users.
* `registry_run_keys.txt`: Persistence hooks in `HKLM` and `HKCU`.
* `scheduled_tasks.csv`: Tasks created or modified in the last 24 hours.
* `temp_executables.txt`: All `.exe`, `.bat`, `.ps1`, and `.tmp` files in `C:\Windows\Temp` and `C:\Users\*\AppData\Local\Temp`.

### How to Run:
```powershell
# Run with Administrator privileges
powershell.exe -ExecutionPolicy Bypass -File .\collect_triage.ps1
```

---

## 3. Sample Evidence Package (`evidence_sample/`)

An authentic sample triage output captured from the Windows 10 victim VM during the Certutil LOLBAS and LSASS dump incidents is provided in [`evidence_sample/`](evidence_sample/):
* [`network_sockets.txt`](evidence_sample/network_sockets.txt): Captures active C2 connection (`PID 4928 -> 89.238.73.97:443`).
* [`process_list.csv`](evidence_sample/process_list.csv): Process lineage showing `explorer.exe -> cmd.exe -> certutil.exe` and `powershell.exe -> rundll32.exe comsvcs.dll`.
* [`dns_cache.txt`](evidence_sample/dns_cache.txt): Host DNS resolver cache containing adversary infrastructure domains.
* [`registry_persistence.txt`](evidence_sample/registry_persistence.txt): Triage audit identifying suspicious Run key in `HKCU`.
