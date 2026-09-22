#!/usr/bin/env python3
"""
================================================================================
  Local Webhook Receiver & SOAR Dispatch Simulator
  Author: Dil Mahmud Khan (SOC Tier-1 Analyst)
  Purpose: Simulates the Tines webhook receiver locally for offline testing.
================================================================================
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {"raw": post_data.decode('utf-8', errors='ignore')}

        timestamp = datetime.now().strftime("%H:%M:%S")

        print("\n" + "="*60)
        print(f"  🚨 [{timestamp}] INCOMING EDR DETECTION WEBHOOK RECEIVED")
        print("="*60)
        print(f"  • Source Sensor: {payload.get('hostname', 'WIN10-ENT-LAB')}")
        print(f"  • Detection:     {payload.get('detection_name', 'T1105 - Ingress Tool Transfer')}")
        print(f"  • Target Binary: {payload.get('process', 'certutil.exe')}")
        print(f"  • Command Line:  {payload.get('command_line', 'N/A')}")
        print(f"  • Threat Score:  58/72 Malicious (VirusTotal v3)")
        print("  • SOAR Action:   [✓] Dispatched Interactive Card to Slack #soc-alerts")
        print("="*60 + "\n")

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        response = {"status": "success", "message": "EDR webhook ingested into SOAR pipeline"}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def log_message(self, format, *args):
        return  # Suppress default HTTP logging for cleaner terminal output

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    print(f"[*] Local SOAR Webhook Listener running on http://localhost:{port}/webhook")
    print("[*] Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping Webhook Server.")

if __name__ == "__main__":
    run_server()
