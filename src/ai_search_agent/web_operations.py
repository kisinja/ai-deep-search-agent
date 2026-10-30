import os
import requests
from typing import List, Optional, Dict, Any
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# ======================
# Tavily (Web Search)
# ======================
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def serp_search(
    query: str, engine: str = "google", max_results: int = 8
) -> Optional[Dict[str, Any]]:
    """
    Replacement for Bright Data SERP search.
    Uses Tavily (much better for AI agents).
    """
    try:
        response = tavily.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=False,
            include_raw_content=False,
        )

        organic = []
        for r in response.get("results", []):
            organic.append(
                {
                    "title": r.get("title"),
                    "link": r.get("url"),
                    "snippet": r.get("content"),
                    "position": r.get("score", 0),
                }
            )

        return {
            "organic": organic,
            "search_parameters": {"q": query, "engine": "tavily"},
        }

    except Exception as e:
        print(f"[serp_search] Error: {e}")
        return None


# ======================
# Reddit Search (Free)
# ======================
def reddit_search_api(
    keyword: str, date: str = "All time", sort_by: str = "Hot", num_of_posts: int = 25
) -> Optional[Dict[str, Any]]:
    """
    Free Reddit search using PullPush API (no key needed).
    """
    try:
        # Map sort_by to PullPush parameters
        sort_map = {
            "Hot": "score",
            "New": "created_utc",
            "Top": "score",
            "Relevance": "score",
        }
        sort_type = sort_map.get(sort_by, "score")

        url = "https://api.pullpush.io/reddit/search/submission/"
        params = {
            "q": keyword,
            "size": min(num_of_posts, 100),
            "sort_type": sort_type,
            "sort": "desc",
        }

        headers = {"User-Agent": "ai-search-agent/1.0"}
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        parsed_posts = []
        for post in data.get("data", []):
            parsed_posts.append(
                {
                    "title": post.get("title"),
                    "url": f"https://www.reddit.com{post.get('permalink', '')}",
                    "score": post.get("score"),
                    "num_comments": post.get("num_comments"),
                    "subreddit": post.get("subreddit"),
                    "created_utc": post.get("created_utc"),
                    "selftext": post.get("selftext", "")[:500],  # truncate long text
                }
            )

        return {"parsed_posts": parsed_posts, "total_found": len(parsed_posts)}

    except Exception as e:
        print(f"[reddit_search_api] Error: {e}")
        return None


# ======================
# Reddit Post Retrieval (Free)
# ======================
def reddit_post_retrieval(
    urls: List[str],
    days_back: int = 10,
    load_all_replies: bool = False,
    comment_limit: str = "",
) -> Optional[List[Dict[str, Any]]]:
    """
    Retrieve full Reddit post + top comments using public JSON endpoint.
    """
    results = []

    for url in urls:
        try:
            # Convert normal Reddit URL to .json
            if not url.endswith(".json"):
                json_url = url.rstrip("/") + ".json"
            else:
                json_url = url

            headers = {"User-Agent": "ai-search-agent/1.0"}
            response = requests.get(json_url, headers=headers, timeout=12)
            response.raise_for_status()
            data = response.json()

            # Post data
            post_data = data[0]["data"]["children"][0]["data"]
            post = {
                "title": post_data.get("title"),
                "selftext": post_data.get("selftext"),
                "score": post_data.get("score"),
                "num_comments": post_data.get("num_comments"),
                "subreddit": post_data.get("subreddit"),
                "url": f"https://www.reddit.com{post_data.get('permalink')}",
                "author": post_data.get("author"),
            }

            # Comments
            comments = []
            if len(data) > 1:
                for child in data[1]["data"]["children"]:
                    if child.get("kind") == "t1":
                        c = child["data"]
                        comments.append(
                            {
                                "author": c.get("author"),
                                "body": c.get("body"),
                                "score": c.get("score"),
                            }
                        )
                        if not load_all_replies and len(comments) >= 15:
                            break

            post["comments"] = comments
            results.append(post)

        except Exception as e:
            print(f"[reddit_post_retrieval] Failed for {url}: {e}")
            continue

    return results if results else None
