import sys
import os
import subprocess
import shlex

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
BLANK_STRING = ""

def split_preserve_quotes(s):
    """Split string while preserving quoted content as single elements."""
    # return shlex.split(s) # Alternative using shlex
    result = []
    current = ""
    in_quotes = False
    backslash_escape = False
    backslash_escape_inside_double_quotes = False
    quote_type = BLANK_STRING

    for char in s:
        if backslash_escape:
            backslash_escape = False
            current += char
            continue

        if backslash_escape_inside_double_quotes:
            backslash_escape_inside_double_quotes = False
            if char in (DOUBLE_QUOTE, "\\"):
                current += char
            else:
                current += "\\" + char
            continue

        if char == "\\":
            if not in_quotes:
                backslash_escape = True
                continue
            elif in_quotes and quote_type == DOUBLE_QUOTE:
                backslash_escape_inside_double_quotes = True
                continue

            # if in_quotes and quote_type == DOUBLE_QUOTE:
            #     backslash_escape_inside_double_quotes = True
            #     continue
            # else:
            #     backslash_escape = True
            # continue

        if char in (SINGLE_QUOTE, DOUBLE_QUOTE):
            if not in_quotes:
                in_quotes = not in_quotes # Entering quotes: Assigning True
                quote_type = char
            elif quote_type == char:
                in_quotes = not in_quotes # Exiting quotes: Assigning False
                quote_type = BLANK_STRING
            else:
                current += char

        elif char == " " and not in_quotes:
            if current:
                result.append(current)
                current = ""
        else:
            current += char

    if current:
        result.append(current)

    return result

def read_cli():
    sys.stdout.write("$ ")
    prompt = input()
    return prompt

# def echo_command(args):
#     print(" ".join(args))

def list_builtins_commands():
    return ["echo", "exit", "type"]

def check_is_executable(command):
    paths = os.getenv("PATH", "").split(os.pathsep)

    for path in paths:
        fully_qualified_path = os.path.join(path, command)
        if os.path.isfile(fully_qualified_path) and os.access(fully_qualified_path, os.X_OK):
            return True, fully_qualified_path

    return False, None

def check_command_type(args):
    if not args:
        print("type: missing argument")
        return

    command = args[0]
    if command in list_builtins_commands():
        print(f"{command} is a shell builtin")
    else:
        is_executable, executable_path = check_is_executable(command)
        if is_executable:
            print(f"{command} is {executable_path}")
        else:
            print(f"{command} not found")

    return

def redirect_standard_output(command: str, args: list):
    if not any(arg in args for arg in (">", "1>")):
        return
    
    redirection_operator_index = args.index(">") if ">" in args else args.index("1>")

    if redirection_operator_index == len(args) - 1:
        # No file specified for redirection
        print("syntax error near unexpected token `newline'")
        return
    
    redirection_file_destination = args[redirection_operator_index + 1]
    args.pop(redirection_operator_index) # Remove the redirection operator
    # Remove the file destination
    # As after poping operator, the file destination shifts to the same index
    args.pop(redirection_operator_index)

    # write to the destination file
    with open(redirection_file_destination, "w") as f:
        subprocess.run([command] + args, stdout=f)

def execute_command(command, args):
    is_executable, executable_path = check_is_executable(command)
    if is_executable:
        if any(arg in args for arg in (">", "1>")):
            redirect_standard_output(command, args)

        else:
            subprocess.run([command] + args)
        # alternatively, we can use os.execv to replace the current process
        # os.execv(executable_path, [command] + args)
        return
    
    print(f"{command}: command not found")

def repl_cli():
    prompt = read_cli()

    parts = split_preserve_quotes(prompt)
    command, args = parts[0], parts[1:]
    match command:
        # case "echo": 
        # No need to explicitly handle echo here,
        # execute_command will take care of it
        #     echo_command(args)
        #     return
        case "exit":
            sys.exit()
        case "type":
            check_command_type(args)
            return
        case _:
            execute_command(command, args)
            return

def main():
    while True:
        repl_cli()

if __name__ == "__main__":
    main()