from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()


class BaseLLM(ABC):
    """
    Abstract base class for LLM implementations
    """

    def __init__(self, api_key: str, model_name: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url if base_url is not None else ""

    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Perform a chat completion with the LLM
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions for function calling
        Returns:
            Dictionary containing the response from the LLM
        """
        pass

    @staticmethod
    def load_model_config(
        config_path: str = "apps/agent/brain/models_config.json",
    ) -> List[Dict[str, Any]]:
        """
        Load model configurations from JSON file
        """
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("models", [])
        else:
            # Return a default configuration if file doesn't exist
            return [
                {
                    "name": "default-model",
                    "provider": "openai",
                    "api_key_env": "OPENAI_API_KEY",
                    "model_name": "gpt-3.5-turbo",
                    "base_url": "https://api.openai.com/v1/",
                    "type": "chat",
                }
            ]

    @classmethod
    def create_llm_instance(cls, config: Dict[str, Any]):
        """
        Factory method to create an LLM instance based on provider
        """
        provider = config.get("provider", "openai")

        # Get the API key
        api_key = os.getenv(config["api_key_env"])
        if not api_key:
            raise ValueError(
                f"API Key environment variable {config['api_key_env']} not set"
            )

        model_name = config["model_name"]
        base_url = config.get("base_url")

        if provider == "ali_bailian":
            from .ali_bailian import AliBailianLLM

            return AliBailianLLM(
                api_key=api_key,
                model_name=model_name,
                base_url=base_url if base_url is not None else "",
            )
        elif provider == "openai":
            from .openai import OpenAICompatibleLLM

            return OpenAICompatibleLLM(
                api_key=api_key,
                model_name=model_name,
                base_url=base_url if base_url is not None else "",
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
