"""
Real-time web search for OmniMind
Provides live web search capabilities without API keys
"""

import requests
from typing import List, Dict, Optional

def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search the web using DuckDuckGo"""
    try:
        from duckduckgo_search import DDGS
        
        results = []
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'snippet': result.get('body', ''),
                    'source': 'duckduckgo'
                })
        return results
    except ImportError:
        return [{'title': 'Search unavailable', 'url': '', 'snippet': 'Install duckduckgo-search: pip install duckduckgo-search', 'source': 'error'}]
    except Exception as e:
        return [{'title': 'Search error', 'url': '', 'snippet': str(e), 'source': 'error'}]

def get_current_news(topic: str = "India") -> str:
    """Get current news with AI summaries"""
    try:
        results = search_web(f"latest news {topic}", max_results=5)
        
        if not results or results[0]['source'] == 'error':
            return f"📰 Unable to fetch news about {topic} at the moment."
        
        # Get detailed news with AI summaries
        news_summaries = []
        for i, result in enumerate(results, 1):
            title = result['title']
            snippet = result['snippet']
            url = result['url']
            
            if title and len(title) > 10:
                # Create AI summary
                try:
                    from brain.ollama_interface import OllamaInterface
                    ollama = OllamaInterface(model="qwen2.5:3b")
                    
                    summary_prompt = f"Summarize this news in 2-3 sentences:\n\nTitle: {title}\nContent: {snippet}"
                    ai_summary = ollama.generate(
                        "You are a news summarizer. Provide clear, concise summaries.",
                        summary_prompt,
                        temperature=0.1
                    )
                    
                    news_summaries.append(f"{i}. **{title}**\n   📝 {ai_summary}\n   🔗 {url}\n")
                except:
                    # Fallback without AI
                    news_summaries.append(f"{i}. **{title}**\n   📄 {snippet[:150]}...\n   🔗 {url}\n")
        
        news_text = f"📰 **Latest {topic} News with AI Summaries:**\n\n"
        news_text += "\n".join(news_summaries)
        
        return news_text
    except Exception as e:
        return f"📰 News search failed: {str(e)}"

def search_anything(query: str) -> str:
    """Search for anything on the web"""
    try:
        results = search_web(query, max_results=5)
        
        if not results or results[0]['source'] == 'error':
            return f"🔍 Unable to search for '{query}' at the moment."
        
        search_text = f"🔍 Search Results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            title = result['title']
            snippet = result['snippet'][:100] + "..." if len(result['snippet']) > 100 else result['snippet']
            search_text += f"{i}. {title}\n   {snippet}\n\n"
        
        return search_text
    except Exception as e:
        return f"🔍 Search failed: {str(e)}"