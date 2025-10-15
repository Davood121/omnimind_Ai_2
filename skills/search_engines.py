import os
import requests
from typing import List, Dict
from utils.config import searxng_url, yacy_url

# -----------------------------
# SearXNG (open-source meta search)
# -----------------------------
# Configure via environment variable SEARXNG_URL (e.g., https://searxng.my.domain)


def searxng_search(query: str, count: int = 5) -> List[Dict[str, str]]:
    base = (os.environ.get("SEARXNG_URL") or searxng_url() or "").rstrip("/")
    if not base:
        raise RuntimeError("SEARXNG_URL not set")
    url = f"{base}/search"
    params = {
        "q": query,
        "format": "json",
        "language": "en",
        "safesearch": 1,
        "categories": "general",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    out: List[Dict[str, str]] = []
    for item in data.get("results", [])[:count]:
        title = item.get("title") or item.get("url") or "(no title)"
        href = item.get("url", "")
        snippet = item.get("content", "")
        if href:
            out.append({"title": title, "url": href, "snippet": snippet, "source": "searxng"})
    return out


# -----------------------------
# Wikipedia (MediaWiki API)
# -----------------------------

def wikipedia_search(query: str, count: int = 5) -> List[Dict[str, str]]:
    api = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "format": "json",
        "srlimit": max(1, min(count, 10)),
    }
    r = requests.get(api, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    out: List[Dict[str, str]] = []
    for item in data.get("query", {}).get("search", [])[:count]:
        title = item.get("title", "(no title)")
        page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        snippet = item.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
        out.append({"title": title, "url": page_url, "snippet": snippet, "source": "wikipedia"})
    return out


# -----------------------------
# YaCy (open-source P2P search engine)
# -----------------------------
# Configure via environment variable YACY_URL (e.g., http://localhost:8090)


def yacy_search(query: str, count: int = 5) -> List[Dict[str, str]]:
    base = (os.environ.get("YACY_URL") or yacy_url() or "").rstrip("/")
    if not base:
        raise RuntimeError("YACY_URL not set")
    url = f"{base}/yacysearch.json"
    params = {
        "query": query,
        "maximumRecords": max(1, min(count, 20)),
        "verify": "false",
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    # YaCy JSON format can vary; try common structure
    items = []
    if isinstance(data, dict):
        if "channels" in data and data["channels"]:
            items = data["channels"][0].get("items", [])
        elif "items" in data:
            items = data.get("items", [])
    out: List[Dict[str, str]] = []
    for it in items[:count]:
        title = it.get("title") or it.get("url", "(no title)")
        url_item = it.get("link") or it.get("url") or ""
        snippet = it.get("description", "")
        if url_item:
            out.append({"title": title, "url": url_item, "snippet": snippet, "source": "yacy"})
    return out
