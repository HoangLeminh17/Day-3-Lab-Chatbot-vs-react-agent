#!/usr/bin/env python3
"""
Example script showing voice interaction with the ReAct Agent.
The user can speak their queries instead of typing them.
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
from src.tools.voice_interaction import VoiceInteractionTool
from src.tools.searching import search

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
    speech_language = os.getenv("SPEECH_LANGUAGE", "vi-VN")
    speech_timeout = int(os.getenv("SPEECH_TIMEOUT", "20"))
    phrase_limit_env = os.getenv("SPEECH_PHRASE_TIME_LIMIT")
    speech_phrase_limit = int(phrase_limit_env) if phrase_limit_env and phrase_limit_env.isdigit() else None
    speech_ambient_duration = float(os.getenv("SPEECH_AMBIENT_DURATION", "1.2"))
    speech_pause_threshold = float(os.getenv("SPEECH_PAUSE_THRESHOLD", "1.2"))
    speech_non_speaking_duration = float(os.getenv("SPEECH_NON_SPEAKING_DURATION", "0.7"))
    
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
    
    # Define tools with voice input and search
    tools = [
        {
            "name": "voice_input",
            "description": "Capture voice input from user and convert to text.",
            "fn": lambda: VoiceInteractionTool(
                language=speech_language,
                ambient_duration=speech_ambient_duration,
                pause_threshold=speech_pause_threshold,
                non_speaking_duration=speech_non_speaking_duration,
            ).listen_and_transcribe(timeout=speech_timeout, phrase_time_limit=speech_phrase_limit)
        },
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
    
    print("Voice Interactive ReAct Agent")
    print(f"Speech Language: {speech_language}")
    print("Microphone: default system microphone")
    print(f"Speech Timeout: {speech_timeout}s")
    print(f"Speech Phrase Limit: {speech_phrase_limit if speech_phrase_limit is not None else 'no-limit'}")
    print(f"Ambient Duration: {speech_ambient_duration}s")
    print(f"Pause Threshold: {speech_pause_threshold}s")
    print(f"Non-speaking Duration: {speech_non_speaking_duration}s")
    print("Commands:")
    print("  - Type your question, or")
    print("  - Type 'voice' to interact with voice input, or")
    print("  - Type 'quit' to exit")
    print("-" * 50)

    voice_tool = VoiceInteractionTool(
        language=speech_language,
        ambient_duration=speech_ambient_duration,
        pause_threshold=speech_pause_threshold,
        non_speaking_duration=speech_non_speaking_duration,
    )
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
            
            # If user says 'voice', capture voice input
            if user_input.lower() == 'voice':
                print("\nSwitching to voice mode...")
                user_input = voice_tool.listen_and_transcribe(
                    timeout=speech_timeout,
                    phrase_time_limit=speech_phrase_limit,
                )
                if not user_input:
                    print("No input captured. Try again.")
                    continue
                print(f"You (voice): {user_input}")
            
            print("\nAgent: ", end="", flush=True)
            response = agent.run(user_input)
            print(response)
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()