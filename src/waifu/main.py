"""Main entry point for the waifu assistant."""
from openai import OpenAI
from .config import Config
from .storage import StorageManager
from .ui import UIManager
from .enhanced import EnhancedWaifuAssistant
from datetime import datetime
import colorama
from colorama import Fore, Style
import os

# Initialize colorama
colorama.init()

def initialize_user_data(storage_manager: StorageManager) -> dict:
    """Initialize or load user data with default values."""
    user_data = storage_manager.load_user_data()
    if not user_data.get("waifu_name"):
        user_data["waifu_name"] = "Waifu"
    if not user_data.get("name"):
        user_data["name"] = "Senpai"
    if not user_data.get("location"):
        user_data["location"] = "Unknown"
    if not user_data.get("session_goals"):
        user_data["session_goals"] = "No goals set"
    storage_manager.save_user_data(user_data)
    return user_data

def user_never_used_waifu(storage_manager: StorageManager) -> bool:
    """Check if this is the user's first time using the waifu assistant."""
    # Check if the user_file exists instead of checking the data
    return not os.path.exists(storage_manager.user_file)

def welcome_message(waifu: EnhancedWaifuAssistant, storage_manager: StorageManager, ui_manager: UIManager) -> dict:
    """Original kawaii onboarding flow."""
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
        f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}First, what's your name? {Fore.GREEN}",
        "Senpai"
    )

    print(f"\n{Fore.CYAN}WAIFU:  {Fore.YELLOW}Nice to meet you, {user_data['name']}!✨{Style.RESET_ALL}")
    print(f"\n{Fore.MAGENTA}✨ New unlock: Your name is {user_data['name']} ✨{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

    # Waifu reacts to name
    ai_comment_name = waifu.waifu_ai_comment(f"Make a fun or playful remark about {user_data['name']}.")
    print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...*\n{Style.RESET_ALL}")
    print(f"WAIFU:  {ai_comment_name}\n")

    # Waifu name
    user_data["waifu_name"] = ui_manager.get_input(
        f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}What would you like to call me? {Fore.GREEN}",
        "Waifu"
    )
    print(f"\n{Fore.MAGENTA}✨ You named your waifu: {user_data['waifu_name']} ✨{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

    ai_comment_waifu_name = waifu.waifu_ai_comment(
        f"The user named you {user_data['waifu_name']}. Your reaction is up to you. "
        "Make a fun remark about it. Keep it brief!"
    )
    print(f"{user_data['waifu_name']}:  {ai_comment_waifu_name}\n")

    # Location
    user_data["location"] = ui_manager.get_input(
        f"{Fore.CYAN}{user_data['waifu_name']}:  {Fore.YELLOW}Where do ya live? {Fore.GREEN}",
        "Unknown"
    )
    print(f"\n{Fore.MAGENTA}✨ New unlock: You live in {user_data['location']} ✨{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

    ai_comment_location = waifu.waifu_ai_comment(
        f"The user lives in {user_data['location']}. Make a fun remark. End with a "
        "joke about living inside the terminal."
    )
    print(f"{user_data['waifu_name']}:  {ai_comment_location}\n")

    # Goals
    user_data["session_goals"] = ui_manager.get_input(
        f"{Fore.CYAN}{user_data['waifu_name']}:  {Fore.YELLOW}What do you want to accomplish today? {Fore.GREEN}",
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

    # After setting goals, introduce code review feature
    print(f"\n{Fore.MAGENTA}✨ Special Feature Introduction! ✨{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Oh! I should mention - I can help review your code too! 💻✨{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Just type these commands when you need me:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  !review [file_path]{Style.RESET_ALL} - I'll review a specific file")
    print(f"{Fore.GREEN}  !review-dir [directory_path]{Style.RESET_ALL} - I'll review all Python files in a directory")
    
    ai_comment_feature = waifu.waifu_ai_comment(
        "Make a cute, encouraging comment about helping with code review. Mention being thorough but gentle."
    )
    print(f"\n{user_data['waifu_name']}: {ai_comment_feature}")

    storage_manager.save_user_data(user_data)
    return user_data

def handle_chat_loop(user_data: dict, waifu: EnhancedWaifuAssistant, ui_manager: UIManager) -> None:
    """Main chat loop with original kawaii styling and code review commands."""
    print(f"\n{Fore.YELLOW}Available commands:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}!review [file_path]{Style.RESET_ALL} - Review a specific file")
    print(f"{Fore.GREEN}!review-dir [directory_path]{Style.RESET_ALL} - Review all Python files in a directory")
    print(f"{Fore.GREEN}exit{Style.RESET_ALL} - Exit the chat")
    
    while True:
        try:
            user_input = ui_manager.get_input(
                f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Type a command or message > {Style.RESET_ALL}"
            )
            
            if user_input.lower() in ['exit', 'quit']:
                print(f"{Fore.CYAN}Sayonara! (｡♥‿♥｡){Style.RESET_ALL}")
                break
            
            # Handle code review commands - now more flexible with input formatting
            if "!review" in user_input:
                if "!review-dir" in user_input:
                    dir_path = user_input.replace("!review-dir", "").strip("[] ").strip()
                    if dir_path:
                        waifu.review_directory(dir_path)
                    else:
                        print(f"{Fore.RED}Please provide a directory path! Example: !review-dir /path/to/directory{Style.RESET_ALL}")
                    continue
                else:
                    file_path = user_input.replace("!review", "").strip("[] ").strip()
                    if file_path:
                        waifu.review_file(file_path)
                    else:
                        print(f"{Fore.RED}Please provide a file path! Example: !review /path/to/file.py{Style.RESET_ALL}")
                    continue
                
            response = waifu.chat(user_input)
            print(f"\n{Fore.CYAN}{user_data['waifu_name']}: {response}{Style.RESET_ALL}\n")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Sayonara! (｡♥‿♥｡){Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}Gomen nasai! An error occurred: {str(e)} (╥﹏╥){Style.RESET_ALL}")

def handle_settings(user_data: dict, ui_manager: UIManager, storage_manager: StorageManager) -> dict:
    """Original settings handler with kawaii styling."""
    print(f"\n{Fore.MAGENTA}📝 Settings Menu:{Style.RESET_ALL}")
    print("1. Change your name")
    print("2. Change waifu's name")
    print("3. Change location")
    print("4. Back to chat")

    choice = ui_manager.get_input(f"{Fore.YELLOW}Choose an option (1-4): {Style.RESET_ALL}", "4")

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

def main():
    """Main entry point with complete kawaii onboarding and returning user flow."""
    config = Config()
    
    # Debug prints
    print("Debug: Checking OpenAI API Key...")
    print(f"API Key exists: {bool(config.get('openai_api_key'))}")
    print(f"API Key length: {len(config.get('openai_api_key')) if config.get('openai_api_key') else 0}")
    print(f"First few chars: {config.get('openai_api_key')[:5] if config.get('openai_api_key') else 'None'}")
    
    storage_manager = StorageManager()
    ui_manager = UIManager()
    
    # Initialize OpenAI client
    try:
        client = OpenAI(api_key=config.get("openai_api_key"))
        # Test the client
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}]
        )
        print("OpenAI client test successful!")
    except Exception as e:
        print(f"OpenAI client error: {str(e)}")
        raise

    waifu = EnhancedWaifuAssistant(client, storage_manager, ui_manager)
    
    if user_never_used_waifu(storage_manager):
        user_data = welcome_message(waifu, storage_manager, ui_manager)
    else:
        user_data = initialize_user_data(storage_manager)
        print(f"\n{Fore.MAGENTA}✨ Welcome Back ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        print(
            f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Hey there {user_data['name']}! 💖 "
            f"{user_data['waifu_name']} missed you~!\n{Style.RESET_ALL}"
        )

        # Add reminder about code review feature
        print(f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Remember, I can help review your code! Just use:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  !review [file_path]{Style.RESET_ALL} - For single file review")
        print(f"{Fore.GREEN}  !review-dir [directory_path]{Style.RESET_ALL} - For directory review\n")

        # Location greeting
        ai_comment_location_greeting = waifu.waifu_ai_comment(
            f"Make a timely remark about the user's location {user_data['location']}. Keep it brief!"
        )
        print(f"{user_data['waifu_name']}: {ai_comment_location_greeting}\n")

        # Mood check
        user_data["mood"] = ui_manager.get_input(
            f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}How are you feeling today? Mental health is important! {Fore.GREEN}",
            "I'm good!"
        )
        ai_comment_mood = waifu.waifu_ai_comment(
            f"The user is feeling {user_data['mood']}. If they seem sad, cheer them up, "
            "if happy, celebrate. Keep it brief!"
        )
        print(f"\n{user_data['waifu_name']}: {ai_comment_mood}\n")

        # Last session check
        print(f"{user_data['waifu_name']}: How was your last coding session?")
        print(f"{user_data['waifu_name']}: You planned to: {user_data['session_goals']}")
        user_data["session_goals"] = ui_manager.get_input(
            f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Did you get it done? {Fore.GREEN}",
            "No goals set"
        )
        ai_comment_session_goals = waifu.waifu_ai_comment(
            f"The user got {user_data['session_goals']} done. React accordingly."
        )
        print(f"\n{user_data['waifu_name']}: {ai_comment_session_goals}\n")

        # Suggest new goals
        ai_comment_new_goals = waifu.waifu_ai_comment(
            "Make a brief quip about setting new goals. Then joke about living in the terminal."
        )
        print(f"{user_data['waifu_name']}: {ai_comment_new_goals}\n")

        user_data["session_goals"] = ui_manager.get_input(
            f"{Fore.CYAN}{user_data['waifu_name']}: {Fore.YELLOW}Any new goals for this session? {Fore.GREEN}",
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
        print(f"\n{user_data['waifu_name']}: {ai_comment_new_goals2}")

        # Update mood and save data
        waifu.mood.update_mood({"time_since_break": 0, "code_quality": 0})
        storage_manager.save_user_data(user_data)
        
    handle_chat_loop(user_data, waifu, ui_manager)

if __name__ == "__main__":
    main()