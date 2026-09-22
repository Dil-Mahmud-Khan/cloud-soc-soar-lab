# Network Forensics & Deep Packet Telemetry Analysis

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*  
*Standard: Correlating Host Telemetry with Network Evidence*

An EDR shows what process executed on the host, but **Network Telemetry** confirms what left the network: bytes transferred, external IP addresses, DNS queries, and TLS Server Name Indication (SNI).

---

## 1. Network Evidence Correlated in This Lab

```
[ Windows Endpoint: certutil.exe (PID: 4928) ]
                     │
                     ▼ Outbound Port 443
[ Firewall / Network TAP Sensor ]
                     │
     ┌───────────────┴───────────────┐
     ▼                               ▼
[ DNS Query Log ]           [ TCP Session Log ]
Query: secure.eicar.org     Dst: 89.238.73.97:443
Type: A Record              Duration: 1.2s | Bytes: 4,096
Response: 89.238.73.97      TLS SNI: secure.eicar.org
```

---

## 2. Network Log Analyzer Tool (`analyze_network.py`)

Run this script to parse raw network connection and DNS telemetry for suspicious indicators:

```bash
python3 network-forensics/analyze_network.py
```
