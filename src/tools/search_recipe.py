from src.tools.searching import search
from src.telemetry.logger import logger

def search_recipes(query: str) -> str:
    """
    Tool cho agent: search công thức món ăn
    """
    # tối ưu query cho domain nấu ăn"

    result = search("Finding some recipes relevant to " + query)
    print("Search successful, logging result...")
    # logger.log("TOOL_CALL", {"tool": "search_recipes", "query": query, "result": result})
    return f"Recipe search results for '{query}':\n\n{result}"