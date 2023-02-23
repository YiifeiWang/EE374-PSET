import socket
import utils
import time
import json

HOST = ''#socket.gethostbyname(socket.gethostname())
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
# msg = f"{message_hello}\n"
str = json.dumps({"type":"hello"})
msg = f"{str}\n"
s.send(bytes(msg,FORMAT))
# send getpeers message
msg = f"{message_getpeer}\n"
s.send(bytes(msg,FORMAT))
# receive peers message
msg = next(msg_recv_iter)
print(msg)
msg = f"{DISCONNECT_MESSAGE}\n"
s.send(bytes(msg,FORMAT))
s.close()


# msg = next(msg_recv_iter) # receive the getpeer message
# print(msg)
# print('copy peer list')
# peer_list = BOOTSTRAP_PEER.copy()
# # peer_list.append(f'{HOST}:{PORT}')
# msg = utils.message(message_type='peers', input_dict={'peers':peer_list}).content_json
# msg = f"{msg}\n"
# print(msg)
# print('set peer list')
# s.send(bytes(msg,FORMAT))
