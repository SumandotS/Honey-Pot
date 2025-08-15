import socket
import threading
import logging
import datetime
import requests
import smtplib
from email.mime.text import MIMEText

HOST = '0.0.0.0'
PORT = 2222
LOG_FILE = 'honeypot_log.txt'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
)

def send_email_alert(ip, geo):
    sender_email = "sumangowda0010@gmail.com"
    receiver_email = "sumans100305@gmail.com"
    app_password = "sjmnywsxcsdztiin"

    subject = f"[SSH Honeypot] Connection from {ip}"
    body = f"""
    A new SSH connection was detected.

    IP Address: {ip}
    Location: {geo.get('city', 'Unknown')}, {geo.get('regionName', '')}, {geo.get('country', '')}
    ISP: {geo.get('isp', 'N/A')}
    Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"[+] Email alert sent to {receiver_email}")
    except Exception as e:
        print(f"[!] Failed to send email: {e}")

def get_geolocation(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return data  # Return full dictionary
        else:
            return {"city": "Unknown", "regionName": "", "country": "", "isp": "N/A"}
    except Exception as e:
        return {"city": "Unknown", "regionName": "", "country": "", "isp": f"Error: {e}"}

def handle_client(conn, addr):
    real_ip, port = addr
    ip = "103.21.244.0"  # Replace with real_ip in production
    geo = get_geolocation(ip)

    log_entry = f"Connection from {ip}:{port} | Location: {geo.get('country', 'Unknown')} - {geo.get('regionName', '')}, {geo.get('city', '')} | ISP: {geo.get('isp', 'N/A')}"
    print(log_entry)
    logging.info(log_entry)

    banner = "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n"
    conn.send(banner.encode())

    send_email_alert(ip, geo)

    conn.close()

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Starting SSH honeypot on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_honeypot()
