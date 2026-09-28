from contextlib import AsyncExitStack
from typing import Optional, List
import anyio
from mcp import ClientSession, StdioServerParameters, stdio_client
from mcp.types import CallToolResult, Tool

server = StdioServerParameters(command="uv", args=["run", "server.py"])


class MCPClient:
    def __init__(
        self, command: str, args: List[str], env: Optional[dict] = None
    ) -> None:
        self._command = command
        self._args = args
        self._env = env
        self._session: Optional[ClientSession] = None
        self._exit_stack: AsyncExitStack = AsyncExitStack()

    async def connect(self):
        server_params = StdioServerParameters(
            command=self._command, args=self._args, env=self._env
        )

        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        _stdio, _write = stdio_transport
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(_stdio, _write)
        )
        await self._session.initialize()

    def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError
        return self._session

    async def list_tools(self) -> List[Tool]:
        results = await self.session().list_tools()
        return results.tools

    async def call_tool(
        self, tool_name: str, tool_input: dict
    ) -> CallToolResult | None:
        return await self.session().call_tool(tool_name, tool_input)

    async def cleanup(self):
        await self._exit_stack.aclose()
        self._session = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self):
        await self.cleanup()


async def main() -> None:
    async with MCPClient(server) as client:
        result = await client.list_tools()
        print([tool.name for tool in result.tools])


if __name__ == "__main__":
    anyio.run(main)
