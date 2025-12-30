#!/usr/bin/env python3
"""
OpenHands SDK - Hello World Agent with Qwen3 Coder via OpenRouter

This runs the agent LOCALLY in Python (not in Docker).
The agent operates on your local workspace directory.

Usage:
    uv run python hello_agent.py

LiteLLM Integration:
    OpenHands uses LiteLLM for model routing. For OpenRouter models:
    - Model format: openrouter/<provider>/<model-name>
    - API key: OPENROUTER_API_KEY environment variable
    - Docs: https://docs.litellm.ai/docs/providers/openrouter
"""

from openhands_agent import run_qwen_agent


def main():
    task = "List the files in the current directory and write a summary to SUMMARY.txt"
    run_qwen_agent(task)


if __name__ == "__main__":
    main()
