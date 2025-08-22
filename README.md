Honey Pot 🕵️

Honey Pot is a custom SSH honeypot system designed to detect, log, and analyze unauthorized access attempts. Built from scratch in Python, it simulates a real SSH server to lure attackers, capture their activity, and provide insights into potential security threats. The project also includes a Flask-powered dashboard for real-time visualization of attack data.

✨ Features

SSH Honeypot – Mimics a real SSH server on a chosen port (default: 2222).

Logging System – Captures connection attempts (IP, username, password, timestamp).

Flask Dashboard – Web-based UI to monitor logs in a structured format.

Modular Design – Easy to extend with new features (alerts, geolocation, analytics).

Safe Environment – Currently runs locally to avoid exposure while testing.

🛠️ Tech Stack

Language: Python

Backend Framework: Flask (for dashboard)

Database/Storage: Log file system (honeypot_log)

Libraries: socket, threading, datetime, Flask

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/your-username/Honey-Pot.git
cd Honey-Pot


Run the Honeypot

python honeypot.py


The honeypot will start listening on port 2222.

Run the Flask Dashboard

python app.py


Open your browser at: http://localhost:5000

🚀 Future Enhancements

🌍 IP Geolocation – Map attacker IPs to physical locations.

📧 Email Alerts – Notify admins of suspicious login attempts.

📊 Advanced Dashboard – Graphs & analytics for attack trends.

☁️ Cloud Deployment – Deploy to a VPS for real-world data collection.

🔒 Disclaimer

This honeypot is for educational and research purposes only. Do not expose it to the public internet unless you fully understand the security risks involved.

🤝 Contributing

Contributions are welcome! Feel free to fork this repo, open issues, or submit pull requests.
