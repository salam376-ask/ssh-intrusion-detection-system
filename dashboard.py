from flask import Flask, render_template_string
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SOC Dashboard</title>
    <style>
        body { font-family: Arial; background: #111; color: white; }
        h1 { text-align: center; margin-top: 20px;}
        table { width: 95%; margin: 30px auto; border-collapse: collapse; box-shadow: 0 0 10px rgba(255,255,255,0.1); }
        th, td { padding: 12px; border: 1px solid #444; text-align: center; }
        th { background-color: #222; color: #00d2ff; }
        .LOW { background-color: #f1c40f; color: black; font-weight: bold; }
        .MEDIUM { background-color: #e67e22; color: white; font-weight: bold; }
        .HIGH { background-color: #e74c3c; color: white; font-weight: bold; animation: blinker 1.5s linear infinite; }
        @keyframes blinker { 50% { opacity: 0.6; } }
    </style>
</head>
<body>
    <h1>🔵 SOC SSH Monitoring Dashboard</h1>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>Source IP Address</th>
            <th>Attempt Logs Count</th>
            <th>Severity Rating</th>
            <th>Raw Syslog Message Payload</th>
        </tr>
        {% for log in logs %}
        <tr class="{{log.severity}}">
            <td>{{log.time}}</td>
            <td>{{log.ip}}</td>
            <td>{{log.attempts}}</td>
            <td>{{log.severity}}</td>
            <td>{{log.message}}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    logs = []
    try:
        with open("alerts.log", "r") as f:
            lines = f.readlines()
            # Ingesting the last 20 log actions for processing display
            for line in lines[-20:]:
                parts = line.split("|")
                time = parts[0].strip("[] ")
                severity = parts[1].split()[0].strip()
                ip = parts[2].replace("IP:", "").strip()
                attempts = parts[3].replace("Attempts:", "").strip()
                message = parts[4].strip()
                logs.append({
                    "time": time,
                    "severity": severity,
                    "ip": ip,
                    "attempts": attempts,
                    "message": message
                })
    except:
        pass
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
