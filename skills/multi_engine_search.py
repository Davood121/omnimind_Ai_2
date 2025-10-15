"""
Multi-Engine Search System
SearXNG + Wikipedia + YaCy with automatic fallback
"""

import requests
import concurrent.futures
from typing import List, Dict, Optional
import time

class MultiEngineSearch:
    def __init__(self):
        self.engines = {
            'searxng': {
                'url': 'https://searx.be',  # Public SearXNG instance
                'backup_urls': ['https://searx.tiekoetter.com', 'https://searx.prvcy.eu']
            },
            'wikipedia': {
                'url': 'https://en.wikipedia.org/w/api.php'
            },
            'yacy': {
                'url': 'https://yacy.searchlab.eu',  # Public YaCy instance
                'backup_urls': ['https://search.yacy.net']
            }
        }
    
    def search_searxng(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search using SearXNG with fallback URLs"""
        urls_to_try = [self.engines['searxng']['url']] + self.engines['searxng']['backup_urls']
        
        for base_url in urls_to_try:
            try:
                url = f"{base_url}/search"
                params = {
                    'q': query,
                    'format': 'json',
                    'language': 'en',
                    'safesearch': 1,
                    'categories': 'general'
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    
                    for item in data.get('results', [])[:max_results]:
                        results.append({
                            'title': item.get('title', ''),
                            'url': item.get('url', ''),
                            'snippet': item.get('content', ''),
                            'source': 'SearXNG'
                        })
                    
                    if results:
                        return results
            except Exception:
                continue
        
        return []
    
    def search_wikipedia(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Wikipedia API"""
        try:
            # Search for pages
            search_url = self.engines['wikipedia']['url']
            search_params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': max_results
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('query', {}).get('search', []):
                    title = item.get('title', '')
                    snippet = item.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
                    page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    
                    results.append({
                        'title': title,
                        'url': page_url,
                        'snippet': snippet,
                        'source': 'Wikipedia'
                    })
                
                return results
        except Exception:
            pass
        
        return []
    
    def search_yacy(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search using YaCy with fallback URLs"""
        urls_to_try = [self.engines['yacy']['url']] + self.engines['yacy']['backup_urls']
        
        for base_url in urls_to_try:
            try:
                url = f"{base_url}/yacysearch.json"
                params = {
                    'query': query,
                    'maximumRecords': max_results,
                    'verify': 'false'
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = []
                    
                    # YaCy has different response formats
                    items = []
                    if isinstance(data, dict):
                        if 'channels' in data and data['channels']:
                            items = data['channels'][0].get('items', [])
                        elif 'items' in data:
                            items = data.get('items', [])
                    
                    for item in items[:max_results]:
                        results.append({
                            'title': item.get('title', item.get('link', '')),
                            'url': item.get('link', item.get('url', '')),
                            'snippet': item.get('description', ''),
                            'source': 'YaCy'
                        })
                    
                    if results:
                        return results
            except Exception:
                continue
        
        return []
    
    def search_all_engines(self, query: str, max_per_engine: int = 5) -> List[Dict]:
        """Search all engines concurrently with fallback"""
        all_results = []
        
        # Use ThreadPoolExecutor for concurrent searches
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all search tasks
            future_to_engine = {
                executor.submit(self.search_searxng, query, max_per_engine): 'SearXNG',
                executor.submit(self.search_wikipedia, query, 3): 'Wikipedia',
                executor.submit(self.search_yacy, query, 3): 'YaCy'
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_engine, timeout=15):
                engine_name = future_to_engine[future]
                try:
                    results = future.result()
                    if results:
                        all_results.extend(results)
                        print(f"✓ {engine_name}: {len(results)} results")
                    else:
                        print(f"✗ {engine_name}: No results")
                except Exception as e:
                    print(f"✗ {engine_name}: Error - {str(e)}")
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def smart_search(self, query: str) -> str:
        """Intelligent search with AI summary"""
        try:
            print(f"🔍 Searching across multiple engines for: {query}")
            results = self.search_all_engines(query, 5)
            
            if not results:
                return f"🔍 No results found for '{query}' across all search engines."
            
            # Format results
            search_text = f"Search Results for '{query}' ({len(results)} found)\n\n"
            
            for i, result in enumerate(results[:10], 1):
                title = result['title']
                snippet = result['snippet'][:150] + "..." if len(result['snippet']) > 150 else result['snippet']
                url = result['url']
                source = result['source']
                
                search_text += f"**{i}. {title}** [{source}]\n"
                search_text += f"📄 {snippet}\n"
                search_text += f"🔗 {url}\n\n"
            
            # Add AI summary if available
            try:
                from brain.ollama_interface import OllamaInterface
                ollama = OllamaInterface(model="qwen2.5:3b")
                
                # Create summary from top results
                top_results = results[:3]
                context = "\n".join([f"- {r['title']}: {r['snippet']}" for r in top_results])
                
                summary = ollama.generate(
                    "You are a search result analyzer. Provide a brief summary of the key information.",
                    f"Summarize the key information about '{query}' from these search results:\n\n{context}",
                    temperature=0.3
                )
                
                search_text += f"🤖 **AI Summary:**\n{summary}\n\n"
            except Exception:
                pass
            
            return search_text
            
        except Exception as e:
            return f"🔍 Search failed: {str(e)}"

# Global instance
multi_search = MultiEngineSearch()

def search_web_multi_engine(query: str) -> str:
    """Main search function using multi-engine system"""
    return multi_search.smart_search(query)