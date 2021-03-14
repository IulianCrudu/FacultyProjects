def get_function_name(function_def: str):
    parts = function_def.split("(")
    return parts[0]


def get_parameters_list(function_params: str):
    params = function_params.split(",")
    paramaters = []
    for param in params:
        paramaters.append(int(param.strip()))
    return paramaters


def get_function(functions_dict, function_name):
    try:
        return functions_dict[function_name]
    except KeyError:
        raise ValueError(f"Function {function_name} not defined.")


def get_function_params(function):
    return function["params"]


def get_function_declaration(function):
    return function["declaration"]


def add_function(functions_dict, function_def: str, function_body: str):
    """
    Adds a new function to the function dictionary.
    :param functions_dict: The dictionary that holds all the functions
    :param function_def: The definition of a function. For example add(a,b)
    :param function_body: The body of a function. For example: a+b
    :return: None
    """
    # function parts will be ["add", "a,b)"]
    function_parts = function_def.split("(")
    function_name = function_parts[0]
    # We need to delete the "0"
    function_params = function_parts[1][:-1]  # "a,b,c"
    function_declaration = (
        f"""
def {function_def}:
    return {function_body}
        """
    )
    functions_dict[function_name] = {"declaration": function_declaration, "params": function_params}


def eval_function(functions_dict, function_name, function_params):
    function = get_function(functions_dict, function_name)
    func_declaration = get_function_declaration(function)
    python_code = ""
    python_code += func_declaration
    python_code += f"\nprint({function_name}({function_params}))"
    python_code = """
        def add(a,b):
            return a+b
            
        print(add(1,2))
    """
    return python_code


def get_function_definition(functions_dict, function_name):
    function = get_function(functions_dict, function_name)
    return get_function_declaration(function)
