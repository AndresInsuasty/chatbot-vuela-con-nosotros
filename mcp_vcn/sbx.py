import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(vuelo: str):
    async with client:
        result = await client.call_tool("estado_vuelo", {"numero_vuelo": vuelo})
        print(result)

asyncio.run(call_tool("PSO-ASU-101"))
