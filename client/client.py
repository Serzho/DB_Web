
from requests.exceptions import ConnectionError

from commands_handler import *

# главный исполняемый файл клиента
#TODO:отформатировать файлы

commandHandler = CommandHandler()

server_connected = False

try:
    server_connected = bool(commandHandler.test_request())
except ConnectionError:
    print("Server is not connected!!!")

if server_connected:  # проверка работы сервера
    is_running = True
    print("Waiting for command...")
    commandHandler.print_help()  # вывод сообщения с доступными командами
    while True:
        command_input = commandHandler.input_command()
        if command_input.get("command") in commandHandler.commands_dict.keys():
            commandHandler.run_command(command_input)
        elif command_input.get("command") == "/exit":
            commandHandler.log_out()
            print("Exiting the program...")
            break
        else:
            print('Invalid command!!! Please write "/help" for a list of available commands')
