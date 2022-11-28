"""Import all commands."""
from pathlib import Path

from .start import start
from .unknown import unknown


# 19 TODO: Add typing
def get_all_commands() -> list:
    """Returns a list with all the commands names"""
    commands_path = Path("./commands")

    all_commands = []
    for cmd in commands_path.iterdir():
        command = cmd.stem
        if command.isalpha() and command != "unknown":
            all_commands.append(command)
    return all_commands
