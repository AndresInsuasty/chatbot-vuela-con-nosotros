import os
from typing import Dict, Any

from utilidades import consulta_estado_vuelo, conectar_base_datos
from fastmcp import FastMCP

mcp = FastMCP(
    name="vuela-con-nosotros-servicio",
    description="Servicio para consultas y gestiones sobre vuelos.",
)


@mcp.tool
def estado_vuelo(numero_vuelo: str) -> Dict[str, Any]:
    conn = None
    try:
        conn = conectar_base_datos()
        return consulta_estado_vuelo(numero_vuelo, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
