import requests
from getpass import getpass


login = 'http://127.0.0.1:8000/auth/login/'
endpoint = 'http://127.0.0.1:8000/api/burgers/comment/'

data = {
    "comment":"I dont like ya"
}

username = input("What is your username?\n")
password = getpass("What is your password?\n")

r = requests.post(login, json={'username': username, 'password': password}) 
if r.status_code == 200:
    print('access granted')
    auth_token = r.json()['data']['token']
    print(auth_token)
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    
    get_response = requests.post(endpoint,json=data ,headers=headers)

    print(get_response.json())
else:
    raise Exception(f"Access not granted: {r.text}")
