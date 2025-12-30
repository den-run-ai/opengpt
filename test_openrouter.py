#!/usr/bin/env python3
"""
Test OpenRouter API connection with Qwen3 Coder model.

Uses LiteLLM for OpenRouter routing (same as OpenHands internally).
See: https://docs.litellm.ai/docs/providers/openrouter
"""

import os
from dotenv import load_dotenv
from litellm import completion

# Load environment variables from .env file
load_dotenv()

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    # LiteLLM format: openrouter/<model-name>
    model = os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder")
    
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. "
            "Please set it in your .env file."
        )
    
    # Ensure LiteLLM picks up the API key
    os.environ["OPENROUTER_API_KEY"] = api_key
    
    print(f"📡 Testing OpenRouter API via LiteLLM with model: {model}")
    
    # LiteLLM handles OpenRouter routing automatically
    response = completion(
        model=model,
        messages=[
            {"role": "user", "content": "Say 'Hello from Qwen3 Coder!' in exactly 5 words."}
        ],
        max_tokens=50,
    )
    
    reply = response.choices[0].message.content
    print(f"✅ Response: {reply}")
    print(f"📊 Model used: {response.model}")
    print(f"🔢 Tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")


if __name__ == "__main__":
    main()

