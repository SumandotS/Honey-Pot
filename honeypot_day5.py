# honeypot_day5.py

import socket
import threading
import datetime

HOST = '0.0.0.0'
PORT = 2222
LOG_FILE = 'honeypot_log.txt'

def log_event(data):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} {data}\n")
    print(f"{timestamp} {data}")

def fake_shell(conn, addr):
    try:
        # Send fake SSH banner
        conn.sendall(b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n")

        # Simulate SSH login prompts
        conn.sendall(b"login: ")
        username = conn.recv(1024).strip().decode(errors='ignore')
        conn.sendall(b"password: ")
        password = conn.recv(1024).strip().decode(errors='ignore')

        log_event(f"[{addr[0]}] Login attempt with username='{username}' password='{password}'")

        # Pretend login was successful
        conn.sendall(b"\nWelcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.15.0 x86_64)\n\n")
        conn.sendall(b"$ ")

        while True:
            cmd = conn.recv(1024).strip().decode(errors='ignore')
            if not cmd:
                break

            log_event(f"[{addr[0]}] Command: {cmd}")

            # Fake command responses
            if cmd == "ls":
                conn.sendall(b"Desktop  Documents  Downloads  Music  Pictures\n$ ")
            elif cmd == "pwd":
                conn.sendall(b"/home/fakeuser\n$ ")
            elif cmd == "whoami":
                conn.sendall(f"{username}\n$ ".encode())
            elif cmd in ["exit", "quit"]:
                conn.sendall(b"logout\n")
                break
            else:
                conn.sendall(f"bash: {cmd}: command not found\n$ ".encode())
    except Exception as e:
        log_event(f"Error with {addr[0]}: {str(e)}")
    finally:
        conn.close()

def start_honeypot():
    log_event(f"[+] Starting SSH honeypot on {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        log_event(f"[+] Connection from {addr[0]}:{addr[1]}")
        threading.Thread(target=fake_shell, args=(conn, addr)).start()

if __name__ == '__main__':
    start_honeypot()
