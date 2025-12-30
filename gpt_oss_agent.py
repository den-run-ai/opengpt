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

from openhands_agent import run_gpt_oss_agent


def main():
    task = "List the files in the current directory and write a summary to SUMMARY.txt"
    run_gpt_oss_agent(task)


if __name__ == "__main__":
    main()
