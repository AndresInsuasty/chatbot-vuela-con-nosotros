from typing import Dict, Any
import sqlite3
import os


def crear_base_datos_si_no_existe(nombre_db: str = "vuelos.db", script_sql: str = "inicial.sql") -> None:
    """
    Crea una base de datos SQLite con las tablas estado_vuelos y reservas solo si no existe.
    Llena las tablas con datos iniciales desde un archivo .sql.
    """
    if not os.path.exists(nombre_db):
        conn = sqlite3.connect(nombre_db)
        with open(script_sql, "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.close()


def consulta_estado_vuelo(numero_vuelo: str) -> Dict[str, Any]:
    """
    Consulta el estado de un vuelo dado su número.

    Args:
        numero_vuelo (str): El número del vuelo a consultar.

    Returns:
        dict: Un diccionario con la información del estado del vuelo.
    """
    estado = "Cancelado" if numero_vuelo == "AB1234" else "Activo"
    estado_vuelo = {
        "numero_vuelo": numero_vuelo,
        "estado": estado,
        "hora_salida": "14:30",
        "hora_llegada": "16:45",
        "puerta_embarque": "A12"
    }
    return estado_vuelo

def consultar_opciones_vuelo(origen: str, destino: str, fecha: str) -> Dict[str, Any]:
    """
    Consulta las opciones de vuelo entre un origen y un destino en una fecha específica.

    Args:
        origen (str): Ciudad de origen.
        destino (str): Ciudad de destino.
        fecha (str): Fecha del vuelo en formato 'YYYY-MM-DD'.

    Returns:
        dict: Un diccionario con las opciones de vuelo disponibles.
    """
    opciones_vuelo = {
        "origen": origen,
        "destino": destino,
        "fecha": fecha,
        "vuelos_disponibles": [
            {"numero_vuelo": "AB1234", "hora_salida": "14:30", "hora_llegada": "16:45"},
            {"numero_vuelo": "CD5678", "hora_salida": "18:00", "hora_llegada": "20:15"}
        ]
    }
    return opciones_vuelo

