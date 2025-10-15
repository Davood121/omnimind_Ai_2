import concurrent.futures
from typing import List, Dict
from urllib.parse import urlparse

from .search_engines import searxng_search, wikipedia_search, yacy_search


def _host(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return url


def multi_search(query: str, count_per_engine: int = 5, timeout: int = 15) -> List[Dict[str, str]]:
    """
    Run SearXNG, Wikipedia, and YaCy searches concurrently.
    Merge results, de-duplicate by URL host + path, and return a combined list.
    """
    results: List[Dict[str, str]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(fn, query, count_per_engine): name
            for fn, name in [
                (searxng_search, 'searxng'),
                (wikipedia_search, 'wikipedia'),
                (yacy_search, 'yacy'),
            ]
        }
        for fut in concurrent.futures.as_completed(futures, timeout=timeout):
            try:
                part = fut.result()
                results.extend(part)
            except Exception:
                # Ignore failed engines to remain robust
                continue

    # De-duplicate by normalized URL
    seen = set()
    deduped: List[Dict[str, str]] = []
    for r in results:
        url = r.get('url', '')
        key = url.lower().rstrip('/')
        if key and key not in seen:
            seen.add(key)
            deduped.append(r)

    return deduped
