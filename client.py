import socket
import utils
import time

HOST = '127.0.0.1'#socket.gethostbyname(socket.gethostname())
PORT = 18018
FORMAT = "utf-8"
RECVSIZE = 10
DISCONNECT_MESSAGE = '!DISCONNECT'
BOOTSTRAP_PEER = ['45.63.84.226:18018', '45.63.89.228:18018', '144.202.122.8:18018']


message_hello = utils.message(message_type='hello', input_dict={}).content_json
message_getpeer = utils.message(message_type='getpeer', input_dict={}).content_json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# receive hello message
msg_recv = utils.message_receiver(s, RECVSIZE=RECVSIZE, FORMAT=FORMAT)
msg_recv_iter = iter(msg_recv)
msg = next(msg_recv_iter)
print(msg)
# implement PSET1 1.7.a
# send hello message
msg = f"{message_hello}\n"
s.send(bytes(msg,FORMAT))
msg = next(msg_recv_iter) # receive the hello message
print(msg)
msg = next(msg_recv_iter) # receive the getpeer message
print(msg)
peer_list = BOOTSTRAP_PEER.copy()
peer_list.append(f'{HOST}:{PORT}')
msg = utils.message(message_type='peers', input_dict={'peers':peer_list}).content_json
msg = f"{msg}\n"
print(msg)
s.send(bytes(msg,FORMAT))
print('set peer list')
# time.sleep(1)
# s.send(bytes(DISCONNECT_MESSAGE,FORMAT))
s.close()