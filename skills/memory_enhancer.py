"""
Advanced Memory Enhancement for OmniMind
Provides sophisticated conversation memory and context tracking
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class AdvancedMemory:
    def __init__(self, memory_dir: str):
        self.memory_dir = memory_dir
        self.conv_path = os.path.join(memory_dir, 'conversations.json')
        self.context_path = os.path.join(memory_dir, 'context_memory.json')
        
    def analyze_conversation_flow(self) -> Dict:
        """Analyze conversation patterns and topic flow"""
        try:
            with open(self.conv_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history = data.get('history', [])
            
            if len(history) < 2:
                return {"flow": "new_conversation"}
            
            # Analyze recent messages for topic continuity
            recent = history[-5:]  # Last 5 exchanges
            topics = []
            questions = []
            
            for entry in recent:
                user_msg = entry.get('user', '').lower()
                
                # Identify question types
                if any(word in user_msg for word in ['why', 'how', 'what', 'when', 'where', 'who']):
                    questions.append(user_msg)
                
                # Identify topics
                if 'ai' in user_msg or 'artificial intelligence' in user_msg:
                    topics.append('ai')
                elif 'memory' in user_msg or 'remember' in user_msg:
                    topics.append('memory')
                elif 'news' in user_msg:
                    topics.append('news')
                elif 'search' in user_msg:
                    topics.append('search')
            
            return {
                "flow": "continuing_conversation",
                "recent_topics": list(set(topics)),
                "question_pattern": len(questions) > 2,
                "conversation_depth": len(history),
                "last_topic": topics[-1] if topics else None
            }
            
        except Exception:
            return {"flow": "error_reading_history"}
    
    def get_contextual_memory(self, current_message: str) -> str:
        """Generate contextual memory prompt based on conversation history"""
        try:
            flow_analysis = self.analyze_conversation_flow()
            
            with open(self.conv_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history = data.get('history', [])
            
            if not history:
                return "This is the start of our conversation."
            
            # Build memory context
            memory_context = "CONVERSATION MEMORY:\n"
            
            # Add recent exchanges with emphasis on continuity
            recent_history = history[-8:]  # Last 8 for good context
            for i, entry in enumerate(recent_history, 1):
                user_msg = entry.get('user', '')
                ai_msg = entry.get('assistant', '')
                memory_context += f"Exchange {i}:\n"
                memory_context += f"  User: {user_msg}\n"
                memory_context += f"  You: {ai_msg[:100]}{'...' if len(ai_msg) > 100 else ''}\n\n"
            
            # Add topic continuity analysis
            if flow_analysis.get('recent_topics'):
                memory_context += f"Recent topics discussed: {', '.join(flow_analysis['recent_topics'])}\n"
            
            if flow_analysis.get('last_topic'):
                memory_context += f"Current topic thread: {flow_analysis['last_topic']}\n"
            
            # Check for topic connections
            current_lower = current_message.lower()
            topic_connections = []
            
            for entry in recent_history:
                prev_msg = entry.get('user', '').lower()
                # Simple keyword matching for topic continuity
                common_words = set(current_lower.split()) & set(prev_msg.split())
                if len(common_words) > 1:  # More than just common words like 'the', 'is'
                    topic_connections.append(f"Relates to: '{entry.get('user', '')[:50]}...'")
            
            if topic_connections:
                memory_context += f"\nTopic connections found:\n"
                for connection in topic_connections[:2]:  # Top 2 connections
                    memory_context += f"- {connection}\n"
            
            memory_context += f"\nCONVERSATION INSTRUCTIONS:\n"
            memory_context += f"- Reference relevant previous messages\n"
            memory_context += f"- Build upon established topics\n"
            memory_context += f"- Show continuity in your responses\n"
            memory_context += f"- Connect current question to conversation history when appropriate\n"
            
            return memory_context
            
        except Exception as e:
            return f"Memory system error: {str(e)}"
    
    def save_context_markers(self, user_message: str, ai_response: str):
        """Save important context markers for future reference"""
        try:
            # Load existing context
            try:
                with open(self.context_path, 'r', encoding='utf-8') as f:
                    context_data = json.load(f)
            except Exception:
                context_data = {"markers": [], "topics": {}}
            
            # Extract important markers
            markers = context_data.get("markers", [])
            topics = context_data.get("topics", {})
            
            # Add new marker
            marker = {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "ai_response": ai_response[:200],  # First 200 chars
                "keywords": self._extract_keywords(user_message)
            }
            
            markers.append(marker)
            
            # Keep only last 50 markers
            if len(markers) > 50:
                markers = markers[-50:]
            
            # Update topic tracking
            for keyword in marker["keywords"]:
                if keyword not in topics:
                    topics[keyword] = 0
                topics[keyword] += 1
            
            # Save updated context
            context_data = {
                "markers": markers,
                "topics": topics,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.context_path, 'w', encoding='utf-8') as f:
                json.dump(context_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error saving context markers: {e}")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction
        words = text.lower().split()
        
        # Filter out common words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by'}
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        return keywords[:5]  # Top 5 keywords

# Global memory instance
def get_memory_context(memory_dir: str, current_message: str) -> str:
    """Get contextual memory for current message"""
    memory = AdvancedMemory(memory_dir)
    return memory.get_contextual_memory(current_message)

def save_memory_markers(memory_dir: str, user_message: str, ai_response: str):
    """Save memory markers for future context"""
    memory = AdvancedMemory(memory_dir)
    memory.save_context_markers(user_message, ai_response)