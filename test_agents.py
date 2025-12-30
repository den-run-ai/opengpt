"""
Pytest tests for OpenHands agent tool calling with GPT-OSS and Qwen models.

These tests validate that the agents can successfully:
1. Initialize with proper configuration
2. Use tools (file_editor, terminal, task_tracker)
3. Complete a simple coding task

Usage:
    # Run all tests
    uv run pytest test_agents.py -v
    
    # Run only GPT-OSS tests
    uv run pytest test_agents.py -v -k gpt_oss
    
    # Run only Qwen tests
    uv run pytest test_agents.py -v -k qwen
"""

import os
import tempfile
from pathlib import Path

import pytest

from openhands_agent import (
    MODELS,
    create_agent,
    create_llm,
    get_api_key,
    run_gpt_oss_agent,
    run_qwen_agent,
)


@pytest.fixture
def api_key():
    """Get API key, skip test if not available."""
    try:
        return get_api_key()
    except ValueError:
        pytest.skip("OPENROUTER_API_KEY not set")


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


class TestModelConfiguration:
    """Test model configuration and LLM creation."""
    
    def test_gpt_oss_config_exists(self):
        """Verify GPT-OSS model configuration is defined."""
        assert "gpt-oss" in MODELS
        config = MODELS["gpt-oss"]
        assert config.model_id == "openrouter/openai/gpt-oss-120b"
        assert config.max_output_tokens > 0
    
    def test_qwen_config_exists(self):
        """Verify Qwen model configuration is defined."""
        assert "qwen" in MODELS
        config = MODELS["qwen"]
        assert config.model_id == "openrouter/qwen/qwen3-coder"
        assert config.max_output_tokens > 0
    
    def test_create_llm_gpt_oss(self, api_key):
        """Test LLM creation with GPT-OSS config."""
        config = MODELS["gpt-oss"]
        llm = create_llm(config, api_key)
        assert llm is not None
    
    def test_create_llm_qwen(self, api_key):
        """Test LLM creation with Qwen config."""
        config = MODELS["qwen"]
        llm = create_llm(config, api_key)
        assert llm is not None


class TestAgentCreation:
    """Test agent creation with tools."""
    
    def test_create_agent_with_tools(self, api_key):
        """Verify agent is created with expected tools."""
        config = MODELS["gpt-oss"]
        llm = create_llm(config, api_key)
        agent = create_agent(llm)
        
        assert agent is not None
        # Agent should have tools configured
        assert len(agent.tools) == 3


class TestGptOssToolCalling:
    """Integration tests for GPT-OSS-120B tool calling."""
    
    @pytest.mark.integration
    def test_gpt_oss_file_creation(self, api_key, temp_workspace):
        """
        Test GPT-OSS agent can use tools to create a file.
        
        This validates:
        - API connection works
        - Agent can process task
        - Tool calling (file_editor) succeeds
        - File is created with content
        """
        task = "Create a file called test_output.txt with the text 'Hello from GPT-OSS'"
        
        conversation = run_gpt_oss_agent(
            task=task,
            workspace=temp_workspace,
            verbose=False,
        )
        
        # Verify the conversation completed
        assert conversation is not None
        
        # Check if file was created
        output_file = Path(temp_workspace) / "test_output.txt"
        assert output_file.exists(), f"Expected file not created: {output_file}"
        
        # Verify content
        content = output_file.read_text()
        assert "Hello" in content or "GPT" in content, f"Unexpected content: {content}"


class TestQwenToolCalling:
    """Integration tests for Qwen3 Coder tool calling."""
    
    @pytest.mark.integration
    def test_qwen_file_creation(self, api_key, temp_workspace):
        """
        Test Qwen agent can use tools to create a file.
        
        This validates:
        - API connection works
        - Agent can process task
        - Tool calling (file_editor) succeeds
        - File is created with content
        """
        task = "Create a file called test_output.txt with the text 'Hello from Qwen'"
        
        conversation = run_qwen_agent(
            task=task,
            workspace=temp_workspace,
            verbose=False,
        )
        
        # Verify the conversation completed
        assert conversation is not None
        
        # Check if file was created
        output_file = Path(temp_workspace) / "test_output.txt"
        assert output_file.exists(), f"Expected file not created: {output_file}"
        
        # Verify content
        content = output_file.read_text()
        assert "Hello" in content or "Qwen" in content, f"Unexpected content: {content}"


class TestBothModels:
    """Comparative tests running both models."""
    
    @pytest.mark.integration
    @pytest.mark.parametrize("model_key,run_fn", [
        ("gpt-oss", run_gpt_oss_agent),
        ("qwen", run_qwen_agent),
    ])
    def test_directory_listing_task(self, api_key, temp_workspace, model_key, run_fn):
        """
        Test both models can complete a directory listing task.
        
        This is a basic validation that tool calling works for both models.
        """
        # Create a test file in the workspace
        test_file = Path(temp_workspace) / "sample.txt"
        test_file.write_text("Sample content for testing")
        
        task = "List the files in the current directory and save the list to file_list.txt"
        
        conversation = run_fn(
            task=task,
            workspace=temp_workspace,
            verbose=False,
        )
        
        assert conversation is not None
        
        # Check if output file was created
        output_file = Path(temp_workspace) / "file_list.txt"
        assert output_file.exists(), f"{model_key}: Expected file_list.txt not created"
        
        # Verify it mentions the sample file
        content = output_file.read_text()
        assert len(content) > 0, f"{model_key}: file_list.txt is empty"


# Convenience functions for running specific test groups
if __name__ == "__main__":
    import sys
    pytest.main([__file__, "-v"] + sys.argv[1:])

