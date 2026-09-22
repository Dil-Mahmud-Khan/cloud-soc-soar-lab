# Tines SOAR Workflow & Playbook Guide

*Author: Dil Mahmud Khan*

This document breaks down the four logical stages of our automated Tines SOAR playbook (`soar-playbooks/tines_soar_story.json`).

---

## 1. The Story Structure in Tines

```
[ Node 1: Webhook Ingest ]
           │
           ▼
[ Node 2: Extract Artifacts ]
           │
           ▼
[ Node 3: Query VirusTotal API ]
           │
           ▼
[ Node 4: Send Formatted Slack Card ]
```

---

## 2. Breakdown of Each Node

### Node 1: Webhook Ingest (`Agents::WebhookAgent`)
* **Purpose:** Listens for HTTPS POST requests sent from LimaCharlie when a D&R detection rule triggers.
* **Payload Ingested:** Raw JSON containing `routing` (hostname, IP, sensor ID, timestamp) and `event` (process path, command line, hash, parent process).

### Node 2: Extract Artifacts (`Agents::EventTransformationAgent`)
* **Purpose:** Cleans and normalizes the raw JSON into standard variables so subsequent nodes can easily use them.
* **Extracted Fields:**
  * `sensor_id` -> Used for API isolation command.
  * `hostname` -> Displayed in Slack.
  * `command_line` -> Displayed in Slack code block.
  * `hash` -> Passed to VirusTotal.

### Node 3: Query VirusTotal API (`Agents::HttpRequestAgent`)
* **Purpose:** Sends an authenticated GET request to the VirusTotal v3 API:
  `GET https://www.virustotal.com/api/v3/files/{{.extract_artifacts.hash}}`
* **Response Parsed:**
  * `data.attributes.last_analysis_stats.malicious` (number of engines flagging as malware).
  * `data.attributes.popular_threat_classification` (e.g., trojan, downloader, test).

### Node 4: Send Slack Alert Card (`Agents::HttpRequestAgent`)
* **Purpose:** Uses Slack Block Kit to construct a high-visibility incident notification card.
* **Card Features:**
  * 🔴 Red header indicating threat severity.
  * Grid showing Host, User, IP, and MITRE ATT&CK technique.
  * Formatted code block showing exact command line arguments.
  * VirusTotal detection ratio.
  * Interactive containment button.
