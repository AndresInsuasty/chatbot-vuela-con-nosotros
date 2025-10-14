"""
Example demonstrating session memory functionality.

This example shows how to use session memory to maintain conversation history
across multiple agent runs without manually handling .to_input_list().
"""

import os
from typing import Any, Dict

from agents import Agent, OpenAIConversationsSession, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.model_settings import ModelSettings
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Asistente VuelaConNosotros API")

# Shared objects initialized on startup
server: MCPServerStreamableHttp | None = None
agent: Agent | None = None
session = OpenAIConversationsSession()

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()


class ChatRequest(BaseModel):
    message: str


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize MCP server and Agent on application startup."""
    global server, agent
    # create and enter the MCP server context so it's available for requests
    server = MCPServerStreamableHttp(
        name="Streamable HTTP Python Server",
        params={
            "url": os.getenv("URL_MCP", "http://0.0.0.0:8000/mcp"),
            "timeout": 10,
        },
        cache_tools_list=True,
        max_retry_attempts=3,
    )
    # enter async context
    await server.__aenter__()

    agent = Agent(
        name="Asistente VuelaConNosotros",
        instructions=prompt,
        mcp_servers=[server],
        model_settings=ModelSettings(tool_choice="required"),
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up MCP server on shutdown."""
    global server
    if server is not None:
        try:
            await server.__aexit__(None, None, None)
        except Exception:
            pass


@app.post("/chat")
async def chat_endpoint(payload: ChatRequest) -> Dict[str, Any]:
    """Accepts JSON {message: str} and returns {output: str, raw: ...}.

    The endpoint uses the shared session so conversation history is preserved
    across calls from the same process.
    """
    global agent, session
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        result = await Runner.run(agent, payload.message, session=session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Build a JSON-serializable summary of the RunResult to avoid Pydantic
    # attempting to serialize complex objects (like MCPServerStreamableHttp)
    def summarize_model_response(mr):
        try:
            return {
                "response_id": getattr(mr, "response_id", None),
                "output": getattr(mr, "output", None),
            }
        except Exception:
            return {"repr": repr(mr)}

    def summarize_item(item):
        try:
            return {
                "type": type(item).__name__,
                # Many RunItem types expose a to_input_item() or raw_item
                "repr": getattr(item, "to_input_item", lambda: repr(item))(),
            }
        except Exception:
            return {"repr": repr(item)}

    raw_summary = [summarize_model_response(m) for m in getattr(result, "raw_responses", [])]
    new_items_summary = [summarize_item(i) for i in getattr(result, "new_items", [])]

    summary = {
        "output": result.final_output,
        "last_agent": getattr(result, "_last_agent", None) and getattr(result._last_agent, "name", repr(result._last_agent)),
        "last_response_id": getattr(result, "last_response_id", None),
        "raw_responses": raw_summary,
        "new_items": new_items_summary,
    }

    return summary