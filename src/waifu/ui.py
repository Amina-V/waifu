"""User interface management for the waifu assistant."""
import os
import readline
from typing import Optional
from colorama import Fore, Style

class UIManager:
    """Manages user interface interactions."""
    def __init__(self):
        self.setup_readline()

    def setup_readline(self) -> None:
        """Sets up readline with history."""
        histfile = os.path.expanduser("~/.waifu_history")
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
        readline.set_history_length(1000)
        readline.parse_and_bind('tab: complete')

    def get_input(self, prompt: str, default: str = "") -> str:
        """Gets input from the user with history support and default value."""
        try:
            user_input = input(prompt).strip()
            if user_input:
                print(f"{Fore.GREEN}You: {user_input}{Style.RESET_ALL}")
                return user_input
            if default:
                print(f"{Fore.GREEN}You: {default}{Style.RESET_ALL}")
                return default
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "exit"

    def clear_screen(self) -> None:
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_message(self, message: str, message_type: str = "info") -> None:
        """Displays a message with kawaii styling."""
        if message_type == "error":
            print(f"{Fore.RED}{message} (╥﹏╥){Style.RESET_ALL}")
        elif message_type == "success":
            print(f"{Fore.GREEN}{message} ✨{Style.RESET_ALL}")
        else:
            print(message) 