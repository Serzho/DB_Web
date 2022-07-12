
from requests.exceptions import ConnectionError

from admin_commands import *

# главный исполняемый файл клиента

commands_dict = {
    "/help": print_help, "/test": test_request, "/auth": auth, "/test_token": test_token,
    "/get_users": get_users, "/add_user": add_user, "/delete_user": delete_user,
    "/log_out": log_out
}  # словарь доступных команд

token = ''
server_connected = False

try:
    server_connected = bool(test_request())
except ConnectionError:
    print("Server is not connected!!!")

if server_connected:  # проверка работы сервера
    is_running = True
    print("Waiting for command...")
    print_help()  # вывод сообщения с доступными командами
    while is_running:
        command_input = [*input().split(), '', '', token]
        # разделение ввода на команду и параметры
        params = command_input[1:]
        command_input = command_input[0]
        # print(command_input, params)
        if command_input in commands_dict.keys():
            function_return = commands_dict.get(command_input)(params)
            if function_return is not None:
                token = function_return
        elif command_input == "/exit":
            log_out(token)
            print("Exiting the program...")
            is_running = False
        else:
            print("Wrong command!!! To see available commands print /help.")
