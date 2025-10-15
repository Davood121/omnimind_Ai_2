"""
Enhanced Real-time News with AI Summaries
Provides detailed news analysis and summaries
"""

import requests
from typing import List, Dict
from datetime import datetime

def get_detailed_news(topic: str = "India", max_articles: int = 5) -> str:
    """Get detailed news with AI summaries and analysis"""
    try:
        # Multiple news sources
        sources = [
            f"https://news.google.com/rss/search?q={topic}&hl=en-IN&gl=IN&ceid=IN:en",
            f"https://feeds.feedburner.com/ndtvnews-top-stories",
            f"https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
        ]
        
        all_articles = []
        
        for source_url in sources:
            try:
                import feedparser
                feed = feedparser.parse(source_url)
                
                for entry in feed.entries[:max_articles]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    link = entry.get('link', '')
                    published = entry.get('published', '')
                    
                    # Clean HTML tags
                    import re
                    title = re.sub('<.*?>', '', title)
                    summary = re.sub('<.*?>', '', summary)
                    
                    if title and len(title) > 10:
                        all_articles.append({
                            'title': title,
                            'summary': summary,
                            'link': link,
                            'published': published,
                            'source': source_url
                        })
                
                if len(all_articles) >= max_articles:
                    break
                    
            except Exception as e:
                continue
        
        if not all_articles:
            return f"📰 No news articles found for '{topic}'"
        
        # Generate AI summaries
        news_report = f"📰 **DETAILED {topic.upper()} NEWS REPORT**\n"
        news_report += f"🕒 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for i, article in enumerate(all_articles[:max_articles], 1):
            try:
                from brain.ollama_interface import OllamaInterface
                ollama = OllamaInterface(model="qwen2.5:3b")
                
                # Create comprehensive AI analysis
                analysis_prompt = f"""
                Analyze this news article and provide:
                1. A clear 2-3 sentence summary
                2. Key points or implications
                3. Context or background if relevant
                
                Title: {article['title']}
                Content: {article['summary'][:400]}
                """
                
                ai_analysis = ollama.generate(
                    "You are a professional news analyst. Provide clear, informative analysis.",
                    analysis_prompt,
                    temperature=0.2
                )
                
                news_report += f"**{i}. {article['title']}**\n"
                news_report += f"📅 {article['published']}\n"
                news_report += f"🤖 **AI Analysis:**\n{ai_analysis}\n"
                news_report += f"🔗 Read more: {article['link']}\n"
                news_report += "─" * 50 + "\n\n"
                
            except Exception as e:
                # Fallback without AI
                news_report += f"**{i}. {article['title']}**\n"
                news_report += f"📅 {article['published']}\n"
                news_report += f"📄 {article['summary'][:200]}...\n"
                news_report += f"🔗 {article['link']}\n"
                news_report += "─" * 50 + "\n\n"
        
        return news_report
        
    except Exception as e:
        return f"📰 Error fetching detailed news: {str(e)}"

def get_breaking_news() -> str:
    """Get breaking news with immediate AI analysis"""
    try:
        # Focus on breaking news sources
        breaking_sources = [
            "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN:en",
            "https://feeds.feedburner.com/ndtvnews-latest"
        ]
        
        latest_news = []
        
        for source in breaking_sources:
            try:
                import feedparser
                feed = feedparser.parse(source)
                
                for entry in feed.entries[:3]:
                    title = entry.get('title', '')
                    summary = entry.get('summary', '')
                    link = entry.get('link', '')
                    
                    import re
                    title = re.sub('<.*?>', '', title)
                    summary = re.sub('<.*?>', '', summary)
                    
                    if title:
                        latest_news.append({
                            'title': title,
                            'summary': summary,
                            'link': link
                        })
                
                if len(latest_news) >= 3:
                    break
                    
            except:
                continue
        
        if not latest_news:
            return "🚨 No breaking news available at the moment"
        
        breaking_report = "🚨 **BREAKING NEWS ALERT**\n\n"
        
        for i, news in enumerate(latest_news, 1):
            try:
                from brain.ollama_interface import OllamaInterface
                ollama = OllamaInterface(model="qwen2.5:3b")
                
                urgent_analysis = ollama.generate(
                    "You are a breaking news analyst. Provide immediate, clear analysis of urgent news.",
                    f"Provide urgent analysis of this breaking news:\n\nTitle: {news['title']}\nDetails: {news['summary'][:300]}",
                    temperature=0.1
                )
                
                breaking_report += f"**{i}. {news['title']}**\n"
                breaking_report += f"⚡ **Urgent Analysis:** {urgent_analysis}\n"
                breaking_report += f"🔗 {news['link']}\n\n"
                
            except:
                breaking_report += f"**{i}. {news['title']}**\n"
                breaking_report += f"📄 {news['summary'][:150]}...\n"
                breaking_report += f"🔗 {news['link']}\n\n"
        
        return breaking_report
        
    except Exception as e:
        return f"🚨 Error fetching breaking news: {str(e)}"