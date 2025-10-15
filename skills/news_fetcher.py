"""
Real-time News Fetcher for OmniMind
Fetches latest news from multiple sources
"""

import requests
from datetime import datetime
try:
    import feedparser
except ImportError:
    feedparser = None

def get_india_news():
    """Get latest India news with AI summaries"""
    try:
        # Try multiple RSS feeds for India news
        feeds = [
            "https://feeds.feedburner.com/ndtvnews-top-stories",
            "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
            "https://www.hindustantimes.com/feeds/rss/india-news/index.xml"
        ]
        
        for feed_url in feeds:
            try:
                import feedparser
                feed = feedparser.parse(feed_url)
                
                if feed.entries:
                    news_summaries = []
                    
                    for i, entry in enumerate(feed.entries[:5], 1):
                        title = entry.get('title', 'No title')
                        summary = entry.get('summary', '')
                        link = entry.get('link', '')
                        
                        # Clean HTML tags
                        import re
                        title = re.sub('<.*?>', '', title)
                        summary = re.sub('<.*?>', '', summary)
                        
                        # Get AI summary
                        try:
                            from brain.ollama_interface import OllamaInterface
                            ollama = OllamaInterface(model="qwen2.5:3b")
                            
                            ai_summary = ollama.generate(
                                "You are a news analyst. Provide clear, informative summaries.",
                                f"Summarize this Indian news in 2-3 sentences:\n\nTitle: {title}\nContent: {summary[:300]}",
                                temperature=0.1
                            )
                            
                            news_summaries.append(f"{i}. **{title}**\n   📝 {ai_summary}\n   🔗 {link}\n")
                        except:
                            # Fallback without AI
                            news_summaries.append(f"{i}. **{title}**\n   📄 {summary[:150]}...\n   🔗 {link}\n")
                    
                    news_text = "🇮🇳 **Latest India News with AI Analysis:**\n\n"
                    news_text += "\n".join(news_summaries)
                    return news_text
            except:
                continue
        
        # Fallback to web scraping
        return get_news_web_scrape()
        
    except Exception as e:
        return f"📰 India News: Service temporarily unavailable. Error: {str(e)}"

def get_news_web_scrape():
    """Fallback: Web scraping for news"""
    try:
        # Simple web scraping approach
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Try Google News RSS
        url = "https://news.google.com/rss/search?q=India&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            import feedparser
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                news_text = "📰 Latest India News (Google):\n\n"
                for i, entry in enumerate(feed.entries[:7], 1):
                    title = entry.get('title', 'No title')
                    import re
                    title = re.sub('<.*?>', '', title)
                    news_text += f"{i}. {title}\n"
                return news_text
        
        return "📰 News service temporarily unavailable. Please try again later."
        
    except Exception as e:
        return f"📰 News: Unable to fetch at the moment. {str(e)}"

def get_world_news():
    """Get world news headlines"""
    try:
        # Multiple international news sources
        feeds = [
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://rss.cnn.com/rss/edition.rss",
            "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
        ]
        
        for feed_url in feeds:
            try:
                import feedparser
                feed = feedparser.parse(feed_url)
                
                if feed.entries:
                    news_text = "🌍 Latest World News:\n\n"
                    for i, entry in enumerate(feed.entries[:7], 1):
                        title = entry.get('title', 'No title')
                        import re
                        title = re.sub('<.*?>', '', title)
                        news_text += f"{i}. {title}\n"
                    return news_text
            except:
                continue
        
        return "🌍 World news temporarily unavailable."
        
    except Exception as e:
        return f"🌍 World News: Service unavailable. {str(e)}"

if __name__ == "__main__":
    print(get_india_news())