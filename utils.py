# utils.py

# This builds a general class of message

import json

class message:
    def __init__(self, message_type='hello', input_dict={}):
        self.message_type = message_type
        self.input_dict = input_dict
        self.content = ''
        self.content_json = '' # JSON
        self.content_binary = '' # binary
        self.convert2content() # read input_dict based on message_type to write on content
        self.convert2json()
        self.convert2binary()

    def convert2content(self):
        # read input_dict based on message_type to write on content
        if self.message_type == 'hello':
            self.content = {"version": "0.9.0",
                            "agent": "Marabu-Core Client 0.9"}
        elif self.message_type == 'error':
            self.content = self.input_dict
            # input_dict_example = {"name": "INVALID_FORMAT",
            #    "description": "The note field in the block message contains more than 128 characters."}
        elif self.message_type == 'getpeers':
            self.content = {}

        self.content['type'] = self.message_type

    def convert2json(self):
        self.content_json = json.dumps(self.content)

    def convert2binary(self):
        self.content_binary = self.content_json.encode('ascii') #' '.join(format(ord(letter), 'b') for letter in self.content_json)

    def build_from_json(self, json_str):
        self.content_json = json_str
        self.content = json.loads(json_str)
        self.message_type = self.content['type']
        self.input_dict = self.content

class message_receiver:
    # create an iterator to receive message
    def __init__(self,conn,RECVSIZE=10,FORMAT='utf-8'):
        self.conn = conn
        self.RECVSIZE = RECVSIZE
        self.FORMAT = FORMAT
        self.buffer = ''
        self.messages = []

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            msg = self.conn.recv(self.RECVSIZE)
            self.buffer += msg.decode(self.FORMAT)
            self.messages = self.buffer.split('\n')
            if len(self.messages) > 1:
                self.buffer = ''
                for i in range(1,len(self.messages)):
                    if i<len(self.messages)-1:
                        self.buffer += self.messages[i] + '\n'
                    else:
                        self.buffer += self.messages[i]
                return self.messages[0]

def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        return False
    return True