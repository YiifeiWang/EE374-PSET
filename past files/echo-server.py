# echo-server.py

import socket
from utils import message

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 18018  # Port to listen on (non-privileged ports are > 1023)

# initilize message based on the class message
hello_msg = message(message_type='hello')
hello_json = hello_msg.content_json
hello_binary = hello_msg.content_binary
getpeers_msg = message(message_type='getpeers')
getpeers_json = getpeers_msg.content_json
getpeers_binary = getpeers_msg.content_binary

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        conn.sendall(hello_binary)
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

