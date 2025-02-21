"""Enhanced features for the waifu assistant."""
import json
import os
import time
import readline
import atexit
import asyncio
import pygame
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import speech_recognition as sr
from gtts import gTTS
import pylint.lint
import github
from .base import WaifuAssistant
from .storage import StorageManager
from .ui import UIManager

@dataclass
class WaifuMood:
    """Tracks the waifu's current mood and factors affecting it."""
    happiness: float = 75.0  # Base happiness level
    energy: float = 100.0
    last_break: datetime = datetime.now()
    coding_streak: int = 0
    
    def update_mood(self, factors: Dict[str, float]) -> None:
        """Updates mood based on various factors."""
        for factor, value in factors.items():
            if factor == "time_since_break":
                self.energy = max(0, self.energy - value)
            elif factor == "code_quality":
                self.happiness = min(100, self.happiness + value)

class PomodoroTimer:
    """Manages pomodoro sessions with cute notifications."""
    def __init__(self, work_time: int = 25, break_time: int = 5):
        self.work_time = work_time
        self.break_time = break_time
        self.is_running = False
        self.is_break = False
        self.time_left = work_time * 60
        
    async def start_timer(self, waifu_instance: 'WaifuAssistant') -> None:
        """Starts the pomodoro timer with waifu notifications."""
        self.is_running = True
        while self.is_running and self.time_left > 0:
            await asyncio.sleep(1)
            self.time_left -= 1
            if self.time_left == 0:
                if not self.is_break:
                    await waifu_instance.notify("Time for a break! (*˘︶˘*).｡.:*♡")
                else:
                    await waifu_instance.notify("Let's get back to coding! (ง •̀ω•́)ง✧")
                self.toggle_break()

    def toggle_break(self) -> None:
        """Toggles between work and break periods."""
        self.is_break = not self.is_break
        self.time_left = self.break_time * 60 if self.is_break else self.work_time * 60

class AchievementSystem:
    """Manages user achievements and rewards."""
    def __init__(self):
        self.achievements = {
            "first_commit": {"name": "First Commit!", "desc": "Made your first commit", "unlocked": False},
            "coding_streak": {"name": "Coding Warrior", "desc": "Coded for 7 days straight", "unlocked": False},
            "clean_code": {"name": "Clean Coder", "desc": "Wrote code with no pylint errors", "unlocked": False}
        }
        
    def check_achievement(self, achievement_id: str, condition: bool) -> Optional[Dict]:
        """Checks and awards achievements."""
        if not self.achievements[achievement_id]["unlocked"] and condition:
            self.achievements[achievement_id]["unlocked"] = True
            return self.achievements[achievement_id]
        return None

class CodeReviewer:
    """Provides kawaii code reviews."""
    def __init__(self, waifu_personality: str = "default"):
        self.personality = waifu_personality
        self.linter = pylint.lint.PyLinter()
        
    def review_code(self, file_path: str) -> Dict[str, Any]:
        """Reviews code and returns kawaii-styled feedback."""
        if not os.path.exists(file_path):
            return {"error": "Gomen ne~ I couldn't find that file! (╥﹏╥)"}
            
        results = {
            "style_issues": [],
            "security_concerns": [],
            "performance_tips": [],
            "praise": []
        }
        
        try:
            self.linter.check(file_path)
            if self.linter.stats['global_note'] >= 9:
                results["praise"].append("Sugoi! Your code is so clean! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
        except Exception as e:
            results["error"] = f"Oopsie! Something went wrong: {str(e)} (｡•́︿•̀｡)"
            
        return results

class VoiceInterface:
    """Handles voice input/output for the waifu."""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.voice_enabled = False
        pygame.mixer.init()
        
    def speak(self, text: str) -> None:
        """Converts text to speech with a cute voice."""
        if not self.voice_enabled:
            return
            
        tts = gTTS(text=text, lang='ja')
        tts.save("waifu_speech.mp3")
        pygame.mixer.music.load("waifu_speech.mp3")
        pygame.mixer.music.play()
        
    def listen(self) -> Optional[str]:
        """Listens for voice commands."""
        if not self.voice_enabled:
            return None
            
        with sr.Microphone() as source:
            try:
                audio = self.recognizer.listen(source)
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Gomen, I couldn't understand that (╥﹏╥)"
            except sr.RequestError:
                return "Ah, something went wrong with my listening powers! (｡•́︿•̀｡)"

class GitHubIntegration:
    """Handles GitHub integration features."""
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.gh = github.Github(token) if token else None
        
    def track_activity(self, username: str) -> Dict[str, Any]:
        """Tracks GitHub activity with kawaii comments."""
        if not self.gh:
            return {"error": "GitHub integration not configured (｡•́︿•̀｡)"}
            
        try:
            user = self.gh.get_user(username)
            recent_commits = user.get_events()
            activity = {
                "commits": [],
                "pull_requests": [],
                "comments": []
            }
            
            for event in recent_commits:
                if event.type == "PushEvent":
                    activity["commits"].append({
                        "repo": event.repo.name,
                        "message": event.payload.get("commits", [{}])[0].get("message", ""),
                        "timestamp": event.created_at
                    })
                    
            return activity
        except Exception as e:
            return {"error": f"Oopsie! Couldn't fetch GitHub activity: {str(e)} (╥﹏╥)"}

class LearningTracker:
    """Tracks learning progress and provides educational content."""
    def __init__(self):
        self.topics_covered = set()
        self.study_schedule = {}
        self.challenges = []
        
    def add_topic(self, topic: str, confidence_level: int) -> None:
        """Tracks a new programming topic discussed."""
        self.topics_covered.add({
            "topic": topic,
            "confidence": confidence_level,
            "last_reviewed": datetime.now()
        })
        
    def suggest_review(self) -> List[Dict]:
        """Suggests topics to review based on spaced repetition."""
        now = datetime.now()
        to_review = []
        
        for topic in self.topics_covered:
            days_since_review = (now - topic["last_reviewed"]).days
            if days_since_review > (7 - topic["confidence"]):
                to_review.append(topic)
                
        return to_review

class EnhancedWaifuAssistant(WaifuAssistant):
    """Enhanced version of WaifuAssistant with additional features."""
    def __init__(self, openai_client, storage_manager: StorageManager, ui_manager: UIManager):
        super().__init__(openai_client, storage_manager, ui_manager)
        
        # Initialize new features
        self.mood = WaifuMood()
        self.pomodoro = PomodoroTimer()
        self.achievements = AchievementSystem()
        self.code_reviewer = CodeReviewer()
        self.voice = VoiceInterface()
        self.github = GitHubIntegration()
        self.learning = LearningTracker()
        
        # Initialize command history
        self.setup_command_history()
        
    def setup_command_history(self) -> None:
        """Sets up command history and auto-completion."""
        histfile = os.path.expanduser("~/.waifu_history")
        try:
            readline.read_history_file(histfile)
        except FileNotFoundError:
            pass
            
        atexit.register(readline.write_history_file, histfile)
        
        # Define completions
        self.commands = ['20q', 'settings', 'clear', 'exit', 'review', 'pomodoro', 
                        'achievements', 'voice', 'github', 'learn', 'export']
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.complete_command)
        
    def complete_command(self, text: str, state: int) -> Optional[str]:
        """Provides command completion."""
        matches = [cmd for cmd in self.commands if cmd.startswith(text)]
        return matches[state] if state < len(matches) else None

    def chat(self, user_input: str) -> str:
        """Enhanced chat method that updates mood and tracks learning."""
        response = self.waifu_ai_comment(user_input)
        
        # Update mood based on interaction
        self.mood.update_mood({"time_since_break": 0.1})
        
        # Track programming topics discussed
        # TODO: Implement topic detection
        return response
        
    def process_command(self, command: str) -> bool:
        """Enhanced command processor with new features."""
        if command.startswith("review"):
            _, file_path = command.split(" ", 1)
            self.review_code(file_path)
            return True
        elif command == "pomodoro":
            asyncio.run(self.pomodoro.start_timer(self))
            return True
        elif command == "voice":
            self.voice.voice_enabled = not self.voice.voice_enabled
            status = "enabled" if self.voice.voice_enabled else "disabled"
            print(f"Voice mode {status} (｡♥‿♥｡)")
            return True
        elif command.startswith("export"):
            format_type = command.split(" ")[-1] if len(command.split(" ")) > 1 else "json"
            output_file = self.export_chat_history(format_type)
            if output_file:
                print(f"Chat history exported to {output_file} ✨")
            return True
        
        return False  # Command not handled 