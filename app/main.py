import sys

def read_cli():
    sys.stdout.write("$ ")
    prompt = input()
    return prompt

def echo_command(args):
    print(" ".join(args))

def repl_cli():
    prompt = read_cli()

    if prompt == "exit":
        sys.exit()

    command, args = prompt.split()[0], prompt.split()[1:]
    match command:
        case "echo":
            echo_command(args)
            return
        case _:
            pass

    print(f"{prompt}: command not found")

def main():
    while True:
        repl_cli()

if __name__ == "__main__":
    main()