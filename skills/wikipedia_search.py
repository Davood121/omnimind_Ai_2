"""Wikipedia knowledge base"""
import requests

def search_wikipedia(query):
    """Search Wikipedia and get summary"""
    try:
        # First try search API to find the right page
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'srlimit': 1
        }
        
        search_response = requests.get(search_url, params=search_params, timeout=5)
        if search_response.status_code == 200:
            search_data = search_response.json()
            search_results = search_data.get('query', {}).get('search', [])
            
            if search_results:
                page_title = search_results[0]['title']
                
                # Get page summary
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{page_title.replace(' ', '_')}"
                summary_response = requests.get(summary_url, timeout=5)
                
                if summary_response.status_code == 200:
                    data = summary_response.json()
                    title = data.get('title', '')
                    extract = data.get('extract', '')
                    
                    if extract:
                        return f"📖 {title}:\n\n{extract}"
        
        return f"📖 No Wikipedia information found for '{query}'"
    except Exception as e:
        return f"📖 Wikipedia search unavailable: {str(e)}"
