import unittest
from datetime import datetime
from user import CustomUser
from user_list_generator import  CustomUserListGenerator
from user_online_predictor import UserOnlinePredictorWithPrediction
from users_online_predictor import UserOnlinePredictor

class TestCustomUserIntegration(unittest.TestCase):

    def setUp(self):
        # Sample user data
        self.user_data = [
            {
                "nickname": "user1",
                "lastSeenDate": "2023-10-17T10:00:00.000",
                "isOnline": True
            },
            {
                "nickname": "user2",
                "lastSeenDate": "2023-10-16T20:30:00.000",
                "isOnline": False,
            },
            {
                "nickname": "user3",
                "lastSeenDate": "2023-10-16T21:45:00.000",
                "isOnline": False,
            },
        ]

        # Current date and time
        self.current_time = datetime(2023, 10, 17, 11, 0)

        # Generate custom users
        self.custom_user_generator = CustomUserListGenerator()
        self.custom_users = self.custom_user_generator.get_custom_users(self.user_data)
        self.custom_user_generator.custom_when_online(self.custom_users, self.current_time)

    def test_predict_user_online(self):
        # Test predicting a single user's online status
        predictor = UserOnlinePredictorWithPrediction(self.custom_users)
        result = predictor.predict_user_online("user1", "2023-10-17-10:30", 0.5)
        self.assertEqual(result["willBeOnline"], False)

        result = predictor.predict_user_online("user2", "2023-10-17-10:30", 0.5)
        self.assertEqual(result["willBeOnline"], False)

        result = predictor.predict_user_online("nonexistent_user", "2023-10-17-10:30", 0.5)
        self.assertEqual(result["error"], "User not found.")

    def test_predict_user_online_invalid_date_format(self):
        # Test predicting user online with an invalid date format
        predictor = UserOnlinePredictorWithPrediction(self.custom_users)
        result = predictor.predict_user_online("user1", "2023-10-17-1030", 0.5)
        self.assertEqual(result["error"], "Invalid date format.")


if __name__ == '__main__':
    unittest.main()
