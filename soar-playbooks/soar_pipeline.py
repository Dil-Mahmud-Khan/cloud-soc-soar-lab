#!/usr/bin/env python3
"""
================================================================================
  Cloud SOC & SOAR Pipeline — Python Automation Script
  Author: Dil Mahmud Khan
  Purpose: Demonstrates the programmatic SOAR automation logic:
           1. Ingests or simulates a LimaCharlie EDR detection event
           2. Automatically queries VirusTotal API v3 for file hash reputation
           3. Formats and sends an alert card to a Slack webhook
           4. Prompts or triggers automated isolation via LimaCharlie API
================================================================================
"""

import os
import sys
import json
import requests
import datetime

def _load_env_if_present():
    """Auto-load .env file from project root or current directory if present."""
    search_paths = [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "..", ".env"),
    ]
    for path in search_paths:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip("'\"")
                            if k not in os.environ and v:
                                os.environ[k] = v
                break
            except Exception:
                pass

_load_env_if_present()

# --- CONFIGURATION (Reads from .env, shell environment, or simulated fallback) ---
VIRUSTOTAL_API_KEY = os.getenv("VT_API_KEY", "YOUR_VIRUSTOTAL_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "YOUR_SLACK_WEBHOOK_URL")
LIMACHARLIE_API_KEY = os.getenv("LC_API_KEY", "YOUR_LIMACHARLIE_API_KEY")
LIMACHARLIE_OID = os.getenv("LC_OID", "YOUR_ORGANIZATION_ID")

def query_virustotal(file_hash):
    """Queries the VirusTotal v3 API for a file hash reputation."""
    print(f"[*] Querying VirusTotal API for hash: {file_hash}")
    
    if VIRUSTOTAL_API_KEY == "YOUR_VIRUSTOTAL_API_KEY":
        print("[!] No real VT API key set. Returning simulated threat score.")
        return {
            "positives": 54,
            "total": 72,
            "status": "Malicious",
            "threat_label": "trojan.certutil.downloader"
        }
        
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            positives = stats.get("malicious", 0)
            total = sum(stats.values())
            return {
                "positives": positives,
                "total": total,
                "status": "Malicious" if positives > 0 else "Clean",
                "threat_label": "Known Threat" if positives > 0 else "Benign"
            }
        elif response.status_code == 404:
            return {"positives": 0, "total": 0, "status": "Unknown", "threat_label": "Unseen in VT"}
    except Exception as e:
        print(f"[!] VirusTotal API error: {e}")
        
    return {"positives": 0, "total": 0, "status": "Error", "threat_label": "Lookup Failed"}

def send_slack_alert(incident_data, vt_result):
    """Sends a rich formatted alert to the Slack SOC channel."""
    print("[*] Formatting and sending alert to Slack...")
    
    payload = {
        "text": f"🚨 *CRITICAL EDR ALERT: {incident_data['detection_name']}*",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 EDR Alert: {incident_data['detection_name']}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Endpoint:* `{incident_data['hostname']}`"},
                    {"type": "mrkdwn", "text": f"*IP Address:* `{incident_data['ip']}`"},
                    {"type": "mrkdwn", "text": f"*User:* `{incident_data['user']}`"},
                    {"type": "mrkdwn", "text": f"*MITRE Technique:* `{incident_data['mitre_id']}`"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Command Line:*\n```{incident_data['command_line']}```"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*VirusTotal Score:* `{vt_result['positives']}/{vt_result['total']} Malicious`"},
                    {"type": "mrkdwn", "text": f"*Threat Assessment:* `{vt_result['status']}`"}
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "🔴 Isolate Endpoint"},
                        "style": "danger",
                        "value": "isolate"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "⚪ Dismiss Alert"},
                        "value": "dismiss"
                    }
                ]
            }
        ]
    }
    
    if SLACK_WEBHOOK_URL == "YOUR_SLACK_WEBHOOK_URL":
        print("[✓] Slack Webhook simulated. Payload generated successfully:")
        print(json.dumps(payload, indent=2))
        return True
        
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            print("[✓] Alert successfully delivered to Slack!")
            return True
        else:
            print(f"[!] Slack API error status: {response.status_code}")
    except Exception as e:
        print(f"[!] Slack posting failed: {e}")
        
    return False

def isolate_endpoint(sensor_id):
    """Sends API request to LimaCharlie to isolate the compromised endpoint."""
    print(f"[*] Triggering LimaCharlie network isolation for sensor: {sensor_id}...")
    
    if LIMACHARLIE_API_KEY == "YOUR_LIMACHARLIE_API_KEY":
        print(f"[✓] [SIMULATED] Sensor {sensor_id} isolated from network successfully!")
        return True
        
    url = f"https://api.limacharlie.io/v1/sensor/{sensor_id}/isolation"
    headers = {"Authorization": f"Bearer {LIMACHARLIE_API_KEY}"}
    
    try:
        response = requests.post(url, headers=headers, timeout=10)
        if response.status_code in [200, 201]:
            print(f"[✓] Sensor {sensor_id} is now NETWORK ISOLATED.")
            return True
    except Exception as e:
        print(f"[!] Failed to isolate sensor: {e}")
        
    return False

def run_pipeline(mock_event):
    """Main execution loop simulating the SOAR pipeline."""
    print("==========================================================")
    print("  🚀 Starting SOAR Pipeline Workflow Execution")
    print("==========================================================")
    
    # 1. Parse Event
    print(f"[1] Ingested event from {mock_event['hostname']} ({mock_event['detection_name']})")
    
    # 2. Enrich with VirusTotal
    vt_result = query_virustotal(mock_event['file_hash'])
    
    # 3. Post to Slack
    send_slack_alert(mock_event, vt_result)
    
    # 4. Human-in-the-Loop decision (Console prompt for testing)
    print("\n----------------------------------------------------------")
    if "--auto-isolate" in sys.argv or not sys.stdin.isatty():
        action = "yes"
        print("Analyst decision: [Auto-approved 'yes' for automated / non-interactive run]")
    else:
        try:
            action = input("Analyst decision prompt: Isolate host? (yes/no): ").strip().lower()
        except EOFError:
            action = "yes"
    if action in ["yes", "y"]:
        isolate_endpoint(mock_event['sensor_id'])
    else:
        print("[*] Alert dismissed by analyst. Host remains active.")
        
    print("==========================================================")
    print("  [✓] SOAR Pipeline Cycle Finished.")
    print("==========================================================")

if __name__ == "__main__":
    # Sample incident event emulating an Atomic Red Team execution
    sample_incident = {
        "detection_name": "T1105 - Ingress Tool Transfer (certutil.exe)",
        "mitre_id": "T1105",
        "hostname": "WIN10-ENT-LAB",
        "ip": "192.168.56.105",
        "user": "DESKTOP-TEST\\DilMahmud",
        "sensor_id": "8a72b94f-12d4-49c0-9fa1-abc123456789",
        "command_line": "certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com payload.tmp",
        "file_hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    run_pipeline(sample_incident)
