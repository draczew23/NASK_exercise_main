import unittest
from app import app

class TestApp(unittest.TestCase):

    def test_invalid_ip_address(self):
        client = app.test_client()
        response = client.get('/ip-tags/198.51..22')
        self.assertEqual(response.status_code, 400)

    def test_valid_ip_tags(self):
        client = app.test_client()
        response = client.get('/ip-tags/198.51.100.227')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertListEqual(data, ["just a TAG","za\u017c\u00f3\u0142\u0107 \u2665","{$(\n a-tag\n)$}"])

    def test_valid_ip_tags_report(self):
        client = app.test_client()
        response = client.get('/ip-tags-report/198.51.100.227')
        self.assertEqual(response.status_code, 200)
        html_content = response.get_data(as_text=True)
        self.assertIn('<table border=\'1\'>', html_content)

    def test_invalid_ip_tags_report(self):
        client = app.test_client()
        response = client.get('/ip-tags-report/198.51..22s')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data, {'error': 'Bad request', 'message': 'Invalid IPv4 address format.'})

if __name__ == '__main__':
    unittest.main()
