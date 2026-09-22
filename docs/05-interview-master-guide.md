# Master SOC Interview Defense & Storytelling Guide

*Candidate: Dil Mahmud Khan*  
*Target Roles: SOC Analyst Level 1 / Blue Team Cybersecurity Intern*  
*Academic Context: 2nd-Year Erasmus Mundus Joint Master's in Applied Cybersecurity (EMJM CyberMACS)*

This document is your secret weapon for both **HR Screening Calls** and **Technical Interviews**. It provides structured, word-for-word answers using the **STAR methodology** (Situation, Task, Action, Result) based directly on your projects.

---

## 1. The 90-Second Master Elevator Pitch ("Tell me about yourself")

> *"I am currently a second-year Master's student in the Erasmus Mundus CyberMACS program, studying applied cybersecurity across SRH Berlin and Kadir Has University.*
>
> *Before my Master's, I worked as a software developer, where I built backend APIs and implemented authentication, access controls, and structured audit logging. That software background gave me a deep understanding of how applications are built, how logs are generated, and where security vulnerabilities originate.*
>
> *Over the past year, I transitioned fully into defensive security and Blue Team operations. In my cybersecurity internship at Sibereum, I supported security monitoring, triage, and vulnerability assessments.*
>
> *To push beyond classroom theory, I built two major enterprise-grade labs: First, a Wazuh and Suricata home lab to understand host and network IDS. Second, a cloud-native EDR and SOAR pipeline using LimaCharlie, Tines, and VirusTotal, where I emulated real Windows adversary techniques like LOLBAS and LSASS dumping, automated threat enrichment, and implemented interactive one-click network isolation via Slack.*
>
> *I am looking for a SOC Analyst Level 1 or Blue Team Internship where I can leverage my developer mindset, detection engineering skills, and incident response foundation to protect your organization's infrastructure."*

---

## 2. Behavioral Questions (The STAR Method)

### Question 1: "Tell me about a complex technical problem you encountered and how you solved it."
* **Situation:** While building my automated EDR-to-SOAR pipeline, my initial automated containment workflow was firing on routine IT tasks, creating a high risk of business disruption.
* **Task:** I needed to eliminate false alarms for legitimate administrative tools without opening a security blind spot for attacker living-off-the-land techniques.
* **Action:** Instead of whitelisting the `certutil.exe` binary name or entire directories, I engineered a contextual suppression rule. I analyzed the parent process lineage and exact command-line syntax, configuring LimaCharlie to suppress alerts only when `certutil.exe` was invoked with specific internal certificate update flags by `svchost.exe` (Task Scheduler).
* **Result:** We eliminated 100% of recurring administrative false positives while preserving 100% detection fidelity against external download attacks (`-urlcache -split`).

### Question 2: "Describe a security incident you investigated from start to finish."
* **Situation:** During an adversary emulation test in my lab, a critical P1 alert fired detecting `rundll32.exe` invoking `comsvcs.dll` with the `MiniDump` function.
* **Task:** As the Tier-1 analyst, I had to immediately verify whether this was an active credential theft attempt and contain the threat within our 15-minute P1 SLA.
* **Action:** I inspected the process tree in LimaCharlie and confirmed the target process was `lsass.exe` (PID 748). Recognizing this as an attempt to extract plaintext credentials and hashes from memory, I approved network isolation directly from our Slack alert card. With the host isolated from external C2, I used the remote EDR shell to execute my live forensic triage script (`collect_triage.ps1`), capturing volatile network sockets and memory artifacts, and deleted the generated `.dmp` file.
* **Result:** The threat was contained in 2.3 minutes (well below our 15-minute SLA limit), the affected credentials were scheduled for rotation, and I compiled a formal NIST SP 800-61 incident report.

---

## 3. The 10 Hard Technical Questions (With Model Answers)

### Q1: "How does an attacker dump LSASS without dropping Mimikatz?"
> *"Adversaries abuse native Windows binaries—a technique called LOLBAS. For example, they invoke `rundll32.exe` targeting the native `comsvcs.dll` library with the `MiniDump` export parameter. Windows provides this function for legitimate memory crash diagnostics, but an elevated attacker can pass the Process ID of `lsass.exe` to write the entire memory space to a dump file, which they can later parse offline for NTLM hashes and Kerberos tickets."*

### Q2: "Why did you use Human-in-the-Loop in Slack instead of 100% automated isolation?"
> *"Blind automated isolation is dangerous in enterprise production. If an automated rule has a false positive on a Domain Controller, SQL database, or an executive machine during business hours, instant automated isolation causes an expensive operational outage. By implementing a Human-in-the-Loop Slack card, the SOAR does all the tedious enrichment work (saving 10 minutes per ticket), but leaves the final containment decision to the human analyst."*

### Q3: "Walk me through how you inspect an email header for phishing."
> *"I inspect four key areas: First, check the `Authentication-Results` header to verify SPF, DKIM, and DMARC status. Second, compare the envelope `Return-Path` against the friendly `From:` address to check for spoofing. Third, trace the `Received: from` hops to identify the true originating mail server IP address. Finally, extract and defang embedded URLs (`hxxp://`) and calculate SHA-256 hashes of any attachments for VirusTotal lookup."*

### Q4: "What is RFC 3227 and why is it important during incident response?"
> *"RFC 3227 defines the 'Order of Volatility' for digital evidence collection. Volatile artifacts disappear when a computer loses power or reboots. We must acquire evidence from most volatile to least volatile: First registers and cache, then physical memory and network sockets, then running processes, then temporary files and disk artifacts, and finally archived backups."*

### Q5: "What is the difference between traditional Syslog and modern EDR?"
> *"Syslog and standard Event Viewer are passive log collectors—they only see events that software explicitly writes to a log file, and they cannot take response actions. A modern EDR like LimaCharlie operates as a kernel driver: it captures deep process parent-child relationships, injected threads, memory access masks, and open network sockets in real time, and allows the analyst to isolate the endpoint from the network over a secure cloud channel."*

### Q6: "What are MTTD, MTTA, and MTTR, and how did your SOAR project affect them?"
> *"MTTD is Mean Time to Detect (how long until an alert triggers). MTTA is Mean Time to Acknowledge (how long until an analyst opens the alert). MTTR is Mean Time to Respond or Contain. In my project, manual enrichment took ~24 minutes per incident. By using Tines to auto-query VirusTotal and post interactive Slack cards, we reduced our MTTR to 2.3 minutes, achieving a 92% reduction in response time."*

### Q7: "What is a Sigma rule, and why not just write Wazuh or Splunk rules directly?"
> *"Sigma is the vendor-agnostic open standard for detection rules (similar to what Snort is for network traffic or YARA is for files). If you only write Splunk SPL or Wazuh XML, your detection logic is locked to that single tool. By writing in Sigma HQ YAML format, your rules can be converted into any SIEM or EDR query language using automated tools like `sigma-cli`."*

### Q8: "What happens to the endpoint when LimaCharlie executes network isolation?"
> *"The LimaCharlie agent interacts directly with the Windows network filtering engine (NDIS driver). It drops all inbound and outbound IPv4 and IPv6 traffic—killing the attacker's C2 reverse shell and preventing lateral movement—while keeping a single encrypted communication channel alive between the sensor and the LimaCharlie cloud console. This allows the analyst to still run forensic commands remotely."*

### Q9: "How would you investigate an obfuscated PowerShell command?"
> *"I extract the Base64 payload from the `-EncodedCommand` or `-enc` argument. Using CyberChef or a Python script, I decode it from UTF-16LE / Unicode to plain text. I analyze the decoded command to see if it makes network calls (like `DownloadString` or `Net.WebClient`), touches the registry for persistence, or injects shellcode into memory."*

### Q10: "Why are you applying for a SOC Tier-1 / Intern role if you already have software engineering experience?"
> *"Because my ultimate career goal is to become an exceptional Blue Team Detection Engineer and Incident Responder. Software engineering taught me how systems, APIs, and databases work under the hood. But to be a world-class defender, you need front-line experience: triaging real alerts, understanding attacker behaviors, and handling operational pressure. I want to bring my coding and automation mindset to your Tier-1 queue to help the team reduce noise, automate workflows, and stop real attacks."*
