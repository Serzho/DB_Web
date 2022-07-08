from admin_commands import *

def exit():
    global is_running
    is_running = False
    print("Exiting the program...")

commands_list = ["/help", "/test", "/auth", "/test_token", "/get_users", "/add_user", "/delete_user", "/log_out", "/exit"]

token = ""
if bool(test_request()):
    is_running = True
    print("Waiting for command...")
    print_help()
    while is_running:
        command_input = input().split()
        command_input.append("")
        command_input.append("")
        params = command_input[1:]
        command_input = command_input[0]
        #print(command_input, params)
        if command_input in commands_list:
            if command_input == "/help":
                print_help()
            elif command_input == "/test":
                test_request()
            elif command_input == "/auth":
                token = auth(*params[:2])
            elif command_input == "/test_token":
                test_token(token)
            elif command_input == "/get_users":
                get_users(token)
            elif command_input == "/add_user":
                pass
            elif command_input == "/delete_user":
                pass
            elif command_input == "/log_out":
                pass
            elif command_input == "/exit":
                exit()

        else:
            print("\nWrong command! Please, print /help to get help!")
