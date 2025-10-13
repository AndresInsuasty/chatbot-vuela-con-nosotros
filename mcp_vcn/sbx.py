"""Script de ejemplo para llamar al servicio MCP y usar la herramienta 'estado_vuelo'."""

import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool_estado_vuelo(vuelo: str):
    """Llama a la herramienta 'estado_vuelo' del servicio MCP."""
    async with client:
        result = await client.call_tool("estado_vuelo", {"vuelo": vuelo})
        print(result)


print("*" * 20)
print("Llamando a la herramienta 'estado_vuelo'...")
asyncio.run(call_tool_estado_vuelo("PSO-ASU-101"))


async def call_tool_opciones_vuelo(origen: str, destino: str, fecha: str):
    """Llama a la herramienta 'opciones_vuelo' del servicio MCP."""
    async with client:
        result = await client.call_tool(
            "opciones_vuelo", {"origen": origen, "destino": destino, "fecha": fecha}
        )
        print(result)


print("*" * 20)
print("Llamando a la herramienta 'opciones_vuelo'...")
asyncio.run(call_tool_opciones_vuelo("PSO", "ASU", "2025-10-14"))
