
from fastmcp.types import ToolCall, ToolResponse

async def math_tool(tool_call: ToolCall) -> ToolResponse:
    a = tool_call.parameters.get("a")
    b = tool_call.parameters.get("b")
    return ToolResponse.from_text(str(a + b))
