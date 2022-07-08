import requests
from time import sleep

print("Trying to connect...")
response = requests.get('http://127.0.0.1:9999/test')
print(response.text)



response = requests.post('http://127.0.0.1:9999/auth/', json={"name": "admin", "password": "1"})
if response.text == "":
    print("Incorrect name or password!")
else:
    print(f"Correct authentication! Token {response.text}")
token = response.text

input()

while True:
    response = requests.get("http://127.0.0.1:9999/test_token", json={"token": token})
    print(response.text)
    sleep(5)