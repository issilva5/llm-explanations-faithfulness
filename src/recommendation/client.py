from abc import ABC, abstractmethod
from typing import Tuple, List

from openai import OpenAI
from groq import Groq

from openai.types import Completion as OpenAICompletion
from openai.types import Model as OpenAIModel
from groq.types.chat import ChatCompletion as GroqCompletion
from groq.types.model import Model as GroqModel

ModelAPI = OpenAI | Groq
ChatCompletion = OpenAICompletion | GroqCompletion
Model = OpenAIModel | GroqModel

class LLMClient(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.available_models = {}
        self.clients = []
    
    def add_client(self, client: ModelAPI, models: List[Model]) -> None:
        self.clients.append(client)
        client_index = len(self.clients) - 1
        for m in models:
            self.available_models[m.id] = client_index
    
    def add_openai_client(self, api_key: str) -> None:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        self.add_client(client, models)
    
    def add_groq_client(self, api_key: str) -> None:
        client = Groq(api_key=api_key)
        models = client.models.list()
        self.add_client(client, models.data)
    
    def get_client_from_model(self, model: str) -> ModelAPI:

        if model not in self.available_models:
            raise KeyError(f"Model must be one of {self.available_models}")

        return self.clients[self.available_models[model]]
    
    def get_chat_completion(self, prompt: str, model: str, system: dict = None) -> Tuple[str, float]:
        client = self.get_client_from_model(model)
        response: ChatCompletion = client.chat.completions.create(
            messages= ([system] if system else []) + [
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model,
            temperature=0,
            # Streaming is not supported in JSON mode
            stream=False,
            # Enable JSON mode by setting the response format
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content