# opengpt

OpenHands GPS-OSS OpenRouter setup.

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set your OpenRouter API key:
   ```bash
   export OPENROUTER_API_KEY="your-key-here"
   ```

3. Run an agent:
   ```bash
   # Qwen3 Coder (default)
   uv run python hello_agent.py
   
   # GPT-OSS-120B (cost-effective)
   uv run python gpt_oss_agent.py
   ```

## Models

| Script | Model | Cost |
|--------|-------|------|
| `hello_agent.py` | Qwen3 Coder 480B | $0.22/M in, $0.95/M out |
| `gpt_oss_agent.py` | GPT-OSS-120B | $0.039/M in, $0.19/M out |

## License

MIT

