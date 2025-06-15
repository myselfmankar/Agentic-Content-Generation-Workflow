import os
import re

CACHE_DIR = "cache"

def get_safe_filename_from_url(url: str) -> str:
    """
    Creates a safe, valid filename from a URL.
    Example: 'https://.../Chapter_1' -> 'en.wikisource.org_wiki_The_Gates_of_Morning_Book_1_Chapter_1.txt'
    """
    # Remove protocol (http://, https://)
    safe_name = re.sub(r'^https?://', '', url)
    # Replace invalid filename characters with an underscore
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', safe_name)
    # Ensure the filename isn't too long (some OS have limits)
    return safe_name[:200] + ".txt"

def get_cached_content(url):
    """
    Checks if a cached version for the given URL exists and returns its content.
    Returns None if no cache is found.
    """
    filename = get_safe_filename_from_url(url)
    filepath = os.path.join(CACHE_DIR, filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_content_to_cache(url: str, content: str):
    """
    Saves content to a file in the cache directory, named after the URL.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    filename = get_safe_filename_from_url(url)
    filepath = os.path.join(CACHE_DIR, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Error: {e}")