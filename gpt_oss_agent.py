#!/usr/bin/env python3
"""
OpenHands SDK - GPT-OSS-120B Agent via OpenRouter

OpenAI's open-source MoE model (117B total, 5.1B activated).
Very cost-effective: $0.039/M input, $0.19/M output tokens.

Usage:
    uv run python gpt_oss_agent.py

Model Info:
    - Model: openrouter/openai/gpt-oss-120b
    - Context: 131,072 tokens
    - Architecture: MoE (117B params, 5.1B activated)
"""

import os

from dotenv import load_dotenv

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

load_dotenv()


def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. "
            "Please set it in your .env file or environment."
        )
    
    # GPT-OSS-120B via OpenRouter
    model = "openrouter/openai/gpt-oss-120b"
    
    llm = LLM(
        model=model,
        api_key=api_key,
        max_output_tokens=8192,
    )

    agent = Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
    )

    cwd = os.getcwd()
    conversation = Conversation(agent=agent, workspace=cwd)

    task = "List the files in the current directory and write a summary to SUMMARY.txt"
    print(f"🚀 Sending task to agent: {task}")
    print(f"📡 Using model: {model}")
    
    conversation.send_message(task)
    conversation.run()
    
    print("✅ All done!")


if __name__ == "__main__":
    main()

