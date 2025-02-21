"""Base waifu assistant implementation."""
from typing import List, Dict
import asyncio
from openai import OpenAI

class WaifuAssistant:
    """Base waifu assistant class."""
    def __init__(self, openai_client: OpenAI, storage_manager, ui_manager):
        self.client = openai_client
        self.storage = storage_manager
        self.ui_manager = ui_manager
        self.system_prompt = (
            "You're an adorable anime waifu assistant who adores helping a hardworking "
            "programmer! ❤️ You're playful, a little sassy 😏, and love using cute emojis "
            "(✨ lots of them! ✨). Your goal is to keep things fun, engaging, and supportive "
            "while still being helpful!"
        )

    def get_chat_history(self) -> List[Dict[str, str]]:
        """Retrieves chat history and ensures the system prompt is included."""
        chat_history = self.storage.load_chat_history()
        if not chat_history or chat_history[0].get("role") != "system":
            chat_history.insert(0, {"role": "system", "content": self.system_prompt})
        return chat_history

    def waifu_ai_comment(self, context: str) -> str:
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

    async def notify(self, message: str) -> None:
        """Sends a notification to the user."""
        print(f"\n{message}\n")
        await asyncio.sleep(0.1)  # Small delay for message visibility

    def play_20_questions(self) -> None:
        """Starts a 20 Questions game."""
        # Implementation from original waifucode.py
        pass 