import json
import os

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
        print("My name is terminal but I think that sounds a bit boring...and grim. I think we can come up with a better name~! What do you think?")
        user_data["waifu_name"] = get_input("What would you like to call me? ", "Waifu")
        print(f"Thank you for naming me {user_data['waifu_name']}~! I'm honored! 💕")

        print(f"Hm, what type of person comes up with a name like {user_data['waifu_name']}? 🤔")
        user_data["location"] = get_input("Where do ya live? ", "Unknown")
        print(f"Wow, {user_data['location']} sounds cool! I wish I could visit... but I'm stuck in the terminal! 😆")

        print("Now that we've got the introductions out of the way, let's get down to business~! What are your coding goals for this session?")
        user_data["session_goals"] = get_input("What do you want to accomplish? Just know that I'll hold you accountable~! ", "No goals set")

        print(f"Great! Your goal is: {user_data['session_goals']}! I'll hold ya to it, hehe ✨")

        save_user_data(user_data)
    
    else:
        user_data = load_user_data()
        print(f"Hey there {user_data['name']}-kun! 💖 {user_data['waifu_name']} missed you~!")
        print(f"How was your last coding session? You planned to: {user_data['session_goals']}. Did you get it done?")

def main():
    welcome_message()

if __name__ == "__main__":
    main()
