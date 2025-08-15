from flask import Flask, render_template_string
import os

app = Flask(__name__)
LOG_FILE = "honeypot.log"

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>SSH Honeypot Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h1>SSH Honeypot Log Dashboard</h1>
    <table>
        <tr><th>Log Entry</th></tr>
        {% for entry in logs %}
        <tr><td>{{ entry }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    if not os.path.exists(LOG_FILE):
        logs = ["No log file found."]
    else:
        with open(LOG_FILE, "r") as f:
            logs = [line.strip() for line in f.readlines()]
    return render_template_string(HTML_TEMPLATE, logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
