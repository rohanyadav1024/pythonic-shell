import sys
import os
import subprocess
import shlex

def split_preserve_quotes(s):
    """Split string while preserving quoted content as single elements."""
    # return shlex.split(s) # Alternative using shlex
    result = []
    current = ""
    in_quotes = False

    for char in s:
        if char == "'":
           in_quotes = not in_quotes
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

def echo_command(args):
    print(" ".join(args))

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

def execute_command(command, args):
    is_executable, executable_path = check_is_executable(command)
    if is_executable:
        subprocess.run([command] + args)
        # os.execv(executable_path, [command] + args)
        return
    
    print(f"{command}: command not found")

def repl_cli():
    prompt = read_cli()

    parts = split_preserve_quotes(prompt)
    command, args = parts[0], parts[1:]
    match command:
        case "echo":
            echo_command(args)
            return
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