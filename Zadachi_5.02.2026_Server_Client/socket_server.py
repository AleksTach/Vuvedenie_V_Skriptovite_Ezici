import socket
import random
import datetime
import threading
import os

HOST = ''                 
PORT = 50007 
clients = []
clients_lock = threading.Lock()    

def broadcast(message, sender):
    with clients_lock:
        for conn in clients:
            if conn is not sender:
                conn.sendall(message)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data: break
                if data == b'time':
                    data = str(datetime.datetime.now()).encode()
                elif data == b'Number':
                    data = str(random.randint(1, 100)).encode()
                elif data == b'ip':
                    data = socket.gethostbyname(socket.gethostname()).encode()
                elif data == b'File':
                    with open('text.txt', 'r') as f:
                        data = f.read().encode()
                    data = b'Image opened!'
                conn.sendall(data)