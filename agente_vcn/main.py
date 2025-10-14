"""
Example demonstrating session memory functionality.

This example shows how to use session memory to maintain conversation history
across multiple agent runs without manually handling .to_input_list().
"""

import asyncio

from agents import Agent, OpenAIConversationsSession, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings
import os
from dotenv import load_dotenv

load_dotenv() 

session = OpenAIConversationsSession()

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

async def main() -> None:
    async with MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp"),
            "timeout": 10,
        },
        cache_tools_list=True,
        max_retry_attempts=3,
    ) as server:
        agent = Agent(
            name="Asistente VuelaConNosotros",
            instructions=prompt,
            mcp_servers=[server],
            model_settings=ModelSettings(tool_choice="required"),
        )

        result = await Runner.run(agent, "me ayudas consultando el estado del vuelo PSO-ASU-101?", session=session)
        print(result.final_output)

asyncio.run(main())