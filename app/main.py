import sys
import os
import subprocess
import shlex
import readline

SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
BLANK_STRING = ""

REDIRECTION_OPERATORS = (">", "1>", "2>", ">>", "1>>", "2>>")
REDIRECTION_MODE_STDOUT = 'stdout'
REDIRECTION_MODE_STDERR = 'stderr'
REDIRECTION_MODE_STDOUT_APPEND = 'stdout_append'
REDIRECTION_MODE_STDERR_APPEND = 'stderr_append'

commands = []

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
    # sys.stdout.write("$ ")
    prompt = input("$ ")
    return prompt

def echo_command(args, return_output=False):
    if return_output:
        return " ".join(args)
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

def check_command_type(args, return_output=False):
    if not args:
        print("type: missing argument")
        return

    command = args[0]
    if command in list_builtins_commands():
        output = f"{command} is a shell builtin"
    else:
        is_executable, executable_path = check_is_executable(command)
        if is_executable:
            output = f"{command} is {executable_path}"
        else:
            output = f"{command} not found"

    if return_output:
        return output
    print(output)

def redirect_standard_output(command: str, args: list):
    redirection_mode = None
        
    redirection_operator_index = -1
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
        return

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
    if redirection_mode in (REDIRECTION_MODE_STDOUT_APPEND, REDIRECTION_MODE_STDERR_APPEND):
        write_mode = "a"
    else:
        write_mode = "w"

    with open(redirection_file_destination, mode=write_mode) as f:
        if redirection_mode in (REDIRECTION_MODE_STDERR, REDIRECTION_MODE_STDERR_APPEND):
            subprocess.run([command] + args, stderr=f)
        elif redirection_mode in (REDIRECTION_MODE_STDOUT, REDIRECTION_MODE_STDOUT_APPEND):
            subprocess.run([command] + args, stdout=f)

def execute_command(command, args):
    is_executable, executable_path = check_is_executable(command)
    if is_executable:
        if any(arg in args for arg in REDIRECTION_OPERATORS):
            redirect_standard_output(command, args)

        else:
            subprocess.run([command] + args)
        # alternatively, we can use os.execv to replace the current process
        # os.execv(executable_path, [command] + args)
        return
    
    print(f"{command}: command not found")

def text_completion(text, state):
    # ToDO: Implement effiecient fetching of commands with caching

    global commands
    matches = [cmd for cmd in commands if cmd.startswith(text)]

    if state < len(matches):
        match = matches[state]
        # Add trailing space ONLY if this is the sole match
        if len(matches) == 1:
            # print(f"RETURNING: '{match} ' (with space)")
            return match + " "
        else:
            # print(f"RETURNING: '{match}' (no space, multiple matches)")
            return match
    else:
        # print("RETURNING: None")
        return None

class PipelineParser:
    @staticmethod
    def parse(pipeline_str: str):
        for cmd in pipeline_str.split("|"):
            yield cmd.strip()

    @staticmethod
    def validate_commands(commands: list):
        for command in commands:
            parts = split_preserve_quotes(command)
            cmd_name = parts[0]

            if cmd_name in list_builtins_commands():
                continue

            is_executable, _ = check_is_executable(cmd_name)
            if not is_executable:
                print(f"{cmd_name}: command not found")
                return False
        return True

def execute_builtin_in_pipeline(command: str, args):
    match command:
        case "echo":
            return echo_command(args, return_output=True)
        case "type":
            return check_command_type(args, return_output=True)
        case _:
            return None

def execute_pipeline_commands(prompt: str):

    commands = list(PipelineParser.parse(prompt))
    if not PipelineParser.validate_commands(commands):
        return

    processes = []
    previous_process = None

    for i in range(len(commands)):
        parts_of_command = split_preserve_quotes(commands[i])

        # implement support for built-in commands in pipeline
        command, args = parts_of_command[0], parts_of_command[1:]

        if command in list_builtins_commands():
            builtin_output = execute_builtin_in_pipeline(command, args)
            if builtin_output is not None:
                executable_command = ["echo", builtin_output]
                # executable_command = ["echo", "-n", builtin_output]
            else:
                print(f"{command}: command not found")
                return

        else:
            is_executable, executable_path = check_is_executable(command)
            if not is_executable:
                print(f"{command}: command not found")
                return

            executable_command = [executable_path] + args

        if i == 0:
            # First command
            process = subprocess.Popen(executable_command, stdout=subprocess.PIPE)
        elif i == len(commands) - 1:
            # Last command
            process = subprocess.Popen(executable_command, stdin=previous_process.stdout, stdout=sys.stdout)
        else:
            # Intermediate command
            process = subprocess.Popen(executable_command, stdin=previous_process.stdout, stdout=subprocess.PIPE)

        # Close previous process's stdout in parent (important for EOF!)
        if previous_process:
            previous_process.stdout.close()

        processes.append(process)
        previous_process = process

    # Wait for all processes to complete
    for process in processes:
        process.wait()

def repl_cli():
    prompt = read_cli()

    # for pipeline commands
    if "|" in prompt:
        execute_pipeline_commands(prompt)
        return

    parts = split_preserve_quotes(prompt)
    command, args = parts[0], parts[1:]
    match command:
        # case "echo": 
        # No need to explicitly handle echo here,
        # execute_command will take care of it
            # echo_command(args)
            # return
        case "exit":
            sys.exit()
        case "type":
            check_command_type(args)
            return
        case _:
            execute_command(command, args)
            return

def initializer():
    global commands
    commands = []
    # commands = list_builtins_commands()

    # Add executables from PATH
    paths = os.getenv("PATH", "").split(os.pathsep)
    for path in paths:
        if os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) and os.access(item_path, os.X_OK):
                    commands.append(item)

    commands = list(set(commands + list_builtins_commands()))

def main():
    initializer()
    # print("Welcome to the Python Shell!")
    # print(commands)
    readline.set_completer(text_completion) # Set the custom completion function
    readline.parse_and_bind("tab: complete") # Enable tab completion

    while True:
        repl_cli()

if __name__ == "__main__":
    main()