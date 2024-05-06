import unittest
from app import app

class TestApp(unittest.TestCase):
    """
    Unit tests for the web application functions.

    Each test method within this class represents a specific test scenario.
    """

    def test_invalid_ip_address(self):
        """
        Test to check handling of invalid IP address.

        Checks whether the server returns a response status code 400 for an invalid IP address.
        """
        client = app.test_client()
        response = client.get('/ip-tags/198.51..22')
        self.assertEqual(response.status_code, 400)

    def test_valid_ip_tags(self):
        """
        Test to check correctness of returned tags for a valid IP address.

        Checks whether the server returns a response status code 200 and expected data in the form of a list of tags.
        """
        client = app.test_client()
        response = client.get('/ip-tags/198.51.100.227')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertListEqual(data, ["just a TAG","za\u017c\u00f3\u0142\u0107 \u2665","{$(\n a-tag\n)$}"])

    def test_valid_ip_tags_report(self):
        """
        Test to check correctness of HTML report generation for a valid IP address.

        Checks whether the server returns a response status code 200 and whether the HTML content contains an expected <table> tag.
        """
        client = app.test_client()
        response = client.get('/ip-tags-report/198.51.100.227')
        self.assertEqual(response.status_code, 200)
        html_content = response.get_data(as_text=True)
        self.assertIn('<table border=\'1\'>', html_content)

    def test_invalid_ip_tags_report(self):
        """
        Test to check handling of invalid IP address during report generation.

        Checks whether the server returns a response status code 400 and an expected error message for an invalid IP address.
        """
        client = app.test_client()
        response = client.get('/ip-tags-report/198.51..22s')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data, {'error': 'Bad request', 'message': 'Invalid IPv4 address format.'})

if __name__ == '__main__':
    unittest.main()
