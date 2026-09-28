from anthropic import Anthropic
from anthropic.types import Message
from typing import Any


class Claude:
    def __init__(self, model: str) -> None:
        self.client = Anthropic()
        self.model = model

    def add_user_message(self, messages: list, message) -> None:
        user_message = {
            "role": "user",
            "content": message.content if isinstance(message, Message) else message,
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message) -> None:
        assistant_message = {
            "role": "assistant",
            "content": message.content if isinstance(message, Message) else message,
        }
        messages.append(assistant_message)

    def text_from_message(self, message: Message) -> str:
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )

    def chat(
        self,
        messages,
        system=None,
        temperature: float = 1.0,
        stop_sequences: list[Any] = [],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            # "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        message = self.client.messages.create(**params)

        return message
