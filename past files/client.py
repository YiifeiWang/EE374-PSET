import socket
import utils

HEADER = 64
PORT = 18018
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = '127.0.0.1'
ADDR = (SERVER, PORT)

message_hello = utils.message(message_type='hello', input_dict={})

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER-len(send_length))

    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    # msg_length = client.recv(HEADER).decode(FORMAT)
    # if msg_length:
    #     msg_length = int(msg_length)
    #     msg_recv = client.recv(msg_length).decode(FORMAT)
    #     print(msg_recv)

# send(message_hello.content_json)
# input()
send("Hello!")
send(DISCONNECT_MESSAGE)