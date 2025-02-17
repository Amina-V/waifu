import pytest
from unittest.mock import MagicMock
from ..waifucode import WaifuAssistant, StorageManager, UIManager

class MockOpenAI:
    def __init__(self):
        self.chat = MagicMock()
        self.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Mock response"))]
        )

class MockStorage:
    def __init__(self):
        self.chat_history = []
        self.user_data = {}

    def load_chat_history(self):
        return self.chat_history

    def save_chat_history(self, history):
        self.chat_history = history

def test_waifu_response():
    mock_client = MockOpenAI()
    mock_storage = MockStorage()
    mock_ui = UIManager()
    waifu = WaifuAssistant(mock_client, mock_storage, mock_ui)
    response = waifu.waifu_ai_comment("Hello!")
    assert response is not None
    assert isinstance(response, str) 