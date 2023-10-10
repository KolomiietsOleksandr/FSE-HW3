import unittest
from datetime import datetime
from user_list_generator import CustomUserListGenerator
from UserStatsUserController import UserStatsHistoryController

class TestUserStatsHistoryController(unittest.TestCase):

    def setUp(self):
        custom_data = [
            {"nickname": "user1", "lastSeenDate": "2023-10-01T12:00:00.000Z", "isOnline": True, "lastSeenTime": None},
            {"nickname": "user2", "lastSeenDate": "2023-10-01T13:00:00.000Z", "isOnline": False, "lastSeenTime": None},
            {"nickname": "user3", "lastSeenDate": "2023-10-01T14:00:00.000Z", "isOnline": True, "lastSeenTime": None},
        ]
        self.controller = UserStatsHistoryController(custom_data)

    def test_get_user_history_user_found_online(self):
        result, status_code = self.controller.get_user_history("user1", "2023-10-01-12:30")
        self.assertEqual(status_code, 200)
        self.assertEqual(result["wasUserOnline"], True)
        self.assertIsNone(result["nearestOnlineTime"])

    def test_get_user_history_user_found_offline(self):
        result, status_code = self.controller.get_user_history("user2", "2023-10-01-12:30")
        self.assertEqual(status_code, 200)
        self.assertEqual(result["wasUserOnline"], False)
        self.assertEqual(result["nearestOnlineTime"], "2023-10-01-13:00")

    def test_get_user_history_user_not_found(self):
        result, status_code = self.controller.get_user_history("user4", "2023-10-01-12:30")
        self.assertEqual(status_code, 404)
        self.assertIsNone(result["wasUserOnline"])
        self.assertIsNone(result["nearestOnlineTime"])

    def test_find_nearest_online_time(self):
        custom_users = self.controller.custom_user_list_generator.get_custom_users(self.controller.custom_data)
        requested_datetime = datetime.strptime("2023-10-01-12:30", '%Y-%d-%m-%H:%M')
        nearest_online_time = self.controller.find_nearest_online_time(custom_users, requested_datetime)
        self.assertEqual(nearest_online_time, datetime(2023, 10, 1, 12, 0))

if __name__ == '__main__':
    unittest.main()
