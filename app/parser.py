SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
BLANK_STRING = ""

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

class PipelineParser:
    @staticmethod
    def parse(pipeline_str: str):
        for cmd in pipeline_str.split("|"):
            yield cmd.strip()

    @staticmethod
    def validate_commands(commands: list, commands_manager):
        for command in commands:
            parts = split_preserve_quotes(command)
            cmd_name = parts[0]

            if cmd_name in commands_manager.list_builtins_commands():
                continue

            is_executable, _ = commands_manager.check_is_executable(cmd_name)
            if not is_executable:
                print(f"{cmd_name}: command not found")
                return False
        return True