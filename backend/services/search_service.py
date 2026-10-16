import re
from typing import List, Dict, Any, Tuple
from urllib.parse import urlparse
from backend.config import settings
from backend.services.demo_data import DEMO_ARTICLES

def is_valid_url(url: str) -> bool:
    """Validate that the URL has a valid HTTP/HTTPS scheme and netloc."""
    if not url or not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme in ("http", "https") and parsed.netloc and "." in parsed.netloc)
    except Exception:
        return False

def normalize_title(title: str) -> str:
    """Normalize a title for deduplication."""
    return re.sub(r'[^a-zA-Z0-9]', '', title.lower())

def deduplicate_articles(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate articles based on normalized title or exact URL."""
    seen_urls = set()
    seen_titles = set()
    unique_articles = []

    for art in articles:
        url = (art.get("url") or "").strip().rstrip("/")
        title_norm = normalize_title(art.get("title") or "")
        
        if not url or not title_norm:
            continue
        if not is_valid_url(url):
            continue
            
        if url in seen_urls or title_norm in seen_titles:
            continue
            
        seen_urls.add(url)
        seen_titles.add(title_norm)
        unique_articles.append(art)
        
    return unique_articles

class SearchService:
    def __init__(self):
        self.tavily_key = settings.TAVILY_API_KEY
        self.client = None
        if self.tavily_key:
            try:
                from tavily import TavilyClient
                self.client = TavilyClient(api_key=self.tavily_key)
            except Exception as e:
                print(f"Warning: Failed to initialize TavilyClient: {e}")
                self.client = None

    def search(self, query: str, max_results: int = 10) -> Tuple[List[Dict[str, Any]], bool, str]:
        """
        Executes a search query.
        Returns:
            (articles, is_demo_mode, provider_name)
        """
        if self.client and not settings.FORCE_DEMO:
            try:
                response = self.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=max_results,
                    include_domains=[],
                    exclude_domains=[]
                )
                raw_results = response.get("results", [])
                articles = []
                for res in raw_results:
                    url = res.get("url", "")
                    if not is_valid_url(url):
                        continue
                    articles.append({
                        "title": res.get("title", "Untitled Article"),
                        "url": url,
                        "source": urlparse(url).netloc.replace("www.", ""),
                        "snippet": res.get("content", ""),
                        "published_date": res.get("published_date") or "Recent",
                        "score": res.get("score", 0.9),
                        "approved": True
                    })
                deduped = deduplicate_articles(articles)
                if deduped:
                    return deduped, False, "Tavily Live Search API"
            except Exception as e:
                print(f"Error during Tavily search: {e}. Falling back to curated demo data.")

        # Fallback to Curated Demo Intelligence
        filtered = []
        q_tokens = [t.lower() for t in query.split() if len(t) > 3]
        
        for art in DEMO_ARTICLES:
            text = (art["title"] + " " + art["snippet"]).lower()
            relevance = sum(1 for token in q_tokens if token in text) if q_tokens else 1
            filtered.append({
                "title": art["title"],
                "url": art["url"],
                "source": art["source"],
                "snippet": art["snippet"],
                "published_date": art.get("published_date", "Recent"),
                "score": 0.8 + (0.04 * relevance),
                "approved": True
            })
            
        deduped = deduplicate_articles(filtered)
        return deduped[:max_results], True, "Curated AI Agent News Intelligence (Demo Fallback)"

search_service = SearchService()
