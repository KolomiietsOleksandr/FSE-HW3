import requests
import json

class CustomDataFetcher:
    def get_custom_data_from_url(self, base_url, desired_custom_user_count, max_offset):
        custom_all_data = []
        for offset in range(max_offset):
            if len(custom_all_data) >= desired_custom_user_count:
                break
            url = f"{base_url}?offset={offset}"
            response = requests.get(url)
            if response.status_code == 200:
                json_content = response.text
                try:
                    container = json.loads(json_content)
                    custom_user_data = container["data"]
                    remaining_custom_users = desired_custom_user_count - len(custom_all_data)
                    custom_users_to_add = min(len(custom_user_data), remaining_custom_users)
                    custom_all_data.extend(custom_user_data[:custom_users_to_add])
                    print(custom_all_data)
                except json.JSONDecodeError as ex:
                    print(f"Failed to parse JSON: {ex}")
            else:
                print(f"Failed to fetch data for offset {offset}")
        return custom_all_data
