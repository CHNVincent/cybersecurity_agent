import openai
from typing import List, Dict, Any, Optional
from .base import BaseLLM


class OpenAICompatibleLLM(BaseLLM):
    """
    OpenAI Compatible LLM implementation that supports other providers with OpenAI-compatible APIs
    """

    def __init__(self, api_key: str, model_name: str, base_url: Optional[str] = None):
        super().__init__(api_key, model_name, base_url)
        # Set up OpenAI client with potentially custom base URL
        if base_url:
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = openai.OpenAI(api_key=api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Perform a chat completion with the OpenAI-compatible LLM
        """
        try:
            # Prepare the call parameters
            params = {
                "model": self.model_name,
                "messages": messages,
            }

            # Add tools if provided
            if tools:
                params["tools"] = tools

            # Make the API call
            response = self.client.chat.completions.create(**params)

            # Convert response to dict format
            return {
                "choices": [
                    {
                        "message": {
                            "role": choice.message.role,
                            "content": choice.message.content,
                        },
                        "finish_reason": choice.finish_reason,
                    }
                    for choice in response.choices
                ],
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens
                    if response.usage
                    else 0,
                    "completion_tokens": response.usage.completion_tokens
                    if response.usage
                    else 0,
                    "total_tokens": response.usage.total_tokens
                    if response.usage
                    else 0,
                },
            }
        except Exception as e:
            print(f"Error calling OpenAI Compatible API: {str(e)}")
            # Return a mock response for testing purposes
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"[API Error: {str(e)}]",
                        },
                        "finish_reason": "error",
                    }
                ],
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
