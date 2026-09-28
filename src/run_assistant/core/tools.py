import json
from os import error
from typing import List, Literal, Optional
from anthropic.types import Message, ToolResultBlockParam
from mcp import Client, Tool
from mcp_types import CallToolResult, TextContent
from run_assistant.mcp_helpers.client import MCPClient


class ToolManager:
    @classmethod
    async def get_all_tools(cls, clients: dict[str, MCPClient]) -> list[Tool]:
        tools = []
        for client in clients.values():
            tool_models = await client.list_tools()
            tools += [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.input_schema,
                }
                for t in tool_models
            ]
        return tools

    @classmethod
    async def _find_client_with_tool(
        cls, clients: list[Client], tool_name: str
    ) -> Optional[Client]:
        for client in clients:
            tools = await client.list_tools()
            tool = next((t for t in tools if t.name == tool_name), None)
            if tool:
                return client
        return None

    @classmethod
    def _build_tool_result_part(
        cls, tool_use_id: str, text: str, status: Literal["success"] | Literal["error"]
    ) -> ToolResultBlockParam:
        return {
            "tool_use_id": tool_use_id,
            "type": "tool_result",
            "content": text,
            "is_error": status == "error",
        }

    @classmethod
    async def execute_tool_requests(
        cls, clients: dict[str, Client], message: Message
    ) -> List[ToolResultBlockParam]:
        tool_requests = [block for block in message.content if block.type == "tool_use"]
        tool_result_blocks: List[ToolResultBlockParam] = []
        for tool_request in tool_requests:
            tool_use_id = tool_request.id
            tool_name = tool_request.name
            tool_input = tool_request.input

            client = await cls._find_client_with_tool(list(clients.values()), tool_name)

            if not client:
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id, "Could not find that tool", "error"
                )
                tool_result_blocks.append(tool_result_part)
                continue
            try:
                tool_output: CallToolResult | None = await client.call_tool(
                    tool_name, tool_input
                )
                items = []
                if tool_output:
                    items = tool_output.content
                content_list = [
                    item.text for item in items if isinstance(item, TextContent)
                ]
                content_json = json.dumps(content_list)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    content_json,
                    "error" if tool_output and tool_output.is_error else "success",
                )
            except Exception as e:
                error_message = f"Error executing tool {tool_name}: {e}"
                print(error_message)
                tool_result_part = cls._build_tool_result_part(
                    tool_use_id,
                    json.dumps({"error": error_message}),
                    "error" if tool_output and tool_output.is_error else "success",
                )
            tool_result_blocks.append(tool_result_part)
        return tool_result_blocks
