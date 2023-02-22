import socket
import utils
import time

HOST = '127.0.0.1' #socket.gethostbyname(socket.gethostname())
PORT = 18018
FORMAT = "utf-8"
RECVSIZE = 10
DISCONNECT_MESSAGE = '!DISCONNECT'

message_hello = utils.message(message_type='hello', input_dict={}).content_json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
# receive hello message
msg_recv = utils.message_receiver(s, RECVSIZE=RECVSIZE, FORMAT=FORMAT)
msg_recv_iter = iter(msg_recv)
msg = next(msg_recv_iter)
print(msg)
# send hello message
msg = f"hello \n"
# msg = f"{message_hello}\n"
s.send(bytes(msg,FORMAT))
msg = next(msg_recv_iter) # receive the error message
print(msg)
# time.sleep(1)
# s.send(bytes(DISCONNECT_MESSAGE,FORMAT))
s.close()