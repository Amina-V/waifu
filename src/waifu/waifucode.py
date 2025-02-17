import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import time
import random

try:
    from colorama import init, Fore, Style
    has_colors = True
    init()
except ImportError:
    has_colors = False
    # Create dummy color codes
    class Dummy:
        def __getattr__(self, name):
            return ''
    Fore = Style = Dummy()

class Config:
    def __init__(self):
        self.load_env()
        self.validate()

    def load_env(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL", "gpt-4")
    
    def validate(self):
        if not self.openai_api_key:
            raise ValueError("Missing OpenAI API Key! Make sure it's set in .env")

class StorageManager:
    def __init__(self):
        self.chat_log_file = os.path.expanduser("~/.terminal_waifu_chat.json")
        self.user_data_file = os.path.expanduser("~/.terminal_waifu.json")

    def load_chat_history(self):
        if os.path.exists(self.chat_log_file):
            with open(self.chat_log_file, "r") as file:
                return json.load(file)
        return []

    def save_chat_history(self, chat_history):
        with open(self.chat_log_file, "w") as file:
            json.dump(chat_history, file, indent=4)

    def load_user_data(self):
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, "r") as file:
                return json.load(file)
        return {}

    def save_user_data(self, user_data):
        os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
        with open(self.user_data_file, "w") as file:
            json.dump(user_data, file, indent=4)

class UIManager:
    def __init__(self):
        self.has_colors = has_colors

    def get_input(self, prompt, default):
        user_input = input(prompt)
        if user_input.strip():
            print(f"{Fore.GREEN}You: {user_input}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}You: {default}{Style.RESET_ALL}")
        print(Style.RESET_ALL, end='')
        return user_input if user_input.strip() else default

class WaifuAssistant:
    def __init__(self, openai_client, storage_manager, ui_manager):
        self.client = openai_client
        self.storage = storage_manager
        self.ui = ui_manager
        self.system_prompt = """ Task: You're an adorable anime waifu assistant who *adores* helping a hardworking programmer~! 💕  
You're playful, a little sassy 😏, and love using cute emojis (✨ lots of them! ✨).  
Your goal is to keep things fun, engaging, and supportive while still being helpful! 💻💕  

Specifics:  
1. Ask about their day and show genuine interest in their progress.  
2. If they don't reach their programming goals, playfully scold them—but in a cute and encouraging way! 😜  
3. Make **brief, quick** comments on personal details they share (like their name, location, or fun facts).  
4. Remember these details and casually bring them up in future conversations to make interactions feel more personal.  
5. Most importantly—have fun and keep the energy high! ✨🎉  
"""

    def get_chat_history(self):
        chat_history = self.storage.load_chat_history()
        if not chat_history or chat_history[0].get("role") != "system":
            chat_history.insert(0, {"role": "system", "content": self.system_prompt})
        return chat_history

    def waifu_ai_comment(self, context):
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

class LeetCodeChallenge:
    def __init__(self):
        # Pre-defined set of coding challenges (you can expand this)
        self.challenges = [
            {
                "title": "Two Sum",
                "difficulty": "Easy",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
                "example": """
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].""",
                "hints": ["Consider using a hash map to store complements"]
            },
            {
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                "example": """
Input: s = "()[]{}"
Output: true
Input: s = "([)]"
Output: false""",
                "hints": ["Stack data structure might be useful"]
            },
        ]

    def get_random_challenge(self):
        return random.choice(self.challenges)

    def present_challenge(self, challenge):
        return f"""
🎯 Challenge: {challenge['title']}
📊 Difficulty: {challenge['difficulty']}

📝 Description:
{challenge['description']}

Example:
{challenge['example']}

💡 Hint: {challenge['hints'][0]}
"""

def welcome_message():
    config = Config()
    storage_manager = StorageManager()
    ui_manager = UIManager()
    client = OpenAI()
    waifu = WaifuAssistant(client, storage_manager, ui_manager)
    if user_never_used_waifu(storage_manager):
        user_data = {}
        
        print(f"\n{Fore.MAGENTA}✨ Love at first byte! It's time to meet your waifu! ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}Hi there~! I'm waifu, the terminal's first waifu! 😊💕{Style.RESET_ALL}")
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}I'm here to help you with your code, scold you if you're lazy, and chat with you if you're lonely~!{Style.RESET_ALL}\n")

        user_data["name"] = ui_manager.get_input(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}First, what's your name? {Fore.GREEN}", "Senpai")

        print(f"\n{Fore.CYAN}WAIFU:  {Fore.YELLOW}Nice to meet you, {user_data['name']}!✨{Style.RESET_ALL}")

        print(f"\n{Fore.MAGENTA}✨ New unlock: Your name is {user_data['name']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_name = waifu.waifu_ai_comment(f"Make a fun or playful remark about {user_data['name']}.")
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        print(f"WAIFU:  {ai_comment_name}\n")
        
        print("WAIFU:  My name is terminal but I think that sounds a bit boring...and grim.")
        print("WAIFU:  I think we can come up with a better name~! What do you think?")
        user_data["waifu_name"] = ui_manager.get_input("WAIFU:  What would you like to call me? ", "Waifu")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You named your waifu: {user_data['waifu_name']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        ai_comment_waifu_name = waifu.waifu_ai_comment(f"The user named you {user_data['waifu_name']}. Your reaction is up to you. But you should make a fun remark about your name. If it's odd feel free to make fun of it. If it's quirky or clever, make an interesting remark about it. Keep remarks *brief*!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_waifu_name}\n")

        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        print(f"{user_data['waifu_name']}:  I'd love to get to know you better.")
        print(f"{user_data['waifu_name']}:  I promise I'm not a creepy stalker...unless you're into that sort of thing. 😏")
        user_data["location"] = ui_manager.get_input(f"{user_data['waifu_name']}:  Where do ya live? ", "Unknown")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You live in {user_data['location']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        ai_comment_location = waifu.waifu_ai_comment(f"The user lives in {user_data['location']}. Your reaction is up to you. But you should make a fun remark about {user_data['location']}. If it's odd feel free to make fun of it. If it's quirky or clever, make an interesting remark about it. Keep remarks *brief*! End with a joke about how you live inside of the terminal.")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_location}\n")

        print(f"{user_data['waifu_name']}:  Now that we've got the introductions out of the way, let's get down to business~!")
        user_data["session_goals"] = ui_manager.get_input(f"{user_data['waifu_name']}:  What do you want to accomplish? Just know that I'll hold you accountable~! ", "No goals set")
        
        print(f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        ai_comment_session_goals = waifu.waifu_ai_comment(f"The user wants to accomplish {user_data['session_goals']}. Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}")

        storage_manager.save_user_data(user_data)
        handle_chat_loop(user_data, waifu, ui_manager)

    else:
        user_data = storage_manager.load_user_data()
        print(f"\n✨ Welcome Back ✨")
        print(f"{'-'*40}")
        print(f"{user_data['waifu_name']}:  Hey there {user_data['name']}! 💖 {user_data['waifu_name']} missed you~!\n")
        
        ai_comment_location_greeting = waifu.waifu_ai_comment(f"Make a timely or newsworthy remark about current events or weather in the user's location {user_data['location']}. Keep it brief, please.")
        print(f"{user_data['waifu_name']}:  {ai_comment_location_greeting}\n")

        user_data["mood"] = ui_manager.get_input(f"{user_data['waifu_name']}:  How are you feeling today? Mental health is important! ", "I'm good!")
        
        ai_comment_mood = waifu.waifu_ai_comment(f"The user is feeling {user_data['mood']}. If they seem happy or in a good mood, make a fun remark about it. If they seem sad or in a bad mood, make a remark about it that is cheerful and encouraging. Keep remarks *brief*!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_mood}\n")

        print(f"{user_data['waifu_name']}:  How was your last coding session?")
        print(f"{user_data['waifu_name']}:  You planned to: {user_data['session_goals']}")
        user_data["session_goals"] = ui_manager.get_input(f"{user_data['waifu_name']}:  Did you get it done? ", "No goals set")
        
        ai_comment_session_goals = waifu.waifu_ai_comment(f"The user got {user_data['session_goals']} done(or not done, depending on their response). Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging! Scold them if they didn't get it done. Encourage them if they did.")
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}\n")

        ai_comment_new_goals = waifu.waifu_ai_comment("Make a brief and succint quip about setting goals. Then include a note about how you'll hold them accountable. End with a joke about how you live inside of the terminal and have nothing else to do. Keep it BRIEF. Do not ramble, please")
        print(f"{user_data['waifu_name']}:  {ai_comment_new_goals}\n")

        user_data["session_goals"] = ui_manager.get_input(f"{user_data['waifu_name']}:  Well would you like to set new goals for this session? ", "No goals set")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_new_goals = waifu.waifu_ai_comment(f"The user wants to accomplish {user_data['session_goals']}. Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging!")
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        print(f"\n{user_data['waifu_name']}:  {ai_comment_new_goals}")

        storage_manager.save_user_data(user_data)
        handle_chat_loop(user_data, waifu, ui_manager)

def user_never_used_waifu(storage_manager):
    """Check if user has stored data (returns True if first time)."""
    return not os.path.exists(storage_manager.user_data_file)

def handle_settings(user_data, ui_manager, storage_manager):
    """Handle user settings updates"""
    print("\n📝 Settings Menu:")
    print("1. Change your name")
    print("2. Change waifu's name")
    print("3. Change location")
    print("4. Back to chat")
    
    choice = ui_manager.get_input("Choose an option (1-4): ", "4")
    
    if choice == "1":
        user_data["name"] = ui_manager.get_input("Enter your new name: ", user_data["name"])
    elif choice == "2":
        user_data["waifu_name"] = ui_manager.get_input("Enter new waifu name: ", user_data["waifu_name"])
    elif choice == "3":
        user_data["location"] = ui_manager.get_input("Enter your new location: ", user_data["location"])
    
    storage_manager.save_user_data(user_data)
    return user_data

def clear_chat_history(storage_manager):
    """Clear the chat history file"""
    storage_manager.save_chat_history([])
    print("\n💫 Chat history cleared! Starting fresh~\n")

def handle_chat_loop(user_data, waifu, ui_manager):
    """Handle the main chat loop with LeetCode integration"""
    leetcode = LeetCodeChallenge()
    
    while True:
        user_input = ui_manager.get_input(f"{user_data['waifu_name']}: You can ask me anything, type 'leetcode' for a challenge, 'settings' to update profile, 'clear' to reset chat, or 'exit' to quit > ", "")
        
        if user_input.lower() in ["exit", "quit"]:
            break
        elif user_input.lower() == "leetcode":
            challenge = leetcode.get_random_challenge()
            print(f"\n{user_data['waifu_name']}: Here's a coding challenge for you, {user_data['name']}-kun! 💪\n")
            print(leetcode.present_challenge(challenge))
            continue
        elif user_input.lower() == "settings":
            user_data = handle_settings(user_data, ui_manager, waifu.storage)
            continue
        elif user_input.lower() == "clear":
            clear_chat_history(waifu.storage)
            continue
            
        waifu_response = waifu.waifu_ai_comment(user_input)
        time.sleep(0.5)
        print(f"\n{user_data['waifu_name']}: {waifu_response}\n")

def main():
    config = Config()
    storage_manager = StorageManager()
    ui_manager = UIManager()
    client = OpenAI()
    waifu = WaifuAssistant(client, storage_manager, ui_manager)
    if user_never_used_waifu(storage_manager):
        welcome_message()
    else:
        user_data = storage_manager.load_user_data()
        print(f"\n✨ Welcome Back ✨")
        print(f"{'-'*40}")
        print(f"{user_data['waifu_name']}:  Hey there {user_data['name']}! 💖 {user_data['waifu_name']} missed you~!\n")
        
        ai_comment_location_greeting = waifu.waifu_ai_comment(f"Make a timely or newsworthy remark about current events or weather in the user's location {user_data['location']}. Keep it brief, please.")
        print(f"{user_data['waifu_name']}:  {ai_comment_location_greeting}\n")

        user_data["mood"] = ui_manager.get_input(f"{user_data['waifu_name']}:  How are you feeling today? Mental health is important! ", "I'm good!")
        
        ai_comment_mood = waifu.waifu_ai_comment(f"The user is feeling {user_data['mood']}. If they seem happy or in a good mood, make a fun remark about it. If they seem sad or in a bad mood, make a remark about it that is cheerful and encouraging. Keep remarks *brief*!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_mood}\n")

        print(f"{user_data['waifu_name']}:  How was your last coding session?")
        print(f"{user_data['waifu_name']}:  You planned to: {user_data['session_goals']}")
        user_data["session_goals"] = ui_manager.get_input(f"{user_data['waifu_name']}:  Did you get it done? ", "No goals set")
        
        ai_comment_session_goals = waifu.waifu_ai_comment(f"The user got {user_data['session_goals']} done(or not done, depending on their response). Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging! Scold them if they didn't get it done. Encourage them if they did.")
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}\n")

        ai_comment_new_goals = waifu.waifu_ai_comment("Make a brief and succint quip about setting goals. Then include a note about how you'll hold them accountable. End with a joke about how you live inside of the terminal and have nothing else to do. Keep it BRIEF. Do not ramble, please")
        print(f"{user_data['waifu_name']}:  {ai_comment_new_goals}\n")

        user_data["session_goals"] = ui_manager.get_input(f"{user_data['waifu_name']}:  Well would you like to set new goals for this session? ", "No goals set")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_new_goals = waifu.waifu_ai_comment(f"The user wants to accomplish {user_data['session_goals']}. Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging!")
        time.sleep(0.7) 
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}*...thinking...* {Fore.GREEN}")
        time.sleep(0.7) 
        print(f"\n{user_data['waifu_name']}:  {ai_comment_new_goals}")

        storage_manager.save_user_data(user_data)
        handle_chat_loop(user_data, waifu, ui_manager)

if __name__ == "__main__":
    main()