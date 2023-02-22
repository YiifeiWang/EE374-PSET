import socket
import threading
import time
import utils

# define constants
HOST = '127.0.0.1'#socket.gethostbyname(socket.gethostname())
PORT = 18018
FORMAT = "utf-8"
RECVSIZE = 10
DISCONNECT_MESSAGE = '!DISCONNECT'

# predefine messages
message_hello = utils.message(message_type='hello', input_dict={}).content_json

def handle_client(conn, addr): #conn stands for connect
    # handle inidividual connection for each client
    print(f"[NEW CONNECTION] {addr} connected.")
    msg = f"{message_hello}\n"
    conn.send(bytes(msg,FORMAT))
    msg_recv = utils.message_receiver(conn, RECVSIZE=RECVSIZE, FORMAT=FORMAT)
    msg_recv_iter = iter(msg_recv)
    connected = True
    while connected:
        msg = next(msg_recv_iter)
        print(msg) # print the message for debugging

        # implement PSET1 1.6
        # examine whether msg is a valid json string
        # if not, send error message and close the connection
        if not utils.is_json(msg):
            print('invalid message')
            msg = utils.message(message_type='error', input_dict={"name": "INVALID_FORMAT","description": ""}).content_json
            msg = f"{msg}\n"
            conn.send(bytes(msg,FORMAT))
            connected = False


        if msg == DISCONNECT_MESSAGE:
            connected = False

    conn.close()

def start():
    server.listen() # listen to new connection
    print("[LISTENING] server is listening on {}".format(PORT))
    while True:
        conn, addr = server.accept()
        # pass conn, addr to handle_client
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        # tells how many threads are running
        print('[ACTIVE CONNECTIONS] {}'.format(threading.active_count()-1)) 
        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print('[STARTING] server is starting ...')
start()