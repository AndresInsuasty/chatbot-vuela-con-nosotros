"""Script de ejemplo para llamar al servicio MCP y usar la herramienta 'estado_vuelo'."""

import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool(vuelo: str):
    """Llama a la herramienta 'estado_vuelo' del servicio MCP."""
    async with client:
        result = await client.call_tool("estado_vuelo", {"numero_vuelo": vuelo})
        print(result)

asyncio.run(call_tool("PSO-ASU-101"))
