class History:
    # TODO: Implement custom UP and DOWN arrow navigation through history
    def __init__(self):
        self.history_file_commands = []
        self.current_session_commands = []
        self.history_command_index = -1
        self.distinct_commands = set()

    def add_to_history(self, command):
        if command.strip() == "":
            return

        if command in self.distinct_commands:
            return

        self.distinct_commands.add(command)
        self.current_session_commands.append(command)

    def show_history(self, limit):
        if limit is None or limit > len(self.current_session_commands):
            limit = len(self.current_session_commands)

        start_index = len(self.current_session_commands) + 1 - limit
        history_commands = self.current_session_commands[-limit:]

        # Display with 1-based indexing
        for idx, cmd in enumerate(history_commands):
            print(f"{idx + start_index}  {cmd}")

    def get_command_from_history(self, index):
        pass

    def load_history_from_file(self, file_path):
        # read history from file and populate self.current_session_commands and self.distinct_commands
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    command = line.strip()
                    if command and command not in self.distinct_commands:
                        self.current_session_commands.append(command)
                        self.distinct_commands.add(command)
        except FileNotFoundError:
            pass

    def write_history_to_file(self, file_path):
        # write self.current_session_commands to file
        try:
            with open(file_path, 'w') as f:
                for command in self.current_session_commands:
                    f.write(command + '\n')
        except FileExistsError:
            pass

    def append_command_to_file(self, file_path):
        # append current commands to history file
        try:
            with open(file_path, 'a') as f:
                for command in self.current_session_commands:
                    f.write(command + '\n')
        except FileExistsError:
            pass
        