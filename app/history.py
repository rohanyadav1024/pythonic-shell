# class History:
#     # TODO: Implement custom UP and DOWN arrow navigation through history
#     def __init__(self):
#         self.history_file_commands = []
#         self.current_session_commands = []
#         self.history_command_index = -1
#         self.distinct_commands = set()

#     def add_to_history(self, command):
#         if command.strip() == "":
#             return

#         if command in self.distinct_commands:
#             return

#         self.distinct_commands.add(command)
#         self.current_session_commands.append(command)

#     def show_history(self, limit):
#         if limit is None or limit > len(self.current_session_commands):
#             limit = len(self.current_session_commands)

#         start_index = len(self.current_session_commands) + 1 - limit
#         history_commands = self.current_session_commands[-limit:]

#         # Display with 1-based indexing
#         for idx, cmd in enumerate(history_commands):
#             print(f"{idx + start_index}  {cmd}")

#     def get_command_from_history(self, index):
#         pass

#     def load_history_from_file(self, file_path):
#         # read history from file and populate self.current_session_commands and self.distinct_commands
#         try:
#             # self.clear_history()
#             with open(file_path, 'r') as f:
#                 for line in f:
#                     command = line.strip()
#                     if command and command not in self.distinct_commands:
#                         self.current_session_commands.append(command)
#                         self.distinct_commands.add(command)
#         except FileNotFoundError:
#             pass

#     def write_history_to_file(self, file_path):
#         # write self.current_session_commands to file
#         try:
#             with open(file_path, 'w') as f:
#                 for command in self.current_session_commands:
#                     f.write(command + '\n')
#         except FileExistsError:
#             pass

#     def append_command_to_file(self, file_path):
#         # append current commands to history file
#         try:
#             with open(file_path, 'a') as f:
#                 for command in self.current_session_commands:
#                     f.write(command + '\n')
#         except FileExistsError:
#             pass

#     def clear_history(self):
#         self.history_file_commands = []
#         self.current_session_commands = []
#         self.history_command_index = -1
#         self.distinct_commands = set()

# class History:
#     def __init__(self):
#         self.history_file_commands = []      # From file (old)
#         self.current_session_commands = []   # This session (new)
#         self.history_command_index = -1
#         # self.distinct_commands = set()

#     def add_to_history(self, command):
#         """Add command to current session history"""
#         if command.strip() == "":
#             return

#         # if command in self.distinct_commands:
#         #     return

#         # self.distinct_commands.add(command)
#         self.current_session_commands.append(command)

#     def show_history(self, limit=None):
#         """Show all history (file + current session)"""
#         # Combine both lists
#         all_commands = self.history_file_commands + self.current_session_commands
        
#         if limit is None or limit > len(all_commands):
#             limit = len(all_commands)

#         # Get last 'limit' commands
#         display_commands = all_commands[-limit:]
#         # Calculate starting index
#         start_index = len(all_commands) - len(display_commands) + 1

#         # Display with 1-based indexing
#         for idx, cmd in enumerate(display_commands):
#             print(f"{start_index + idx}  {cmd}")

#     def load_history_from_file(self, file_path):
#         """Load history from file (old commands)"""
#         try:
#             self.history_file_commands.clear()
#             with open(file_path, 'r') as f:
#                 for line in f:
#                     command = line.strip()
#                     if command:
#                         self.history_file_commands.append(command)
#                         # self.distinct_commands.add(command)
#         except FileNotFoundError:
#             pass

#     def append_command_to_file(self, file_path):
#         """Append ONLY NEW commands (current session) to file"""
#         try:
#             with open(file_path, 'a') as f:
#                 # Only append new commands from this session
#                 for command in self.current_session_commands:
#                     f.write(command + '\n')
#             self.current_session_commands.clear()
#         except Exception as e:
#             pass

#     def write_history_to_file(self, file_path):
#         """Overwrite file with ALL history (file + session)"""
#         try:
#             with open(file_path, 'w') as f:
#                 all_commands = self.history_file_commands + self.current_session_commands
#                 for command in all_commands:
#                     f.write(command + '\n')
#             self.current_session_commands.clear()
#         except Exception as e:
#             pass

#     def clear_session(self):
#         self.current_session_commands = []

HISTORY_SOURCE_SESSION = 'Session'
HISTORY_SOURCE_FILE = 'File'

class HistoryEntry:
    def __init__(self, command: str, source: str = HISTORY_SOURCE_SESSION, appended: bool = False):
        self.command = command
        self.source = source
        self.appended = appended

class History:
    def __init__(self):
        self.session_history = []
        self.history_index = []

    def add_to_history(self, command: str, source: str=HISTORY_SOURCE_SESSION):
        """Add command to current session history"""
        if command.strip() == "":
            return

        self.session_history.append(HistoryEntry(command, source))

    def show_history(self, limit=None):
        """Show all history (file + current session)"""
        all_commands = self.session_history

        if limit is None or limit > len(all_commands):
            limit = len(all_commands)

        # Get last 'limit' commands
        display_commands = all_commands[-limit:]
        # Calculate starting index
        start_index = len(all_commands) - len(display_commands) + 1

        # Display with 1-based indexing
        for idx, entry in enumerate(display_commands):
            print(f"{start_index + idx}  {entry.command}")

    def load_history_from_file(self, file_path):
        """Load history from file (old commands)"""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    command = line.strip()
                    if command:
                        self.session_history.append(HistoryEntry(command, HISTORY_SOURCE_FILE))
        except FileNotFoundError:
            pass

    def append_command_to_file(self, file_path):
        """Append ONLY NEW commands (current session) to file"""
        try:
            with open(file_path, 'a') as f:
                # Only append new commands from this session
                for entry in self.session_history:
                    if entry.source == HISTORY_SOURCE_SESSION and not entry.appended:
                        f.write(entry.command + '\n')
                        entry.appended = True
        except Exception as e:
            pass


    def write_history_to_file(self, file_path):
        """Overwrite file with ALL history (file + session)"""
        try:
            with open(file_path, 'w') as f:
                for entry in self.session_history:
                    f.write(entry.command + '\n')
                    entry.appended = True
        except Exception as e:
            pass


    def clear_session(self):
        self.session_history = []