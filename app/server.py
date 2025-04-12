
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from mcp.server.lowlevel import Server
import mcp.types as types
import uvicorn

app = Server("example-server")
sse = SseServerTransport("/messages/")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="calculate_sum",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        ),
        types.Tool(
            name="reverse_text",
            description="Reverse a string",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"}
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "calculate_sum":
        return [types.TextContent(type="text", text=str(arguments["a"] + arguments["b"]))]
    elif name == "reverse_text":
        return [types.TextContent(type="text", text=arguments["text"][::-1])]
    raise ValueError(f"Tool not found: {name}")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)

if __name__ == "__main__":
    uvicorn.run("app.server:starlette_app", host="0.0.0.0", port=10000, reload=True)
