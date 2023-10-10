from datetime import datetime
from user_list_generator import CustomUserListGenerator
from data_fetcher import CustomDataFetcher
from translator import CustomTranslator
from online_count import UserStatsController
from UserStatsUserController import UserStatsHistoryController
from users_online_predictor import UserOnlinePredictor

def main():
    custom_base_url = "https://sef.podkolzin.consulting/api/users/lastSeen"

    while True:
        try:
            desired_custom_count = int(input("Enter the number of users you want to use: "))
            max_offset = int(input("Enter max number of offset you want to use: "))

            if desired_custom_count > 0:
                break
            else:
                print("The desired number of users must be greater than zero.")
        except ValueError:
            print("Enter the correct number.")

    custom_data_fetcher = CustomDataFetcher()
    custom_data = custom_data_fetcher.get_custom_data_from_url(custom_base_url, desired_custom_count, max_offset)

    custom_user_list_generator = CustomUserListGenerator()
    custom_users = custom_user_list_generator.get_custom_users(custom_data)
    current_time = datetime.utcnow()

    print("Choose language (en, uk, ja, fi): ")
    custom_lang = input()

    custom_translator = CustomTranslator()
    custom_user_list_generator.custom_when_online(custom_users, current_time)

    history_controller = UserStatsHistoryController(custom_data)  # Передаем custom_data

    while True:
        print("Enter '1' to check users online stats, '2' to get user history, '3' to list all users, '4' to predict online of users or 'q' to quit: ")
        command = input()

        if command == '1':
            date = input("Enter the date (YYYY-MM-DD): ")
            controller = UserStatsController()
            result = controller.get_users_online_stats(date)
            print(f"Users Online on {date}: {result.UsersOnline}")
        elif command == '2':
            user_id = input("Enter the user ID: ")
            date = input("Enter the date (YYYY-MM-DD-HH:MM): ")
            history_result, status_code = history_controller.get_user_history(user_id, date)
            if status_code == 404:
                print("User not found.")
            else:
                print(f"wasUserOnline: {history_result['wasUserOnline']}, nearestOnlineTime: {history_result['nearestOnlineTime']}")
        elif command == '3':
            print("List of all users:")
            for user in custom_users:
                translated_last_seen = custom_translator.translate(user.last_seen, custom_lang)
                print(f"Username: {user.username}, Last Seen: {translated_last_seen}, Is Online: {user.is_online}")
        elif command == '4':
            user_online_predictor = UserOnlinePredictor(custom_users)
            date = input("Enter the date (YYYY-MM-DD-HH:MM) to predict online users: ")
            prediction_result = user_online_predictor.predict_users_online(date)
            print(f"Predicted online users at {date}: {prediction_result['onlineUsers']}")
        elif command == 'q':
            break
        else:
            print("Invalid command. Please enter '1', '2', '3', '4' or 'q'.")

if __name__ == "__main__":
    main()
