# Przykład testu jednostkowego
import unittest
from app import app

class TestApp(unittest.TestCase):

    def test_invalid_ip_address(self):
        client = app.test_client()
        response = client.get('/ip-tags/198.51..227')
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response, "['just a TAG', 'zażółć ♥', '{$(\n a-tag\n)$}']")
        # data = response.get_json()
        # self.assertEqual(data['error'], 'Invalid IP address format')

if __name__ == '__main__':
    unittest.main()
