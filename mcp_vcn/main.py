"""Servicio MCP para consultas y gestiones sobre vuelos.

Este módulo expone herramientas MCP (decoradas con `@mcp.tool`) para:
- consultar el estado de un vuelo,
- listar opciones de vuelo por origen/destino/fecha,
- reservar un asiento y
- eliminar una reserva.

Las funciones abren y cierran la conexión a la base de datos local usando
`conectar_base_datos` y devuelven diccionarios con los resultados o con la
clave `error` en caso de excepción.
"""

from typing import Dict, Any
from fastmcp import FastMCP
from utilidades import (
    consulta_estado_vuelo,
    conectar_base_datos,
    consultar_opciones_vuelo,
    reservar_asiento,
    eliminar_reserva,
    verificar_reserva
)


mcp = FastMCP(name="vuela-con-nosotros-servicio")


@mcp.tool
def estado_vuelo(vuelo: str) -> Dict[str, Any]:
    """Consultar el estado de un vuelo por número.

    Esta herramienta devuelve la información de estado de un vuelo
    consultando la base de datos local. Si ocurre un error al abrir o
    consultar la base de datos, la función captura la excepción y devuelve
    un diccionario con la clave ``error`` y el mensaje correspondiente.

    Args:
        vuelo (str): Identificador del vuelo a consultar (p. ej. "PSO-ASU-101").

    Returns:
        Dict[str, Any]: Diccionario con la información del vuelo. Ejemplo:
            {
                "vuelo": "PSO-ASU-101",
                "estado": "Activo",
                "origen": "PSO",
                "destino": "ASU",
                "fecha": "2025-10-13",
                "hora": 630
            }

        En caso de error, retorna: {"error": "mensaje"}.
    """
    conn = None
    try:
        conn = conectar_base_datos()
        return consulta_estado_vuelo(vuelo, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@mcp.tool
def opciones_vuelo(origen: str, destino: str, fecha: str) -> Dict[str, Any]:
    """Listar opciones de vuelo entre origen y destino en una fecha.

    Para cada vuelo que coincida con `origen`, `destino` y `fecha`, la
    función calcula el primer asiento disponible en el rango 1..20 consultando
    la tabla `reservas`. Si todos los asientos 1..20 están ocupados, el
    campo ``asiento`` será ``None`` indicando que el vuelo está lleno.

    Args:
        origen (str): Código o nombre del aeropuerto de origen.
        destino (str): Código o nombre del aeropuerto de destino.
        fecha (str): Fecha en formato ISO "YYYY-MM-DD".

    Returns:
        Dict[str, Any]: Diccionario con la estructura:
            {
                "origen": origen,
                "destino": destino,
                "fecha": fecha,
                "opciones": [
                    {
                        "numero_vuelo": "PSO-ASU-101",
                        "hora": 630,
                        "estado": "Activo",
                        "asiento": 2  # primer asiento libre en 1..20 o None si lleno
                    },
                    ...
                ]
            }

        En caso de error, retorna: {"error": "mensaje"}.
    """
    conn = None
    try:
        conn = conectar_base_datos()
        return consultar_opciones_vuelo(origen, destino, fecha, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@mcp.tool
def reservar_vuelo(vuelo: str, numero_asiento: int, id_pasajero: str) -> Dict[str, Any]:
    """Reservar un asiento para un pasajero en un vuelo.

    Llama a la función `reservar_asiento` del módulo `utilidades`, encargada
    de realizar la inserción en la tabla `reservas`. La función maneja la
    apertura y cierre de la conexión y captura excepciones, devolviendo
    un diccionario con el resultado o con la clave ``error`` en caso de
    fallo.

    Args:
        vuelo (str): Identificador del vuelo donde reservar (p. ej. "PSO-ASU-101").
        numero_asiento (int): Número de asiento deseado (1..20).
        id_pasajero (str): Identificador del pasajero.

    Returns:
        Dict[str, Any]: Resultado de la operación según `reservar_asiento`.
            En caso de error, retorna: {"error": "mensaje"}.
    """
    conn = None
    try:
        conn = conectar_base_datos()
        return reservar_asiento(vuelo, numero_asiento, id_pasajero, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()


@mcp.tool
def eliminar_reserva_vuelo(
    vuelo: str, numero_asiento: int, id_pasajero: str
) -> Dict[str, Any]:
    """Eliminar una reserva existente para un pasajero.

    Llama a `eliminar_reserva` en `utilidades` para borrar la fila de la
    tabla `reservas` que coincida con los parámetros. Devuelve el resultado
    de la operación o un diccionario con ``error`` si ocurre alguna excepción.

    Args:
        vuelo (str): Identificador del vuelo asociado a la reserva.
        numero_asiento (int): Número de asiento asignado en la reserva.
        id_pasajero (str): Identificador del pasajero cuya reserva se eliminará.

    Returns:
        Dict[str, Any]: Resultado de la eliminación. En caso de error,
            retorna: {"error": "mensaje"}.
    """
    conn = None
    try:
        conn = conectar_base_datos()
        return eliminar_reserva(vuelo, numero_asiento, id_pasajero, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

@mcp.tool
def verificar_reserva_vuelo(vuelo: str, id_pasajero: str) -> Dict[str, Any]:
    """Verificar si un pasajero tiene una reserva en un vuelo específico.

    Llama a `verificar_reserva` en `utilidades` para comprobar si existe
    una reserva en la tabla `reservas` que coincida con los parámetros.
    Devuelve el resultado de la operación o un diccionario con ``error``
    si ocurre alguna excepción.

    Args:
        vuelo (str): Identificador del vuelo a verificar (p. ej. "PSO-ASU-101").
        id_pasajero (str): Identificador del pasajero cuya reserva se verificará.

    Returns:
        Dict[str, Any]: Resultado de la verificación. En caso de error,
            retorna: {"error": "mensaje"}.
    """
    conn = None
    try:
        conn = conectar_base_datos()
        return verificar_reserva(vuelo, id_pasajero, conn)
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Bind to 0.0.0.0 so the MCP server is reachable from other containers
    # in the docker-compose network (using the service name `mcp_vcn`).
    mcp.run(transport="http", host="0.0.0.0", port=8000)
