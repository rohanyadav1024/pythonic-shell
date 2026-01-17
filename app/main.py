import sys

def repl_cli():
    sys.stdout.write("$ ")
    prompt = input()

    if prompt == "exit":
        sys.exit()

    print(f"{prompt}: command not found")

def main():
    while True:
        repl_cli()

if __name__ == "__main__":
    main()