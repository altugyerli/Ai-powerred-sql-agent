"""
LLM Agent Configuration Module

This module handles the initialization and configuration of the IBM Watson LLM
used by the SQL Agent. It provides a clean interface for LLM setup.
"""

import os
import warnings

from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM

# Suppress warnings
warnings.filterwarnings("ignore")
load_dotenv()


class LLMConfig:
    """Configuration class for LLM parameters"""

    def __init__(self):
        self.model_id = os.getenv("MODEL_ID", "ibm/granite-3-2-8b-instruct")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "256"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.5"))
        self.top_p = float(os.getenv("TOP_P", "0.95"))
        self.repetition_penalty = float(os.getenv("REPETITION_PENALTY", "1.2"))
        self.ibm_url = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
        self.ibm_project_id = os.getenv("IBM_PROJECT_ID", "skills-network")


def create_llm(config: LLMConfig = None) -> WatsonxLLM:
    """
    Create and return a configured WatsonxLLM instance

    Args:
        config: LLMConfig object with custom parameters

    Returns:
        WatsonxLLM: Configured language model instance
    """
    if config is None:
        config = LLMConfig()

    parameters = {
        GenParams.MAX_NEW_TOKENS: config.max_tokens,
        GenParams.TEMPERATURE: config.temperature,
        GenParams.TOP_P: config.top_p,
        GenParams.REPETITION_PENALTY: config.repetition_penalty,
    }

    credentials = {"url": config.ibm_url}

    model = ModelInference(
        model_id=config.model_id,
        params=parameters,
        credentials=credentials,
        project_id=config.ibm_project_id,
    )

    return WatsonxLLM(model=model)


def test_llm():
    """Test the LLM with a simple query"""
    print("🧪 Testing LLM Configuration...\n")

    try:
        llm = create_llm()
        response = llm.invoke("What is the capital of Ontario?")
        print(f"✅ LLM Test Successful!\n")
        print(f"Response: {response}\n")
        return True
    except Exception as e:
        print(f"❌ LLM Test Failed: {str(e)}\n")
        return False


if __name__ == "__main__":
    test_llm()

