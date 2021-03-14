# Source code for Test 1 program. Success!
from functions import get_function_name, get_parameters_list, add_function, eval_function, get_function_definition


def start_command_ui():
    functions_dict = {}
    command_dict = {
        "add": add_function_ui,
        "list": list_function_ui,
        "eval": eval_function_ui
    }
    done = False
    while not done:
        command = input("command>")
        try:
            cmd_word, cmd_params = split_command(command)
            if cmd_word in command_dict:
                command_dict[cmd_word](functions_dict, cmd_params)
            elif cmd_word == "exit":
                done = True
            else:
                print("Bad Command")
        except ValueError as ve:
            print(str(ve))


def split_command(command):
    """
    Split command string into command word and parameters
    :return: (command_word, command_params)
    """
    command = command.strip()
    tokens = command.split(" ", 1)
    command_word = tokens[0].strip().lower()
    command_params = tokens[1].strip() if len(tokens) == 2 else ""

    return command_word, command_params


def add_function_ui(functions_dict, cmd_params):
    """add add(a,b)=a+b"""
    tokens = cmd_params.split("=")

    if len(tokens) != 2:
        raise ValueError("Invalid parameter count.")

    function_def = tokens[0]
    function_body = tokens[1]
    add_function(functions_dict, function_def, function_body)


def list_function_ui(functions_dict, cmd_params):
    """list add"""
    function_name = cmd_params.strip()
    function_def = get_function_definition(functions_dict, function_name)
    print(function_def)


def eval_function_ui(functions_dict, cmd_params):
    """ eval add(2,4) """
    tokens = cmd_params.split("(")
    function_name = tokens[0]  # function_name = add
    function_params = tokens[1]
    function_params = function_params[:-1]  # function_params = "2, 4"
    eval_code = eval_function(functions_dict, function_name, function_params)
    try:
        exec(eval_code)
    except SyntaxError:
        raise ValueError(f"The definition of {function_name} is incorrect. It can not run without errors.")


start_command_ui()
