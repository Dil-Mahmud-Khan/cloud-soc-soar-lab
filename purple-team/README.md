# Purple Team Detection Verification & Coverage Scorecard

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*

In modern security operations, Blue Teams do not simply write rules and hope they work. Through **Purple Teaming**, we systematically execute adversary techniques and immediately verify if our detection and response controls fired as expected.

---

## 1. The Verification Lifecycle

```
[ Red Team Action ] -> Execute Atomic Red Team technique on endpoint
          │
          ▼
[ Blue Team Sensor ] -> Verify LimaCharlie EDR received process creation
          │
          ▼
[ Detection Engine ] -> Confirm D&R rule matched and published alert
          │
          ▼
[ SOAR Pipeline ] -> Confirm Tines received webhook and enriched artifact
          │
          ▼
[ Scorecard Output ] -> Log Pass/Fail status and detection latency in seconds
```

---

## 2. Automated Scorecard Runner (`purple_team_runner.py`)

This automated script evaluates the detection fidelity across our attack test suite and outputs a coverage matrix:

```bash
python3 purple-team/purple_team_runner.py
```
