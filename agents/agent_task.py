from typing import Type
from pydantic import BaseModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent

def agent_task_classification(ollama_model_name: str, identified_command: Type[BaseModel]) -> Agent:
    """
    Define PydanticAI Agent for task classification
    """
    ollama_provider = OpenAIProvider(
        base_url="http://127.0.0.1:11434/v1",
        api_key="ollama_dummy_key"
    )

    ollama_model = OpenAIChatModel(
        model_name=ollama_model_name,
        provider=ollama_provider,
    )

    agent = Agent(
        ollama_model,
        output_type=identified_command,
        system_prompt="Use the following schema to decide which command to run.",
    )
    return Agent