import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((socket.gethostname(),6060))

message = s.recv(2048)
print(f"Message received: {message}")
