import requests


def print_help():
    text = "\nPrint '/help' to get help.\n/test - test connection to the server\n/auth [username] [password] - " \
           "authentication to the server\n/get_users - print dictionary with users from database\n/add_user [name] [" \
           "password] [is_admin] - adding new user to the database with users\n" \
           "/delete_user [id] - deleting user from " \
           "database with users\n/log_out - log out from the current user\n/exit - exit the program "
    print(text)


def test_request():
    print("Trying to connect...")
    response = requests.get('http://127.0.0.1:9999/test')
    if bool(response.text):
        print("Successful request to server!!!")
    else:
        print("Invalid request to server...")
    return response.text


def auth(name = None, password = None):
    if name == None:
        print("Please, input the name: ")
        name = input()
        print("Please, input the password: ")
        password = input()
    response = requests.post('http://127.0.0.1:9999/auth/', json={"name": name, "password": password})
    if response.text == "":
        print("Incorrect name or password!")
    else:
        print(f"Correct authentication! Token {response.text}")
    token = response.text
    return token

def test_token(token):
    response = requests.get("http://127.0.0.1:9999/test_token", json={"token": token})
    if bool(response):
        print("Correct access token!")
    else:
        print("Incorrect access token!")

def get_users(token):
    response = requests.get("http://127.0.0.1:9999/get_users", json={"token": token})
    if response.text != "null":
        print(response.text)
        return response.text
    else:
        print("Incorrect access token!")
        return None