import os
import subprocess
import sys

from .command_trie import Trie

class CommandsManager:
    def __init__(self):
        self.commands = []
        self.trie = Trie()
        self._load_commands()

    def _load_commands(self):
        """Load all executable commands from PATH and builtins."""
        paths = os.getenv("PATH", "").split(os.pathsep)
        for path in paths:
            if os.path.isdir(path):
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isfile(item_path) and os.access(item_path, os.X_OK):
                        self.commands.append(item)
        self.commands = list(set(self.commands + self.list_builtins_commands()))
        for cmd in self.commands:
            self.trie.insert(cmd)

    def list_builtins_commands(self):
        return ["echo", "exit", "type", "history", "cd", "pwd"]

    def get_commands(self):
        """Return the list of commands for autocomplete."""
        return self.commands

    def get_autocomplete_suggestions(self, prefix):
        """Return autocomplete suggestions using the Trie."""
        return self.trie.autocomplete(prefix)

    def check_is_executable(self, command):
        paths = os.getenv("PATH", "").split(os.pathsep)
        for path in paths:
            fully_qualified_path = os.path.join(path, command)
            if os.path.isfile(fully_qualified_path) and os.access(fully_qualified_path, os.X_OK):
                return True, fully_qualified_path
        return False, None

    def check_command_type(self, args, return_output=False):
        if not args:
            if return_output:
                return "type: missing argument"
            print("type: missing argument")
            return

        command = args[0]
        if command in self.list_builtins_commands():
            if return_output:
                return f"{command} is a shell builtin"
            print(f"{command} is a shell builtin")
        else:
            is_executable, executable_path = self.check_is_executable(command)
            if is_executable:
                if return_output:
                    return f"{command} is {executable_path}"
                print(f"{command} is {executable_path}")
            else:
                if return_output:
                    return f"{command}: not found"
                print(f"{command}: not found")

    def echo_command(self, args, return_output=False):
        if return_output:
            return " ".join(args)
        print(" ".join(args))

    def execute_command(self, command, args):
        is_executable, executable_path = self.check_is_executable(command)
        if is_executable:
            if any(arg in args for arg in [">", "1>", "2>", ">>", "1>>", "2>>"]):
                self.redirect_standard_output(command, args)
            else:
                subprocess.run([command] + args)
            return
        
        print(f"{command}: command not found")

    def redirect_standard_output(self, command: str, args: list):
        REDIRECTION_OPERATORS = (">", "1>", "2>", ">>", "1>>", "2>>")
        REDIRECTION_MODE_STDOUT = 'stdout'
        REDIRECTION_MODE_STDERR = 'stderr'
        REDIRECTION_MODE_STDOUT_APPEND = 'stdout_append'
        REDIRECTION_MODE_STDERR_APPEND = 'stderr_append'

        redirection_operator_index = None
        redirection_mode = None

        if ">" in args:
            redirection_operator_index = args.index(">")
            redirection_mode = REDIRECTION_MODE_STDOUT
        elif "1>" in args:
            redirection_operator_index = args.index("1>")
            redirection_mode = REDIRECTION_MODE_STDOUT
        elif "2>" in args:
            redirection_operator_index = args.index("2>")
            redirection_mode = REDIRECTION_MODE_STDERR
        elif ">>" in args:
            redirection_operator_index = args.index(">>")
            redirection_mode = REDIRECTION_MODE_STDOUT_APPEND
        elif "1>>" in args:
            redirection_operator_index = args.index("1>>")
            redirection_mode = REDIRECTION_MODE_STDOUT_APPEND
        elif "2>>" in args:
            redirection_operator_index = args.index("2>>")
            redirection_mode = REDIRECTION_MODE_STDERR_APPEND
        else:
            # No redirection, just execute
            is_executable, executable_path = self.check_is_executable(command)
            if is_executable:
                subprocess.run([command] + args)
            return

        if redirection_operator_index == len(args) - 1:
            print("syntax error near unexpected token `newline'")
            return
        
        redirection_file_destination = args[redirection_operator_index + 1]
        args.pop(redirection_operator_index)  # Remove the redirection operator
        # Remove the file destination
        # As after popping operator, the file destination shifts to the same index
        args.pop(redirection_operator_index)

        # write to the destination file
        if redirection_mode in (REDIRECTION_MODE_STDOUT_APPEND, REDIRECTION_MODE_STDERR_APPEND):
            write_mode = "a"
        else:
            write_mode = "w"

        with open(redirection_file_destination, mode=write_mode) as f:
            if redirection_mode in (REDIRECTION_MODE_STDERR, REDIRECTION_MODE_STDERR_APPEND):
                result = subprocess.run([command] + args, stderr=f)
            elif redirection_mode in (REDIRECTION_MODE_STDOUT, REDIRECTION_MODE_STDOUT_APPEND):
                result = subprocess.run([command] + args, stdout=f)