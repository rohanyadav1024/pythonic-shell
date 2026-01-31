import sys
import os
import subprocess
import shlex
import readline

from .history import History
from .commands import CommandsManager
from .parser import split_preserve_quotes, PipelineParser
from .utils import text_completion, navigate_directory
from .pipeline import execute_pipeline_commands

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
BLANK_STRING = ""

REDIRECTION_OPERATORS = (">", "1>", "2>", ">>", "1>>", "2>>")
REDIRECTION_MODE_STDOUT = 'stdout'
REDIRECTION_MODE_STDERR = 'stderr'
REDIRECTION_MODE_STDOUT_APPEND = 'stdout_append'
REDIRECTION_MODE_STDERR_APPEND = 'stderr_append'

DEFAULT_HISTFILE_PATH = "default_history_file.txt"

def read_cli():
    # sys.stdout.write("$ ")
    prompt = input("$ ")
    return prompt

def manage_history_command(args):
    file_mode = None
    limit = None
    if args:
        if args[0] == "-r":
            # read history from file
            if args[1] is None:
                print("history: missing file operand")
                return

            file_path = args[1]
            history.load_history_from_file(file_path)
            return
        elif args[0] == "-w":
            # write history to the file
            if args[1] is None:
                print("history: missing file operand")
                return

            file_path = args[1]
            history.write_history_to_file(file_path)
            return
        elif args[0] == "-a":
            # write history to the file
            if args[1] is None:
                print("history: missing file operand")
                return

            file_path = args[1]
            history.append_command_to_file(file_path)
            return
        elif args[0].isdigit():
            limit = int(args[0])

    # Default: show entire history if none other
    history.show_history(limit)

def repl_cli():
    prompt = read_cli()

    # for pipeline commands
    if "|" in prompt:
        execute_pipeline_commands(prompt, commands_manager)
        return

    parts = split_preserve_quotes(prompt)
    command, args = parts[0], parts[1:]

    history.add_to_history(prompt)
    match command:
        # case "echo": 
        # No need to explicitly handle echo here,
        # execute_command will take care of it
            # echo_command(args)
            # return
        case "exit":
            exit_shell()
        case "type":
            commands_manager.check_command_type(args)
            return
        case "history":
            manage_history_command(args)
            return
        case "pwd":
            print(os.getcwd())
            return
        case "cd":
            if not args or args[0] == "~":
                target_directory = os.path.expanduser("~")
            else:
                target_directory = args[0]
            navigate_directory(target_directory)
            return
        case _:
            commands_manager.execute_command(command, args)
            return

def initializer():
    global commands_manager, history, HISTFILE_PATH
    commands_manager = CommandsManager()

    history = History()
    HISTFILE_PATH = os.environ.get("HISTFILE", DEFAULT_HISTFILE_PATH)
    history.load_history_from_file(HISTFILE_PATH)

def exit_shell():
    history.append_command_to_file(HISTFILE_PATH)
    sys.exit(0)

def main():
    initializer()
    # print("Welcome to the Python Shell!")
    # print(commands)
    readline.set_completer(lambda text, state: text_completion(text, state, commands_manager)) # Set the custom completion function
    readline.parse_and_bind("tab: complete") # Enable tab completion

    while True:
        repl_cli()

if __name__ == "__main__":
    main()