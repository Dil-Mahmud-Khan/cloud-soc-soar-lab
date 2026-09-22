# Standard Operating Procedure (SOP): Tier-1 EDR Alert Handling

*Author: Dil Mahmud Khan*  
*Role: SOC Tier-1 Analyst / Blue Team Incident Handler*  
*Framework Reference: NIST SP 800-61 Rev. 2 (Incident Response Life Cycle)*

This document outlines the operational SOP followed by an analyst when an alert fires from our Cloud EDR & SOAR pipeline.

---

## Stage 1: Preparation & Monitoring
* Monitor the `#soc-alerts` Slack channel and the LimaCharlie real-time detections feed.
* Ensure API credentials for VirusTotal and LimaCharlie remain healthy.

---

## Stage 2: Identification & Triage (Target SLA: < 5 Minutes)

When an alert notification card arrives in Slack:
1. **Check the Command Line:** Review the executing binary and parameters.
   * *Is it an administrative script or unusual user activity?*
   * *Does it match known LOLBAS patterns (`certutil -urlcache`, `rundll32 comsvcs`, `-enc` powershell)?*
2. **Review VirusTotal Reputation:**
   * **Score >= 5/70:** Strong indicator of malicious artifact. Proceed to Containment.
   * **Score 0/70 (Unknown):** Check file age and signer. If unsigned binary from `C:\Temp` or `C:\Users\AppData`, treat as suspicious.
   * **Known Clean Tool:** Validate if the user is authorized IT staff. If yes, document as benign false positive.

---

## Stage 3: Containment (Target SLA: < 2 Minutes from Confirmation)

1. If confirmed True Positive or high risk of active lateral movement:
   * Click **[ Isolate Machine ]** in Slack or trigger isolation via the LimaCharlie sensor interface.
2. Confirm isolation status in the LimaCharlie dashboard (`Sensor State: Isolated`).
3. Notify the incident response lead and ticket system.

---

## Stage 4: Eradication & Recovery

1. Open the remote shell in LimaCharlie to inspect the compromised system:
   * Kill any running malicious parent/child processes.
   * Navigate to the target path and delete the downloaded payload or dump file.
   * Check registry Run keys (`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`) and Scheduled Tasks for persistence.
2. Verify system clean via an on-demand scan.
3. Remove isolation status from the sensor.
4. Notify the user to perform an account password reset.

---

## Stage 5: Post-Incident & Lessons Learned

1. Complete the formal incident investigation report (`docs/incident-reports/`).
2. Evaluate if detection rules need tuning (e.g., adding whitelist paths for legitimate admin tools).
