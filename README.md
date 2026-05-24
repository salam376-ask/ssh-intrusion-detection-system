# Real-Time SSH Intrusion Detection System & SOC Dashboard

A Blue Team / Security Operations Center (SOC) simulation environment designed to intercept, analyze, and visualize authentication threats on a Linux endpoint. This system continuously monitors system authentication logs for SSH brute-force patterns, triggers automated alert actions, and displays telemetry metrics on a web administration interface.

---

## 🛠️ System Architecture & Workflow

1. **Log Ingestion Engine (`ssh_monitor.py`):** Pipes live systemd service logs using `journalctl` to dynamically filter for authentication failures.
2. **Threat Correlation & Alerting:** Uses threshold-based rules to classify incoming incidents into severity tiers (LOW, MEDIUM, HIGH) and routes critical alerts to defenders using secure SMTP email delivery.
3. **SIEM Visualization UI (`dashboard.py`):** A custom Flask application that ingests the forensic alert database logs and surfaces real-time situational awareness statistics in a clean web browser interface.

---

## 📂 Project Structure

```text
├── ssh_monitor.py     # Log tracking daemon & alerting engine
├── dashboard.py       # Flask multi-tier web visualization server
├── .gitignore         # Prevents local alert databases from uploading
└── README.md          # Project technical documentation
