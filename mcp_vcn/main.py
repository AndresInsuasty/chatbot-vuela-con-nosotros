"""Servicio MCP para consultas y gestiones sobre vuelos."""

from typing import Dict, Any
from fastmcp import FastMCP
from utilidades import (
    consulta_estado_vuelo,
    conectar_base_datos,
    consultar_opciones_vuelo,
)


mcp = FastMCP(name="vuela-con-nosotros-servicio")


@mcp.tool
def estado_vuelo(numero_vuelo: str) -> Dict[str, Any]:
    """
    Consulta el estado de un vuelo dado su número.
    Args:
        numero_vuelo (str): El número del vuelo a consultar.
    Returns:
        dict: Un diccionario con la información del estado del vuelo.
    """
    conn = None
    try:
        conn = conectar_base_datos()
        return consulta_estado_vuelo(numero_vuelo, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@mcp.tool
def opciones_vuelo(origen: str, destino: str, fecha: str) -> Dict[str, Any]:
    """Consulta las opciones de vuelo disponibles entre un origen y un destino en una fecha dada."""
    conn = None
    try:
        conn = conectar_base_datos()
        return consultar_opciones_vuelo(origen, destino, fecha, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
