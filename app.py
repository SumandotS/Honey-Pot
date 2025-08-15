from flask import Flask, render_template
import re

app = Flask(__name__)

LOG_FILE = 'honeypot_log.txt'

def parse_log():
    entries = []
    with open(LOG_FILE, 'r') as file:
        for line in file:
            match = re.search(
                r'Connection from ([\d.]+):(\d+) \| Location: (.*?) - (.*?), (.*?) \| ISP: (.*)', 
                line
            )
            if match:
                ip, port, country, region, city, isp = match.groups()
                entries.append({
                    'ip': ip,
                    'port': port,
                    'country': country,
                    'region': region,
                    'city': city,
                    'isp': isp
                })
    return entries

@app.route('/')
def index():
    logs = parse_log()
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
