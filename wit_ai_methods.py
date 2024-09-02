import requests


def get_message(user_message: str, token: str):
    response = requests.get(
        f'https://api.wit.ai/message?q={user_message}',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()
