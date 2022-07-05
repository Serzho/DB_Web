import requests


print("Trying to connect...")
request = requests.get('http://127.0.0.1:8000/')
print(request)
