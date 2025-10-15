"""
Conversation Enhancement Module
Improves chat quality with context awareness and personality
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class ConversationEnhancer:
    def __init__(self, memory_dir: str):
        self.memory_dir = memory_dir
        self.profile_path = os.path.join(memory_dir, 'user_profile.json')
        self.conv_path = os.path.join(memory_dir, 'conversations.json')
        
    def analyze_conversation_patterns(self) -> Dict:
        """Analyze user's conversation patterns and preferences"""
        try:
            with open(self.conv_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history = data.get('history', [])
            
            if not history:
                return {"patterns": "No conversation history yet"}
            
            # Analyze patterns
            total_messages = len(history)
            topics = []
            question_types = []
            
            for entry in history[-20:]:  # Last 20 conversations
                user_msg = entry.get('user', '').lower()
                
                # Identify topics
                if any(word in user_msg for word in ['news', 'current', 'today']):
                    topics.append('news')
                elif any(word in user_msg for word in ['what', 'how', 'why', 'explain']):
                    topics.append('questions')
                elif any(word in user_msg for word in ['search', 'find', 'look']):
                    topics.append('search')
                elif any(word in user_msg for word in ['code', 'program', 'script']):
                    topics.append('coding')
            
            # Most common topics
            from collections import Counter
            common_topics = Counter(topics).most_common(3)
            
            return {
                "total_conversations": total_messages,
                "recent_topics": [topic[0] for topic in common_topics],
                "conversation_style": "analytical" if "questions" in topics else "casual",
                "last_interaction": history[-1].get('timestamp', 0) if history else 0
            }
            
        except Exception:
            return {"patterns": "Unable to analyze conversation patterns"}
    
    def get_contextual_greeting(self) -> str:
        """Generate contextual greeting based on time and history"""
        hour = datetime.now().hour
        patterns = self.analyze_conversation_patterns()
        
        # Time-based greeting
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 22:
            time_greeting = "Good evening"
        else:
            time_greeting = "Hello"
        
        # Personalized based on patterns
        if patterns.get("recent_topics"):
            topic = patterns["recent_topics"][0]
            if topic == "news":
                return f"{time_greeting}! Ready for today's news updates?"
            elif topic == "questions":
                return f"{time_greeting}! What would you like to explore today?"
            elif topic == "coding":
                return f"{time_greeting}! Ready to dive into some coding?"
        
        return f"{time_greeting}! How can I assist you today?"
    
    def enhance_response(self, response: str, user_message: str) -> str:
        """Enhance AI response with personality and context"""
        patterns = self.analyze_conversation_patterns()
        
        # Add personality markers
        if "?" in user_message:
            if not response.endswith((".", "!", "?")):
                response += "."
            
            # Add follow-up suggestions for questions
            if any(word in user_message.lower() for word in ['what', 'how', 'explain']):
                response += "\n\n💡 Would you like me to elaborate on any specific aspect?"
        
        # Add contextual suggestions based on patterns
        if patterns.get("recent_topics"):
            topic = patterns["recent_topics"][0]
            if topic == "news" and "news" not in user_message.lower():
                response += "\n\n📰 By the way, I can also get you the latest news if you're interested!"
            elif topic == "coding" and "code" not in user_message.lower():
                response += "\n\n💻 Need any coding help? I'm great with programming questions too!"
        
        return response
    
    def update_user_preferences(self, user_message: str, ai_response: str):
        """Update user preferences based on interaction"""
        try:
            # Load current profile
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
            except Exception:
                profile = {"preferences": {}, "summary": ""}
            
            # Analyze preferences from message
            msg_lower = user_message.lower()
            
            # Update communication style preference
            if len(user_message.split()) > 20:  # Long messages
                profile["preferences"]["communication_style"] = "detailed"
            elif len(user_message.split()) < 5:  # Short messages
                profile["preferences"]["communication_style"] = "concise"
            
            # Update topic interests
            interests = profile["preferences"].get("interests", [])
            
            if any(word in msg_lower for word in ['news', 'current', 'politics']):
                if "news" not in interests:
                    interests.append("news")
            elif any(word in msg_lower for word in ['tech', 'technology', 'ai', 'computer']):
                if "technology" not in interests:
                    interests.append("technology")
            elif any(word in msg_lower for word in ['science', 'research', 'study']):
                if "science" not in interests:
                    interests.append("science")
            
            profile["preferences"]["interests"] = interests[:5]  # Keep top 5
            
            # Update summary
            patterns = self.analyze_conversation_patterns()
            profile["summary"] = f"User prefers {profile['preferences'].get('communication_style', 'balanced')} responses. Interested in: {', '.join(interests)}. Total conversations: {patterns.get('total_conversations', 0)}"
            
            # Save updated profile
            with open(self.profile_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error updating preferences: {e}")

def get_smart_suggestions(user_message: str) -> List[str]:
    """Generate smart follow-up suggestions"""
    msg_lower = user_message.lower()
    suggestions = []
    
    if any(word in msg_lower for word in ['what', 'explain', 'how']):
        suggestions.extend([
            "Can you give me more details?",
            "What are the practical applications?",
            "Are there any examples?"
        ])
    elif "news" in msg_lower:
        suggestions.extend([
            "Get breaking news alerts",
            "Show detailed news analysis",
            "Search for specific topics"
        ])
    elif any(word in msg_lower for word in ['search', 'find']):
        suggestions.extend([
            "Search the web for more info",
            "Get recent updates on this topic",
            "Find related articles"
        ])
    else:
        suggestions.extend([
            "Tell me more about this",
            "What's the latest news?",
            "Help me search for something"
        ])
    
    return suggestions[:3]  # Return top 3 suggestions