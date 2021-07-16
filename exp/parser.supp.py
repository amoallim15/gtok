# tuple => _AND_(): pass
# list  => _OR_(): pass
# set   => _IF_(): pass
# None  =>

# def _AND_(): pass # sequence operator
# def _OR_(): pass # alternative operator
def _IF_():
    pass  # predicate operator


def _LOOP_():
    pass  # repition operator


def _PASS_():
    pass  # skip operator


def _TOKEN_():
    pass  # custom operator


class GrammarRules:
    #
    path = "PATH_TYPE"
    identifier = "IDENTIFIER"
    arg_value = ["BOOLEAN_TYPE", "NUMBER_TYPE", "STRING_TYPE"]
    arg_key_eq = "ARG_KEY_EQ"
    arg_key_flag = "ARG_KEY_FLAG"
    #
    version_flag = ["-v", "--version"]
    help_flag = ["-h", "--help"]
    list_flag = ["-l", "--list"]
    #
    kwarg_type_2 = (arg_key_eq, "=", arg_value)
    kwarg_type_1 = [(arg_key_flag, arg_value), arg_key_flag]
    kwarg = [kwarg_type_1, kwarg_type_2]
    func_type_1 = (identifier, ["-a", "--args"], _LOOP_, arg_value)
    func_type_2 = (identifier, arg_value)
    func_type_3 = (identifier, _LOOP_, kwarg)
    func_type_4 = identifier
    function = [func_type_1, func_type_2, func_type_3, func_type_4]
    functions = [function, _LOOP_, function]
    paths = [_LOOP_, path, True]
    app_flags = [version_flag, help_flag, list_flag, True]
    describe_command = ("desc", path)
    execute_command = (paths, functions)
    #
    commands = [describe_command, execute_command]
    start = ("SOF", "supp", app_flags, [commands, "EOF"])
    execute_command = (paths, functions)


print(GrammarRules.start)
print()
print(vars(GrammarRules))

class C:
    pass

print(vars(C))