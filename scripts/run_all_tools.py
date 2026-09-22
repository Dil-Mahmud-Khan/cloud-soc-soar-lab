#!/usr/bin/env python3
"""
================================================================================
  Master SOC Suite Runner — Test All Blue Team Tools & Pipelines
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
  Usage:  python3 scripts/run_all_tools.py
================================================================================
"""

import subprocess
import sys
import os

TOOLS = [
    ("Threat Intel Feeds Normalizer", [sys.executable, "threat-intelligence/ingest_ioc_feed.py"]),
    ("Phishing Email Header Analyzer", [sys.executable, "phishing-analysis/phishing_analyzer.py"]),
    ("SOAR Pipeline (EDR -> VT -> Slack)", [sys.executable, "soar-playbooks/soar_pipeline.py", "--auto-isolate"]),
    ("Case Management Dispatch (TheHive/Jira)", [sys.executable, "case-management/create_case.py"]),
    ("Network Telemetry & PCAP Session Triage", [sys.executable, "network-forensics/analyze_network.py"]),
    ("SOC Operational Metrics (MTTA/MTTR/SLA)", [sys.executable, "soc-metrics/calculate_metrics.py"]),
    ("Dynamic Malware Detonation Sandbox", [sys.executable, "malware-sandbox/detonate_sample.py"]),
    ("Purple Team MITRE ATT&CK Scorecard", [sys.executable, "purple-team/purple_team_runner.py"]),
]

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    print("=" * 72)
    print("  🛡️  RUNNING ALL CLOUD SOC & SOAR LAB SUITE VERIFICATION CHECKS")
    print(f"  Root Directory: {root}")
    print("=" * 72)

    passed = 0
    failed = 0

    for name, cmd in TOOLS:
        print(f"\n▶ [{name}]")
        res = subprocess.run(cmd, cwd=root)
        if res.returncode == 0:
            passed += 1
        else:
            print(f"❌ FAILED: {name} exited with status {res.returncode}")
            failed += 1

    print("\n" + "=" * 72)
    print(f"  🏁 SUMMARY: {passed}/{len(TOOLS)} Tools Passed ({failed} failed)")
    print("=" * 72)
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
