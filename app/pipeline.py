import subprocess
import sys
import os

from .parser import split_preserve_quotes, PipelineParser

def execute_builtin_in_pipeline(command: str, args, commands_manager):
    match command:
        case "echo":
            return commands_manager.echo_command(args, return_output=True)
        case "type":
            return commands_manager.check_command_type(args, return_output=True)
        case _:
            return None

def execute_pipeline_commands(prompt: str, commands_manager):
    commands = list(PipelineParser.parse(prompt))
    if not PipelineParser.validate_commands(commands, commands_manager):
        return

    processes = []
    previous_process = None

    for i in range(len(commands)):
        parts_of_command = split_preserve_quotes(commands[i])

        # implement support for built-in commands in pipeline
        command, args = parts_of_command[0], parts_of_command[1:]

        if command in commands_manager.list_builtins_commands():
            builtin_output = execute_builtin_in_pipeline(command, args, commands_manager)
            if builtin_output is not None:
                executable_command = ["echo", builtin_output]
                # executable_command = ["echo", "-n", builtin_output]
            else:
                print(f"{command}: command not found")
                return

        else:
            is_executable, executable_path = commands_manager.check_is_executable(command)
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