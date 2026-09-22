# Architecture & Detection Engineering Design

*Author: Dil Mahmud Khan*

When designing this project, I wanted to understand how enterprise security operations differ from basic home labs. This document explains the design decisions, telemetry choices, and response mechanisms used in this lab.

---

## 1. Why EDR Instead of Just a Traditional SIEM?

In my earlier Wazuh lab, I learned that a SIEM is essentially a central log collector. It is great for compliance, log retention, and high-level correlation. But in real-world incident response, a SIEM has blind spots:

* **No direct endpoint control:** If a ransomware attack begins encrypting files, a SIEM cannot isolate the host. It can only alert you while the damage spreads.
* **Missing process lineage:** Traditional Windows Event Viewer logs often miss detailed parent-child relationships, command-line arguments, and memory access patterns unless advanced auditing (like Sysmon) is manually installed and maintained.
* **Kernel-level visibility:** LimaCharlie operates as a lightweight kernel agent, providing real-time visibility into process creation, network sockets, file modifications, and memory injection.

---

## 2. Why SOAR is Critical for Level 1 Analysts

The biggest problem junior SOC analysts face is **Alert Fatigue**:

```
Traditional Manual Workflow (10–15 minutes per alert):
[Alert Fires] -> [Open Browser] -> [Copy Hash] -> [Check VirusTotal] -> [Write Ticket] -> [Decide Action]

Automated SOAR Workflow (< 5 seconds):
[Alert Fires] -> [Tines Auto-queries VirusTotal] -> [Slack Alert Ready] -> [Click Isolate]
```

By delegating the repetitive, manual tasks (enrichment, formatting, API querying) to a SOAR engine, the analyst can focus solely on decision-making.

---

## 3. How LimaCharlie Network Isolation Works

When the **Isolate Machine** action is executed:

1. LimaCharlie sends a command from the cloud to the endpoint sensor driver.
2. The sensor hooks into the Windows network stack (filtering engine / NDIS driver).
3. All inbound and outbound IPv4 and IPv6 traffic is dropped, **except** encrypted traffic to the LimaCharlie cloud command server.
4. **Why this is critical:** The attacker loses remote access (reverse shell dies, C2 beaconing stops), but the security analyst can still open a remote command prompt through the EDR web console to perform forensic investigations without physically walking to the machine.
