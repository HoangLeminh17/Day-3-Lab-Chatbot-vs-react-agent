#!/usr/bin/env python3
"""
Simple script to run the ReAct Agent as a chatbot.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.agent import ReActAgent
from src.core.gemini_provider import GeminiProvider
from src.core.openai_provider import OpenAIProvider
from src.core.local_provider import LocalProvider
from src.tools.cooking_time import estimate_cooking_time


def search_web(query: str) -> str:
    """Lazy import to avoid startup failure when optional search deps are missing."""
    from src.tools.searching import search

    return search(query)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get config
    provider = os.getenv("DEFAULT_PROVIDER", "google")
    model = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
    local_path = os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf")
    
    # Initialize LLM provider
    if provider == "google":
        api_key = os.getenv("GEMINI_API_KEY")
        llm = GeminiProvider(model_name=model, api_key=api_key)
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        llm = OpenAIProvider(model_name=model, api_key=api_key)
    elif provider == "local":
        llm = LocalProvider(model_path=local_path)
    else:
        print(f"Unknown provider: {provider}")
        return
    
    # Define tools (empty for now - add your tools here)
    tools = [
        {
            "name": "estimate_cooking_time",
            "description": "Estimate cooking and prep time for a dish. Use when the user asks how long a dish takes to cook, boil, bake, fry, steam, or stew. Arguments: dish_type, ingredients_count, servings, technique, complexity, marinate_minutes, needs_thawing, needs_preheat.",
            "fn": estimate_cooking_time,
        },
        {
            "name": "search",
            "description": "Search the web for cooking facts, nutrition references, or recipe ideas when specific information is needed. Argument: query.",
            "fn": search_web,
        },
    ]
    
    # Create agent
    agent = ReActAgent(llm=llm, tools=tools, max_steps=5)
    
    print("🤖 ReAct Agent Chatbot")
    print("Type 'quit' to exit.")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        print("Agent: ", end="", flush=True)
        response = agent.run(user_input)
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    main()