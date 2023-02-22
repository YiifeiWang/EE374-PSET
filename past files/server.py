import socket
import threading
import time
import utils

# time.sleep(1) # wait 1 second
# print("hello")

HEADER = 64
PORT = 18018
SERVER = '127.0.0.1'
# SERVER = socket.gethostbyname(socket.gethostname()) #inner address
# print(SERVER) # should print 10.34.169.14
ADDR = (SERVER, PORT) #shortname for address
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

message_hello = utils.message(message_type='hello', input_dict={})

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup

server.bind(ADDR)

def handle_client(conn, addr): #conn stands for connect
    # handle inidividual connection for each client
    print('[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # print(msg_length)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            conn.send("Message received".encode(FORMAT))
            
            # msg_instance = utils.message()
            # # assume that msg is already in json format
            # msg_instance.build_from_json(msg)
            # if msg_instance.message_type != 'hello':
            #     # send invalid format error
            #     message = utils.message(message_type='error', input_dict={"name": "INVALID_FORMAT"}).content_json.endcode(FORMAT)
            #     send_length = str(msg_length).encode(FORMAT)
            #     send_length += b' '*(HEADER-len(send_length))
            #     conn.send(send_length)
            #     conn.send(message)
            #     connected = False
            # else:
            #     message = utils.message(message_type='hello', input_dict={}).content_json.endcode(FORMAT)
            #     send_length = str(msg_length).encode(FORMAT)
            #     send_length += b' '*(HEADER-len(send_length))
            #     conn.send(send_length)
            #     conn.send(message)

            
            

            print("[{}] {}".format(addr,msg))
            
    
    conn.close()
    
# def handle_first_connection(msg, first_connect=False):
#     # handle 7b assume that they will send in our desired format
#     # such that we first get a message with message length
#     # then we get the message

#     if first_connect:
#         if msg
#     else:
#         pass

def start():
    server.listen() # listen to new connection
    print("[LISTENING] server is listening on {}".format(SERVER))
    while True:
        conn, addr = server.accept()
        # pass conn, addr to handle_client
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        # tells how many threads are running
        print('[ACTIVE CONNECTIONS] {}'.format(threading.active_count()-1)) 


print('[STARTING] server is starting ...')
start()