import webbrowser
import subprocess
import shlex
from typing import Optional


def build_search_query(user_query: str) -> str:
    terms = user_query.strip()
    if not terms:
        return "royalty free music"
    soft_filters = "no copyright OR royalty free"
    return f"{terms} {soft_filters}"


def open_youtube_search(query: str) -> Optional[str]:
    """
    Builds a YouTube search URL and opens it in the default browser. Returns the URL.
    We do not autoplay; only open results so the user can choose.
    """
    base = "https://www.youtube.com/results"
    import urllib.parse
    url = f"{base}?search_query={urllib.parse.quote_plus(query)}"
    webbrowser.open(url)
    return url


def best_video_via_ytdlp(query: str) -> Optional[str]:
    """
    Uses yt-dlp in "ytsearch" mode to fetch the first result URL for the query.
    We still do NOT autoplay; we open the URL in a browser.
    """
    try:
        # Using yt-dlp in a lightweight way to get first video URL
        cmd = [
            "yt-dlp",
            "--default-search", "ytsearch",
            "--get-id",
            "--skip-download",
            query,
        ]
        out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
        video_id = out.strip().splitlines()[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        return None
    return None


def play_music(query: str) -> str:
    """
    Public API. Prefer quick, privacy-preserving YouTube search (no autoplay).
    If yt-dlp is available, we also fetch the top result to surface as a direct link.
    """
    q = build_search_query(query)
    url = open_youtube_search(q)
    direct = best_video_via_ytdlp(q)
    if direct:
        return f"Opened YouTube search for: '{q}'. Top result (not auto-playing): {direct}"
    return f"Opened YouTube search for: '{q}'."
