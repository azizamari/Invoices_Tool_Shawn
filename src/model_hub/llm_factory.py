from typing import Any, Dict, List, Type

import instructor
from config.settings import get_settings
from openai import OpenAI
from openai import AzureOpenAI
from pydantic import BaseModel, Field
from .utils import model_dict


class LLMFactory:
    def __init__(self, provider: str, config: Dict[str, str]):
        self.provider = provider
        self.settings = get_settings()
        self.api_key = config['AZURE_API_KEY']
        self.url = config['AZURE_URL']
        self.client = self._initialize_client()

    def _initialize_client(self) -> Any:
        client_initializers = {
            'azure': lambda: instructor.from_openai(AzureOpenAI(api_key=self.api_key, base_url=self.url, api_version=self.settings.azure_api_version)),
        }

        initializer = client_initializers.get(self.provider)
        if initializer:
            return initializer()
        raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def create_completion(
        self, response_model: Type[BaseModel], messages: List[Dict[str, str]], **kwargs
    ) -> Any:
        completion_params = {
            "model": model_dict[self.provider],
            "temperature": kwargs.get("temperature", self.settings.temperature),
            "max_retries": kwargs.get("max_retries", self.settings.max_retries),
            "max_tokens": kwargs.get("max_tokens", self.settings.max_tokens),
            "response_model": response_model,
            "messages": messages,
        }
        return self.client.chat.completions.create(**completion_params)