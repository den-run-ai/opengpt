# OpenHands Local Setup

## Architecture Overview

There are **two ways** to run OpenHands:

| Mode | Agent Runs In | Sandbox/Workspace | Use Case |
|------|---------------|-------------------|----------|
| **SDK (Recommended)** | Local Python | Local directory OR Docker | Development, scripting, custom agents |
| **Docker CLI** | Docker container | Docker container | Simple one-command setup, GUI mode |

**This setup uses the SDK approach** - agent logic runs locally in Python, and you can optionally use Docker only for sandboxed code execution.

## References

- [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk)
- [SDK Documentation](https://docs.openhands.dev/sdk/getting-started)
- [SDK Architecture](https://docs.openhands.dev/sdk/arch/overview)

## Prerequisites

- **Python 3.12+** installed
- **uv** package manager (v0.8.13+) - [installation guide](https://github.com/astral-sh/uv)
- **Docker** (optional) - only needed if you want sandboxed workspaces

## Installation

### Step 1: Install with uv (Recommended)

This project uses `pyproject.toml` for dependency management with uv:

```bash
# Clone this repo (or create your own project)
cd openhands-eval

# Install all dependencies including OpenHands SDK
uv sync
```

This installs:
- `openhands-sdk` and `openhands-tools` from GitHub
- `litellm` for LLM routing
- `python-dotenv` for environment management

**Note:** On macOS, you may need Xcode Command Line Tools:
```bash
xcode-select --install
```

### Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
# .env file - Qwen3 Coder via OpenRouter (default)
# LiteLLM format: openrouter/<model-name>
OPENROUTER_API_KEY=your-openrouter-api-key
LLM_MODEL=openrouter/qwen/qwen3-coder
```

Get your API key from [OpenRouter](https://openrouter.ai/keys).

**Alternative providers:**

```bash
# Option 1: OpenHands Cloud (verified models)
export LLM_API_KEY="your-openhands-api-key"
export LLM_MODEL="openhands/claude-sonnet-4-5-20250929"

# Option 2: Direct provider (Anthropic, OpenAI, etc.)
export LLM_API_KEY="your-anthropic-api-key"
export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"
```

## Testing the API Connection

Before running the full agent, verify your OpenRouter API key works:

```bash
python test_openrouter.py
```

Expected output:
```
📡 Testing OpenRouter API via LiteLLM with model: openrouter/qwen/qwen3-coder
✅ Response: Hello from Qwen3 Coder!
📊 Model used: qwen/qwen3-coder
🔢 Tokens: 24 in, 8 out
```

## Usage

### Hello World Example

Create `hello_agent.py`:

```python
import os
from dotenv import load_dotenv

from openhands.sdk import LLM, Agent, Conversation, Tool
from openhands.tools.file_editor import FileEditorTool
from openhands.tools.task_tracker import TaskTrackerTool
from openhands.tools.terminal import TerminalTool

# Load environment variables from .env file
load_dotenv()

# Configure LLM - Qwen3 Coder via OpenRouter (LiteLLM format)
llm = LLM(
    model=os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_output_tokens=16384,  # Prevent context window overflow
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

conversation.send_message("Write 3 facts about the current project into FACTS.txt.")
conversation.run()
print("All done!")
```

Run it:

```bash
uv run python hello_agent.py
```

### Available Tools

| Tool | Purpose |
|------|---------|
| `TerminalTool` | Execute bash commands |
| `FileEditorTool` | Read, write, edit files |
| `TaskTrackerTool` | Track task progress |

### Shared Module

The `openhands_agent.py` module provides reusable functions for running agents:

```python
from openhands_agent import run_gpt_oss_agent, run_qwen_agent, run_agent

# Run GPT-OSS agent (cost-effective)
run_gpt_oss_agent("Create a hello.py file")

# Run Qwen agent (high quality)
run_qwen_agent("List files and summarize them")

# Or use the generic function with model selection
run_agent("gpt-oss", "Your task here", workspace="/path/to/workspace")
run_agent("qwen", "Your task here", verbose=False)
```

This enables code reuse between different agent scripts and simplifies testing.

### Workspace Options

**Local workspace (default):**
```python
conversation = Conversation(agent=agent, workspace=os.getcwd())
```
Agent operates directly on your filesystem.

**Docker-sandboxed workspace:**
```python
from openhands.workspace import DockerWorkspace

workspace = DockerWorkspace()
conversation = Conversation(agent=agent, workspace=workspace)
```
Agent operates in an isolated Docker container - safer for untrusted code execution.

## Configuration Options

### LiteLLM Integration

OpenHands uses [LiteLLM](https://docs.litellm.ai/) for unified LLM routing. This allows seamless switching between providers using a consistent model format.

**Key Documentation:**
- [OpenHands OpenRouter Configuration](https://docs.openhands.dev/openhands/usage/llms/openrouter)
- [LiteLLM OpenRouter Provider](https://docs.litellm.ai/docs/providers/openrouter)

### LLM Providers

| Provider | Model Format (LiteLLM) | API Key Env Var |
|----------|------------------------|-----------------|
| **OpenRouter (Default)** | `openrouter/qwen/qwen3-coder` | `OPENROUTER_API_KEY` |
| OpenRouter (gpt-oss-120b) | `openrouter/openai/gpt-oss-120b` | `OPENROUTER_API_KEY` |
| OpenHands Cloud | `openhands/claude-sonnet-4-5-20250929` | `LLM_API_KEY` |
| Anthropic | `anthropic/claude-sonnet-4-5-20250929` | `ANTHROPIC_API_KEY` |
| OpenAI | `openai/gpt-4o` | `OPENAI_API_KEY` |

### Qwen3 Coder 480B via OpenRouter (Default)

```python
from dotenv import load_dotenv
load_dotenv()

# LiteLLM format: openrouter/<model-name>
# LiteLLM handles routing automatically - no need for base_url
llm = LLM(
    model=os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder"),
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_output_tokens=16384,  # Prevent context window overflow
)
```

**Important:** Set `max_output_tokens` to prevent exceeding the model's context window (262K tokens). Without this, the default may request too many output tokens.

**Model Details:**
- **Model ID**: `qwen/qwen3-coder` (via [OpenRouter](https://openrouter.ai/qwen/qwen3-coder))
- **Parameters**: 480B total, 35B activated (MoE architecture)
- **Context Length**: 262,144 tokens
- **Pricing**: $0.22/M input tokens, $0.95/M output tokens
- **Recommended Settings**: `temperature=0.7`, `top_p=0.8`, `max_tokens=65536`

## Model Evaluations

### OpenAI gpt-oss-120b via OpenRouter

- **Model ID**: `openrouter/openai/gpt-oss-120b` (via [OpenRouter](https://openrouter.ai/openai/gpt-oss-120b))
- **Parameters**: 117B total, 5.1B activated (MoE architecture)
- **Context Length**: 131,072 tokens
- **Pricing**: $0.039/M input tokens, $0.19/M output tokens
- **Evaluated**: 2025-12-30

**Test Task**: "List the files in the current directory and write a summary to SUMMARY.txt"

**Result**: ✅ **PASSED**

The agent completed the task in 2 actions:
1. Used file_editor view to list directory contents
2. Created SUMMARY.txt with a well-formatted summary including file descriptions

**Token Usage**: ~15K input, ~800 output, ~290 reasoning tokens. Cost: ~$0.002

## Examples

The SDK includes 24+ examples:

```bash
# Clone the SDK repo for examples
git clone https://github.com/OpenHands/software-agent-sdk.git
cd software-agent-sdk

# Run examples
uv run python examples/01_standalone_sdk/01_hello_world.py
uv run python examples/01_standalone_sdk/02_custom_tools.py
uv run python examples/01_standalone_sdk/03_activate_microagent.py

# See all examples
ls examples/
```

## Comparison: SDK vs Docker CLI

### SDK Approach (This Setup) ✅

```bash
uv sync
export LLM_API_KEY="your-key"
uv run python my_agent.py
```

**Pros:**
- Agent runs locally (faster, easier to debug)
- Full Python control and customization
- Can use local workspace (no Docker needed)
- Scriptable and automatable

### Docker CLI Approach (Old Setup)

```bash
uv tool install openhands
openhands serve
```

**Pros:**
- One command setup
- GUI at localhost:3000
- Everything sandboxed

**Cons:**
- Agent runs in Docker (overhead)
- Less customizable
- Harder to debug

---

## Migration Notes

If you previously used `uv tool install openhands` + `openhands serve`:

1. That installed a CLI wrapper that launches Docker containers
2. The SDK approach runs the agent natively in Python
3. You can uninstall the old tool: `uv tool uninstall openhands`
4. Keep Docker if you want sandboxed workspaces, otherwise it's optional

---

## Project Structure

```
openhands-eval/
├── .env                  # API keys (not in git)
├── .venv/                # Virtual environment (created by uv sync)
├── pyproject.toml        # Dependencies and project config
├── uv.lock               # Locked dependency versions
├── openhands_agent.py    # Shared agent module (common functionality)
├── gpt_oss_agent.py      # GPT-OSS-120B agent script
├── hello_agent.py        # Qwen3 Coder agent script
├── test_agents.py        # Pytest tests for tool calling validation
├── test_openrouter.py    # API connection test
└── setup.md              # This documentation
```

## Testing

The project includes pytest tests to validate tool calling works correctly for both GPT-OSS and Qwen models.

### Run Tests

```bash
# Run all tests
uv run pytest test_agents.py -v

# Run only unit tests (fast, no API calls)
uv run pytest test_agents.py -v -m "not integration"

# Run only GPT-OSS integration tests
uv run pytest test_agents.py -v -k gpt_oss -m integration

# Run only Qwen integration tests
uv run pytest test_agents.py -v -k qwen -m integration
```

### Test Coverage

| Test Class | Description |
|------------|-------------|
| `TestModelConfiguration` | Validates model configs are defined correctly |
| `TestAgentCreation` | Verifies agents are created with proper tools |
| `TestGptOssToolCalling` | Integration tests for GPT-OSS-120B tool calling |
| `TestQwenToolCalling` | Integration tests for Qwen3 Coder tool calling |
| `TestBothModels` | Parametrized tests running both models |

Integration tests require a valid `OPENROUTER_API_KEY` and will make actual API calls.

## Quick Reference

```bash
# Install dependencies with uv
uv sync

# Create .env file with OpenRouter API key
echo 'OPENROUTER_API_KEY=your-openrouter-key' > .env
echo 'LLM_MODEL=openrouter/qwen/qwen3-coder' >> .env  # LiteLLM format

# Test API connection
uv run python test_openrouter.py

# Run tests
uv run pytest test_agents.py -v

# Run agent
uv run python hello_agent.py
```

## Resources

- [SDK Documentation](https://docs.openhands.dev/sdk)
- [Getting Started Guide](https://docs.openhands.dev/sdk/getting-started)
- [Architecture Overview](https://docs.openhands.dev/sdk/arch/overview)
- [GitHub Repository](https://github.com/OpenHands/software-agent-sdk)
- [Slack Community](https://openhands.dev/joinslack)
