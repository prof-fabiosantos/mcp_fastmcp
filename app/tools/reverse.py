
from fastmcp.types import ToolCall, ToolResponse

async def reverse_tool(tool_call: ToolCall) -> ToolResponse:
    text = tool_call.parameters.get("text", "")
    return ToolResponse.from_text(text[::-1])
