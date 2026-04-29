import socket

# local host and port to listen on
HOST = '127.0.0.1'
PORT = 10000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  print(f'Connected to server at {HOST}:{PORT}')
  while True:
    message = input('Enter message to send to server (or "exit" to quit): ')
    if message.lower() == 'exit':
      print('Exiting client.')
      break
    s.sendall(message.encode())
    data = s.recv(1024)
    print(f'Received from server: {data.decode()}')
 