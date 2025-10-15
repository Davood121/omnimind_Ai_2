import os
import requests
from typing import List, Dict

BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"


def search_web(query: str, count: int = 5) -> List[Dict[str, str]]:
    """
    Use Brave Search API to fetch top results. Requires BRAVE_API_KEY in env.
    Returns a list of dicts: { 'title': str, 'url': str }.
    """
    api_key = os.environ.get("BRAVE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("BRAVE_API_KEY environment variable not set.")

    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }
    params = {
        "q": query,
        "count": max(1, min(count, 20)),
        "source": "web",
        "safesearch": "moderate",
    }

    r = requests.get(BRAVE_API_URL, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    results: List[Dict[str, str]] = []
    for item in data.get("web", {}).get("results", [])[:count]:
        title = item.get("title", "(no title)")
        url = item.get("url", "")
        if url:
            results.append({"title": title, "url": url})
    return results
