import requests
from typing import List, Dict, Any, Optional
from .base import BaseLLM


class AliBailianLLM(BaseLLM):
    """
    AliBailian LLM implementation for the cybersecurity agent
    Uses DashScope compatible mode API
    """

    def __init__(self, api_key: str, model_name: str, base_url: Optional[str] = None):
        super().__init__(api_key, model_name, base_url)
        self.base_url = (
            base_url
            if base_url is not None
            else "https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Perform a chat completion with the AliBailian LLM
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {"model": self.model_name, "messages": messages}

        # Add tools if provided
        if tools:
            payload["tools"] = tools

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions", headers=headers, json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling AliBailian API: {str(e)}")
            # Return a mock response for testing purposes
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"[API Error: {str(e)}]",
                        }
                    }
                ],
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
