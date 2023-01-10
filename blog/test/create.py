import requests
import re
from getpass import getpass


login = 'http://127.0.0.1:8000/auth/login/'
endpoint = 'http://127.0.0.1:8000/api/create/'


username = input("What is your username?\n")
password = getpass("What is your password?\n")

data = {
    "title":"You no sabi me ni",
    "desc": "hellow i can do as i like",
    "content": "what do you want to do here",
    "category": "programming"
}

# def token_converter(data):
    

#     return val

r = requests.post(login, json={'username': username, 'password': password}) 
if r.status_code == 200:
    print('access granted')
    auth_token = r.json()['data']['token']
    print(auth_token)
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    get_response = requests.post(endpoint,json=data, headers=headers)

    print(get_response.json())
else:
    raise Exception(f"Access not granted: {r.text}")



