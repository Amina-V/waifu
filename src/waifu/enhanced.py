"""Enhanced features for the waifu assistant."""
from typing import List, Dict, Optional, Any
from datetime import datetime
from io import StringIO
from .base import WaifuAssistant
from .storage import StorageManager
from .ui import UIManager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import Fore, Style
import pylint.lint
import ast
from pathlib import Path
import time

class Mood:
    """Manages the waifu's mood state."""
    def __init__(self):
        self.current_mood = 100  # Start with happy mood
        
    def update_mood(self, factors: dict) -> None:
        """Updates mood based on various factors."""
        # Simple mood adjustment based on factors
        if factors.get("time_since_break"):
            self.current_mood -= factors["time_since_break"] * 0.1
        if factors.get("code_quality"):
            self.current_mood += factors["code_quality"] * 0.2
        # Keep mood within bounds
        self.current_mood = max(0, min(100, self.current_mood))

class EnhancedWaifuAssistant(WaifuAssistant):
    """Enhanced waifu assistant with code review capabilities."""
    def __init__(self, openai_client, storage_manager, ui_manager):
        super().__init__(openai_client, storage_manager, ui_manager)
        self.mood = Mood()  # Initialize mood
        
    def review_file(self, file_path: str) -> None:
        """Review a single Python file."""
        try:
            print(f"\n{Fore.CYAN}Code Review for {Path(file_path).name}:{Style.RESET_ALL}")
            
            # Read the file
            with open(file_path, 'r') as file:
                code = file.read()
            
            # Basic static analysis
            try:
                ast.parse(code)
                print(f"{Fore.GREEN}✓ Code syntax is valid{Style.RESET_ALL}")
            except SyntaxError as e:
                print(f"{Fore.RED}✗ Syntax error: {str(e)}{Style.RESET_ALL}")
            
            # Run pylint with updated API
            from pylint.lint import Run
            from pylint.reporters import JSONReporter
            reporter = JSONReporter()
            Run([file_path], reporter=reporter, exit=False)
            
            # Get AI review
            review_prompt = (
                f"Review this Python file as a cute anime waifu assistant. "
                f"Be constructive and encouraging, but also point out areas for improvement: {code}"
            )
            ai_review = self.waifu_ai_comment(review_prompt)
            print(f"\n{Fore.YELLOW}AI Review:{Style.RESET_ALL}")
            print(ai_review)
            
        except Exception as e:
            print(f"{Fore.RED}Error reviewing file: {str(e)}{Style.RESET_ALL}")

    def review_directory(self, dir_path: str) -> None:
        """Review all Python files in a directory."""
        try:
            path = Path(dir_path)
            python_files = list(path.glob("**/*.py"))
            
            if not python_files:
                print(f"{Fore.YELLOW}No Python files found in {dir_path}{Style.RESET_ALL}")
                return
                
            print(f"\n{Fore.CYAN}Reviewing {len(python_files)} Python files in {dir_path}:{Style.RESET_ALL}")
            
            for file_path in python_files:
                self.review_file(str(file_path))
                print(f"{Fore.MAGENTA}{'-' * 40}{Style.RESET_ALL}\n")
                
        except Exception as e:
            print(f"{Fore.RED}Error reviewing directory: {str(e)}{Style.RESET_ALL}")

    def setup_command_history(self) -> None:
        """Sets up command history and auto-completion."""
        self.commands = ['exit']
        
    def start_code_watching(self, path: str) -> None:
        """Start watching a directory for code changes."""
        self.code_watcher = CodeWatcher(self)
        self.observer = Observer()
        self.observer.schedule(self.code_watcher, path, recursive=True)
        self.observer.start()
        print(f"{Fore.CYAN}I'll watch your code and provide feedback! (◕‿◕✿){Style.RESET_ALL}")

    def stop_code_watching(self) -> None:
        """Stop watching for code changes."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print(f"{Fore.CYAN}Stopped watching your code! (｡♥‿♥｡){Style.RESET_ALL}")

    def process_command(self, command: str) -> bool:
        """Basic command processor."""
        return False

    def chat(self, user_input: str) -> str:
        """Basic chat method."""
        response = self.waifu_ai_comment(user_input)
        return response 

class CodeWatcher(FileSystemEventHandler):
    def __init__(self, waifu_assistant):
        self.waifu = waifu_assistant
        self.last_modified = {}

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Only process Python files
        if not event.src_path.endswith('.py'):
            return
            
        # Debounce file changes (prevent multiple triggers)
        current_time = time.time()
        if event.src_path in self.last_modified:
            if current_time - self.last_modified[event.src_path] < 2:  # 2 second debounce
                return
                
        self.last_modified[event.src_path] = current_time
        self.waifu.review_file(event.src_path) 