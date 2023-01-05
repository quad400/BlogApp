import requests
from getpass import getpass

endpoint = 'http://127.0.0.1:8000/auth/login/'


username = input("What is your username?\n")
password = getpass("What is your password?\n")

r = requests.post(endpoint, json={'username': username, 'password': password}) 
print(r.json())
auth_token = r.json()['data']['token']

headers = {
    "Authorization": f"Bearer {auth_token}"
}
get_response = requests.get(endpoint, headers=headers)
if r.status_code == 200:
    print('access granted')
    print(get_response.json())
else:
    raise Exception(f"Access not granted: {r.text}")