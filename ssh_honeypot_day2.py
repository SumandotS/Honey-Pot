import socket
import threading
from datetime import datetime

LOG_FILE = "honeypot_log.txt"
HOST = "0.0.0.0"
PORT = 2222

def log_event(event):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {event}\n")

def handle_client(client_socket, address):
    ip, port = address
    log_event(f"Connection from {ip}:{port}")

    try:
        client_socket.sendall(b"SSH-2.0-OpenSSH_7.4\r\n")
        client_socket.sendall(b"login: ")
        username = client_socket.recv(1024).strip().decode(errors='ignore')

        client_socket.sendall(b"Password: ")
        password = client_socket.recv(1024).strip().decode(errors='ignore')

        log_event(f"Attempted login with username='{username}' and password='{password}'")

        client_socket.sendall(b"Access denied. Try again later.\r\n")

        # Optional: simulate command prompt
        client_socket.sendall(b"$ ")
        cmd = client_socket.recv(1024).strip().decode(errors='ignore')
        log_event(f"Received command after failed login: {cmd}")

        client_socket.sendall(b"Command not recognized. Session will close.\r\n")

    except Exception as e:
        log_event(f"Error handling client {ip}:{port} - {e}")
    finally:
        client_socket.close()

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] SSH honeypot running on {HOST}:{PORT}...")

    while True:
        client, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client, addr))
        client_thread.start()

if __name__ == "__main__":
    start_honeypot()
