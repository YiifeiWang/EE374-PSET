import socket
import threading
import time
import utils

# define constants
# HOST = '127.0.0.1'#socket.gethostbyname(socket.gethostname())
HOST = ''
PORT = 18018
FORMAT = "utf-8"
RECVSIZE = 10
DISCONNECT_MESSAGE = '!DISCONNECT'
BOOTSTRAP_PEER = ['45.63.84.226:18018', '45.63.89.228:18018', '144.202.122.8:18018']

# predefine messages
message_hello = utils.message(message_type='hello', input_dict={}).content_json
message_getpeer = utils.message(message_type='getpeer', input_dict={}).content_json

def handle_client(conn, addr): #conn stands for connect
    # handle inidividual connection for each client
    print(f"[NEW CONNECTION] {addr} connected.")
    # implement PSET1 1.7.a
    msg = f"{message_hello}\n"
    conn.send(bytes(msg,FORMAT))
    msg_recv = utils.message_receiver(conn, RECVSIZE=RECVSIZE, FORMAT=FORMAT)
    msg_recv_iter = iter(msg_recv)
    connected = True
    first_connection = True
    peer_list = BOOTSTRAP_PEER.copy()
    while connected:
        msg = next(msg_recv_iter)
        print(f"[INFO] receive {msg}") # print the message for debugging

        # implement PSET1 1.6
        # examine whether msg is a valid json string
        # if not, send error message and close the connection
        if not utils.is_json(msg):
            print('[INFO] invalid message')
            msg = utils.message(message_type='error', input_dict={"name": "INVALID_FORMAT","description": ""}).content_json
            msg = f"{msg}\n"
            conn.send(bytes(msg,FORMAT))
            connected = False

        # implement PSET1 1.7.b
        # examine whether msg is a valid hello message in first connection
        # if not, send error message and close the connection
        msg_ins = utils.message()
        msg_ins.build_from_json(msg)
        if first_connection:
            if msg_ins.message_type != 'hello' or msg_ins.content != utils.message(message_type='hello', input_dict={}).content:
                print('[INFO] invalid hello message')
                msg = utils.message(message_type='error', input_dict={"name": "INVALID_HANDSHAKE","description": ""}).content_json
                msg = f"{msg}\n"
                conn.send(bytes(msg,FORMAT))
                connected = False
            else:
                print('[INFO] valid hello message')
                msg = f"{message_getpeer}\n"
                conn.send(bytes(msg,FORMAT)) # send getpeer message
                # print('[INFO] send getpeer message')
                # msg = next(msg_recv_iter)
                # print(f"[INFO] receive {msg}") # print the message for peer list
                # # assume that msg is with valid format
                # msg_ins = utils.message()
                # msg_ins.build_from_json(msg)
                # peer_list += msg_ins.input_dict['peers']
                # peer_list = list(set(peer_list)) # remove duplicates
                # print(f"[INFO] peer list: {peer_list}")
        first_connection = False

        if msg_ins.message_type == 'getpeer':
            msg = utils.message(message_type='peers', input_dict={'peers':peer_list}).content_json
            msg = f"{msg}\n"
            print(f"[INFO] send {msg}")
            conn.send(bytes(msg,FORMAT))
        
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