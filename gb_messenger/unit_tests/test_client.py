import unittest
from client.client import action_to_server


class TestClient(unittest.TestCase):
    dict_action_answer = {
        'action': 0,
        'timestamp': 1234
    }

    def test_action_to_server(self):
        test_call = action_to_server(0)
        test_call['timestamp'] = 1234
        self.assertEqual(test_call, self.dict_action_answer)


if __name__ == '__main__':
    unittest.main()
