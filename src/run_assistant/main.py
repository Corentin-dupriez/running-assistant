from contextlib import AsyncExitStack
import os
import sys
import asyncio
from anthropic import Anthropic
from mcp.client import Client
from mcp import StdioServerParameters
from dotenv import load_dotenv
from run_assistant.core.claude import Claude
from run_assistant.core.cli_chat import CliChat
from run_assistant.core.cli import CliApp
from run_assistant.mcp_helpers.client import MCPClient

load_dotenv()

claude_model = os.getenv("CLAUDE_MODEL", "")
authropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


async def main() -> None:
    claude_service = Claude(model=claude_model)
    server_scripts = sys.argv[1:]
    clients = {}

    commands, args = ("uv", ["run", "mcp/mcp_server.py"])

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command="uv", args=["run", "mcp_helpers/server.py"])
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(
                    StdioServerParameters(command="uv", args=["run", "server.py"])
                )
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client, clients=clients, claude_service=claude_service
        )
        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
