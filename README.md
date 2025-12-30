# openhands-eval

OpenHands agent evaluation with GPT-OSS and Qwen models via OpenRouter.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a `.env` file with your OpenRouter API key:
   ```bash
   echo 'OPENROUTER_API_KEY=your-key-here' > .env
   ```

3. Run an agent:
   ```bash
   # Qwen3 Coder (default, high quality)
   uv run python hello_agent.py
   
   # GPT-OSS-120B (cost-effective)
   uv run python gpt_oss_agent.py
   ```

## Testing

Run pytest to validate tool calling works for both models:

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

## Models

| Script | Model | Cost |
|--------|-------|------|
| `hello_agent.py` | Qwen3 Coder 480B | $0.22/M in, $0.95/M out |
| `gpt_oss_agent.py` | GPT-OSS-120B | $0.039/M in, $0.19/M out |

## Project Structure

```
openhands-eval/
├── openhands_agent.py    # Shared agent module (common functionality)
├── gpt_oss_agent.py      # GPT-OSS-120B agent script
├── hello_agent.py        # Qwen3 Coder agent script
├── test_agents.py        # Pytest tests for tool calling validation
├── test_openrouter.py    # API connection test
├── pyproject.toml        # Dependencies
└── .env                  # API keys (not in git)
```

## Shared Module Usage

The `openhands_agent.py` module provides reusable functions:

```python
from openhands_agent import run_gpt_oss_agent, run_qwen_agent

# Run GPT-OSS agent
run_gpt_oss_agent("Create a hello.py file with a greeting function")

# Run Qwen agent
run_qwen_agent("List files and summarize them")

# Or use the generic function with model selection
from openhands_agent import run_agent
run_agent("gpt-oss", "Your task here")
run_agent("qwen", "Your task here")
```

## License

MIT
