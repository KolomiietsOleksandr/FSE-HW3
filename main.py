from datetime import datetime
from user_list_generator import CustomUserListGenerator
from data_fetcher import CustomDataFetcher
from translator import CustomTranslator

if __name__ == "__main__":
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

    for custom_user in custom_users:
        print(f"{custom_user.username} {custom_translator.translate(custom_user.last_seen, custom_lang)}")
