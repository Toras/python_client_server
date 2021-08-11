import unittest
import json
from utils import get_message, send_message


class TestSocket:
    __slots__ = ['test_dict', 'enc_msg', 'rcv_msg']

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.enc_msg = None
        self.rcv_msg = None

    def send(self, msg_to_send):
        json_test_msg = json.dumps(self.test_dict)
        self.enc_msg = json_test_msg.encode('utf-8')
        self.rcv_msg = msg_to_send

    def recv(self, max_len):
        json_test_msg = json.dumps(self.test_dict)
        return json_test_msg.encode('utf-8')


class TestUtils(unittest.TestCase):
    test_dict_send_presence = {
        'action': 0,
        'timestamp': 1234
    }

    dict_200 = {
        'response': 200,
        'timestamp': 1234,
        'alert': 'OK'
    }

    dict_400_action = {
        'response': 400,
        'timestamp': 1234,
        'error': 'wrong action'
    }

    dict_400_msg_format = {
        'response': 400,
        'timestamp': 1234,
        'error': 'wrong msg format'
    }

    def test_send_msg(self):
        test_socket = TestSocket(self.test_dict_send_presence)
        send_message(test_socket, self.test_dict_send_presence, 'utf-8')
        self.assertEqual(test_socket.enc_msg, test_socket.rcv_msg)

    def test_get_msg(self):
        test_socket_200 = TestSocket(self.dict_200)
        test_socket_400_action = TestSocket(self.dict_400_action)
        test_socket_400_msg_format = TestSocket(self.dict_400_msg_format)
        self.assertEqual(get_message(test_socket_200, 1024, 'utf-8'), self.dict_200)
        self.assertEqual(get_message(test_socket_400_action, 1024, 'utf-8'), self.dict_400_action)
        self.assertEqual(get_message(test_socket_400_msg_format, 1024, 'utf-8'), self.dict_400_msg_format)


if __name__ == '__main__':
    unittest.main()
