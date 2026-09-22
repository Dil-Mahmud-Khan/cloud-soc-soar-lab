# Enterprise Phishing Triage & Header Analysis

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*  
*Purpose: Automated & Manual Investigation of Suspicious Inbound Emails*

Phishing is responsible for over **80% of initial access vectors** in enterprise breaches. In a Tier-1 SOC queue, triaging user-reported suspicious emails is a primary daily responsibility.

---

## 1. The 4-Step SOC Phishing Triage Methodology

```
[ Step 1: Authentication Checks ] -> SPF, DKIM, DMARC verification
               │
               ▼
[ Step 2: Sender & Routing Analysis ] -> Return-Path, Reply-To, Received IP hops
               │
               ▼
[ Step 3: Payload & URL Extraction ] -> Defang URLs (hxxps://), Attachment SHA-256
               │
               ▼
[ Step 4: Reputation & Containment ] -> VirusTotal / URLhaus lookup, Domain blocklist
```

---

## 2. Key Header Artifacts Explained (Interview Ready)

| Header Attribute | What an Analyst Checks |
| :--- | :--- |
| **`Authentication-Results`** | Verifies if SPF, DKIM, and DMARC evaluated to `pass`, `fail`, or `softfail`. |
| **`Return-Path`** | The envelope sender. If it does not match the friendly `From:` address, it is likely spoofed. |
| **`Received: from`** | Traces the actual originating mail server IP address before relaying. |
| **`Reply-To`** | If an attacker wants email responses sent to a burner inbox instead of the spoofed address. |

---

## 3. Automated Phishing Parser (`phishing_analyzer.py`)

To eliminate manual copy-pasting, I built an automated Python parser that inspects raw `.eml` files:
* Parses all header routing hops.
* Verifies SPF / DKIM / DMARC authentication status.
* Automatically extracts and **defangs** embedded URLs (`http://` -> `hxxp://`).
* Extracts attachments and calculates their SHA-256 hash.

### Run the Analyzer:
```bash
python3 phishing_analyzer.py samples/suspicious_invoice.eml
```
