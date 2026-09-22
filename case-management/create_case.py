#!/usr/bin/env python3
"""
================================================================================
  TheHive 5 / Jira Case Management Generator
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
  Purpose: Converts raw EDR detection events into structured SOC incident cases.
================================================================================
"""

import json
from datetime import datetime, timezone

def generate_case(incident):
    print("==========================================================")
    print("  📋 SOC Case Management Dispatch (TheHive 5 / Jira)")
    print("==========================================================")

    case_payload = {
        "title": f"INC-2026: {incident['detection_name']} on {incident['hostname']}",
        "description": f"Automated incident case created from LimaCharlie EDR detection.\n\n"
                       f"• Endpoint: {incident['hostname']} ({incident['ip']})\n"
                       f"• User: {incident['user']}\n"
                       f"• Command Line: {incident['command_line']}\n"
                       f"• VirusTotal Reputation: {incident['vt_score']}",
        "severity": 3 if incident["severity"] == "P1" else 2,
        "tlp": "TLP:AMBER",
        "pap": "PAP:AMBER",
        "tags": [
            "EDR:LimaCharlie",
            "SOAR:Tines",
            f"MITRE:{incident['mitre_id']}"
        ],
        "observables": [
            {"type": "ip", "value": incident["ip"], "tags": ["internal", "victim"]},
            {"type": "hash", "value": incident["file_hash"], "tags": ["payload", "sha256"]},
            {"type": "command_line", "value": incident["command_line"], "tags": ["execution"]}
        ],
        "tasks": [
            {"title": "1. Verify VirusTotal score & false-positive check", "status": "Completed"},
            {"title": "2. Confirm endpoint network isolation status", "status": "Completed"},
            {"title": "3. Acquire volatile evidence (collect_triage.ps1)", "status": "In Progress"},
            {"title": "4. Securely delete temporary staging files", "status": "Pending"},
            {"title": "5. Request user password rotation & document root cause", "status": "Pending"}
        ]
    }

    print(f"Case Title:    {case_payload['title']}")
    print(f"Severity:      {incident['severity']} | Classification: {case_payload['tlp']}")
    print(f"Observables:   {len(case_payload['observables'])} IOCs tagged for threat enrichment")
    print(f"Workflow Tasks:{len(case_payload['tasks'])} standard response tasks generated")

    output_path = "case_management_payload.json"
    with open(output_path, "w") as f:
        json.dump(case_payload, f, indent=2)

    print(f"\n[✓] Exported formatted TheHive 5 REST API case payload -> {output_path}")
    print("==========================================================")
    return case_payload

if __name__ == "__main__":
    sample = {
        "detection_name": "T1105 - Ingress Tool Transfer (certutil.exe)",
        "mitre_id": "T1105",
        "hostname": "WIN10-ENT-LAB",
        "ip": "192.168.56.105",
        "user": "DESKTOP-TEST\\DilMahmud",
        "severity": "P2",
        "command_line": "certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com payload.tmp",
        "file_hash": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
        "vt_score": "58/72 Malicious"
    }
    generate_case(sample)
