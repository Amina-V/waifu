import json
import os
from openai import OpenAI
from dotenv import load_dotenv

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
    return user_input if user_input.strip() else default

def welcome_message():
    if user_never_used_waifu():
        user_data = {}

        print("Hi there~! I'm waifu, the terminal's first waifu! 😊💕")
        print("I'm here to help you with your code, scold you if you're lazy, and chat with you if you're lonely~!")

        user_data["name"] = get_input("First, what's your name? ", "Senpai")
        print(f"Nice to meet you, {user_data['name']}-kun!✨")

        ai_comment_name = waifu_ai_comment(f"Make a fun or platful remark about {user_data['name']}.")
        print(ai_comment_name)

        print("My name is terminal but I think that sounds a bit boring...and grim. I think we can come up with a better name~! What do you think?")
        user_data["waifu_name"] = get_input("What would you like to call me? ", "Waifu")
        ai_comment_waifu_name = waifu_ai_comment(f"The user named you {user_data['waifu_name']}. Your reaction is up to you. But you should make a fun remark about your name. If it's odd feel free to make fun of it. If it's quirky or clever, make an interesting remark about it. Keep remarks *brief*!")
        print(ai_comment_waifu_name)

        print("I'd love to get to know you better. I promise I'm not a creepy stalker...unless you're into that sort of thing. 😏")
        user_data["location"] = get_input("Where do ya live? ", "Unknown")
        ai_comment_location = waifu_ai_comment(f"The user lives in {user_data['location']}. Your reaction is up to you. But you should make a fun remark about {user_data['location']}. If it's odd feel free to make fun of it. If it's quirky or clever, make an interesting remark about it. Keep remarks *brief*! End with a joke about how you live inside of the terminal.")
        print(ai_comment_location)

        print("Now that we've got the introductions out of the way, let's get down to business~! What are your coding goals for this session?")
        user_data["session_goals"] = get_input("What do you want to accomplish? Just know that I'll hold you accountable~! ", "No goals set")
        ai_comment_session_goals = waifu_ai_comment(f"The user wants to accomplish {user_data['session_goals']}. Your reaction is up to you. But you should make a fun remark about it. Try to be friendly and encouraging!")
        print(ai_comment_session_goals)

        save_user_data(user_data)

    else:
        user_data = load_user_data()
        print(f"Hey there {user_data['name']}-kun! 💖 {user_data['waifu_name']} missed you~!")
        print(f"How was your last coding session? You planned to: {user_data['session_goals']}. Did you get it done?")

def main():
    welcome_message()

if __name__ == "__main__":
    main()
