import requests
from getpass import getpass

endpoint = 'http://127.0.0.1:8000/api/auth/signup/'




# username = input("Username: ")
# email = input("Email: ")
# password = getpass("Password: ")
# confirm_password = getpass("Retype Password: ")
r = requests.post(endpoint, json={'username': "quad", 'email': "quad@gmail.com", 
                'password': "adediji09"}) 


if r.status_code == 201:
    print('User created')
    print(r.text)
else:
    raise Exception(f"Invalid request: {r.text}")