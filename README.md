# Python Shell

A custom POSIX-compliant shell implementation built in Python. This shell supports interpreting commands, running external programs, and handling builtin commands like `cd`, `pwd`, `echo`, `type`, `history`, and more. It features efficient tab completion using a Trie data structure, command history, input/output redirection, and pipeline execution.

## Features

- **Command Execution**: Run external programs and builtin commands.
- **Builtin Commands**: `cd`, `pwd`, `echo`, `type`, `history`, `exit`.
- **Tab Completion**: Fast autocomplete for commands using a Trie (O(m) complexity).
- **Command History**: Save and load command history from a file.
- **Redirection**: Support for `>`, `>>`, `1>`, `2>`, etc.
- **Pipelines**: Execute commands in pipelines (e.g., `ls | grep py`).
- **Modular Design**: Clean separation of concerns with dedicated modules for commands, parsing, history, etc.

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/python-shell.git
   cd python-shell
   ```

2. (Optional) Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

Run the shell:
```sh
python -m app.main
```

### Example Commands
- `echo hello world`
- `pwd`
- `cd /path/to/dir`
- `ls | grep .py`
- `echo test > output.txt`
- `history` (show command history)
- `type ls` (check command type)

Use Tab for autocompletion of commands.

## Project Structure

- `app/main.py`: Main entry point and REPL loop.
- `app/commands.py`: Command discovery, execution, and builtins.
- `app/parser.py`: Input parsing and pipeline validation.
- `app/pipeline.py`: Pipeline execution.
- `app/history.py`: Command history management.
- `app/utils.py`: Utility functions (e.g., tab completion, navigation).
- `app/command_trie.py`: Trie implementation for efficient autocomplete.

## Contributing

This is a learning project. Feel free to open issues or submit pull requests for improvements!

## License

MIT License
