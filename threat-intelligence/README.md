# Automated Threat Intelligence (CTI) Ingestion & EDR Lookups

*Author: Dil Mahmud Khan (SOC Tier-1 Analyst)*

Cyber Threat Intelligence (CTI) is only valuable if it is operationalized into active detection. This module automates the ingestion of external Indicators of Compromise (IOCs) directly into EDR correlation tables.

---

## 1. The CTI-to-EDR Pipeline

```
[ External CTI Feeds (URLhaus / AlienVault OTX / AbuseIPDB) ]
                             │
                             ▼
[ Normalization Script: ingest_ioc_feed.py ]
                             │
                             ▼
[ LimaCharlie EDR Lookup Tables / Threat Lists ]
                             │
                             ▼
[ Live Sensor Match: Instant P1 Alert Generated ]
```

---

## 2. Ingestion Script Usage (`ingest_ioc_feed.py`)

This script parses raw threat feeds, normalizes IP addresses and SHA-256 hashes, eliminates duplicates, and formats them for EDR ingestion:

```bash
python3 ingest_ioc_feed.py feeds/sample_c2_feed.json
```
