import socket

HOST = '127.0.0.1'
PORT = 10501         # The same port as used by the server

choice = input("Enter time, file, or random to be sent to the server:")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(choice.encode('utf-8'))
    data = s.recv(2048)
    message = data.decode("utf-8")
    print('Received', message)