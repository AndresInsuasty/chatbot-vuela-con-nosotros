import os
from typing import List, Dict, Any, Optional
import logging

from utilidades import consulta_estado_vuelo, crear_base_datos_si_no_existe

from fastmcp import FastMCP


app = FastMCP("vuela-con-nosotros-servicio")


# Configurar un logger de módulo. Si la aplicación principal configura logging,
# esto simplemente usará la configuración superior; de lo contrario, se añade
# un handler básico para evitar que los mensajes se pierdan.
logger = logging.getLogger(__name__)
if not logger.handlers:
    # handler y formato básicos por si la app no configura logging
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# Asegurarse de que la base de datos exista al iniciar el MCP
try:
    crear_base_datos_si_no_existe()
except Exception as e:
    # No debe interrumpir el inicio del servicio, pero se registra el error
    logger.warning("No se pudo crear/verificar la base de datos: %s", e)


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

