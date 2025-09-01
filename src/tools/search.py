import asyncio
from concurrent.futures import ThreadPoolExecutor
from tavily import TavilyClient
from src.config import TAVILY_API_KEY


def tavily_search(query: str) -> list[dict]:
    """
    A tool to search the web for a given query using the Tavily API.
    Returns a list of dictionaries, each containing the 'url' and 'content'.
    """
    print(f"🔎 Searching for: '{query}'")
    client = TavilyClient(TAVILY_API_KEY)
    try:
        result = client.search(query=query, num_results=3, include_raw_content=True)
        return [{"url": res.get("url"), "content": res.get("content", "")} for res in result.get("results", [])]
    except Exception as e:
        print(f"Error searching for '{query}': {e}")
        return []


async def parallel_search(sub_questions: list[str]):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        futures = [loop.run_in_executor(executor, tavily_search, q) for q in sub_questions]
        search_results_list = await asyncio.gather(*futures)
    
    all_sources = [item for sublist in search_results_list for item in sublist]
    source_urls: list[str] = [source['url'] for source in all_sources]
    # Format content for contradiction detection, including the source URL
    content_for_analysis = "\n\n---\n\n".join([f"Source: {source['url']}\n\nContent: {source['content']}" for source in all_sources])
    print("✅ All data gathering complete.\n")
    return (source_urls, content_for_analysis)