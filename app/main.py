import sys

def handle_cli():
    sys.stdout.write("$ ")
    prompt = input()
    print(f"{prompt}: command not found")

def main():
    while True:
        handle_cli()

if __name__ == "__main__":
    main()