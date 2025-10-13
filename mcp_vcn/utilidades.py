"""Utilidades para la gestión de vuelos y reservas."""
from typing import Dict, Any
import sqlite3
import os


def conectar_base_datos(
    nombre_db: str = "vuelos.db", script_sql: str = "inicial.sql"
) -> None:
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
    return sqlite3.connect(nombre_db)


def consulta_estado_vuelo(
    numero_vuelo: str, conn: sqlite3.Connection
) -> Dict[str, Any]:
    """
    Consulta el estado de un vuelo dado su número, obteniendo los datos desde la base de datos.

    Args:
        numero_vuelo (str): El número del vuelo a consultar.
        conn (sqlite3.Connection): Conexión a la base de datos.

    Returns:
        dict: Un diccionario con la información del estado del vuelo.
    """
    cursor = conn.cursor()
    try:
        # Usar parámetros en la consulta evita que valores como PSO se interpreten como columnas
        cursor.execute(
            """SELECT vuelo, estado, origen, destino, fecha, hora
         FROM estado_vuelos WHERE vuelo = ?""",
            (numero_vuelo,),
        )
        resultado = cursor.fetchone()
    finally:
        cursor.close()
    if resultado:
        vuelo, estado, origen, destino, fecha, hora = resultado
    else:
        vuelo, estado, origen, destino, fecha, hora = (
            numero_vuelo,
            "Desconocido",
            None,
            None,
            None,
            None,
        )

    estado_vuelo = {
        "numero_vuelo": vuelo,
        "estado": estado,
        "origen": origen,
        "destino": destino,
        "fecha": fecha,
        "hora": hora,
    }
    return estado_vuelo
