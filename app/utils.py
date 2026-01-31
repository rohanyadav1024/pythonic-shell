import os

def text_completion(text, state, commands_manager):
    # Use Trie for efficient autocomplete
    matches = commands_manager.get_autocomplete_suggestions(text)

    if state < len(matches):
        match = matches[state]
        # Add trailing space ONLY if this is the sole match
        if len(matches) == 1:
            return match + " "
        else:
            return match
    else:
        return None

def navigate_directory(target_directory):
    try:
        os.chdir(target_directory)
    except FileNotFoundError:
        print(f"cd: no such file or directory: {target_directory}")