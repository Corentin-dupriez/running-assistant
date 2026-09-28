from typing import List
from mcp import Client
from mcp.types import ListPromptsResult, Prompt
from run_assistant.core.chat import Chat
from run_assistant.core.claude import Claude


class CliChat(Chat):
    def __init__(
        self, doc_client: Client, clients: dict[str, Client], claude_service: Claude
    ) -> None:
        super().__init__(clients=clients, claude_service=claude_service)
        self.doc_client: Client = doc_client

    async def list_prompts(self) -> ListPromptsResult:
        return await self.doc_client.list_prompts()
