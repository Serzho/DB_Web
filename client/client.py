from requests.exceptions import ConnectionError

from commands_handler import *

# главный исполняемый файл клиента
print("Please, input server ip address: ")
input_ip = input()
print("Please, input server port: ")
input_port = input()

if input_port and input_ip:  # ввод пользовательского ip и port сервера
    commandHandler = CommandsHandler(input_ip=input_ip, input_port=input_port)
else:
    commandHandler = CommandsHandler()

server_connected = False

try:  # проверка доступности сервера
    server_connected = commandHandler.test_request()
except ConnectionError:
    print("Server is not connected!!!")

if server_connected:
    print("Waiting for command...")
    commandHandler.print_help()  # вывод сообщения с доступными командами
    while True:
        command_input = commandHandler.input_command()
        if command_input.get("command") in commandHandler.commands_dict.keys():  # проверка известна ли команда
            commandHandler.run_command(command_input)
        elif command_input.get("command") == "/exit":  # команда выхода
            commandHandler.log_out()
            print("Exiting the program...")
            break
        elif command_input.get("command") == "empty":  # пустой ввод пользователя
            print("Empty input!")
        else: # вывод сообщения при неизвестной команде
            print('Invalid command!!! Please write "/help" for a list of available commands')
