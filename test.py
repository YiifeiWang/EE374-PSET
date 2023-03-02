# test.py

from utils import message
import hashlib
import json

# test the class message

BOOTSTRAP_PEER = ['45.63.84.226:18018', '45.63.89.228:18018', '144.202.122.8:18018']


def test_class_message():
    message_type_list = {'hello', 'error', 'getpeers','peers'}


    for message_type in message_type_list:
        if message_type=='error':
            input_dict = {"name": "INVALID_FORMAT",
                "description": "The note field in the block message contains more than 128 characters."}
        elif message_type=='peers':
            input_dict = {"peers": BOOTSTRAP_PEER.copy()}
        else:
            input_dict = {}
        message_ins = message(message_type=message_type, input_dict=input_dict)
        print(message_ins.content_json)
        print(type(message_ins.content_binary))
        message_tmp = message()
        message_tmp.build_from_json(message_ins.content_json)
        print(message_tmp.content_json)

def test_hash():
    # implement PSET2 1.2
    # hashlib.blake2s
    genesis_block = {
  "T": "00000000abc00000000000000000000000000000000000000000000000000000",
  "created": 1671062400,
  "miner": "Marabu",
  "nonce": "000000000000000000000000000000000000000000000000000000021bea03ed",
  "note": "The New York Times 2022-12-13: Scientists Achieve Nuclear Fusion Breakthrough With Blast of 192 Lasers",
  "previd": None,
  "txids": [],
  "type": "block"
}
    print(hashlib.blake2s(json.dumps(genesis_block).encode('utf-8')).hexdigest())

if __name__ == '__main__':
    # test_class_message()
    test_hash()