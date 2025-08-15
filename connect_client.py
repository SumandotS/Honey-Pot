import socket

HOST = "127.0.0.1"
PORT = 2222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    banner = s.recv(1024).decode()
    print(banner)

    s.recv(1024)  # login:
    s.send(b"root\n")

    s.recv(1024)  # password:
    s.send(b"toor\n")  # 'root' reversed is 'toor'

    try:
        response = s.recv(1024).decode()
        print(response)
    except:
        pass
