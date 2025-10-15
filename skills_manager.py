"""
Skills Manager for OmniMind OS
Manages and executes various AI skills and capabilities
"""

import os
import webbrowser
import subprocess
from typing import Dict, Any, Optional, List
from skills.media_player import play_music


class SkillsManager:
    """Manages all available skills and their execution"""
    
    def __init__(self):
        self.available_skills = {
            "play_music": {
                "name": "Play Music",
                "description": "Search and play music from YouTube",
                "function": self.play_music_skill,
                "keywords": ["play", "music", "song", "audio"]
            },
            "open_website": {
                "name": "Open Website",
                "description": "Open a website in the browser",
                "function": self.open_website_skill,
                "keywords": ["open", "website", "browse", "visit"]
            },
            "search_web": {
                "name": "Search Web",
                "description": "Search the web using default search engine",
                "function": self.search_web_skill,
                "keywords": ["search", "google", "find", "look up"]
            },
            "open_application": {
                "name": "Open Application",
                "description": "Open a system application",
                "function": self.open_application_skill,
                "keywords": ["open", "launch", "start", "run"]
            },
            "system_command": {
                "name": "System Command",
                "description": "Execute system commands",
                "function": self.system_command_skill,
                "keywords": ["execute", "command", "run", "terminal"]
            },
            "file_operations": {
                "name": "File Operations",
                "description": "Create, read, or manage files",
                "function": self.file_operations_skill,
                "keywords": ["file", "create", "read", "write", "delete"]
            }
        }
    
    def get_available_skills(self) -> List[Dict[str, str]]:
        """Get list of all available skills"""
        return [
            {
                "id": skill_id,
                "name": skill["name"],
                "description": skill["description"]
            }
            for skill_id, skill in self.available_skills.items()
        ]
    
    def detect_skill(self, query: str) -> Optional[str]:
        """Detect which skill to use based on query"""
        query_lower = query.lower()
        
        for skill_id, skill in self.available_skills.items():
            if any(keyword in query_lower for keyword in skill["keywords"]):
                return skill_id
        
        return None
    
    def execute_skill(self, skill_id: str, query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a specific skill"""
        if skill_id not in self.available_skills:
            return {
                "success": False,
                "message": f"Unknown skill: {skill_id}"
            }
        
        skill = self.available_skills[skill_id]
        try:
            result = skill["function"](query, params or {})
            return {
                "success": True,
                "skill": skill["name"],
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "skill": skill["name"],
                "error": str(e)
            }
    
    # Skill implementations
    
    def play_music_skill(self, query: str, params: Dict[str, Any]) -> str:
        """Play music from YouTube"""
        result = play_music(query)
        return result
    
    def open_website_skill(self, query: str, params: Dict[str, Any]) -> str:
        """Open a website in the browser"""
        # Extract URL from query
        words = query.split()
        url = None
        
        for word in words:
            if '.' in word and not word.startswith('.'):
                url = word
                if not url.startswith('http'):
                    url = 'https://' + url
                break
        
        if url:
            webbrowser.open(url)
            return f"Opening {url} in your browser"
        else:
            return "Please specify a website URL"
    
    def search_web_skill(self, query: str, params: Dict[str, Any]) -> str:
        """Search the web"""
        # Remove search keywords
        search_query = query.lower()
        for keyword in ['search', 'google', 'find', 'look up']:
            search_query = search_query.replace(keyword, '')
        search_query = search_query.strip()
        
        if search_query:
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching for: {search_query}"
        else:
            return "Please specify what to search for"
    
    def open_application_skill(self, query: str, params: Dict[str, Any]) -> str:
        """Open a system application"""
        query_lower = query.lower()
        
        # Common applications mapping
        apps = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'explorer': 'explorer.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'chrome': 'chrome.exe',
            'edge': 'msedge.exe',
            'firefox': 'firefox.exe'
        }
        
        for app_name, app_exe in apps.items():
            if app_name in query_lower:
                try:
                    subprocess.Popen(app_exe)
                    return f"Opening {app_name.title()}"
                except Exception as e:
                    return f"Failed to open {app_name}: {str(e)}"
        
        return "Application not found. Try: notepad, calculator, paint, explorer, chrome, edge"
    
    def system_command_skill(self, query: str, params: Dict[str, Any]) -> str:
        """Execute system commands (with safety checks)"""
        # For safety, only allow specific safe commands
        safe_commands = {
            'time': 'echo %time%',
            'date': 'echo %date%',
            'username': 'echo %username%',
            'computer name': 'hostname',
            'ip address': 'ipconfig | findstr IPv4'
        }
        
        query_lower = query.lower()
        for cmd_name, cmd in safe_commands.items():
            if cmd_name in query_lower:
                try:
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    return result.stdout.strip() or "Command executed"
                except Exception as e:
                    return f"Error executing command: {str(e)}"
        
        return "For safety, only specific system info commands are allowed"
    
    def file_operations_skill(self, query: str, params: Dict[str, Any]) -> str:
        """Handle file operations"""
        query_lower = query.lower()
        
        if 'create' in query_lower or 'new' in query_lower:
            return "File creation requires specific path and content. Please provide details."
        elif 'read' in query_lower or 'open' in query_lower:
            return "File reading requires specific file path. Please provide the path."
        elif 'delete' in query_lower:
            return "File deletion requires explicit confirmation and path for safety."
        else:
            return "Available file operations: create, read, open, delete. Please specify."


# Global instance
skills_manager = SkillsManager()