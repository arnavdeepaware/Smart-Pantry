import requests
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_user_info(user_id):
    """Fetch user information from the API"""
    try:
        response = requests.get(f'http://127.0.0.1:5000/user/{user_id}')
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

        if response.status_code == 200:
            # Get the first user from the list
            user_json = response.json()[0] if response.json() else None
            
            if user_json:
                user_data = {
                    'first_name': user_json.get('first_name'),
                    'last_name': user_json.get('last_name'),
                    'email': user_json.get('email'),
                    'username': user_json.get('username'),
                    'current_height': user_json.get('current_height'),
                    'current_weight': user_json.get('current_weight'),
                    'target_weight': user_json.get('target_weight'),
                    'time_to_target': user_json.get('time_to_target'),
                    'auth_id': user_json.get('auth_id'),
                    'dietary_preference': user_json.get('dietary_preference'), 
                    'sex': user_json.get('sex'),
                    'age': user_json.get('age')         
                }
                return user_data
            return None
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return None

print(get_user_info('197824dc-2cd7-4431-8a64-918f9ab8a18e'))