import json

actions = {
    0: 'presence',
    1: 'probe',
    2: 'msg',
    3: 'quit',
    4: 'authenticate',
    5: 'leave',
}


def get_message(sock, package_len, enc):
    byte_msg = sock.recv(package_len)
    if isinstance(byte_msg, bytes):
        json_msg = byte_msg.decode(enc)
        msg = json.loads(json_msg)
        if isinstance(msg, dict):
            return msg
        raise ValueError
    raise ValueError


def send_message(sock, msg, enc):
    json_msg = json.dumps(msg)
    byte_msg = json_msg.encode(enc)
    sock.send(byte_msg)
