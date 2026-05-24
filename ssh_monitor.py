kfrom flask import Flask, render_template_string
import sqlite3
app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SOC SQL Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f111a; color: #a6accd; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #00d2ff; text-shadow: 0 0 10px rgba(0,210,255,0.3); }
        .container { max-width: 1200px; margin: auto; }
        table { width: 100%; border-collapse: collapse; background: #151824; margin-top: 20px; border-radius: 8px; overflow: hidden; }
        th, td { padding: 14px; text-align: center; border-bottom: 1px solid #23283d; }
        th { background: #1e2235; color: #00d2ff; font-weight: 600; }
        .LOW { background-color: rgba(241, 196, 15, 0.15); color: #f1c40f; }
        .MEDIUM { background-color: rgba(230, 126, 34, 0.15); color: #e67e22; }
        .HIGH { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; font-weight: bold; animation: pulse 2s infinite; }
        @keyframes pulse { 50% { background-color: rgba(231, 76, 60, 0.4); } }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔵 SOC Advanced Database SIEM</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Timestamp</th>
                <th>Source IP Address</th>
                <th>Attempt Count</th>
                <th>Severity Level</th>
                <th>Raw Security Logs</th>
            </tr>
            {% for log in logs %}
            <tr class="{{log[2]}}">
                <td>{{log[0]}}</td>
                <td>{{log[1]}}</td>
                <td>{{log[3]}}</td>
                <td>{{log[4]}}</td>
                <td><strong>{{log[2]}}</strong></td>
                <td style="text-align: left; font-size: 12px; font-family: monospace;">{{log[5]}}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    logs = []
    try:
        conn = sqlite3.connect("soc_data.db")
        cursor = conn.cursor()
        # Querying the database directly for clean structured sorting
        cursor.execute("SELECT id, timestamp, severity, ip_address, attempt_count, raw_log FROM ssh_alerts ORDER BY id DESC LIMIT 50")
        logs = cursor.fetchall()
        conn.close()
    except Exception as e:
        print("Database Error:", e)
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
