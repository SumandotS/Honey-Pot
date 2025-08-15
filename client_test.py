import socket

s = socket.socket()
s.connect(('127.0.0.1', 2222))
data = s.recv(1024)
print("Received from server:", data.decode('utf-8'))
s.close()
