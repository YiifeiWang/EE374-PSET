# test.py

from utils import message

# test the class message

def test_class_message():
    message_type_list = {'hello', 'error', 'getpeers'}

    for message_type in message_type_list:
        if message_type=='error':
            input_dict = {"name": "INVALID_FORMAT",
                "description": "The note field in the block message contains more than 128 characters."}
        else:
            input_dict = {}
        message_ins = message(message_type=message_type, input_dict=input_dict)
        print(message_ins.content_json)
        print(type(message_ins.content_binary))
        message_tmp = message()
        message_tmp.build_from_json(message_ins.content_json)
        print(message_tmp.content_json)


if __name__ == '__main__':
    test_class_message()