# Incident Case Management & Ticketing Integration

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*  
*Platform Alignment: TheHive 5 & Jira Service Management*

In an enterprise SOC, alerts do not simply live in chat rooms. Every verified alert must automatically convert into an audited **Incident Case** with tagged observables (IOCs), severity ratings, Traffic Light Protocol (TLP) markers, and structured task checklists.

---

## 1. Case Lifecycle in TheHive

```
[ Ingest Alert ] -> EDR/SOAR detection webhook
       │
       ▼
[ Case Creation ] -> Title, Severity (P1-P4), TLP:AMBER, MITRE Tags
       │
       ▼
[ Observables Attached ] -> IP, Hash, Domain, URL (tagged for enrichment)
       │
       ▼
[ Tasks Generated ] -> 1. Triage -> 2. Containment -> 3. Eradication -> 4. Lessons Learned
```

---

## 2. Automated Case Generator (`create_case.py`)

Run this script to convert any incident payload into a fully structured TheHive 5 REST API case:

```bash
python3 case-management/create_case.py
```
