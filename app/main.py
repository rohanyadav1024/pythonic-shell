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

def lookup_executable(command):
    paths = os.getenv("PATH", "").split(os.pathsep)

    is_executable = False
    for path in paths:
        fully_qualified_path = os.path.join(path, command)
        if os.path.isfile(fully_qualified_path) and os.access(fully_qualified_path, os.X_OK):
            print(f"{command} is {fully_qualified_path}")
            is_executable = True
            break

    if not is_executable:
        print(f"{command} not found")

def check_command_type(args):
    if not args:
        print("type: missing argument")
        return

    command = args[0]
    if command in list_builtins_commands():
        print(f"{command} is a shell builtin")
    else:
        lookup_executable(command)
    return

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
            pass

    print(f"{prompt}: command not found")

def main():
    while True:
        repl_cli()

if __name__ == "__main__":
    main()