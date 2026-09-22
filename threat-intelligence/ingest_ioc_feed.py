#!/usr/bin/env python3
"""
================================================================================
  CTI Feed Ingestion & EDR Lookup Normalizer
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
================================================================================
"""

import sys
import os
import json
import re

def is_valid_ipv4(ip):
    parts = ip.split(".")
    return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

def is_valid_sha256(h):
    return bool(re.match(r"^[a-fA-F0-9]{64}$", h))

def process_feed(feed_file):
    if not os.path.exists(feed_file):
        print(f"[!] File '{feed_file}' not found.")
        return

    with open(feed_file, "r") as f:
        iocs = json.load(f)

    print("==========================================================")
    print("  🌐 Cyber Threat Intelligence Feed Ingest & Validation")
    print("==========================================================")
    print(f"Ingesting Feed File: {feed_file}")

    valid_ips = []
    valid_hashes = []

    for item in iocs:
        val = item.get("ioc", "").strip()
        itype = item.get("type", "").lower()

        if itype == "ipv4" and is_valid_ipv4(val):
            valid_ips.append(item)
        elif itype == "sha256" and is_valid_sha256(val):
            valid_hashes.append(item)

    print(f"\n[✓] Validated {len(valid_ips)} C2 IP Addresses:")
    for ip in valid_ips:
        print(f" • [IP]  {ip['ioc']:<16} | Confidence: {ip['confidence']}% | {ip['threat']}")

    print(f"\n[✓] Validated {len(valid_hashes)} Malicious Hashes (SHA-256):")
    for h in valid_hashes:
        print(f" • [SHA] {h['ioc'][:24]}... | {h['threat']}")

    output_file = "feeds/normalized_edr_threat_list.json"
    normalized = {"ips": [x["ioc"] for x in valid_ips], "hashes": [x["ioc"] for x in valid_hashes]}
    with open(output_file, "w") as out:
        json.dump(normalized, out, indent=2)

    print(f"\n[✓] Exported normalized lookup list for EDR ingestion -> {output_file}")
    print("==========================================================")

if __name__ == "__main__":
    feed = sys.argv[1] if len(sys.argv) > 1 else "feeds/sample_c2_feed.json"
    process_feed(feed)
