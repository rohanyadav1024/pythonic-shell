import sys

def read_cli():
    sys.stdout.write("$ ")
    prompt = input()
    return prompt

def echo_command(args):
    print(" ".join(args))

def list_builtins_commands():
    return ["echo", "exit", "type"]

def check_builtin_type(args):
    if not args:
        print("type: missing argument")
        return

    command = args[0]
    if command in list_builtins_commands():
        print(f"{command} is a shell builtin")
    else:
        print(f"{command} not found")
    return

def repl_cli():
    prompt = read_cli()

    if prompt == "exit":
        sys.exit()

    command, args = prompt.split()[0], prompt.split()[1:]
    match command:
        case "echo":
            echo_command(args)
            return
        case "type":
            check_builtin_type(args)
            return
        case _:
            pass

    print(f"{prompt}: command not found")

def main():
    while True:
        repl_cli()

if __name__ == "__main__":
    main()