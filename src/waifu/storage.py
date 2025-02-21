"""Storage management for the waifu assistant."""
import os
import json
from typing import Dict, List, Any
from datetime import datetime

class StorageManager:
    """Manages persistent storage for the assistant."""
    def __init__(self):
        self.data_dir = os.path.expanduser("~/.waifu_data")
        self.chat_file = os.path.join(self.data_dir, "chat_history.json")
        self.user_file = os.path.join(self.data_dir, "user_data.json")
        self._ensure_data_dir()
        
    def _ensure_data_dir(self) -> None:
        """Ensures the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)

    def _get_default_user_data(self) -> Dict[str, Any]:
        """Returns default user data structure."""
        return {
            "name": "Senpai",
            "waifu_name": "Waifu",
            "location": "Unknown",
            "session_goals": "No goals set",
            "mood": "Unknown",
            "first_login": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }

    def load_chat_history(self) -> List[Dict[str, str]]:
        """Loads chat history from storage."""
        if os.path.exists(self.chat_file):
            with open(self.chat_file, 'r') as f:
                return json.load(f)
        return []

    def save_chat_history(self, history: List[Dict[str, str]]) -> None:
        """Saves chat history to storage."""
        with open(self.chat_file, 'w') as f:
            json.dump(history, f, indent=4)

    def load_user_data(self) -> Dict[str, Any]:
        """Loads user data from storage with defaults."""
        default_data = self._get_default_user_data()
        if os.path.exists(self.user_file):
            try:
                with open(self.user_file, 'r') as f:
                    stored_data = json.load(f)
                    # Merge stored data with defaults, preserving stored values
                    return {**default_data, **stored_data}
            except (json.JSONDecodeError, FileNotFoundError):
                return default_data
        return default_data

    def save_user_data(self, data: Dict[str, Any]) -> None:
        """Saves user data to storage."""
        # Ensure all required fields exist
        full_data = {**self._get_default_user_data(), **data}
        full_data["last_login"] = datetime.now().isoformat()
        
        with open(self.user_file, 'w') as f:
            json.dump(full_data, f, indent=4) 