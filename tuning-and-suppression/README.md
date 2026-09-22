# False-Positive Reduction & Alert Tuning Framework

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*

The #1 operational hazard in any SOC is **Alert Fatigue**. If an analyst sees 20 false alarms a day from the same rule, they begin ignoring alerts, eventually missing a true intrusion.

---

## 1. The Golden Rule of Detection Tuning

> **Never whitelist an entire binary name or a generic directory.**  
> Whitelisting `certutil.exe` or `powershell.exe` creates massive security blind spots that attackers actively exploit.

Instead, tuning must be **contextual**, requiring at least 2 of these attributes:
1. **Specific Parent Process:** e.g., only when spawned by the verified enterprise deployment agent (`C:\Program Files\IT-Agent\agent.exe`).
2. **Exact Command-Line Syntax:** Matching specific internal parameters (e.g., `-downloadConfig https://internal-corp-pki.local/`).
3. **Cryptographic Hash or Code Signer:** Valid Microsoft or internal CA digital signature.

---

## 2. Real-World Tuning Example: Administrative Certutil Suppression

* **The Problem:** The IT infrastructure team runs an automated scheduled task once a month to update Root Certificates using `certutil.exe -syncWithWU`. Our detection rule was alerting on it as suspicious LOLBAS activity.
* **The Solution:** We deployed a suppression rule (`suppression_rules.yaml`) that suppresses alerts ONLY when:
  * Binary is `certutil.exe`
  * Command line strictly equals the authorized update parameters: `-syncWithWU \\internal-server\certs`
  * Parent process is `svchost.exe` (Task Scheduler)
* **The Result:** Eliminated 100% of recurring false alarms from the IT admin task, while keeping detections for external `-urlcache -split` attacks fully active.
