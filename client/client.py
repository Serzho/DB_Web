from admin_commands import *

# главный исполняемый файл клиента


def exit_program():  # функция выхода из программы
    global is_running, token #TODO: убрать глобальные переменные
    is_running = False
    log_out(token)
    print("Exiting the program...")


commands_list = ["/help", "/test", "/auth", "/test_token", "/get_users", "/add_user", "/delete_user", "/log_out",
                 "/exit"]  # список доступных команд

token = ""
if bool(test_request()):  # проверка работы сервера
    is_running = True
    print("Waiting for command...")
    print_help()  # вывод сообщения с доступными командами
    while is_running:
        command_input = input().split()
        command_input.append("")
        command_input.append("")
        # разделение ввода на команду и параметры
        params = command_input[1:]
        command_input = command_input[0]
        # print(command_input, params)
        try: #TODO: в трай засовывать минимальные строки
            if command_input in commands_list: #TODO: переделать вызов команды в список словарей
                if command_input == "/help":  # вывод сообщения с доступными командами
                    print_help()
                elif command_input == "/test":  # проверка доступа к серверу
                    test_request()
                elif command_input == "/auth":  # запрос аутентификации
                    token = auth(*params[:2])
                elif command_input == "/test_token":  # проверка токена доступа
                    test_token(token)
                elif command_input == "/get_users":  # получение списка всех пользователей
                    get_users(token)
                elif command_input == "/add_user":  # запрос на добавление нового пользователя
                    add_user(token, *params[:3])
                elif command_input == "/delete_user":  # запрос на удаление пользователя
                    delete_user(token, int(params[0]))
                elif command_input == "/log_out":  # запрос на отключение токена доступа
                    log_out(token)
                elif command_input == "/exit":  # выход из программы
                    exit_program()

            else:
                print("\nWrong command! Please, print /help to get help!")
        except TypeError:
            print("Wrong type of parameter!!!")
