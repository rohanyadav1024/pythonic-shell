import sys
import os

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

def execute_command(prompt):
    is_executable, executable_path = check_is_executable(prompt)
    if is_executable:
        os.execv(executable_path, [prompt])

def repl_cli():
    prompt = read_cli()

    command, args = prompt.split()[0], prompt.split()[1:]
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
            execute_command(prompt)

    print(f"{prompt}: command not found")

def main():
    while True:
        repl_cli()

if __name__ == "__main__":
    main()