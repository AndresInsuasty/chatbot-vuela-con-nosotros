import os
from typing import List, Dict, Any, Optional

from utilidades import consulta_estado_vuelo

from fastmcp import FastMCP


app = FastMCP("vuela-con-nosotros-servicio")


@app.tool
def estado_vuelo(numero_vuelo: str) -> Dict[str, Any]:
    """
    Consulta el estado de un vuelo dado su número.

    Args:
        numero_vuelo (str): El número del vuelo a consultar.

    Returns:
        dict: Un diccionario con la información del estado del vuelo.
    """
    try:
        return consulta_estado_vuelo(numero_vuelo)
    except Exception as e:
        return {"error": str(e)}

