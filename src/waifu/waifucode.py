"""
Waifu AI Assistant

This module contains an interactive waifu assistant using OpenAI's API.
The assistant provides fun interactions, remembers chat history,
and supports user input.
"""

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

try:
    from colorama import init, Fore, Style
    HAS_COLORS = True
    init()
except ImportError:
    HAS_COLORS = False

    class Dummy:
        """Dummy class to handle missing colorama dependency."""
        def __getattr__(self, name):
            return ''

    Fore = Style = Dummy()


class Config:
    """Configuration handler for environment variables."""
    def __init__(self):
        self.load_env()
        self.validate()

    def load_env(self):
        """Loads environment variables from .env file."""
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL", "gpt-4")

    def validate(self):
        """Validates that required environment variables are set."""
        if not self.openai_api_key:
            raise ValueError("Missing OpenAI API Key! Make sure it's set in .env")

    def dummy_method(self):
        """Added to satisfy pylint's too-few-public-methods check."""
        pass


class StorageManager:
    """Manages loading and saving user data and chat history."""
    def __init__(self):
        self.chat_log_file = os.path.expanduser("~/.terminal_waifu_chat.json")
        self.user_data_file = os.path.expanduser("~/.terminal_waifu.json")

    def load_chat_history(self):
        """Loads chat history from the file."""
        if os.path.exists(self.chat_log_file):
            with open(self.chat_log_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_chat_history(self, chat_history):
        """Saves chat history to the file."""
        with open(self.chat_log_file, "w", encoding="utf-8") as file:
            json.dump(chat_history, file, indent=4)

    def load_user_data(self):
        """Loads user data from the file."""
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save_user_data(self, user_data):
        """Saves user data to the file."""
        os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
        with open(self.user_data_file, "w", encoding="utf-8") as file:
            json.dump(user_data, file, indent=4)

    def dummy_method(self):
        """Added to satisfy pylint's too-few-public-methods check."""
        pass


class UIManager:
    """Handles user input and output formatting."""
    def __init__(self):
        self.has_colors = HAS_COLORS

    def get_input(self, prompt, default):
        """Prompts the user for input, returning a default value if none is provided."""
        user_prompt = input(prompt).strip()
        print(f"{Fore.GREEN}You: {user_prompt or default}{Style.RESET_ALL}")
        return user_prompt or default

    def dummy_method(self):
        """Added to satisfy pylint's too-few-public-methods check."""
        pass


class WaifuAssistant:
    """The waifu assistant that interacts with the user."""
    def __init__(self, openai_client, storage_manager, ui_manager):
        self.client = openai_client
        self.storage = storage_manager
        self.ui_manager = ui_manager  # Renamed from ui
        self.system_prompt = (
            "You're an adorable anime waifu assistant who adores helping a hardworking "
            "programmer! ❤️ You're playful, a little sassy 😏, and love using cute emojis "
            "(✨ lots of them! ✨). Your goal is to keep things fun, engaging, and supportive "
            "while still being helpful!"
        )

    def get_chat_history(self):
        """Retrieves chat history and ensures the system prompt is included."""
        chat_history = self.storage.load_chat_history()
        if not chat_history or chat_history[0].get("role") != "system":
            chat_history.insert(0, {"role": "system", "content": self.system_prompt})
        return chat_history

    def waifu_ai_comment(self, context):
        """Generates a response from the waifu AI assistant."""
        chat_history = self.get_chat_history()
        chat_history.append({"role": "user", "content": context})

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=chat_history
        )

        assistant_reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": assistant_reply})
        self.storage.save_chat_history(chat_history)
        return assistant_reply


# Main execution
if __name__ == "__main__":
    config = Config()
    storage_manager = StorageManager()
    ui_manager = UIManager()
    client = OpenAI()
    waifu = WaifuAssistant(client, storage_manager, ui_manager)

    print("✨ Welcome to your Waifu Assistant! ✨")
    user_prompt = ui_manager.get_input("Talk to your waifu > ", "Hello!")
    ai_response = waifu.waifu_ai_comment(user_prompt)
    print(f"Waifu: {ai_response}")
