import requests

endpoint = 'http://127.0.0.1:8000/api/'


get_response = requests.get(endpoint)
if get_response.status_code == 200:
    print(get_response.json())
else:
    raise Exception(f"Access not granted: {get_response.text}")