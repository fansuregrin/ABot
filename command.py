from config import commands


def register_cmd(command_name, command_func):
            commands[command_name] = command_func
            print(f'[{command_name}] is loaded.')