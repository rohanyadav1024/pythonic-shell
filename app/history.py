class History:
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