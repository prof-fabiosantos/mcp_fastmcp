
from fastapi import FastAPI
from fastmcp import FastMCP
from app.tools.math import math_tool
from app.tools.reverse import reverse_tool

app = FastAPI()
mcp = FastMCP()

mcp.register_tool("calculate_sum", math_tool)
mcp.register_tool("reverse_text", reverse_tool)

app.mount("/", mcp.app)
