import unittest
from unittest.mock import Mock, patch
from data_fetcher import CustomDataFetcher  # Import your CustomDataFetcher class

class TestCustomDataFetcher(unittest.TestCase):
    @patch('data_fetcher.requests.get')
    def test_get_custom_data_from_url_success(self, mock_requests_get):
        # Create an instance of CustomDataFetcher
        data_fetcher = CustomDataFetcher()

        # Mock a successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"data": ["user1", "user2"]}'
        mock_requests_get.return_value = mock_response

        # Call the method under test
        result = data_fetcher.get_custom_data_from_url("https://sef.podkolzin.consulting/api/users/lastSeen", 2)

        # Assert that the method returns the expected data
        self.assertEqual(result, ["user1", "user2"])

if __name__ == '__main__':
    unittest.main()
