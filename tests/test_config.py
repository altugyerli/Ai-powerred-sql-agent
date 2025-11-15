"""
Tests for configuration modules
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TestSQLAgentConfig:
    """Test SQLAgentConfig initialization"""

    def test_config_initialization(self):
        """Test that config initializes with default values"""
        from sql_agent import SQLAgentConfig

        config = SQLAgentConfig()
        assert config.model_id == "ibm/granite-3-2-8b-instruct"
        assert config.max_tokens == 1024
        assert config.temperature == 0.2
        assert config.top_p == 0.95
        assert config.repetition_penalty == 1.2

    def test_config_from_env(self):
        """Test that config reads from environment variables"""
        os.environ["MAX_TOKENS"] = "512"
        os.environ["TEMPERATURE"] = "0.7"

        from sql_agent import SQLAgentConfig

        config = SQLAgentConfig()
        assert config.max_tokens == 512
        assert config.temperature == 0.7

        # Cleanup
        del os.environ["MAX_TOKENS"]
        del os.environ["TEMPERATURE"]


class TestLLMConfig:
    """Test LLMConfig initialization"""

    def test_llm_config_initialization(self):
        """Test that LLM config initializes with default values"""
        from llm_agent import LLMConfig

        config = LLMConfig()
        assert config.model_id == "ibm/granite-3-2-8b-instruct"
        assert config.max_tokens == 256
        assert config.temperature == 0.5

    def test_llm_config_from_env(self):
        """Test that LLM config reads from environment variables"""
        os.environ["MAX_TOKENS"] = "1024"

        from llm_agent import LLMConfig

        config = LLMConfig()
        assert config.max_tokens == 1024

        # Cleanup
        del os.environ["MAX_TOKENS"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

