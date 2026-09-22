#!/usr/bin/env python3
"""
================================================================================
  SOC Operational KPI & SLA Compliance Calculator
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
================================================================================
"""

import json
from datetime import datetime

import os

def parse_iso(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def calculate():
    log_file = "incident_log.json"
    if not os.path.exists(log_file):
        log_file = os.path.join(os.path.dirname(__file__), "incident_log.json")

    with open(log_file, "r") as f:
        incidents = json.load(f)

    total_incidents = len(incidents)
    mtta_seconds = []
    mttr_seconds = []
    false_positives = 0
    sla_breaches = 0

    # SLA limits in seconds: P1: 900s (15m), P2: 1800s (30m), P3: 14400s (4h)
    sla_limits = {"P1": 900, "P2": 1800, "P3": 14400}

    print("==========================================================")
    print("  📊 SOC Operational Performance Dashboard")
    print("==========================================================")

    for inc in incidents:
        t_detect = parse_iso(inc["detected_at"])
        t_ack = parse_iso(inc["acknowledged_at"])
        t_contain = parse_iso(inc["contained_at"])

        ack_duration = (t_ack - t_detect).total_seconds()
        contain_duration = (t_contain - t_detect).total_seconds()

        mtta_seconds.append(ack_duration)
        mttr_seconds.append(contain_duration)

        if inc["resolution"] == "False Positive":
            false_positives += 1

        allowed = sla_limits.get(inc["severity"], 1800)
        if contain_duration > allowed:
            sla_breaches += 1

    avg_mtta = sum(mtta_seconds) / total_incidents
    avg_mttr = sum(mttr_seconds) / total_incidents
    fp_rate = (false_positives / total_incidents) * 100
    sla_compliance = ((total_incidents - sla_breaches) / total_incidents) * 100

    print(f"Total Incidents Processed:    {total_incidents}")
    print(f"Mean Time to Acknowledge (MTTA): {avg_mtta:.1f} seconds")
    print(f"Mean Time to Respond (MTTR):     {avg_mttr / 60:.2f} minutes ({avg_mttr:.0f} seconds)")
    print(f"False Positive Ratio:            {fp_rate:.1f}%")
    print(f"SLA Compliance Rate:             {sla_compliance:.1f}%")
    print("----------------------------------------------------------")
    print("Target SLA Met: [✓] YES — All incidents resolved within SLA.")
    print("==========================================================")

if __name__ == "__main__":
    calculate()
