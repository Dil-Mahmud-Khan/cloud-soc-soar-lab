#!/usr/bin/env python3
"""
================================================================================
  Network Telemetry & PCAP Session Analyzer
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
================================================================================
"""

import json
import os

def analyze(log_file="logs/conn_dns_sample.json"):
    if not os.path.exists(log_file):
        candidate = os.path.join(os.path.dirname(__file__), log_file)
        if os.path.exists(candidate):
            log_file = candidate
        else:
            print(f"[!] File '{log_file}' not found.")
            return

    with open(log_file, "r") as f:
        events = json.load(f)

    print("==========================================================")
    print("  🌐 Network Telemetry & Session Triage")
    print("==========================================================")
    print(f"Log Source: {log_file}")
    print(f"Total Network Sessions Parsed: {len(events)}\n")

    for idx, e in enumerate(events, 1):
        print(f"--- Session #{idx} [{e['timestamp']}] ---")
        print(f" • Flow:       {e['src_ip']}:{e['src_port']} -> {e['dst_ip']}:{e['dst_port']} ({e['proto'].upper()})")
        print(f" • DNS Query:  {e['dns_query']}")
        print(f" • TLS SNI:    {e['tls_sni']}")
        print(f" • User-Agent: {e['user_agent']}")
        print(f" • Bytes Xfer: Sent: {e['bytes_sent']} B | Recv: {e['bytes_recv']} B")

        if "certutil" in e["user_agent"].lower():
            print(" ⚠️  ANOMALY: Outbound connection initiated by Windows CertUtil!")
        if "powershell" in e["user_agent"].lower():
            print(" ⚠️  CRITICAL: Direct PowerShell outbound HTTP communication detected!")
        print()

    print("==========================================================")
    print("  [✓] Network Triage Completed.")
    print("==========================================================")

if __name__ == "__main__":
    analyze()
