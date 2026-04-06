import os

from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def search(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"), max_results=5)
    response = tavily_client.search(query)
    res = ""
    for i in range(5):
        res += f"Result {i+1}:\n"
        res += response['results'][i]['content'] + "\n\n"
    return res
