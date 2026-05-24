import subprocess
import re
from collections import defaultdict
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os  # 👈 Added this to interact with the Linux Firewall

def send_email(alert_message):
    sender = "khanabdussalam727@gmail.com"
    receiver = "khanabdussalam727@gmail.com"
    password = "czhckfecffdskwnx"   
    msg = MIMEText(alert_message)
    msg["Subject"] = "🚨 HIGH ALERT: SSH Brute Force Detected"
    msg["From"] = sender
    msg["To"] = receiver
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("📧 Email Alert Sent!")
    except Exception as e:
        print("❌ Email Error:", e)

print("🔵 SOC SSH MONITOR STARTED (IPS MODE ACTIVE)...\n")
failed_attempts = defaultdict(int)
alerted_ips = set()
blocked_ips = set()  # 👈 Keeps track of who we already banned

process = subprocess.Popen(
    ["journalctl", "-u", "ssh", "-f"],
    stdout=subprocess.PIPE,
    text=True
)

for line in process.stdout:
    if "Failed password" in line:
        ip_match = re.search(r'from (.*?) port', line)
        ip = ip_match.group(1) if ip_match else "Unknown"
        failed_attempts[ip] += 1
        count = failed_attempts[ip]
        
        if count >= 5:
            severity = "HIGH"
        elif count >= 3:
            severity = "MEDIUM"
        else:
            severity = "LOW"
            
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = (
            f"[{time_now}] | {severity} ALERT | "
            f"IP: {ip} | Attempts: {count} | {line.strip()}"
        )
        print("\n" + "="*60)
        print(alert_message)
        print("="*60)
        
        with open("alerts.log", "a") as f:
            f.write(alert_message + "\n")
            
        # 🛡️ ACTIVE DEFENSE ZONE 🛡️
        if severity == "HIGH":
            # 1. Trigger automated firewall rule blocking
            if ip not in blocked_ips and ip != "Unknown" and ip != "::1" and ip != "127.0.0.1":
                os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
                print(f"🛑 IPS ACTION: IP {ip} has been permanently dropped by iptables firewall!")
                blocked_ips.add(ip)
            
            # 2. Trigger administrative notification email
            if ip not in alerted_ips:
                send_email(alert_message)
                alerted_ips.add(ip)
