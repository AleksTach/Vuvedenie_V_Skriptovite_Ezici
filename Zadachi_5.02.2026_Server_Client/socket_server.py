from datetime import datetime
import socket
import random

HOST = '127.0.0.1'
PORT = 10501
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                cmd = data.decode('utf-8')
                if cmd == "time":
                    response = f"{datetime.now()}"
                elif cmd == "number":
                    response = f"{random.randint(1, 100)}"
                elif cmd == "file":
                    with open("test.txt") as f:
                        response = f.read()
                else:
                    response = "Bad command"
                conn.sendall(response.encode())