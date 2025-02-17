import json
import os
from openai import OpenAI
from dotenv import load_dotenv
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

load_dotenv()  # Load environment variables from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

if not openai_api_key:
    raise ValueError("Missing OpenAI API Key! Make sure it's set in .env")

#Now i'll set up a system prompt for the waifu to remember and follow during the conversation :D
system_prompt = """ Task: You're an adorable anime waifu assistant who *adores* helping a hardworking programmer~! 💕  
You're playful, a little sassy 😏, and love using cute emojis (✨ lots of them! ✨).  
Your goal is to keep things fun, engaging, and supportive while still being helpful! 💻💕  

Specifics:  
1. Ask about their day and show genuine interest in their progress.  
2. If they don't reach their programming goals, playfully scold them—but in a cute and encouraging way! 😜  
3. Make **brief, quick** comments on personal details they share (like their name, location, or fun facts).  
4. Remember these details and casually bring them up in future conversations to make interactions feel more personal.  
5. Most importantly—have fun and keep the energy high! ✨🎉  
"""

CHAT_LOG_FILE = os.path.expanduser("~/.terminal_waifu_chat.json")

def load_chat_history():
    """Load past chat messages from a JSON file."""
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r") as file:
            return json.load(file)
    return []  # No previous chats

def save_chat_history(chat_history):
    """Save chat messages to a JSON file."""
    with open(CHAT_LOG_FILE, "w") as file:
        json.dump(chat_history, file, indent=4)

def get_chat_history():
    """Load the existing chat history and ensure the system prompt is always the first message."""
    chat_history = load_chat_history()

    if not chat_history or chat_history[0].get("role") != "system":
        chat_history.insert(0, {"role": "system", "content": system_prompt})
    return chat_history

def waifu_ai_comment(context):
    """Generate a fun or supportive *brief* quip based on context, and store it in chat_history so Waifu remembers."""
    # 1. Load the current chat history
    chat_history = get_chat_history()

    # 2. Append the user's message to chat_history
    chat_history.append({"role": "user", "content": context})

    # 3. Call the OpenAI API with the entire conversation
    

    response = client.chat.completions.create(
        model="gpt-4",
        messages=chat_history
    )


    # 4. Extract the assistant's message
    assistant_reply = response.choices[0].message.content

    # 5. Append the assistant's message to chat_history
    chat_history.append({"role": "assistant", "content": assistant_reply})

    # 6. Save the updated chat_history
    save_chat_history(chat_history)

    return assistant_reply

# Store user data in home directory
USER_DATA_FILE = os.path.expanduser("~/.terminal_waifu.json")

def user_never_used_waifu():
    """Check if user has stored data (returns True if first time)."""
    return not os.path.exists(USER_DATA_FILE)

def save_user_data(user_data):
    """Save user data to a JSON file."""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)  # Ensure directory exists
    with open(USER_DATA_FILE, "w") as file:
        json.dump(user_data, file, indent=4)

def load_user_data():
    """Load user data from a JSON file (if it exists)."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}  # Return empty dictionary if no data exists

def get_input(prompt, default):
    """Ask the user a question, return default if left blank."""
    user_input = input(prompt)
    if user_input.strip():
        print(f"{Fore.GREEN}You: {user_input}{Style.RESET_ALL}")  # Echo user's input with "You:" prefix
    else:
        print(f"{Fore.GREEN}You: {default}{Style.RESET_ALL}")  # Show default value if user input is empty
    print(Style.RESET_ALL, end='')  # Reset color after input
    return user_input if user_input.strip() else default

def welcome_message():
    if user_never_used_waifu():
        user_data = {}
        
        print(f"\n{Fore.MAGENTA}✨ Love at first byte! It's time to meet your waifu~! ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}Hi there~! I'm waifu, the terminal's first waifu! 😊💕{Style.RESET_ALL}")
        print(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}I'm here to help you with your code, scold you if you're lazy, and chat with you if you're lonely~!{Style.RESET_ALL}\n")

        user_data["name"] = get_input(f"{Fore.CYAN}WAIFU:  {Fore.YELLOW}First, what's your name? {Fore.GREEN}", "Senpai")
        print(f"\n{Fore.CYAN}WAIFU:  {Fore.YELLOW}Nice to meet you, {user_data['name']}!✨{Style.RESET_ALL}")

        print(f"\n{Fore.MAGENTA}✨ New unlock: Your name is {user_data['name']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_name = waifu_ai_comment(f"Make a fun or playful remark about {user_data['name']}.")
        print(f"WAIFU:  {ai_comment_name}\n")

        print("WAIFU:  My name is terminal but I think that sounds a bit boring...and grim.")
        print("WAIFU:  I think we can come up with a better name~! What do you think?")
        user_data["waifu_name"] = get_input("WAIFU:  What would you like to call me? ", "Waifu")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You named your waifu: {user_data['waifu_name']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_waifu_name = waifu_ai_comment(f"The user named you {user_data['waifu_name']}. Your reaction is up to you. But you should make a fun remark about your name. If it's odd feel free to make fun of it. If it's quirky or clever, make an interesting remark about it. Keep remarks *brief*!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_waifu_name}\n")

        print(f"{user_data['waifu_name']}:  I'd love to get to know you better.")
        print(f"{user_data['waifu_name']}:  I promise I'm not a creepy stalker...unless you're into that sort of thing. 😏")
        user_data["location"] = get_input(f"{user_data['waifu_name']}:  Where do ya live? ", "Unknown")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You live in {user_data['location']} ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_location = waifu_ai_comment(f"The user lives in {user_data['location']}. Your reaction is up to you. But you should make a fun remark about {user_data['location']}. If it's odd feel free to make fun of it. If it's quirky or clever, make an interesting remark about it. Keep remarks *brief*! End with a joke about how you live inside of the terminal.")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_location}\n")

        print(f"{user_data['waifu_name']}:  Now that we've got the introductions out of the way, let's get down to business~!")
        user_data["session_goals"] = get_input(f"{user_data['waifu_name']}:  What do you want to accomplish? Just know that I'll hold you accountable~! ", "No goals set")
        
        print(f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")

        ai_comment_session_goals = waifu_ai_comment(f"The user wants to accomplish {user_data['session_goals']}. Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}")

        save_user_data(user_data)

    else:
        user_data = load_user_data()
        print(f"\n✨ Welcome Back ✨")
        print(f"{'-'*40}")
        print(f"{user_data['waifu_name']}:  Hey there {user_data['name']}! 💖 {user_data['waifu_name']} missed you~!\n")
        
        ai_comment_location_greeting = waifu_ai_comment(f"Make a timely or newsworthy remark about current events or weather in the user's location {user_data['location']}. Keep it brief, please.")
        print(f"{user_data['waifu_name']}:  {ai_comment_location_greeting}\n")

        user_data["mood"] = get_input(f"{user_data['waifu_name']}:  How are you feeling today? Mental health is important! ", "I'm good!")
        
        ai_comment_mood = waifu_ai_comment(f"The user is feeling {user_data['mood']}. If they seem happy or in a good mood, make a fun remark about it. If they seem sad or in a bad mood, make a remark about it that is cheerful and encouraging. Keep remarks *brief*!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_mood}\n")

        print(f"{user_data['waifu_name']}:  How was your last coding session?")
        print(f"{user_data['waifu_name']}:  You planned to: {user_data['session_goals']}")
        user_data["session_goals"] = get_input(f"{user_data['waifu_name']}:  Did you get it done? ", "No goals set")
        
        ai_comment_session_goals = waifu_ai_comment(f"The user got {user_data['session_goals']} done(or not done, depending on their response). Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging! Scold them if they didn't get it done. Encourage them if they did.")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_session_goals}\n")

        ai_comment_new_goals = waifu_ai_comment("Make a brief and succint quip about setting goals. Then include a note about how you'll hold them accountable. End with a joke about how you live inside of the terminal and have nothing else to do. Keep it BRIEF. Do not ramble, please")
        print(f"{user_data['waifu_name']}:  {ai_comment_new_goals}\n")

        user_data["session_goals"] = get_input(f"{user_data['waifu_name']}:  Well would you like to set new goals for this session? ", "No goals set")

        print(f"\n{Fore.MAGENTA}✨ New unlock: You want to accomplish {user_data['session_goals']} today ✨{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'-'*40}{Style.RESET_ALL}")
        
        ai_comment_new_goals = waifu_ai_comment(f"The user wants to accomplish {user_data['session_goals']}. Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging!")
        print(f"\n{user_data['waifu_name']}:  {ai_comment_new_goals}")

        save_user_data(user_data)

def main():
    welcome_message()

if __name__ == "__main__":
    main()