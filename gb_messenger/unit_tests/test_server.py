import unittest
from server.server import action_from_client


class TestServer(unittest.TestCase):
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

    def test_no_action(self):
        test_call = action_from_client({'timestamp': int(1234)})
        test_call['timestamp'] = 1234
        self.assertEqual(test_call, self.dict_400_msg_format)

    def test_no_time(self):
        test_call = action_from_client({'action': 1})
        test_call['timestamp'] = 1234
        self.assertEqual(test_call, self.dict_400_msg_format)

    def test_wrong_action(self):
        test_call = action_from_client({'action': 45, 'timestamp': int(1234)})
        test_call['timestamp'] = 1234
        self.assertEqual(test_call, self.dict_400_action)

    def test_ok(self):
        test_call = action_from_client({'action': 0, 'timestamp': int(1234)})
        test_call['timestamp'] = 1234
        self.assertEqual(test_call, self.dict_200)


if __name__ == '__main__':
    unittest.main()
