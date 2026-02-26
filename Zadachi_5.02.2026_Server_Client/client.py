import socket

HOST = '10.101.211.49'
PORT = 50007         # The same port as used by the server

choice = input("Enter time, file, or random to be sent to the server:")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(choice.encode('utf-8'))
    data = s.recv(2048)
    message = data.decode("utf-8")
    print('Received', message)