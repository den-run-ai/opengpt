#!/usr/bin/env python3
"""
OpenHands SDK - Hello World Agent with Qwen3 Coder via OpenRouter

This runs the agent LOCALLY in Python (not in Docker).
The agent operates on your local workspace directory.

Usage:
    # Create .env file with OPENROUTER_API_KEY
    uv run python hello_agent.py

LiteLLM Integration:
    OpenHands uses LiteLLM for model routing. For OpenRouter models:
    - Model format: openrouter/<provider>/<model-name>
    - API key: OPENROUTER_API_KEY environment variable
    - Docs: https://docs.litellm.ai/docs/providers/openrouter
"""

import os

from dotenv import load_dotenv

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

# Load environment variables from .env file
load_dotenv()


def main():
    # Configure LLM - Qwen3 Coder via OpenRouter using LiteLLM routing
    # LiteLLM format: openrouter/<model-name>
    # See: https://docs.openhands.dev/openhands/usage/llms/openrouter
    model = os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder")
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. "
            "Please set it in your .env file or environment."
        )
    
    # LiteLLM handles OpenRouter routing automatically when using openrouter/ prefix
    # No need to manually set base_url - LiteLLM manages this
    llm = LLM(
        model=model,
        api_key=api_key,
        max_output_tokens=16384,  # Limit output to prevent context window overflow
    )

    # Create agent with tools
    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
    )

    # Use current directory as workspace (local, no Docker)
    cwd = os.getcwd()
    conversation = Conversation(agent=agent, workspace=cwd)

    # Send task to agent
    task = "List the files in the current directory and write a summary to SUMMARY.txt"
    print(f"🚀 Sending task to agent: {task}")
    print(f"📡 Using model: {model} via OpenRouter")
    
    conversation.send_message(task)
    conversation.run()
    
    print("✅ All done!")


if __name__ == "__main__":
    main()
