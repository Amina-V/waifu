"""
Waifu AI Assistant

This module contains an interactive waifu assistant using OpenAI's API.
The assistant provides fun interactions, remembers chat history,
runs an onboarding flow for new users, and supports a '20 Questions' game.
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
        """
        Prompts the user for input, returning a default value if none is provided.
        """
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
        self.ui_manager = ui_manager
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

    def play_20_questions(self):
        """
        Starts a 20 Questions game using GPT's reasoning.
        The user thinks of an object, GPT tries to guess it
        within 20 questions or fewer. Answers are Yes/No/Maybe.
        """
        print("\nLet's play 20 Questions!")
        print("Think of an object in your mind, and I'll try to guess it in 20 questions or fewer.")
        print("Answer only with Yes, No, or Maybe.\n")

        question_count = 0
        # A specialized conversation context for the 20Q game:
        game_history = [
            {
                "role": "system",
                "content": (
                    "You're playing 20 Questions. You can only ask Yes/No/Maybe questions "
                    "to guess an object the user is thinking of. After each user response, "
                    "you may guess if confident. Keep track of the question count. "
                    "Don't exceed 20 total questions. Good luck!"
                )
            }
        ]

        while question_count < 20:
            # Ask GPT for the next question:
            question_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=game_history
            )
            next_question = question_response.choices[0].message.content.strip()
            question_count += 1

            print(f"Question {question_count}: {next_question}")
            user_answer = self.ui_manager.get_input("> ", "Maybe")

            # Add the Q&A to the game conversation
            game_history.append({"role": "assistant", "content": next_question})
            game_history.append({"role": "user", "content": user_answer})

            # GPT might guess:
            guess_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=game_history
            )
            guess_text = guess_response.choices[0].message.content.strip()

            # If GPT guesses, check confirmation
            if "i guess it's" in guess_text.lower() or "my guess is" in guess_text.lower():
                print(f"\nGPT guesses: {guess_text}")
                correct = self.ui_manager.get_input("Is that correct? (yes/no) ", "no")
                if correct.lower() in ["yes", "y"]:
                    print("\nYay! I guessed it!\n")
                    return
                print("\nOh no! Let me keep trying...\n")

            game_history.append({"role": "assistant", "content": guess_text})

        # If we exit the loop, GPT didn't guess in time:
        print("\nI've used 20 questions. I give up! You win. 🎉\n")


def user_never_used_waifu(storage_manager):
    """
    Check if user has stored data (returns True if first time).
    """
    return not os.path.exists(storage_manager.user_data_file)


def handle_settings(user_data, ui_manager, storage_manager):
    """
    Handle user settings updates. Lets user rename or
    adjust basic info, then saves changes.
    """
    print("\n📝 Settings Menu:")
    print("1. Change your name")
    print("2. Change waifu's name")
    print("3. Change location")
    print("4. Back to chat")

    choice = ui_manager.get_input("Choose an option (1-4): ", "4")

    if choice == "1":
        user_data["name"] = ui_manager.get_input("Enter your new name: ", user_data["name"])
    elif choice == "2":
        user_data["waifu_name"] = ui_manager.get_input(
            "Enter new waifu name: ", user_data["waifu_name"]
        )
    elif choice == "3":
        user_data["location"] = ui_manager.get_input(
            "Enter your new location: ", user_data["location"]
        )

    storage_manager.save_user_data(user_data)
    return user_data


def clear_chat_history(storage_manager):
    """Clear the chat history file."""
    storage_manager.save_chat_history([])
    print("\n💫 Chat history cleared! Starting fresh~\n")


def handle_chat_loop(user_data, waifu, ui_manager):
    """
    Handle the main chat loop. The user can chat freely,
    go to settings, clear chat, start 20 questions, or exit.
    """
    while True:
        user_input = ui_manager.get_input(
            f"{user_data['waifu_name']}: You can talk, '20q' for a game, 'settings' to update, "
            "'clear' to reset chat, or 'exit' to quit > ",
            ""
        )

        if user_input.lower() in ["exit", "quit"]:
            break
        if user_input.lower() == "20q":
            waifu.play_20_questions()
            continue
        if user_input.lower() == "settings":
            user_data = handle_settings(user_data, ui_manager, waifu.storage)
            continue
        if user_input.lower() == "clear":
            clear_chat_history(waifu.storage)
            continue

        waifu_response = waifu.waifu_ai_comment(user_input)
        print(f"\n{user_data['waifu_name']}: {waifu_response}\n")


def welcome_message():
    """
    Handles the onboarding flow for first-time users.
    Asks them personal info, uses waifu to comment
    and store details, etc.
    """
    config = Config()
    storage_manager = StorageManager()
    ui_manager = UIManager()
    client = OpenAI()
    waifu = WaifuAssistant(client, storage_manager, ui_manager)

    if user_never_used_waifu(storage_manager):
        user_data = {}

        print(f"\n{Fore.MAGENTA}✨ Love at first byte! It's time to meet your waifu! ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}Hi there~! I'm your terminal waifu! 😊💕{Style.RESET_ALL}")
        print(
            f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}I'm here to help you with your code, "
            "scold you if you're lazy, and chat with you if you're lonely~!"
            f"{Style.RESET_ALL}\n"
        )

        user_data["name"] = ui_manager.get_input(
            f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}First, what's your name? {Fore.GREEN}", "Senpai"
        )

        print(f"\n{Fore.CYAN}WAIFU:  {Fore.YELLOW}Nice to meet you, {user_data['name']}!✨{Style.RESET_ALL}")
        print(f"\n{Fore.MAGENTA}✨ New unlock: Your name is {user_data['name']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        # Waifu reacts to name:
        ai_comment_name = waifu.waifu_ai_comment(
            f"Make a fun or playful remark about {user_data['name']}."
        )
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...*\n{Style.RESET_ALL}")
        print(f"WAIFU:  {ai_comment_name}\n")

        # Waifu name:
        user_data["waifu_name"] = ui_manager.get_input(
            "WAIFU:  What would you like to call me? ",
            "Waifu"
        )
        print(f"\n{Fore.MAGENTA}✨ You named your waifu: {user_data['waifu_name']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        ai_comment_waifu_name = waifu.waifu_ai_comment(
            f"The user named you {user_data['waifu_name']}. Your reaction is up to you. "
            "Make a fun remark about it. Keep it brief!"
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_waifu_name}\n")

        # Ask location:
        user_data["location"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  Where do ya live? ",
            "Unknown"
        )

        print(f"\n{Fore.MAGENTA}✨ New unlock: You live in {user_data['location']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        ai_comment_location = waifu.waifu_ai_comment(
            f"The user lives in {user_data['location']}. Make a fun remark. End with a "
            "joke about living inside the terminal."
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_location}\n")

        # Session goals:
        user_data["session_goals"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  What do you want to accomplish today? ",
            "No goals set"
        )
        print(
            f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today "
            f"✨{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        ai_comment_session_goals = waifu.waifu_ai_comment(
            f"The user wants to accomplish {user_data['session_goals']}. Make a fun remark, "
            "friendly and encouraging."
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_session_goals}")

        storage_manager.save_user_data(user_data)
        handle_chat_loop(user_data, waifu, ui_manager)
    else:
        # Already a returning user
        user_data = storage_manager.load_user_data()
        print(f"\n✨ Welcome Back ✨")
        print(f"{'-'*40}")
        print(
            f"{user_data['waifu_name']}:  Hey there {user_data['name']}! 💖 "
            f"{user_data['waifu_name']} missed you~!\n"
        )

        ai_comment_location_greeting = waifu.waifu_ai_comment(
            f"Make a timely remark about the user's location {user_data['location']}. Keep it brief!"
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_location_greeting}\n")

        # Mood
        user_data["mood"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  How are you feeling today? ",
            "I'm good!"
        )
        ai_comment_mood = waifu.waifu_ai_comment(
            f"The user is feeling {user_data['mood']}. Respond briefly, encouraging if sad, "
            "fun if happy."
        )
        print(f"\n{user_data['waifu_name']}:  {ai_comment_mood}\n")

        # Check last session
        print(f"{user_data['waifu_name']}:  How was your last coding session?")
        print(f"{user_data['waifu_name']}:  You planned to: {user_data['session_goals']}")
        user_data["session_goals"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  Did you get it done? ",
            "No goals set"
        )
        ai_comment_session_goals = waifu.waifu_ai_comment(
            f"The user got {user_data['session_goals']} done. Scold if not done, "
            "encourage if done, keep it fun!"
        )
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}\n")

        # Prompt for new goals
        ai_comment_new_goals = waifu.waifu_ai_comment(
            "Make a brief quip about setting new goals. End with a joke about living in the terminal."
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_new_goals}\n")

        user_data["session_goals"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  Would you like to set new goals for this session? ",
            "No goals set"
        )
        print(
            f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today "
            f"✨{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        ai_comment_new_goals2 = waifu.waifu_ai_comment(
            f"The user wants to accomplish {user_data['session_goals']} now. Give a fun remark!"
        )
        print(f"\n{user_data['waifu_name']}:  {ai_comment_new_goals2}")

        # Save updated data, go to chat loop
        storage_manager.save_user_data(user_data)
        handle_chat_loop(user_data, waifu, ui_manager)


def main():
    """
    Main function checks whether it's the user's first time or not.
    If first time, runs welcome_message, else calls handle_chat_loop directly.
    """
    config = Config()  # Keep an instance if needed
    storage_manager = StorageManager()
    ui_manager = UIManager()
    client = OpenAI()
    waifu = WaifuAssistant(client, storage_manager, ui_manager)

    if user_never_used_waifu(storage_manager):
        welcome_message()
    else:
        # Returning user flow
        user_data = storage_manager.load_user_data()
        print(f"\n✨ Welcome Back ✨")
        print(f"{'-'*40}")
        print(
            f"{user_data['waifu_name']}:  Hey there {user_data['name']}! "
            f"{user_data['waifu_name']} missed you~!\n"
        )

        # Greet re: location
        ai_comment_location_greeting = waifu.waifu_ai_comment(
            f"Make a timely remark about the user's location {user_data['location']}. Keep it brief!"
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_location_greeting}\n")

        # Mood
        user_data["mood"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  How are you feeling today? Mental health is important! ",
            "I'm good!"
        )
        ai_comment_mood = waifu.waifu_ai_comment(
            f"The user is feeling {user_data['mood']}. If they seem sad, cheer them up, "
            "if happy, celebrate. Keep it brief!"
        )
        print(f"\n{user_data['waifu_name']}:  {ai_comment_mood}\n")

        # Last session check
        print(f"{user_data['waifu_name']}:  How was your last coding session?")
        print(f"{user_data['waifu_name']}:  You planned to: {user_data['session_goals']}")
        user_data["session_goals"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  Did you get it done? ",
            "No goals set"
        )
        ai_comment_session_goals = waifu.waifu_ai_comment(
            f"The user got {user_data['session_goals']} done. React accordingly."
        )
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}\n")

        # Suggest new goals
        ai_comment_new_goals = waifu.waifu_ai_comment(
            "Make a brief quip about setting new goals. Then joke about living in the terminal."
        )
        print(f"{user_data['waifu_name']}:  {ai_comment_new_goals}\n")

        user_data["session_goals"] = ui_manager.get_input(
            f"{user_data['waifu_name']}:  Any new goals for this session? ",
            "No goals set"
        )
        print(
            f"\n{Fore.MAGENTA}✨ You want to accomplish {user_data['session_goals']} today ✨"
            f"{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        ai_comment_new_goals2 = waifu.waifu_ai_comment(
            f"The user wants to accomplish {user_data['session_goals']} now. React accordingly!"
        )
        print(f"\n{user_data['waifu_name']}:  {ai_comment_new_goals2}")

        storage_manager.save_user_data(user_data)
        handle_chat_loop(user_data, waifu, ui_manager)


if __name__ == "__main__":
    main()
