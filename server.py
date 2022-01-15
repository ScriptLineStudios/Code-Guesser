import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5050))
server.listen()

conn, addr = server.accept()

data = []

while True:
    msg = conn.recv(2048).decode("utf-32")
    print(msg)
