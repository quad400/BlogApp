import requests
from getpass import getpass

endpoint = 'http://127.0.0.1:8000/auth/signup/'




username = input("What is your username?\n")
email = input("What is your email?\n")
password = getpass("What is your password?\n")
r = requests.post(endpoint, json={'username': username, 'email':email, 
                'password': password}) 


if r.status_code == 201:
    print('User created')
    print(r.text)
else:
    raise Exception(f"Invalid request: {r.text}")