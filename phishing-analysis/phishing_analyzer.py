#!/usr/bin/env python3
"""
================================================================================
  Enterprise Phishing Email Analyzer & Header Parser
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
  Purpose: Automatically parses suspicious .eml files to extract routing hops,
           evaluate SPF/DKIM/DMARC authentication, defang URLs, and hash payloads.
================================================================================
"""

import sys
import os
import email
from email import policy
import hashlib
import re

def defang_url(url):
    """Defangs a URL to prevent accidental clicking during triage."""
    url = url.replace("http://", "hxxp://").replace("https://", "hxxps://")
    return url.replace(".", "[.]")

def analyze_eml(file_path):
    if not os.path.exists(file_path):
        candidate = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(candidate):
            file_path = candidate
        else:
            print(f"[!] Error: File '{file_path}' not found.")
            return

    print("==========================================================")
    print("  📧 Enterprise Phishing Email Triage Report")
    print("==========================================================")
    print(f"Target File: {file_path}")

    with open(file_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    # 1. Header Information
    print("\n[1] HEADER & ENVELOPE METADATA")
    print(f" • Subject:      {msg['Subject']}")
    print(f" • From (Header):{msg['From']}")
    print(f" • Return-Path:  {msg['Return-Path']}")
    print(f" • Reply-To:     {msg['Reply-To']}")
    print(f" • Message-ID:   {msg['Message-ID']}")
    print(f" • Date:         {msg['Date']}")

    # 2. Authentication Results (SPF, DKIM, DMARC)
    auth_header = msg.get("Authentication-Results", "")
    print("\n[2] EMAIL AUTHENTICATION EVALUATION")
    if auth_header:
        spf_match = re.search(r"spf=([a-zA-Z]+)", auth_header)
        dkim_match = re.search(r"dkim=([a-zA-Z]+)", auth_header)
        dmarc_match = re.search(r"dmarc=([a-zA-Z]+)", auth_header)

        spf = spf_match.group(1).upper() if spf_match else "UNKNOWN"
        dkim = dkim_match.group(1).upper() if dkim_match else "UNKNOWN"
        dmarc = dmarc_match.group(1).upper() if dmarc_match else "UNKNOWN"

        print(f" • SPF Check:    [{spf}]")
        print(f" • DKIM Check:   [{dkim}]")
        print(f" • DMARC Check:  [{dmarc}]")

        if "FAIL" in [spf, dkim, dmarc]:
            print(" ⚠️  ALERT: Email failed sender domain authentication!")
    else:
        print(" • No Authentication-Results header present.")

    # 3. Extract & Defang Embedded URLs
    print("\n[3] EMBEDDED URLS (DEFANGED)")
    body = ""
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type in ["text/plain", "text/html"]:
            try:
                body += part.get_content()
            except Exception:
                pass

    urls = re.findall(r"(?:https?://|hxxps?://)[^\s\"'<>]+", body)
    if urls:
        for idx, u in enumerate(set(urls), 1):
            print(f" • [{idx}] {defang_url(u)}")
    else:
        print(" • No URLs detected in email body.")

    # 4. Attachments & Hashing
    print("\n[4] ATTACHMENTS & ARTIFACTS")
    attachment_count = 0
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            attachment_count += 1
            filename = part.get_filename() or f"attachment_{attachment_count}.bin"
            payload = part.get_payload(decode=True)
            sha256 = hashlib.sha256(payload).hexdigest()
            size = len(payload)

            print(f" • Filename:    {filename}")
            print(f"   Size:        {size} bytes")
            print(f"   SHA-256:     {sha256}")
            
            # Double extension check
            if re.search(r"\.[a-zA-Z0-9]+\.(exe|vbs|bat|scr|ps1|js)$", filename, re.IGNORECASE):
                print(f"   ⚠️  CRITICAL: Double extension or executable payload detected! ({filename})")

    if attachment_count == 0:
        print(" • No attachments detected.")

    print("\n==========================================================")
    print("  [✓] Phishing Triage Finished. Ready for Threat Intel Query.")
    print("==========================================================")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "samples/suspicious_invoice.eml"
    analyze_eml(target)
