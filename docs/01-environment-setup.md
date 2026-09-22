# Lab Environment Setup Guide

*Author: Dil Mahmud Khan*  
*Target: 100% Free Tier, Low Resource Usage (Runs within 16GB RAM / 256GB SSD)*

This guide walks through how I set up each component of my lab from scratch.

---

## 1. Windows 10/11 Endpoint (VirtualBox)

I used a single virtual machine to act as the victim Windows workstation.

* **Hypervisor:** VirtualBox (Free, open-source).
* **Operating System:** Windows 10 or 11 Enterprise Evaluation (free 90-day trial directly from Microsoft Evaluation Center).
* **Resource Allocation:**
  * **RAM:** 4096 MB (4 GB) — leaves 12 GB free on my 16 GB laptop.
  * **Processors:** 2 vCPUs.
  * **Storage:** 25 GB dynamically allocated virtual hard disk (takes ~15 GB actual space on disk).
  * **Network:** NAT or Bridged Adapter with Internet access.

---

## 2. LimaCharlie EDR Setup (Cloud)

LimaCharlie is a cloud-based Endpoint Detection and Response (EDR) platform. Its free tier provides full enterprise features for up to 2 endpoints without requiring a credit card.

1. Create a free account at [limacharlie.io](https://limacharlie.io).
2. Create a new organization (e.g., `dil-soc-lab`).
3. Select **Add Sensor** -> Choose **Windows** -> Select the `.exe` installer.
4. Download the installer onto the Windows VM.
5. Open PowerShell as Administrator on the Windows VM and run:
   ```powershell
   .\lc_sensor.exe -i YOUR_INSTALLATION_KEY
   ```
6. Verify in the LimaCharlie cloud dashboard under **Sensors**: the Windows VM appears as `Online` and process telemetry begins streaming in real time.

---

## 3. Tines SOAR Setup (Cloud)

Tines is the automation engine that connects our EDR, Threat Intelligence, and Slack.

1. Sign up for a free Community Edition account at [tines.com](https://www.tines.com).
2. Create a new Story named `EDR to Slack Incident Response`.
3. Add a **Webhook Action** to generate a unique receiving URL.
4. Copy the Webhook URL — this will be configured as the destination in LimaCharlie.

---

## 4. Connecting LimaCharlie to Tines (Output Stream)

1. In LimaCharlie, navigate to **Outputs** -> **Add Output**.
2. Select **Detections** as the stream type.
3. Destination: **Webhook**.
4. Paste the unique Tines Webhook URL into the destination field.
5. Save the output. Now, whenever an EDR detection rule triggers, the JSON payload is forwarded automatically to Tines.

---

## 5. Threat Intelligence & Communication APIs

* **VirusTotal API:**
  1. Create a free community account at [virustotal.com](https://www.virustotal.com).
  2. Go to your user profile -> **API Key** -> Copy your 64-character key.
  3. This key allows 500 free lookups per day (plenty for lab testing).

* **Slack Private SOC Channel:**
  1. Create a free private Slack workspace.
  2. Create a channel named `#soc-alerts`.
  3. Go to `api.slack.com/apps` -> Create an App -> Enable **Incoming Webhooks**.
  4. Add a webhook targeting `#soc-alerts` and copy the webhook URL.
