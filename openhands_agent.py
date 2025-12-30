"""
OpenHands Agent - Shared module for running coding agents via OpenRouter.

This module provides a common interface for running OpenHands agents with
different LLM models through OpenRouter's API.

Supported Models:
    - GPT-OSS-120B: openrouter/openai/gpt-oss-120b (cost-effective)
    - Qwen3 Coder: openrouter/qwen/qwen3-coder (default, high quality)
"""

import os
from dataclasses import dataclass
from typing import Callable

from dotenv import load_dotenv

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool


# Model configurations
@dataclass
class ModelConfig:
    """Configuration for an LLM model."""
    name: str
    model_id: str
    max_output_tokens: int
    description: str


# Pre-configured models
MODELS = {
    "gpt-oss": ModelConfig(
        name="GPT-OSS-120B",
        model_id="openrouter/openai/gpt-oss-120b",
        max_output_tokens=8192,
        description="OpenAI's open-source MoE model (117B total, 5.1B activated). Cost-effective: $0.039/M input, $0.19/M output",
    ),
    "qwen": ModelConfig(
        name="Qwen3 Coder",
        model_id="openrouter/qwen/qwen3-coder",
        max_output_tokens=16384,
        description="Qwen3 Coder 480B (35B activated). High quality: $0.22/M input, $0.95/M output",
    ),
}


def get_api_key() -> str:
    """Get OpenRouter API key from environment."""
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. "
            "Please set it in your .env file or environment."
        )
    return api_key


def create_llm(model_config: ModelConfig, api_key: str) -> LLM:
    """Create an LLM instance with the given configuration."""
    return LLM(
        model=model_config.model_id,
        api_key=api_key,
        max_output_tokens=model_config.max_output_tokens,
    )


def create_agent(llm: LLM) -> Agent:
    """Create an agent with standard coding tools."""
    return Agent(
        llm=llm,
        tools=[
            Tool(name=TerminalTool.name),
            Tool(name=FileEditorTool.name),
            Tool(name=TaskTrackerTool.name),
        ],
    )


def run_agent(
    model_key: str,
    task: str,
    workspace: str | None = None,
    verbose: bool = True,
) -> Conversation:
    """
    Run an OpenHands agent with the specified model and task.
    
    Args:
        model_key: Key for the model configuration ("gpt-oss" or "qwen")
        task: The task description to send to the agent
        workspace: Working directory (defaults to current directory)
        verbose: Whether to print progress messages
        
    Returns:
        The completed Conversation object
    """
    if model_key not in MODELS:
        raise ValueError(f"Unknown model: {model_key}. Available: {list(MODELS.keys())}")
    
    model_config = MODELS[model_key]
    api_key = get_api_key()
    
    llm = create_llm(model_config, api_key)
    agent = create_agent(llm)
    
    workspace = workspace or os.getcwd()
    conversation = Conversation(agent=agent, workspace=workspace)
    
    if verbose:
        print(f"🚀 Sending task to agent: {task}")
        print(f"📡 Using model: {model_config.name} ({model_config.model_id})")
    
    conversation.send_message(task)
    conversation.run()
    
    if verbose:
        print("✅ All done!")
    
    return conversation


def run_gpt_oss_agent(task: str, workspace: str | None = None, verbose: bool = True) -> Conversation:
    """Run an agent with GPT-OSS-120B model."""
    return run_agent("gpt-oss", task, workspace, verbose)


def run_qwen_agent(task: str, workspace: str | None = None, verbose: bool = True) -> Conversation:
    """Run an agent with Qwen3 Coder model."""
    return run_agent("qwen", task, workspace, verbose)

